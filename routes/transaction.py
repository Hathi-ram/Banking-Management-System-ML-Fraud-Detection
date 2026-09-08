# ==========================================================
# Imports
# ==========================================================

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    session,
    flash
)

from models.database import get_connection

from datetime import datetime

import time


# ==========================================================
# ML Fraud Detection
# ==========================================================

from ml_service.fraud_detector import predict_transaction


# ==========================================================
# Transaction Blueprint
# ==========================================================

transaction_bp = Blueprint(
    "transaction",
    __name__
)


# ==========================================================
# Helper Function
# ==========================================================

def get_risk_level(risk_score):

    """
    Convert ML risk score into a readable risk level.

    Risk Score:
        0.00 - 0.39  -> Low
        0.40 - 0.69  -> Medium
        0.70 - 1.00  -> High
    """

    if risk_score < 0.40:

        return "Low"

    elif risk_score < 0.70:

        return "Medium"

    else:

        return "High"


# ==========================================================
# View Transactions
# ==========================================================

@transaction_bp.route("/transactions")
def transactions():

    connection = get_connection()

    if not connection:

        return "Database Connection Failed"

    cursor = connection.cursor(
        dictionary=True
    )

    search = request.args.get(
        "search",
        ""
    ).strip()

    page = request.args.get(
        "page",
        1,
        type=int
    )

    if page < 1:

        page = 1

    per_page = 10

    offset = (
        page - 1
    ) * per_page


    # ======================================================
    # Count Transactions
    # ======================================================

    if search == "":

        cursor.execute("""
            SELECT COUNT(*) AS total

            FROM Transactions
        """)

        total = cursor.fetchone()["total"]


        # ==================================================
        # Get Transactions
        # ==================================================

        cursor.execute("""
            SELECT

                t.*,

                a.account_number,

                CONCAT(
                    c.first_name,
                    ' ',
                    c.last_name
                ) AS customer_name

            FROM Transactions t

            INNER JOIN Accounts a
                ON t.account_id = a.account_id

            INNER JOIN Customers c
                ON a.customer_id = c.customer_id

            ORDER BY
                t.transaction_date DESC

            LIMIT %s OFFSET %s

        """, (
            per_page,
            offset
        ))


    else:

        value = f"%{search}%"


        # ==================================================
        # Count Search Results
        # ==================================================

        cursor.execute("""
            SELECT COUNT(*) AS total

            FROM Transactions t

            INNER JOIN Accounts a
                ON t.account_id = a.account_id

            INNER JOIN Customers c
                ON a.customer_id = c.customer_id

            WHERE

                t.transaction_reference LIKE %s

                OR a.account_number LIKE %s

                OR c.first_name LIKE %s

                OR c.last_name LIKE %s

                OR t.transaction_type LIKE %s

                OR t.transaction_status LIKE %s

                OR t.ml_risk_level LIKE %s

        """, (
            value,
            value,
            value,
            value,
            value,
            value,
            value
        ))


        total = cursor.fetchone()["total"]


        # ==================================================
        # Get Search Results
        # ==================================================

        cursor.execute("""
            SELECT

                t.*,

                a.account_number,

                CONCAT(
                    c.first_name,
                    ' ',
                    c.last_name
                ) AS customer_name

            FROM Transactions t

            INNER JOIN Accounts a
                ON t.account_id = a.account_id

            INNER JOIN Customers c
                ON a.customer_id = c.customer_id

            WHERE

                t.transaction_reference LIKE %s

                OR a.account_number LIKE %s

                OR c.first_name LIKE %s

                OR c.last_name LIKE %s

                OR t.transaction_type LIKE %s

                OR t.transaction_status LIKE %s

                OR t.ml_risk_level LIKE %s

            ORDER BY
                t.transaction_date DESC

            LIMIT %s OFFSET %s

        """, (
            value,
            value,
            value,
            value,
            value,
            value,
            value,
            per_page,
            offset
        ))


    transactions = cursor.fetchall()


    # ======================================================
    # Pagination
    # ======================================================

    total_pages = (
        (total + per_page - 1)
        // per_page
    )

    if total_pages == 0:

        total_pages = 1

    if page > total_pages:

        page = total_pages


    cursor.close()

    connection.close()


    return render_template(
        "transactions.html",

        transactions=transactions,

        search=search,

        page=page,

        total_pages=total_pages
    )


