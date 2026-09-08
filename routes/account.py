from flask import Blueprint, render_template, request, redirect, session
from models.database import get_connection

account_bp = Blueprint("account", __name__)


# ==========================================================
# View Accounts
# ==========================================================

@account_bp.route("/accounts")
def accounts():

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    search = request.args.get("search", "").strip()

    page = request.args.get("page", 1, type=int)

    if page < 1:
        page = 1

    per_page = 10
    offset = (page - 1) * per_page

    # ======================================================
    # Count Accounts
    # ======================================================

    if search == "":

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM Accounts
        """)

        total = cursor.fetchone()["total"]

        # ==================================================
        # Get Accounts
        # ==================================================

        cursor.execute("""
            SELECT
                a.*,
                CONCAT(c.first_name, ' ', c.last_name)
                    AS customer_name,
                b.branch_name

            FROM Accounts a

            INNER JOIN Customers c
                ON a.customer_id = c.customer_id

            INNER JOIN Branches b
                ON a.branch_id = b.branch_id

            ORDER BY a.account_id DESC

            LIMIT %s OFFSET %s
        """, (per_page, offset))

    else:

        value = f"%{search}%"

        # ==================================================
        # Count Search Results
        # ==================================================

        cursor.execute("""
            SELECT COUNT(*) AS total

            FROM Accounts a

            INNER JOIN Customers c
                ON a.customer_id = c.customer_id

            INNER JOIN Branches b
                ON a.branch_id = b.branch_id

            WHERE
                a.account_number LIKE %s
                OR c.first_name LIKE %s
                OR c.last_name LIKE %s
                OR a.account_type LIKE %s
                OR a.account_status LIKE %s
                OR b.branch_name LIKE %s
        """,
        (
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
                a.*,
                CONCAT(c.first_name, ' ', c.last_name)
                    AS customer_name,
                b.branch_name

            FROM Accounts a

            INNER JOIN Customers c
                ON a.customer_id = c.customer_id

            INNER JOIN Branches b
                ON a.branch_id = b.branch_id

            WHERE
                a.account_number LIKE %s
                OR c.first_name LIKE %s
                OR c.last_name LIKE %s
                OR a.account_type LIKE %s
                OR a.account_status LIKE %s
                OR b.branch_name LIKE %s

            ORDER BY a.account_id DESC

            LIMIT %s OFFSET %s
        """,
        (
            value,
            value,
            value,
            value,
            value,
            value,
            per_page,
            offset
        ))

    accounts = cursor.fetchall()

    total_pages = (total + per_page - 1) // per_page

    cursor.close()
    connection.close()

    return render_template(
        "accounts.html",
        accounts=accounts,
        search=search,
        page=page,
        total_pages=total_pages
    )


# ==========================================================
# Add Account
# ==========================================================

@account_bp.route("/add_account", methods=["GET", "POST"])
def add_account():

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    # ======================================================
    # Get Customers
    # ======================================================

    cursor.execute("""
        SELECT
            customer_id,
            first_name,
            last_name
        FROM Customers
        ORDER BY first_name, last_name
    """)

    customers = cursor.fetchall()

    # ======================================================
    # Get Branches
    # ======================================================

    cursor.execute("""
        SELECT
            branch_id,
            branch_name
        FROM Branches
        ORDER BY branch_name
    """)

    branches = cursor.fetchall()

    # ======================================================
    # POST
    # ======================================================

    if request.method == "POST":

        account_number = request.form["account_number"].strip()
        customer_id = request.form["customer_id"]
        branch_id = request.form["branch_id"]
        account_type = request.form["account_type"]
        balance = request.form["balance"]
        account_status = request.form["account_status"]
        open_date = request.form["open_date"]

        # ==================================================
        # Check Duplicate Account Number
        # ==================================================

        cursor.execute("""
            SELECT account_id
            FROM Accounts
            WHERE account_number = %s
        """, (account_number,))

        existing_account = cursor.fetchone()

        if existing_account:

            cursor.close()
            connection.close()

            return render_template(
                "add_account.html",
                customers=customers,
                branches=branches,
                error=(
                    f"Account number '{account_number}' "
                    "already exists. Please use a different "
                    "account number."
                )
            )

        # ==================================================
        # Insert Account
        # ==================================================

        cursor.execute("""
            INSERT INTO Accounts
            (
                account_number,
                customer_id,
                branch_id,
                account_type,
                balance,
                account_status,
                open_date
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
            )
        """,
        (
            account_number,
            customer_id,
            branch_id,
            account_type,
            balance,
            account_status,
            open_date
        ))

        # ==================================================
        # Activity Log
        # ==================================================

        username = session.get(
            "username",
            "Unknown Admin"
        )

        cursor.execute("""
            INSERT INTO Activity_Log(activity)
            VALUES(%s)
        """,
        (
            f"Admin '{username}' created account: "
            f"{account_number}",
        ))

        connection.commit()

        cursor.close()
        connection.close()

        return redirect("/accounts")

    # ======================================================
    # GET
    # ======================================================

    cursor.close()
    connection.close()

    return render_template(
        "add_account.html",
        customers=customers,
        branches=branches
    )


