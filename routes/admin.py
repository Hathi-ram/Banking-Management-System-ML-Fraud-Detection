from flask import Blueprint, render_template, request, redirect, session
from models.database import get_connection


admin_bp = Blueprint("admin", __name__)


# ==========================================================
# Admin Profile
# ==========================================================

@admin_bp.route("/admin")
def admin_profile():

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM Admin
        LIMIT 1
    """)

    admin = cursor.fetchone()

    cursor.close()
    connection.close()

    return render_template(
        "admin_profile.html",
        admin=admin
    )


# ==========================================================
# Edit Admin Profile
# ==========================================================

@admin_bp.route(
    "/edit_admin",
    methods=["GET", "POST"]
)
def edit_admin():

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]
        full_name = request.form["full_name"]
        email = request.form["email"]
        phone = request.form["phone"]


        # ==================================================
        # Update Admin Profile
        # ==================================================

        cursor.execute("""
            UPDATE Admin

            SET
                username=%s,
                password=%s,
                full_name=%s,
                email=%s,
                phone=%s

            WHERE admin_id=1
        """,
        (
            username,
            password,
            full_name,
            email,
            phone
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
        """,
        (
            f"Admin '{username}' updated profile",
        ))


        # ==================================================
        # Update Session Username
        # ==================================================

        session["username"] = username


        connection.commit()


        cursor.close()
        connection.close()


        return redirect("/admin")


    # ======================================================
    # Get Admin
    # ======================================================

    cursor.execute("""
        SELECT *
        FROM Admin
        WHERE admin_id=1
    """)

    admin = cursor.fetchone()

    cursor.close()
    connection.close()


    return render_template(
        "edit_admin.html",
        admin=admin
    )


# ==========================================================
# Change Admin Password
# ==========================================================

@admin_bp.route(
    "/change_password",
    methods=["GET", "POST"]
)
def change_password():

    message = None
    error = None

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)


    if request.method == "POST":

        current_password = request.form["current_password"]

        new_password = request.form["new_password"]

        confirm_password = request.form["confirm_password"]


        # ==================================================
        # Get Current Admin Password
        # ==================================================

        cursor.execute("""
            SELECT
                username,
                password
            FROM Admin
            WHERE admin_id=1
        """)

        admin = cursor.fetchone()


        # ==================================================
        # Validation
        # ==================================================

        if not admin:

            error = "Admin account not found."


        elif current_password != admin["password"]:

            error = "Current password is incorrect."


        elif new_password != confirm_password:

            error = "New passwords do not match."


        elif len(new_password) < 6:

            error = "Password must contain at least 6 characters."


        else:

            # ==============================================
            # Update Password
            # ==============================================

            cursor.execute("""
                UPDATE Admin

                SET password=%s

                WHERE admin_id=1
            """,
            (
                new_password,
            ))


            # ==============================================
            # Activity Log
            # ==============================================

            cursor.execute("""
                INSERT INTO Activity_Log
                (
                    activity
                )
                VALUES
                (
                    %s
                )
            """,
            (
                f"Admin '{admin['username']}' changed password",
            ))


            connection.commit()


            message = "Password changed successfully."


    cursor.close()
    connection.close()


    return render_template(
        "change_password.html",
        message=message,
        error=error
    )