# ==========================================================
# Add Transaction
# ==========================================================

@transaction_bp.route(
    "/add_transaction",
    methods=["GET", "POST"]
)
def add_transaction():

    connection = get_connection()

    if not connection:

        return "Database Connection Failed"

    cursor = connection.cursor(
        dictionary=True
    )


    # ======================================================
    # POST
    # ======================================================

    if request.method == "POST":

        try:

            account_id = int(
                request.form["account_id"]
            )

            transaction_type = request.form[
                "transaction_type"
            ]

            amount = float(
                request.form["amount"]
            )

            transaction_status = request.form[
                "transaction_status"
            ]

            remarks = request.form.get(
                "remarks",
                ""
            ).strip()


            # ==================================================
            # Basic Validation
            # ==================================================

            if amount <= 0:

                flash(
                    "Transaction amount must be greater than zero.",
                    "danger"
                )

                cursor.close()
                connection.close()

                return redirect(
                    "/add_transaction"
                )


            # ==================================================
            # Check Account
            # ==================================================

            cursor.execute("""
                SELECT

                    account_id,

                    account_number,

                    account_status,

                    balance

                FROM Accounts

                WHERE account_id=%s

            """, (
                account_id,
            ))

            account = cursor.fetchone()


            if not account:

                flash(
                    "Selected account was not found.",
                    "danger"
                )

                cursor.close()
                connection.close()

                return redirect(
                    "/add_transaction"
                )


            if account["account_status"] != "Active":

                flash(
                    "Transaction cannot be created for an inactive account.",
                    "danger"
                )

                cursor.close()
                connection.close()

                return redirect(
                    "/add_transaction"
                )


            # ==================================================
            # Account Transaction Statistics
            #
            # Calculate statistics BEFORE inserting the
            # new transaction.
            # ==================================================

            cursor.execute("""
                SELECT

                    COUNT(*) AS transaction_count,

                    COALESCE(
                        AVG(amount),
                        0
                    ) AS average_amount,

                    COALESCE(
                        STDDEV_POP(amount),
                        0
                    ) AS std_amount

                FROM Transactions

                WHERE account_id=%s

            """, (
                account_id,
            ))

            account_stats = cursor.fetchone()


            account_transaction_count = int(
                account_stats["transaction_count"] or 0
            )

            account_average_amount = float(
                account_stats["average_amount"] or 0
            )

            account_std_amount = float(
                account_stats["std_amount"] or 0
            )


            # ==================================================
            # Transaction Date
            # ==================================================

            transaction_date = datetime.now()


            # ==================================================
            # ML FRAUD DETECTION
            # ==================================================

            ml_result = predict_transaction(

                amount=amount,

                transaction_type=transaction_type,

                transaction_status=transaction_status,

                transaction_date=transaction_date,

                account_average_amount=
                    account_average_amount,

                account_std_amount=
                    account_std_amount,

                account_transaction_count=
                    account_transaction_count
            )


            prediction = int(
                ml_result["prediction"]
            )

            risk_score = float(
                ml_result["risk_score"]
            )


            # ==================================================
            # Risk Level
            # ==================================================

            risk_level = get_risk_level(
                risk_score
            )


            # ==================================================
            # Fraud Result
            # ==================================================

            if prediction == 1:

                fraud_label = "SUSPICIOUS"

                fraud_message = (
                    "Suspicious transaction detected by ML. "
                    f"Risk score: {risk_score:.2f}"
                )

                # Add ML information to remarks

                if remarks:

                    remarks = (
                        f"{remarks} | "
                        f"ML Alert: Suspicious "
                        f"(Risk: {risk_score:.2f})"
                    )

                else:

                    remarks = (
                        f"ML Alert: Suspicious "
                        f"(Risk: {risk_score:.2f})"
                    )

            else:

                fraud_label = "NORMAL"

                fraud_message = (
                    "Transaction passed ML fraud detection. "
                    f"Risk score: {risk_score:.2f}"
                )


            # ==================================================
            # Generate Transaction Reference
            # ==================================================

            transaction_reference = (
                "TXN"
                + datetime.now().strftime(
                    "%Y%m%d%H%M%S"
                )
                + str(
                    int(time.time() * 1000)
                )[-4:]
            )


            # ==================================================
            # ML Checked Time
            # ==================================================

            ml_checked_at = datetime.now()

            ml_model_version = "v1.0"


            # ==================================================
            # Insert Transaction
            #
            # IMPORTANT:
            # ML results are now stored in the database.
            # ==================================================

            cursor.execute("""
                INSERT INTO Transactions
                (
                    transaction_reference,

                    account_id,

                    transaction_type,

                    amount,

                    transaction_date,

                    transaction_status,

                    remarks,

                    ml_prediction,

                    ml_risk_score,

                    ml_risk_level,

                    ml_checked_at,

                    ml_model_version
                )

                VALUES
                (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                )

            """, (

                transaction_reference,

                account_id,

                transaction_type,

                amount,

                transaction_date,

                transaction_status,

                remarks,

                prediction,

                risk_score,

                risk_level,

                ml_checked_at,

                ml_model_version
            ))


            # ==================================================
            # Logged-in Admin
            # ==================================================

            username = session.get(
                "username",
                "Unknown Admin"
            )


            # ==================================================
            # Activity Log
            # ==================================================

            if prediction == 1:

                activity_message = (
                    f"Admin '{username}' created "
                    f"SUSPICIOUS transaction: "
                    f"{transaction_reference} "
                    f"({transaction_type}, "
                    f"₹{amount:.2f}, "
                    f"ML Risk: {risk_score:.2f}, "
                    f"Risk Level: {risk_level})"
                )

            else:

                activity_message = (
                    f"Admin '{username}' created transaction: "
                    f"{transaction_reference} "
                    f"({transaction_type}, "
                    f"₹{amount:.2f}) "
                    f"[ML: Normal, "
                    f"Risk: {risk_score:.2f}, "
                    f"Risk Level: {risk_level}]"
                )


            cursor.execute("""
                INSERT INTO Activity_Log
                (
                    activity
                )

                VALUES
                (
                    %s
                )

            """, (
                activity_message,
            ))


            # ==================================================
            # Commit
            # ==================================================

            connection.commit()


            # ==================================================
            # User Notification
            # ==================================================

            if prediction == 1:

                flash(
                    f"⚠️ {fraud_message} "
                    f"({risk_level} Risk)",
                    "warning"
                )

            else:

                flash(
                    f"✅ {fraud_message} "
                    f"({risk_level} Risk)",
                    "success"
                )


            cursor.close()

            connection.close()


            return redirect(
                "/transactions"
            )


        except Exception as e:

            connection.rollback()

            print(
                "Transaction Error:",
                str(e)
            )

            flash(
                f"Transaction could not be created: {str(e)}",
                "danger"
            )

            cursor.close()

            connection.close()

            return redirect(
                "/add_transaction"
            )


    # ======================================================
    # Get Active Accounts
    # ======================================================

    cursor.execute("""
        SELECT

            a.account_id,

            a.account_number,

            CONCAT(
                c.first_name,
                ' ',
                c.last_name
            ) AS customer_name

        FROM Accounts a

        INNER JOIN Customers c
            ON a.customer_id = c.customer_id

        WHERE
            a.account_status = 'Active'

        ORDER BY
            a.account_number

    """)


    accounts = cursor.fetchall()


    cursor.close()

    connection.close()


    return render_template(
        "add_transaction.html",

        accounts=accounts
    )