# ==========================================================
# Edit Account
# ==========================================================

@account_bp.route(
    "/edit_account/<int:id>",
    methods=["GET", "POST"]
)
def edit_account(id):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    # ======================================================
    # POST
    # ======================================================

    if request.method == "POST":

        account_number = request.form["account_number"].strip()
        branch_id = request.form["branch_id"]
        account_type = request.form["account_type"]
        balance = request.form["balance"]
        account_status = request.form["account_status"]
        open_date = request.form["open_date"]

        # ==================================================
        # Check Duplicate Account Number
        # Exclude Current Account
        # ==================================================

        cursor.execute("""
            SELECT account_id
            FROM Accounts
            WHERE account_number = %s
            AND account_id != %s
        """,
        (
            account_number,
            id
        ))

        existing_account = cursor.fetchone()

        if existing_account:

            cursor.execute("""
                SELECT *
                FROM Accounts
                WHERE account_id = %s
            """, (id,))

            account = cursor.fetchone()

            cursor.close()
            connection.close()

            return render_template(
                "edit_account.html",
                account=account,
                error=(
                    f"Account number '{account_number}' "
                    "already exists."
                )
            )

        # ==================================================
        # Update Account
        # ==================================================

        cursor.execute("""
            UPDATE Accounts
            SET
                account_number = %s,
                branch_id = %s,
                account_type = %s,
                balance = %s,
                account_status = %s,
                open_date = %s

            WHERE account_id = %s
        """,
        (
            account_number,
            branch_id,
            account_type,
            balance,
            account_status,
            open_date,
            id
        ))

        # ==================================================
        # Activity Log
        # ==================================================

        username = session.get(
            "username",
            "Unknown Admin"
        )

        cursor.execute("""
            INSERT INTO Activity_Log(activity)
            VALUES(%s)
        """,
        (
            f"Admin '{username}' updated account: "
            f"{account_number}",
        ))

        connection.commit()

        cursor.close()
        connection.close()

        return redirect("/accounts")

    # ======================================================
    # Get Account
    # ======================================================

    cursor.execute("""
        SELECT *
        FROM Accounts
        WHERE account_id = %s
    """, (id,))

    account = cursor.fetchone()

    # ======================================================
    # Get Branches
    # ======================================================

    cursor.execute("""
        SELECT
            branch_id,
            branch_name
        FROM Branches
        ORDER BY branch_name
    """)

    branches = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "edit_account.html",
        account=account,
        branches=branches
    )


# ==========================================================
# Delete Account
# ==========================================================

@account_bp.route("/delete_account/<int:id>")
def delete_account(id):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    # ======================================================
    # Get Account Number Before Delete
    # ======================================================

    cursor.execute("""
        SELECT account_number
        FROM Accounts
        WHERE account_id = %s
    """, (id,))

    account = cursor.fetchone()

    if not account:

        cursor.close()
        connection.close()

        return redirect("/accounts")

    account_number = account["account_number"]

    # ======================================================
    # Delete Account
    # ======================================================

    cursor.execute("""
        DELETE FROM Accounts
        WHERE account_id = %s
    """, (id,))

    # ======================================================
    # Activity Log
    # ======================================================

    username = session.get(
        "username",
        "Unknown Admin"
    )

    cursor.execute("""
        INSERT INTO Activity_Log(activity)
        VALUES(%s)
    """,
    (
        f"Admin '{username}' deleted account: "
        f"{account_number}",
    ))

    connection.commit()

    cursor.close()
    connection.close()

    return redirect("/accounts")