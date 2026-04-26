from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import ListFlowable, ListItem, PageBreak, Paragraph, SimpleDocTemplate, Spacer


BASE_DIR = Path(__file__).resolve().parent.parent
SOURCE_PATH = BASE_DIR / "output" / "report_data" / "skillbuddy_project_report.md"
OUTPUT_PATH = BASE_DIR / "output" / "pdf" / "skillbuddy_project_report.pdf"


def build_styles():
    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="ReportTitle",
            parent=styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=22,
            leading=28,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#4b2344"),
            spaceAfter=14,
        )
    )
    styles.add(
        ParagraphStyle(
            name="ReportMeta",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=10.5,
            leading=14,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#6d4c67"),
            spaceAfter=5,
        )
    )
    styles.add(
        ParagraphStyle(
            name="ReportH1",
            parent=styles["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=15,
            leading=20,
            textColor=colors.HexColor("#5f2b57"),
            spaceBefore=10,
            spaceAfter=8,
        )
    )
    styles.add(
        ParagraphStyle(
            name="ReportH2",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=12,
            leading=16,
            textColor=colors.HexColor("#76468e"),
            spaceBefore=8,
            spaceAfter=6,
        )
    )
    styles.add(
        ParagraphStyle(
            name="ReportBody",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=10.5,
            leading=15,
            alignment=TA_JUSTIFY,
            textColor=colors.HexColor("#2f2436"),
            spaceAfter=7,
        )
    )
    styles.add(
        ParagraphStyle(
            name="ReportBullet",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=10.5,
            leading=14,
            leftIndent=10,
            textColor=colors.HexColor("#2f2436"),
        )
    )
    return styles


def page_canvas(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#cfa0c8"))
    canvas.setLineWidth(0.8)
    canvas.line(doc.leftMargin, A4[1] - 1.6 * cm, A4[0] - doc.rightMargin, A4[1] - 1.6 * cm)
    canvas.setFont("Helvetica", 9)
    canvas.setFillColor(colors.HexColor("#6d4c67"))
    canvas.drawString(doc.leftMargin, 1.2 * cm, "SkillBuddy Project Report")
    canvas.drawRightString(A4[0] - doc.rightMargin, 1.2 * cm, f"Page {doc.page}")
    canvas.restoreState()


def parse_markdown(text, styles):
    story = []
    bullet_buffer = []
    title_block = []
    first_heading_seen = False

    def flush_bullets():
        nonlocal bullet_buffer
        if not bullet_buffer:
            return
        items = [
            ListItem(Paragraph(item, styles["ReportBullet"]), leftIndent=12)
            for item in bullet_buffer
        ]
        story.append(
            ListFlowable(
                items,
                bulletType="bullet",
                start="circle",
                leftIndent=14,
                bulletFontName="Helvetica",
                bulletFontSize=8,
                bulletColor=colors.HexColor("#7b4d8e"),
            )
        )
        story.append(Spacer(1, 0.18 * cm))
        bullet_buffer = []

    for raw_line in text.splitlines():
        line = raw_line.strip()

        if not line:
            flush_bullets()
            continue

        if line.startswith("# "):
            if not first_heading_seen:
                first_heading_seen = True
                title_block.append(line[2:].strip())
                continue
            flush_bullets()
            story.append(PageBreak())
            story.append(Paragraph(line[2:].strip(), styles["ReportH1"]))
            continue

        if line.startswith("## "):
            flush_bullets()
            heading = line[3:].strip()
            if not first_heading_seen:
                first_heading_seen = True
            if story:
                story.append(Spacer(1, 0.1 * cm))
            story.append(Paragraph(heading, styles["ReportH1"]))
            continue

        if line.startswith("### "):
            flush_bullets()
            story.append(Paragraph(line[4:].strip(), styles["ReportH2"]))
            continue

        if line.startswith("- "):
            bullet_buffer.append(line[2:].strip())
            continue

        if not first_heading_seen or (title_block and len(story) == 0):
            title_block.append(line)
            continue

        flush_bullets()
        story.append(Paragraph(line, styles["ReportBody"]))

    flush_bullets()

    if title_block:
        title_story = [
            Spacer(1, 4.5 * cm),
            Paragraph(title_block[0], styles["ReportTitle"]),
            Spacer(1, 0.5 * cm),
        ]
        for meta_line in title_block[1:]:
            title_story.append(Paragraph(meta_line, styles["ReportMeta"]))
        title_story.append(Spacer(1, 1.2 * cm))
        title_story.append(
            Paragraph(
                "This document summarizes the current implementation status, available features, technical design, limitations, and future enhancement scope of the SkillBuddy project.",
                styles["ReportBody"],
            )
        )
        title_story.append(PageBreak())
        story = title_story + story

    return story


def main():
    styles = build_styles()
    text = SOURCE_PATH.read_text(encoding="utf-8")
    story = parse_markdown(text, styles)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(OUTPUT_PATH),
        pagesize=A4,
        leftMargin=2.1 * cm,
        rightMargin=2.1 * cm,
        topMargin=2.2 * cm,
        bottomMargin=2.0 * cm,
        title="SkillBuddy Project Report",
        author="OpenAI Codex",
    )
    doc.build(story, onFirstPage=page_canvas, onLaterPages=page_canvas)
    print(f"Generated: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
