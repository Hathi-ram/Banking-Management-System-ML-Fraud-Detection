from flask import Blueprint, render_template, request, redirect
from models.database import get_connection


# ==========================================================
# Customer Blueprint
# ==========================================================

customer_bp = Blueprint("customer", __name__)


# ==========================================================
# View Customers
# ==========================================================

@customer_bp.route("/customers")
def customers():

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
    # Count Customers
    # ======================================================

    if search == "":

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM Customers
        """)

        total = cursor.fetchone()["total"]


        # --------------------------------------------------
        # Get Customers
        # --------------------------------------------------

        cursor.execute("""
            SELECT *
            FROM Customers
            ORDER BY customer_id
            LIMIT %s OFFSET %s
        """, (
            per_page,
            offset
        ))

    else:

        value = f"%{search}%"


        # --------------------------------------------------
        # Count Search Results
        # --------------------------------------------------

        cursor.execute("""
            SELECT COUNT(*) AS total

            FROM Customers

            WHERE
                first_name LIKE %s
                OR last_name LIKE %s
                OR phone LIKE %s
                OR aadhaar_number LIKE %s
                OR pan_number LIKE %s
                OR email LIKE %s
        """, (
            value,
            value,
            value,
            value,
            value,
            value
        ))

        total = cursor.fetchone()["total"]


        # --------------------------------------------------
        # Get Search Results
        # --------------------------------------------------

        cursor.execute("""
            SELECT *

            FROM Customers

            WHERE
                first_name LIKE %s
                OR last_name LIKE %s
                OR phone LIKE %s
                OR aadhaar_number LIKE %s
                OR pan_number LIKE %s
                OR email LIKE %s

            ORDER BY customer_id

            LIMIT %s OFFSET %s
        """, (
            value,
            value,
            value,
            value,
            value,
            value,
            per_page,
            offset
        ))


    customers = cursor.fetchall()


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
        "customers.html",
        customers=customers,
        search=search,
        page=page,
        total_pages=total_pages
    )


# ==========================================================
# Add Customer
# ==========================================================

@customer_bp.route(
    "/add_customer",
    methods=["GET", "POST"]
)
def add_customer():

    if request.method == "POST":

        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        gender = request.form["gender"]
        dob = request.form["dob"]
        phone = request.form["phone"]
        email = request.form["email"]
        aadhaar_number = request.form["aadhaar_number"]
        pan_number = request.form["pan_number"]
        address = request.form["address"]
        city = request.form["city"]
        state = request.form["state"]
        pincode = request.form["pincode"]


        connection = get_connection()
        cursor = connection.cursor()


        # ==================================================
        # Insert Customer
        # ==================================================

        cursor.execute("""
            INSERT INTO Customers
            (
                first_name,
                last_name,
                gender,
                dob,
                phone,
                email,
                aadhaar_number,
                pan_number,
                address,
                city,
                state,
                pincode
            )

            VALUES
            (
                %s,%s,%s,%s,%s,%s,
                %s,%s,%s,%s,%s,%s
            )
        """, (
            first_name,
            last_name,
            gender,
            dob,
            phone,
            email,
            aadhaar_number,
            pan_number,
            address,
            city,
            state,
            pincode
        ))


        # ==================================================
        # Get New Customer ID
        # ==================================================

        customer_id = cursor.lastrowid


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
            f"Customer Added: "
            f"{first_name} {last_name} "
            f"(ID: {customer_id})",
        ))


        connection.commit()


        cursor.close()
        connection.close()


        return redirect("/customers")


    return render_template(
        "add_customer.html"
    )


# ==========================================================
# Edit Customer
# ==========================================================

@customer_bp.route(
    "/edit_customer/<int:id>",
    methods=["GET", "POST"]
)
def edit_customer(id):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)


    # ======================================================
    # POST - Update Customer
    # ======================================================

    if request.method == "POST":

        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        phone = request.form["phone"]
        address = request.form["address"]


        cursor.execute("""
            UPDATE Customers

            SET
                first_name=%s,
                last_name=%s,
                email=%s,
                phone=%s,
                address=%s

            WHERE customer_id=%s
        """, (
            first_name,
            last_name,
            email,
            phone,
            address,
            id
        ))


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
            f"Customer Updated: "
            f"{first_name} {last_name} "
            f"(ID: {id})",
        ))


        connection.commit()


        cursor.close()
        connection.close()


        return redirect("/customers")


    # ======================================================
    # GET - Get Customer
    # ======================================================

    cursor.execute("""
        SELECT *
        FROM Customers
        WHERE customer_id=%s
    """, (
        id,
    ))


    customer = cursor.fetchone()


    cursor.close()
    connection.close()


    return render_template(
        "edit_customer.html",
        customer=customer
    )


# ==========================================================
# Delete Customer
# ==========================================================

@customer_bp.route(
    "/delete_customer/<int:id>"
)
def delete_customer(id):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)


    # ======================================================
    # Get Customer Before Delete
    # ======================================================

    cursor.execute("""
        SELECT
            first_name,
            last_name

        FROM Customers

        WHERE customer_id=%s
    """, (
        id,
    ))


    customer = cursor.fetchone()


    # ======================================================
    # Delete Customer
    # ======================================================

    cursor.execute("""
        DELETE FROM Customers

        WHERE customer_id=%s
    """, (
        id,
    ))


    # ======================================================
    # Activity Log
    # ======================================================

    if customer:

        customer_name = (
            customer["first_name"]
            + " "
            + customer["last_name"]
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
            f"Customer Deleted: "
            f"{customer_name} "
            f"(ID: {id})",
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
            f"Customer Delete Attempt: "
            f"Customer ID {id} not found",
        ))


    connection.commit()


    cursor.close()
    connection.close()


    return redirect("/customers")

