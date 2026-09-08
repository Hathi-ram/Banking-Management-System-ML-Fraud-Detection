from flask import Blueprint, render_template, request, redirect, session
from models.database import get_connection

import random
from datetime import date


card_bp = Blueprint("card", __name__)


# ==========================================================
# View Cards
# ==========================================================

@card_bp.route("/cards")
def cards():

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    search = request.args.get("search", "").strip()

    page = request.args.get("page", 1, type=int)

    # Prevent invalid page numbers
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
            FROM Cards
        """)

        total = cursor.fetchone()["total"]

        cursor.execute("""
            SELECT
                c.card_id,
                c.card_number,
                c.card_type,
                c.card_status,
                c.issue_date,
                c.expiry_date,

                CONCAT(
                    cu.first_name,
                    ' ',
                    cu.last_name
                ) AS customer_name

            FROM Cards c

            INNER JOIN Accounts a
                ON c.account_id = a.account_id

            INNER JOIN Customers cu
                ON a.customer_id = cu.customer_id

            ORDER BY c.card_id DESC

            LIMIT %s OFFSET %s
        """, (
            per_page,
            offset
        ))

    # ======================================================
    # With Search
    # ======================================================

    else:

        value = f"%{search}%"

        cursor.execute("""
            SELECT COUNT(*) AS total

            FROM Cards c

            INNER JOIN Accounts a
                ON c.account_id = a.account_id

            INNER JOIN Customers cu
                ON a.customer_id = cu.customer_id

            WHERE
                c.card_number LIKE %s
                OR cu.first_name LIKE %s
                OR cu.last_name LIKE %s
                OR c.card_type LIKE %s
                OR c.card_status LIKE %s

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
                c.card_id,
                c.card_number,
                c.card_type,
                c.card_status,
                c.issue_date,
                c.expiry_date,

                CONCAT(
                    cu.first_name,
                    ' ',
                    cu.last_name
                ) AS customer_name

            FROM Cards c

            INNER JOIN Accounts a
                ON c.account_id = a.account_id

            INNER JOIN Customers cu
                ON a.customer_id = cu.customer_id

            WHERE
                c.card_number LIKE %s
                OR cu.first_name LIKE %s
                OR cu.last_name LIKE %s
                OR c.card_type LIKE %s
                OR c.card_status LIKE %s

            ORDER BY c.card_id DESC

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

    cards = cursor.fetchall()

    total_pages = (total + per_page - 1) // per_page

    cursor.close()
    connection.close()

    return render_template(
        "cards.html",
        cards=cards,
        search=search,
        page=page,
        total_pages=total_pages
    )


# ==========================================================
# Add Card
# ==========================================================

@card_bp.route("/add_card", methods=["GET", "POST"])
def add_card():

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    # ======================================================
    # Add Card
    # ======================================================

    if request.method == "POST":

        account_id = request.form["account_id"]
        card_type = request.form["card_type"]

        # --------------------------------------------------
        # Generate Unique Card Number
        # --------------------------------------------------

        while True:

            card_number = str(
                random.randint(
                    4000000000000000,
                    4999999999999999
                )
            )

            cursor.execute("""
                SELECT card_id
                FROM Cards
                WHERE card_number=%s
            """, (card_number,))

            existing_card = cursor.fetchone()

            if not existing_card:
                break

        # --------------------------------------------------
        # Generate CVV
        # --------------------------------------------------

        cvv = str(
            random.randint(
                100,
                999
            )
        )

        # --------------------------------------------------
        # Dates
        # --------------------------------------------------

        issue_date = date.today()

        try:
            expiry_date = issue_date.replace(
                year=issue_date.year + 5
            )
        except ValueError:
            # Handles February 29 on leap years
            expiry_date = issue_date.replace(
                year=issue_date.year + 5,
                day=28
            )

        # --------------------------------------------------
        # Insert Card
        # --------------------------------------------------

        cursor.execute("""
            INSERT INTO Cards
            (
                card_number,
                account_id,
                card_type,
                issue_date,
                expiry_date,
                cvv
            )

            VALUES
            (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
            )

        """, (
            card_number,
            account_id,
            card_type,
            issue_date,
            expiry_date,
            cvv
        ))

        # --------------------------------------------------
        # Activity Log
        # --------------------------------------------------

        username = session.get(
            "username",
            "Unknown Admin"
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
            f"Admin '{username}' issued new card: "
            f"{card_number}",
        ))

        connection.commit()

        cursor.close()
        connection.close()

        return redirect("/cards")

    # ======================================================
    # Get Accounts
    # ======================================================

    cursor.execute("""
        SELECT
            account_id,
            account_number

        FROM Accounts

        ORDER BY account_number
    """)

    accounts = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "add_card.html",
        accounts=accounts
    )


