from flask import Blueprint, render_template, request, redirect
from models.database import get_connection


employee_bp = Blueprint("employee", __name__)


# =====================================
# View Employees
# =====================================

@employee_bp.route("/employees")
def employees():

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    search = request.args.get("search", "").strip()

    page = request.args.get("page", 1, type=int)

    per_page = 10

    offset = (page - 1) * per_page


    # ====================================
    # Without Search
    # ====================================

    if search == "":

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM Employees
        """)

        total = cursor.fetchone()["total"]


        cursor.execute("""
            SELECT

                e.employee_id,
                e.employee_code,
                e.first_name,
                e.last_name,
                e.designation,
                e.salary,
                e.phone,
                e.email,
                e.hire_date,

                b.branch_name

            FROM Employees e

            LEFT JOIN Branches b
                ON e.branch_id = b.branch_id

            ORDER BY e.employee_id DESC

            LIMIT %s OFFSET %s

        """, (
            per_page,
            offset
        ))


    # ====================================
    # Search
    # ====================================

    else:

        value = f"%{search}%"


        cursor.execute("""
            SELECT COUNT(*) AS total

            FROM Employees e

            LEFT JOIN Branches b
                ON e.branch_id = b.branch_id

            WHERE

                e.employee_code LIKE %s

                OR e.first_name LIKE %s

                OR e.last_name LIKE %s

                OR e.designation LIKE %s

                OR e.phone LIKE %s

                OR e.email LIKE %s

                OR b.branch_name LIKE %s

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


        cursor.execute("""
            SELECT

                e.employee_id,
                e.employee_code,
                e.first_name,
                e.last_name,
                e.designation,
                e.salary,
                e.phone,
                e.email,
                e.hire_date,

                b.branch_name

            FROM Employees e

            LEFT JOIN Branches b
                ON e.branch_id = b.branch_id

            WHERE

                e.employee_code LIKE %s

                OR e.first_name LIKE %s

                OR e.last_name LIKE %s

                OR e.designation LIKE %s

                OR e.phone LIKE %s

                OR e.email LIKE %s

                OR b.branch_name LIKE %s

            ORDER BY e.employee_id DESC

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


    employees = cursor.fetchall()


    total_pages = (
        total + per_page - 1
    ) // per_page


    cursor.close()
    connection.close()


    return render_template(
        "employees.html",

        employees=employees,

        search=search,

        page=page,

        total_pages=total_pages
    )


# =====================================
# Add Employee
# =====================================

@employee_bp.route(
    "/add_employee",
    methods=["GET", "POST"]
)
def add_employee():

    connection = get_connection()

    cursor = connection.cursor(
        dictionary=True
    )


    if request.method == "POST":

        employee_code = request.form["employee_code"]

        first_name = request.form["first_name"]

        last_name = request.form["last_name"]

        gender = request.form["gender"]

        designation = request.form["designation"]

        salary = request.form["salary"]

        phone = request.form["phone"]

        email = request.form["email"]

        hire_date = request.form["hire_date"]

        branch_id = request.form["branch_id"]


        # ==========================================
        # Insert Employee
        # ==========================================

        cursor.execute("""
            INSERT INTO Employees
            (
                employee_code,
                first_name,
                last_name,
                gender,
                designation,
                salary,
                phone,
                email,
                hire_date,
                branch_id
            )

            VALUES
            (
                %s,%s,%s,%s,%s,
                %s,%s,%s,%s,%s
            )

        """, (
            employee_code,
            first_name,
            last_name,
            gender,
            designation,
            salary,
            phone,
            email,
            hire_date,
            branch_id
        ))


        # ==========================================
        # Activity Log
        # ==========================================

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
            f"New Employee Added: {first_name} {last_name} "
            f"(Code: {employee_code})",
        ))


        connection.commit()


        cursor.close()
        connection.close()


        return redirect("/employees")


    # ==========================================
    # Get Branches
    # ==========================================

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
        "add_employee.html",
        branches=branches
    )


# =====================================
# Edit Employee
# =====================================

@employee_bp.route(
    "/edit_employee/<int:employee_id>",
    methods=["GET", "POST"]
)
def edit_employee(employee_id):

    connection = get_connection()

    cursor = connection.cursor(
        dictionary=True
    )


    if request.method == "POST":

        designation = request.form["designation"]

        salary = request.form["salary"]

        phone = request.form["phone"]

        email = request.form["email"]


        # ==========================================
        # Get Employee Information
        # ==========================================

        cursor.execute("""
            SELECT
                employee_code,
                first_name,
                last_name

            FROM Employees

            WHERE employee_id=%s

        """, (
            employee_id,
        ))


        employee = cursor.fetchone()


        # ==========================================
        # Update Employee
        # ==========================================

        cursor.execute("""
            UPDATE Employees

            SET

                designation=%s,
                salary=%s,
                phone=%s,
                email=%s

            WHERE employee_id=%s

        """, (
            designation,
            salary,
            phone,
            email,
            employee_id
        ))


        # ==========================================
        # Activity Log
        # ==========================================

        if employee:

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
                f"Employee Updated: "
                f"{employee['first_name']} "
                f"{employee['last_name']} "
                f"(Code: {employee['employee_code']})",
            ))


        connection.commit()


        cursor.close()
        connection.close()


        return redirect("/employees")


    # ==========================================
    # Get Employee
    # ==========================================

    cursor.execute("""
        SELECT *
        FROM Employees
        WHERE employee_id=%s
    """, (
        employee_id,
    ))


    employee = cursor.fetchone()


    cursor.close()
    connection.close()


    return render_template(
        "edit_employee.html",
        employee=employee
    )


# =====================================
# Delete Employee
# =====================================

@employee_bp.route(
    "/delete_employee/<int:employee_id>"
)
def delete_employee(employee_id):

    connection = get_connection()

    cursor = connection.cursor(
        dictionary=True
    )


    # ==========================================
    # Get Employee Information Before Delete
    # ==========================================

    cursor.execute("""
        SELECT
            employee_code,
            first_name,
            last_name

        FROM Employees

        WHERE employee_id=%s

    """, (
        employee_id,
    ))


    employee = cursor.fetchone()


    # ==========================================
    # Delete Employee
    # ==========================================

    cursor.execute("""
        DELETE FROM Employees

        WHERE employee_id=%s
    """, (
        employee_id,
    ))


    # ==========================================
    # Activity Log
    # ==========================================

    if employee:

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
            f"Employee Deleted: "
            f"{employee['first_name']} "
            f"{employee['last_name']} "
            f"(Code: {employee['employee_code']})",
        ))


    connection.commit()


    cursor.close()
    connection.close()


    return redirect("/employees")