# ==========================================================
# Edit Transaction
# ==========================================================

@transaction_bp.route(
    "/edit_transaction/<int:id>",
    methods=["GET", "POST"]
)
def edit_transaction(id):

    connection = get_connection()

    if not connection:

        return "Database Connection Failed"

    cursor = connection.cursor(
        dictionary=True
    )


    # ======================================================
    # POST
    # ======================================================

    if request.method == "POST":

        try:

            transaction_type = request.form[
                "transaction_type"
            ]

            amount = float(
                request.form["amount"]
            )

            transaction_status = request.form[
                "transaction_status"
            ]

            remarks = request.form.get(
                "remarks",
                ""
            ).strip()


            # ==================================================
            # Validation
            # ==================================================

            if amount <= 0:

                flash(
                    "Transaction amount must be greater than zero.",
                    "danger"
                )

                cursor.close()

                connection.close()

                return redirect(
                    f"/edit_transaction/{id}"
                )


            # ==================================================
            # Get Existing Transaction
            # ==================================================

            cursor.execute("""
                SELECT

                    transaction_id,

                    transaction_reference,

                    account_id,

                    transaction_date,

                    amount AS old_amount

                FROM Transactions

                WHERE transaction_id=%s

            """, (
                id,
            ))


            transaction = cursor.fetchone()


            if not transaction:

                flash(
                    "Transaction not found.",
                    "danger"
                )

                cursor.close()

                connection.close()

                return redirect(
                    "/transactions"
                )


            account_id = transaction[
                "account_id"
            ]


            # ==================================================
            # Account Statistics
            #
            # Exclude the transaction being edited.
            # ==================================================

            cursor.execute("""
                SELECT

                    COUNT(*) AS transaction_count,

                    COALESCE(
                        AVG(amount),
                        0
                    ) AS average_amount,

                    COALESCE(
                        STDDEV_POP(amount),
                        0
                    ) AS std_amount

                FROM Transactions

                WHERE

                    account_id=%s

                    AND transaction_id != %s

            """, (
                account_id,
                id
            ))


            account_stats = cursor.fetchone()


            account_transaction_count = int(
                account_stats["transaction_count"] or 0
            )

            account_average_amount = float(
                account_stats["average_amount"] or 0
            )

            account_std_amount = float(
                account_stats["std_amount"] or 0
            )


            # ==================================================
            # ML Prediction
            # ==================================================

            transaction_date = (
                transaction["transaction_date"]
            )

            ml_result = predict_transaction(

                amount=amount,

                transaction_type=transaction_type,

                transaction_status=transaction_status,

                transaction_date=transaction_date,

                account_average_amount=
                    account_average_amount,

                account_std_amount=
                    account_std_amount,

                account_transaction_count=
                    account_transaction_count
            )


            prediction = int(
                ml_result["prediction"]
            )

            risk_score = float(
                ml_result["risk_score"]
            )


            # ==================================================
            # Risk Level
            # ==================================================

            risk_level = get_risk_level(
                risk_score
            )


            # ==================================================
            # Add ML Alert to Remarks
            # ==================================================

            if prediction == 1:

                if remarks:

                    remarks = (
                        f"{remarks} | "
                        f"ML Alert: Suspicious "
                        f"(Risk: {risk_score:.2f})"
                    )

                else:

                    remarks = (
                        f"ML Alert: Suspicious "
                        f"(Risk: {risk_score:.2f})"
                    )


            # ==================================================
            # ML Checked Time
            # ==================================================

            ml_checked_at = datetime.now()

            ml_model_version = "v1.0"


            # ==================================================
            # Update Transaction
            #
            # IMPORTANT:
            # ML results are updated whenever the transaction
            # is edited.
            # ==================================================

            cursor.execute("""
                UPDATE Transactions

                SET

                    transaction_type=%s,

                    amount=%s,

                    transaction_status=%s,

                    remarks=%s,

                    ml_prediction=%s,

                    ml_risk_score=%s,

                    ml_risk_level=%s,

                    ml_checked_at=%s,

                    ml_model_version=%s

                WHERE transaction_id=%s

            """, (

                transaction_type,

                amount,

                transaction_status,

                remarks,

                prediction,

                risk_score,

                risk_level,

                ml_checked_at,

                ml_model_version,

                id
            ))


            # ==================================================
            # Logged-in Admin
            # ==================================================

            username = session.get(
                "username",
                "Unknown Admin"
            )


            # ==================================================
            # Activity Log
            # ==================================================

            if prediction == 1:

                activity_message = (
                    f"Admin '{username}' updated "
                    f"SUSPICIOUS transaction: "
                    f"{transaction['transaction_reference']} "
                    f"(Type: {transaction_type}, "
                    f"Amount: ₹{amount:.2f}, "
                    f"ML Risk: {risk_score:.2f}, "
                    f"Risk Level: {risk_level})"
                )

            else:

                activity_message = (
                    f"Admin '{username}' updated transaction: "
                    f"{transaction['transaction_reference']} "
                    f"(Type: {transaction_type}, "
                    f"Amount: ₹{amount:.2f}, "
                    f"Status: {transaction_status}) "
                    f"[ML Risk: {risk_score:.2f}, "
                    f"Risk Level: {risk_level}]"
                )


            cursor.execute("""
                INSERT INTO Activity_Log
                (
                    activity
                )

                VALUES
                (
                    %s
                )

            """, (
                activity_message,
            ))


            # ==================================================
            # Commit
            # ==================================================

            connection.commit()


            # ==================================================
            # Notification
            # ==================================================

            if prediction == 1:

                flash(
                    f"⚠️ Suspicious transaction detected. "
                    f"Risk score: {risk_score:.2f} "
                    f"({risk_level} Risk)",
                    "warning"
                )

            else:

                flash(
                    f"✅ Transaction updated successfully. "
                    f"ML risk score: {risk_score:.2f} "
                    f"({risk_level} Risk)",
                    "success"
                )


            cursor.close()

            connection.close()


            return redirect(
                "/transactions"
            )


        except Exception as e:

            connection.rollback()

            print(
                "Edit Transaction Error:",
                str(e)
            )

            flash(
                f"Transaction could not be updated: {str(e)}",
                "danger"
            )

            cursor.close()

            connection.close()

            return redirect(
                f"/edit_transaction/{id}"
            )


    # ======================================================
    # Get Transaction
    # ======================================================

    cursor.execute("""
        SELECT *

        FROM Transactions

        WHERE transaction_id=%s

    """, (
        id,
    ))


    transaction = cursor.fetchone()


    cursor.close()

    connection.close()


    if not transaction:

        flash(
            "Transaction not found.",
            "danger"
        )

        return redirect(
            "/transactions"
        )


    return render_template(
        "edit_transaction.html",

        transaction=transaction
    )


