from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
import os
def generate_pdf(result, filename):
    pdf_path = "reports/report.pdf"
    os.makedirs("reports", exist_ok=True)
    doc = SimpleDocTemplate(pdf_path)
    styles = getSampleStyleSheet()
    story = []
    story.append(Paragraph("<b>Log File Analysis Report</b>", styles["Title"]))
    story.append(Spacer(1, 20))
    story.append(Paragraph(f"<b>File Name:</b> {filename}", styles["Normal"]))
    story.append(Paragraph(f"<b>Total Log Entries:</b> {result['total_lines']}", styles["Normal"]))
    story.append(Paragraph(f"<b>Failed Login Attempts:</b> {result['failed_logins']}", styles["Normal"]))
    story.append(Paragraph(f"<b>Unique IP Addresses:</b> {len(result['ip_count'])}", styles["Normal"]))

    if result["brute_force_ips"]:
        story.append(
            Paragraph(
                "<b>Brute Force Attack:</b> Detected",
                styles["Normal"]
            )
        )
    else:
        story.append(
            Paragraph(
                "<b>Brute Force Attack:</b> Not Detected",
                styles["Normal"]
            )
        )
    story.append(Spacer(1, 20))
    if os.path.exists("static/images/chart.png"):
        story.append(Image("static/images/chart.png", width=400, height=200))
    story.append(Spacer(1, 20))
    if os.path.exists("static/images/pie.png"):
        story.append(Image("static/images/pie.png", width=300, height=300))
    doc.build(story)
    return pdf_path