# ==========================================================
# Block Card
# ==========================================================

@card_bp.route("/block_card/<int:card_id>")
def block_card(card_id):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    # ------------------------------------------------------
    # Get Card Number
    # ------------------------------------------------------

    cursor.execute("""
        SELECT card_number
        FROM Cards
        WHERE card_id=%s
    """, (
        card_id,
    ))

    card = cursor.fetchone()

    if card:

        # --------------------------------------------------
        # Block Card
        # --------------------------------------------------

        cursor.execute("""
            UPDATE Cards

            SET card_status='Blocked'

            WHERE card_id=%s
        """, (
            card_id,
        ))

        # --------------------------------------------------
        # Activity Log
        # --------------------------------------------------

        username = session.get(
            "username",
            "Unknown Admin"
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
            f"Admin '{username}' blocked card: "
            f"{card['card_number']}",
        ))

    connection.commit()

    cursor.close()
    connection.close()

    return redirect("/cards")


# ==========================================================
# Activate Card
# ==========================================================

@card_bp.route("/activate_card/<int:card_id>")
def activate_card(card_id):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    # ------------------------------------------------------
    # Get Card Number
    # ------------------------------------------------------

    cursor.execute("""
        SELECT card_number
        FROM Cards
        WHERE card_id=%s
    """, (
        card_id,
    ))

    card = cursor.fetchone()

    if card:

        # --------------------------------------------------
        # Activate Card
        # --------------------------------------------------

        cursor.execute("""
            UPDATE Cards

            SET card_status='Active'

            WHERE card_id=%s
        """, (
            card_id,
        ))

        # --------------------------------------------------
        # Activity Log
        # --------------------------------------------------

        username = session.get(
            "username",
            "Unknown Admin"
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
            f"Admin '{username}' activated card: "
            f"{card['card_number']}",
        ))

    connection.commit()

    cursor.close()
    connection.close()

    return redirect("/cards")


# ==========================================================
# Edit Card
# ==========================================================

@card_bp.route(
    "/edit_card/<int:card_id>",
    methods=["GET", "POST"]
)
def edit_card(card_id):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    # ======================================================
    # Update Card
    # ======================================================

    if request.method == "POST":

        card_type = request.form["card_type"]
        card_status = request.form["card_status"]

        # --------------------------------------------------
        # Get Existing Card
        # --------------------------------------------------

        cursor.execute("""
            SELECT
                card_number,
                card_type,
                card_status
            FROM Cards
            WHERE card_id=%s
        """, (
            card_id,
        ))

        card = cursor.fetchone()

        # --------------------------------------------------
        # Card Not Found
        # --------------------------------------------------

        if not card:

            cursor.close()
            connection.close()

            return "Card not found.", 404

        # --------------------------------------------------
        # Update Card
        # --------------------------------------------------

        cursor.execute("""
            UPDATE Cards

            SET
                card_type=%s,
                card_status=%s

            WHERE card_id=%s
        """, (
            card_type,
            card_status,
            card_id
        ))

        # --------------------------------------------------
        # Activity Log
        # --------------------------------------------------

        username = session.get(
            "username",
            "Unknown Admin"
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
            f"Admin '{username}' updated card: "
            f"{card['card_number']} "
            f"(Type: {card_type}, "
            f"Status: {card_status})",
        ))

        connection.commit()

        cursor.close()
        connection.close()

        return redirect("/cards")

    # ======================================================
    # Get Card Details
    # ======================================================

    cursor.execute("""
        SELECT *
        FROM Cards
        WHERE card_id=%s
    """, (
        card_id,
    ))

    card = cursor.fetchone()

    cursor.close()
    connection.close()

    if not card:

        return "Card not found.", 404

    return render_template(
        "edit_card.html",
        card=card
    )