# ==========================================================
# Delete Transaction
# ==========================================================

@transaction_bp.route(
    "/delete_transaction/<int:id>"
)
def delete_transaction(id):

    connection = get_connection()

    if not connection:

        return "Database Connection Failed"

    cursor = connection.cursor(
        dictionary=True
    )


    try:

        # ==================================================
        # Get Transaction Before Delete
        # ==================================================

        cursor.execute("""
            SELECT

                transaction_reference,

                transaction_type,

                amount,

                ml_prediction,

                ml_risk_score,

                ml_risk_level

            FROM Transactions

            WHERE transaction_id=%s

        """, (
            id,
        ))


        transaction = cursor.fetchone()


        # ==================================================
        # Delete Transaction
        # ==================================================

        cursor.execute("""
            DELETE FROM Transactions

            WHERE transaction_id=%s

        """, (
            id,
        ))


        # ==================================================
        # Logged-in Admin
        # ==================================================

        username = session.get(
            "username",
            "Unknown Admin"
        )


        # ==================================================
        # Activity Log
        # ==================================================

        if transaction:

            risk_score = transaction[
                "ml_risk_score"
            ]

            risk_level = transaction[
                "ml_risk_level"
            ]


            if risk_score is not None:

                ml_information = (
                    f", ML Risk: {float(risk_score):.2f}, "
                    f"Risk Level: {risk_level}"
                )

            else:

                ml_information = ""


            cursor.execute("""
                INSERT INTO Activity_Log
                (
                    activity
                )

                VALUES
                (
                    %s
                )

            """, (

                f"Admin '{username}' deleted transaction: "
                f"{transaction['transaction_reference']} "
                f"({transaction['transaction_type']}, "
                f"₹{transaction['amount']})"
                f"{ml_information}",

            ))


        else:

            cursor.execute("""
                INSERT INTO Activity_Log
                (
                    activity
                )

                VALUES
                (
                    %s
                )

            """, (

                f"Admin '{username}' attempted to delete "
                f"transaction ID {id}, but it was not found",

            ))


        # ==================================================
        # Commit
        # ==================================================

        connection.commit()


    except Exception as e:

        connection.rollback()

        print(
            "Delete Transaction Error:",
            str(e)
        )

        flash(
            f"Transaction could not be deleted: {str(e)}",
            "danger"
        )


    cursor.close()

    connection.close()


    return redirect(
        "/transactions"
    )