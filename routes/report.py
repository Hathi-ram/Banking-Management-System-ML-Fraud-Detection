from flask import Blueprint, render_template, send_file

from models.database import get_connection

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from io import BytesIO
from datetime import datetime


# ==========================================================
# REPORT BLUEPRINT
# ==========================================================

report_bp = Blueprint("report", __name__)


# ==========================================================
# BANKING REPORTS
# ==========================================================

@report_bp.route("/reports")
def reports():

    connection = get_connection()

    if not connection:
        return "Database Connection Failed"

    cursor = connection.cursor(dictionary=True)

    try:

        # ==================================================
        # BANKING OVERVIEW
        # ==================================================

        # --------------------------------------------------
        # Total Customers
        # --------------------------------------------------

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM Customers
        """)

        customers = cursor.fetchone()["total"]


        # --------------------------------------------------
        # Total Accounts
        # --------------------------------------------------

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM Accounts
        """)

        accounts = cursor.fetchone()["total"]


        # --------------------------------------------------
        # Total Transactions
        # --------------------------------------------------

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM Transactions
        """)

        transactions = cursor.fetchone()["total"]


        # --------------------------------------------------
        # Total Employees
        # --------------------------------------------------

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM Employees
        """)

        employees = cursor.fetchone()["total"]


        # --------------------------------------------------
        # Total Cards
        # --------------------------------------------------

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM Cards
        """)

        cards = cursor.fetchone()["total"]


        # --------------------------------------------------
        # Active Cards
        # --------------------------------------------------

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM Cards
            WHERE card_status = 'Active'
        """)

        active_cards = cursor.fetchone()["total"]


        # --------------------------------------------------
        # Total Bank Balance
        # --------------------------------------------------

        cursor.execute("""
            SELECT COALESCE(
                SUM(balance),
                0
            ) AS total
            FROM Accounts
        """)

        total_balance = cursor.fetchone()["total"]


        # --------------------------------------------------
        # Approved Loan Amount
        # --------------------------------------------------

        cursor.execute("""
            SELECT COALESCE(
                SUM(loan_amount),
                0
            ) AS total
            FROM Loans
            WHERE loan_status = 'Approved'
        """)

        total_loans = cursor.fetchone()["total"]


        # ==================================================
        # ML FRAUD DETECTION
        # ==================================================

        # --------------------------------------------------
        # Transactions Analyzed
        # --------------------------------------------------

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM Transactions
            WHERE ml_risk_score IS NOT NULL
        """)

        ml_analyzed = cursor.fetchone()["total"]


        # --------------------------------------------------
        # Normal Transactions
        # --------------------------------------------------

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM Transactions
            WHERE ml_risk_score IS NOT NULL
            AND ml_prediction = 0
        """)

        ml_normal = cursor.fetchone()["total"]


        # --------------------------------------------------
        # Suspicious Transactions
        # --------------------------------------------------

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM Transactions
            WHERE ml_risk_score IS NOT NULL
            AND ml_prediction = 1
        """)

        ml_suspicious = cursor.fetchone()["total"]


        # --------------------------------------------------
        # High Risk Transactions
        # --------------------------------------------------

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM Transactions
            WHERE ml_risk_score IS NOT NULL
            AND ml_risk_level = 'High'
        """)

        ml_high_risk = cursor.fetchone()["total"]


        # ==================================================
        # RISK DISTRIBUTION
        # ==================================================

        # --------------------------------------------------
        # Low Risk
        # --------------------------------------------------

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM Transactions
            WHERE ml_risk_score IS NOT NULL
            AND ml_risk_level = 'Low'
        """)

        low_risk = cursor.fetchone()["total"]


        # --------------------------------------------------
        # Medium Risk
        # --------------------------------------------------

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM Transactions
            WHERE ml_risk_score IS NOT NULL
            AND ml_risk_level = 'Medium'
        """)

        medium_risk = cursor.fetchone()["total"]


        # --------------------------------------------------
        # High Risk
        # --------------------------------------------------

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM Transactions
            WHERE ml_risk_score IS NOT NULL
            AND ml_risk_level = 'High'
        """)

        high_risk = cursor.fetchone()["total"]


        # ==================================================
        # MODEL INFORMATION
        # ==================================================

        model_name = "Random Forest"

        model_version = "v1.0"

        model_features = 24

        model_threshold = 0.55


        return render_template(
            "reports.html",

            # Banking
            customers=customers,
            accounts=accounts,
            transactions=transactions,
            employees=employees,
            cards=cards,
            active_cards=active_cards,
            total_balance=total_balance,
            total_loans=total_loans,

            # ML
            ml_analyzed=ml_analyzed,
            ml_normal=ml_normal,
            ml_suspicious=ml_suspicious,
            ml_high_risk=ml_high_risk,

            # Risk Distribution
            low_risk=low_risk,
            medium_risk=medium_risk,
            high_risk=high_risk,

            # Model
            model_name=model_name,
            model_version=model_version,
            model_features=model_features,
            model_threshold=model_threshold
        )

    finally:

        cursor.close()
        connection.close()


# ==========================================================
# EXPORT BANKING + ML REPORT AS PDF
# ==========================================================

@report_bp.route("/reports/pdf")
def export_report_pdf():

    connection = get_connection()

    if not connection:
        return "Database Connection Failed"

    cursor = connection.cursor(dictionary=True)

    try:

        # ==================================================
        # BANKING DATA
        # ==================================================

        # Customers
        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM Customers
        """)

        customers = cursor.fetchone()["total"]


        # Accounts
        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM Accounts
        """)

        accounts = cursor.fetchone()["total"]


        # Transactions
        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM Transactions
        """)

        transactions = cursor.fetchone()["total"]


        # Employees
        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM Employees
        """)

        employees = cursor.fetchone()["total"]


        # Cards
        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM Cards
        """)

        cards = cursor.fetchone()["total"]


        # Active Cards
        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM Cards
            WHERE card_status = 'Active'
        """)

        active_cards = cursor.fetchone()["total"]


        # Bank Balance
        cursor.execute("""
            SELECT COALESCE(
                SUM(balance),
                0
            ) AS total
            FROM Accounts
        """)

        total_balance = cursor.fetchone()["total"]


        # Approved Loans
        cursor.execute("""
            SELECT COALESCE(
                SUM(loan_amount),
                0
            ) AS total
            FROM Loans
            WHERE loan_status = 'Approved'
        """)

        total_loans = cursor.fetchone()["total"]


        # ==================================================
        # ML DATA
        # ==================================================

        # Analyzed
        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM Transactions
            WHERE ml_risk_score IS NOT NULL
        """)

        ml_analyzed = cursor.fetchone()["total"]


        # Normal
        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM Transactions
            WHERE ml_risk_score IS NOT NULL
            AND ml_prediction = 0
        """)

        ml_normal = cursor.fetchone()["total"]


        # Suspicious
        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM Transactions
            WHERE ml_risk_score IS NOT NULL
            AND ml_prediction = 1
        """)

        ml_suspicious = cursor.fetchone()["total"]


        # High Risk
        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM Transactions
            WHERE ml_risk_score IS NOT NULL
            AND ml_risk_level = 'High'
        """)

        ml_high_risk = cursor.fetchone()["total"]


        # Risk Distribution
        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM Transactions
            WHERE ml_risk_score IS NOT NULL
            AND ml_risk_level = 'Low'
        """)

        low_risk = cursor.fetchone()["total"]


        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM Transactions
            WHERE ml_risk_score IS NOT NULL
            AND ml_risk_level = 'Medium'
        """)

        medium_risk = cursor.fetchone()["total"]


        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM Transactions
            WHERE ml_risk_score IS NOT NULL
            AND ml_risk_level = 'High'
        """)

        high_risk = cursor.fetchone()["total"]


    finally:

        cursor.close()
        connection.close()


    # ======================================================
    # CREATE PDF
    # ======================================================

    pdf_buffer = BytesIO()

    document = SimpleDocTemplate(
        pdf_buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )


    styles = getSampleStyleSheet()


    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=20,
        spaceAfter=10
    )


    section_style = ParagraphStyle(
        "SectionTitle",
        parent=styles["Heading2"],
        fontSize=15,
        spaceBefore=15,
        spaceAfter=10
    )


    normal_style = styles["Normal"]


    elements = []


    # ======================================================
    # TITLE
    # ======================================================

    elements.append(
        Paragraph(
            "BANKING MANAGEMENT SYSTEM",
            title_style
        )
    )


    elements.append(
        Paragraph(
            "Banking Reports",
            title_style
        )
    )


    elements.append(
        Paragraph(
            "Generated on: " +
            datetime.now().strftime(
                "%d-%m-%Y %H:%M:%S"
            ),
            normal_style
        )
    )


    elements.append(
        Spacer(1, 20)
    )


    # ======================================================
    # BANKING OVERVIEW
    # ======================================================

    elements.append(
        Paragraph(
            "Banking Overview",
            section_style
        )
    )


    banking_data = [

        ["Report", "Value"],

        ["Total Customers", str(customers)],

        ["Total Accounts", str(accounts)],

        ["Total Transactions", str(transactions)],

        ["Total Employees", str(employees)],

        ["Total Cards", str(cards)],

        ["Active Cards", str(active_cards)],

        [
            "Total Bank Balance",
            "Rs. " +
            format(
                float(total_balance),
                ",.2f"
            )
        ],

        [
            "Approved Loan Amount",
            "Rs. " +
            format(
                float(total_loans),
                ",.2f"
            )
        ]

    ]


    banking_table = Table(
        banking_data,
        colWidths=[300, 150]
    )


    banking_table.setStyle(
        TableStyle([

            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.grey
            ),

            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 0),
                colors.white
            ),

            (
                "FONTNAME",
                (0, 0),
                (-1, 0),
                "Helvetica-Bold"
            ),

            (
                "ALIGN",
                (1, 1),
                (1, -1),
                "RIGHT"
            ),

            (
                "GRID",
                (0, 0),
                (-1, -1),
                1,
                colors.black
            ),

            (
                "PADDING",
                (0, 0),
                (-1, -1),
                8
            )

        ])
    )


    elements.append(banking_table)


    # ======================================================
    # ML FRAUD DETECTION
    # ======================================================

    elements.append(
        Paragraph(
            "ML Fraud Detection",
            section_style
        )
    )


    ml_data = [

        ["Metric", "Value"],

        [
            "Transactions Analyzed",
            str(ml_analyzed)
        ],

        [
            "Normal Transactions",
            str(ml_normal)
        ],

        [
            "Suspicious Transactions",
            str(ml_suspicious)
        ],

        [
            "High Risk Transactions",
            str(ml_high_risk)
        ],

        [
            "Model",
            "Random Forest"
        ],

        [
            "Model Version",
            "v1.0"
        ],

        [
            "Features",
            "24"
        ],

        [
            "Threshold",
            "55%"
        ]

    ]


    ml_table = Table(
        ml_data,
        colWidths=[300, 150]
    )


    ml_table.setStyle(
        TableStyle([

            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.grey
            ),

            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 0),
                colors.white
            ),

            (
                "FONTNAME",
                (0, 0),
                (-1, 0),
                "Helvetica-Bold"
            ),

            (
                "ALIGN",
                (1, 1),
                (1, -1),
                "RIGHT"
            ),

            (
                "GRID",
                (0, 0),
                (-1, -1),
                1,
                colors.black
            ),

            (
                "PADDING",
                (0, 0),
                (-1, -1),
                8
            )

        ])
    )


    elements.append(ml_table)


    # ======================================================
    # RISK DISTRIBUTION
    # ======================================================

    elements.append(
        Paragraph(
            "Risk Distribution",
            section_style
        )
    )


    risk_data = [

        ["Risk Level", "Transactions"],

        ["Low Risk", str(low_risk)],

        ["Medium Risk", str(medium_risk)],

        ["High Risk", str(high_risk)]

    ]


    risk_table = Table(
        risk_data,
        colWidths=[300, 150]
    )


    risk_table.setStyle(
        TableStyle([

            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.grey
            ),

            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 0),
                colors.white
            ),

            (
                "FONTNAME",
                (0, 0),
                (-1, 0),
                "Helvetica-Bold"
            ),

            (
                "ALIGN",
                (1, 1),
                (1, -1),
                "RIGHT"
            ),

            (
                "GRID",
                (0, 0),
                (-1, -1),
                1,
                colors.black
            ),

            (
                "PADDING",
                (0, 0),
                (-1, -1),
                8
            )

        ])
    )


    elements.append(risk_table)


    elements.append(
        Spacer(1, 25)
    )


    elements.append(
        Paragraph(
            "Generated by Banking Management System",
            normal_style
        )
    )


    # ======================================================
    # BUILD PDF
    # ======================================================

    document.build(elements)

    pdf_buffer.seek(0)


    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name="Banking_ML_Report.pdf",
        mimetype="application/pdf"
    )