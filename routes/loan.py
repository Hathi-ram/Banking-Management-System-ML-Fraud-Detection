from flask import Blueprint, render_template, request, redirect
from models.database import get_connection
import random
from datetime import datetime
from dateutil.relativedelta import relativedelta


loan_bp = Blueprint("loan", __name__)


# ==========================================================
# View Loans
# ==========================================================

@loan_bp.route("/loans")
def loans():

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    search = request.args.get("search", "").strip()

    page = request.args.get(
        "page",
        1,
        type=int
    )

    if page < 1:
        page = 1

    per_page = 10
    offset = (page - 1) * per_page


    # ======================================================
    # Without Search
    # ======================================================

    if search == "":

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM Loans
        """)

        total = cursor.fetchone()["total"]


        cursor.execute("""
            SELECT

                l.loan_id,

                l.loan_number,

                CONCAT(
                    c.first_name,
                    ' ',
                    c.last_name
                ) AS customer_name,

                l.loan_type,

                l.loan_amount,

                l.interest_rate,

                l.loan_tenure,

                l.emi,

                l.loan_status,

                l.start_date,

                l.end_date

            FROM Loans l

            INNER JOIN Customers c
                ON l.customer_id = c.customer_id

            ORDER BY l.loan_id DESC

            LIMIT %s OFFSET %s
        """, (
            per_page,
            offset
        ))


    # ======================================================
    # Search
    # ======================================================

    else:

        value = f"%{search}%"


        cursor.execute("""
            SELECT COUNT(*) AS total

            FROM Loans l

            INNER JOIN Customers c
                ON l.customer_id = c.customer_id

            WHERE

                l.loan_number LIKE %s

                OR c.first_name LIKE %s

                OR c.last_name LIKE %s

                OR l.loan_type LIKE %s

                OR l.loan_status LIKE %s

        """, (
            value,
            value,
            value,
            value,
            value
        ))

        total = cursor.fetchone()["total"]


        cursor.execute("""
            SELECT

                l.loan_id,

                l.loan_number,

                CONCAT(
                    c.first_name,
                    ' ',
                    c.last_name
                ) AS customer_name,

                l.loan_type,

                l.loan_amount,

                l.interest_rate,

                l.loan_tenure,

                l.emi,

                l.loan_status,

                l.start_date,

                l.end_date

            FROM Loans l

            INNER JOIN Customers c
                ON l.customer_id = c.customer_id

            WHERE

                l.loan_number LIKE %s

                OR c.first_name LIKE %s

                OR c.last_name LIKE %s

                OR l.loan_type LIKE %s

                OR l.loan_status LIKE %s

            ORDER BY l.loan_id DESC

            LIMIT %s OFFSET %s

        """, (
            value,
            value,
            value,
            value,
            value,
            per_page,
            offset
        ))


    loans = cursor.fetchall()


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
        "loans.html",

        loans=loans,

        search=search,

        page=page,

        total_pages=total_pages
    )


# ==========================================================
# Add Loan
# ==========================================================

@loan_bp.route(
    "/add_loan",
    methods=["GET", "POST"]
)
def add_loan():

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)


    # ======================================================
    # Get Customers
    # ======================================================

    cursor.execute("""
        SELECT

            customer_id,

            CONCAT(
                first_name,
                ' ',
                last_name
            ) AS customer_name

        FROM Customers

        ORDER BY first_name
    """)


    customers = cursor.fetchall()


    # ======================================================
    # POST
    # ======================================================

    if request.method == "POST":

        customer_id = request.form["customer_id"]

        loan_type = request.form["loan_type"]

        loan_amount = float(
            request.form["loan_amount"]
        )

        interest_rate = float(
            request.form["interest_rate"]
        )

        tenure = int(
            request.form["loan_tenure"]
        )


        # ==================================================
        # EMI Calculation
        # ==================================================

        r = interest_rate / (12 * 100)

        n = tenure


        if r == 0:

            emi = loan_amount / n

        else:

            emi = (
                loan_amount
                * r
                * pow(1 + r, n)
            ) / (
                pow(1 + r, n) - 1
            )


        emi = round(emi, 2)


        # ==================================================
        # Generate Loan Number
        # ==================================================

        loan_number = (
            "LN"
            + str(
                random.randint(
                    100000,
                    999999
                )
            )
        )


        # ==================================================
        # Dates
        # ==================================================

        start_date = datetime.today().date()

        end_date = (
            start_date
            + relativedelta(
                months=tenure
            )
        )


        # ==================================================
        # Insert Loan
        # ==================================================

        cursor.execute("""
            INSERT INTO Loans
            (
                loan_number,
                customer_id,
                loan_type,
                loan_amount,
                interest_rate,
                loan_tenure,
                emi,
                loan_status,
                start_date,
                end_date
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
                %s
            )
        """, (
            loan_number,
            customer_id,
            loan_type,
            loan_amount,
            interest_rate,
            tenure,
            emi,
            "Pending",
            start_date,
            end_date
        ))


        loan_id = cursor.lastrowid


        # ==================================================
        # Activity Log
        # ==================================================

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
            f"Loan Created: "
            f"{loan_number} "
            f"({loan_type}, ₹{loan_amount}) "
            f"- Status: Pending",
        ))


        connection.commit()


        cursor.close()
        connection.close()


        return redirect("/loans")


    cursor.close()
    connection.close()


    return render_template(
        "add_loan.html",
        customers=customers
    )


# ==========================================================
# Edit Loan
# ==========================================================

@loan_bp.route(
    "/edit_loan/<int:loan_id>",
    methods=["GET", "POST"]
)
def edit_loan(loan_id):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)


    # ======================================================
    # POST - Update Loan
    # ======================================================

    if request.method == "POST":

        loan_type = request.form["loan_type"]

        interest_rate = request.form["interest_rate"]

        loan_status = request.form["loan_status"]


        # ==================================================
        # Get Existing Loan
        # ==================================================

        cursor.execute("""
            SELECT

                loan_number,

                loan_status

            FROM Loans

            WHERE loan_id=%s
        """, (
            loan_id,
        ))


        old_loan = cursor.fetchone()


        # ==================================================
        # Update
        # ==================================================

        cursor.execute("""
            UPDATE Loans

            SET

                loan_type=%s,

                interest_rate=%s,

                loan_status=%s

            WHERE loan_id=%s

        """, (
            loan_type,
            interest_rate,
            loan_status,
            loan_id
        ))


        # ==================================================
        # Activity Log
        # ==================================================

        if old_loan:

            old_status = old_loan["loan_status"]

            loan_number = old_loan["loan_number"]


            # ----------------------------------------------
            # Status Changed to Approved
            # ----------------------------------------------

            if (
                loan_status == "Approved"
                and old_status != "Approved"
            ):

                activity_message = (
                    f"Loan Approved: "
                    f"{loan_number} "
                    f"(ID: {loan_id})"
                )


            # ----------------------------------------------
            # Status Changed to Rejected
            # ----------------------------------------------

            elif (
                loan_status == "Rejected"
                and old_status != "Rejected"
            ):

                activity_message = (
                    f"Loan Rejected: "
                    f"{loan_number} "
                    f"(ID: {loan_id})"
                )


            # ----------------------------------------------
            # Status Changed to Closed
            # ----------------------------------------------

            elif (
                loan_status == "Closed"
                and old_status != "Closed"
            ):

                activity_message = (
                    f"Loan Closed: "
                    f"{loan_number} "
                    f"(ID: {loan_id})"
                )


            # ----------------------------------------------
            # Other Update
            # ----------------------------------------------

            else:

                activity_message = (
                    f"Loan Updated: "
                    f"{loan_number} "
                    f"(ID: {loan_id}) "
                    f"- Type: {loan_type}, "
                    f"Interest: {interest_rate}%, "
                    f"Status: {loan_status}"
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


        connection.commit()


        cursor.close()
        connection.close()


        return redirect("/loans")


    # ======================================================
    # Get Loan
    # ======================================================

    cursor.execute("""
        SELECT *

        FROM Loans

        WHERE loan_id=%s
    """, (
        loan_id,
    ))


    loan = cursor.fetchone()


    cursor.close()
    connection.close()


    return render_template(
        "edit_loan.html",
        loan=loan
    )


# ==========================================================
# Close Loan
# ==========================================================

@loan_bp.route(
    "/close_loan/<int:loan_id>"
)
def close_loan(loan_id):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)


    # ======================================================
    # Get Loan Information
    # ======================================================

    cursor.execute("""
        SELECT

            loan_number,

            loan_status

        FROM Loans

        WHERE loan_id=%s
    """, (
        loan_id,
    ))


    loan = cursor.fetchone()


    # ======================================================
    # Close Loan
    # ======================================================

    cursor.execute("""
        UPDATE Loans

        SET loan_status='Closed'

        WHERE loan_id=%s
    """, (
        loan_id,
    ))


    # ======================================================
    # Activity Log
    # ======================================================

    if loan:

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
            f"Loan Closed: "
            f"{loan['loan_number']} "
            f"(ID: {loan_id})",
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
            f"Loan Close Attempt: "
            f"Loan ID {loan_id} not found",
        ))


    connection.commit()


    cursor.close()
    connection.close()


    return redirect("/loans")