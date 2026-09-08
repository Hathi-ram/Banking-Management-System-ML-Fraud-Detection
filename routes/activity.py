from flask import Blueprint, render_template, request
from models.database import get_connection


# ==========================================================
# Activity Blueprint
# ==========================================================

activity_bp = Blueprint("activity", __name__)


# ==========================================================
# Activity Log
# ==========================================================

@activity_bp.route("/activity")
def activity():

    connection = None
    cursor = None

    try:

        connection = get_connection()

        if not connection:
            return "Database connection failed."

        cursor = connection.cursor(dictionary=True)

        # ==================================================
        # Search
        # ==================================================

        search = request.args.get("search", "").strip()


        # ==================================================
        # Pagination
        # ==================================================

        page = request.args.get(
            "page",
            1,
            type=int
        )

        if page < 1:
            page = 1

        per_page = 10

        offset = (page - 1) * per_page


        # ==================================================
        # Count Activity Records
        # ==================================================

        if search:

            search_value = "%" + search + "%"

            cursor.execute(
                """
                SELECT COUNT(*) AS total

                FROM Activity_Log

                WHERE activity LIKE %s
                """,
                (search_value,)
            )

        else:

            cursor.execute(
                """
                SELECT COUNT(*) AS total

                FROM Activity_Log
                """
            )


        result = cursor.fetchone()

        total = result["total"]


        # ==================================================
        # Get Activity Records
        # ==================================================

        if search:

            cursor.execute(
                """
                SELECT
                    log_id,
                    activity,
                    activity_time

                FROM Activity_Log

                WHERE activity LIKE %s

                ORDER BY activity_time DESC

                LIMIT %s OFFSET %s
                """,
                (
                    search_value,
                    per_page,
                    offset
                )
            )

        else:

            cursor.execute(
                """
                SELECT
                    log_id,
                    activity,
                    activity_time

                FROM Activity_Log

                ORDER BY activity_time DESC

                LIMIT %s OFFSET %s
                """,
                (
                    per_page,
                    offset
                )
            )


        activities = cursor.fetchall()


        # ==================================================
        # Calculate Total Pages
        # ==================================================

        if total > 0:

            total_pages = (
                (total + per_page - 1)
                // per_page
            )

        else:

            total_pages = 1


        # ==================================================
        # Prevent Invalid Page
        # ==================================================

        if page > total_pages:

            page = total_pages


        # ==================================================
        # Render Activity Page
        # ==================================================

        return render_template(
            "activity.html",
            activities=activities,
            search=search,
            page=page,
            total_pages=total_pages
        )


    except Exception as e:

        print("\n========================================")
        print("ACTIVITY PAGE ERROR")
        print("========================================")
        print(e)
        print("========================================\n")

        return "Activity page error: " + str(e)


    finally:

        if cursor:

            cursor.close()

        if connection:

            connection.close()
