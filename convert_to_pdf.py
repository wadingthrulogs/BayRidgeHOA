"""
Convert WEBSITE-SERVICES-AGREEMENT.md to a professional PDF.
Uses Georgia (serif) for body, DejaVu Sans for headings and UI elements.
"""
import re
from fpdf import FPDF

FONTS = "C:/Windows/Fonts/"
MD_FILE = "WEBSITE-SERVICES-AGREEMENT.md"
PDF_FILE = "WEBSITE-SERVICES-AGREEMENT.pdf"

NAVY   = (10, 40, 75)
BLUE   = (31, 124, 236)
GRAY   = (120, 120, 120)
BLACK  = (0, 0, 0)
WHITE  = (255, 255, 255)
LIGHT  = (240, 244, 250)


class ContractPDF(FPDF):
    def header(self):
        # Thin navy bar across the top of every page after page 1
        if self.page_no() > 1:
            self.set_fill_color(*NAVY)
            self.rect(0, 0, 210, 6, style="F")
            self.set_font("Sans", "B", 8)
            self.set_text_color(*WHITE)
            self.set_xy(0, 0)
            self.cell(0, 6, "  WEBSITE SERVICES AGREEMENT  |  Bay Ridge HOA  \u2014  WadingThruSecurity", align="L")
            self.set_text_color(*BLACK)
            self.set_y(12)

    def footer(self):
        self.set_y(-14)
        self.set_draw_color(200, 200, 200)
        self.set_line_width(0.2)
        self.line(self.l_margin, self.get_y(), self.l_margin + self.epw, self.get_y())
        self.ln(1)
        self.set_font("Sans", "", 8)
        self.set_text_color(*GRAY)
        self.cell(0, 6, f"Page {self.page_no()} of {{nb}}  \u2014  Confidential", align="C")
        self.set_text_color(*BLACK)


def build_pdf(lines):
    pdf = ContractPDF()
    pdf.alias_nb_pages()
    pdf.set_author("WadingThruSecurity")
    pdf.set_title("Website Services Agreement - Bay Ridge HOA")

    # Fonts
    pdf.add_font("Serif",     "",  FONTS + "georgia.ttf")
    pdf.add_font("Serif",     "B", FONTS + "georgiab.ttf")
    pdf.add_font("Serif",     "I", FONTS + "georgiai.ttf")
    pdf.add_font("SerifBI",   "",  FONTS + "georgiaz.ttf")
    pdf.add_font("Sans",      "",  FONTS + "DejaVuSans.ttf")
    pdf.add_font("Sans",      "B", FONTS + "DejaVuSans-Bold.ttf")
    pdf.add_font("Sans",      "I", FONTS + "DejaVuSans-Oblique.ttf")

    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=22)
    pdf.set_margins(25, 20, 25)

    # ── Title block ─────────────────────────────────────────────────────────
    # Navy banner
    pdf.set_fill_color(*NAVY)
    pdf.rect(0, 0, 210, 38, style="F")
    pdf.set_y(7)
    pdf.set_font("Sans", "B", 18)
    pdf.set_text_color(*WHITE)
    pdf.cell(0, 9, "WEBSITE SERVICES AGREEMENT", align="C")
    pdf.ln(9)
    pdf.set_font("Sans", "", 9)
    pdf.set_text_color(180, 210, 255)
    pdf.cell(0, 6, "Bay Ridge Homeowners Association, Inc.  \u2014  WadingThruSecurity", align="C")
    pdf.set_text_color(*BLACK)
    pdf.set_y(50)

    i = 0
    skip_h1 = False  # We handled the title in the banner

    while i < len(lines):
        raw  = lines[i].rstrip("\n")
        text = raw.strip()

        # ── Skip the H1 (already in banner) ─────────────────────────────────
        if re.match(r"^# [^#]", text):
            i += 1
            skip_h1 = True
            continue

        # ── Horizontal rule ──────────────────────────────────────────────────
        if re.match(r"^-{3,}$", text):
            pdf.ln(2)
            pdf.set_draw_color(200, 210, 225)
            pdf.set_line_width(0.25)
            pdf.line(pdf.l_margin, pdf.get_y(), pdf.l_margin + pdf.epw, pdf.get_y())
            pdf.ln(4)
            i += 1
            continue

        # ── H2 ───────────────────────────────────────────────────────────────
        if re.match(r"^## [^#]", text):
            heading = strip_md(text[3:]).upper()
            pdf.ln(5)
            # Filled label bar
            pdf.set_fill_color(*LIGHT)
            pdf.set_draw_color(*NAVY)
            pdf.set_line_width(0)
            bar_y = pdf.get_y()
            pdf.rect(pdf.l_margin - 2, bar_y, pdf.epw + 4, 8, style="F")
            # Left accent
            pdf.set_fill_color(*NAVY)
            pdf.rect(pdf.l_margin - 2, bar_y, 3, 8, style="F")
            pdf.set_xy(pdf.l_margin + 4, bar_y)
            pdf.set_font("Sans", "B", 9.5)
            pdf.set_text_color(*NAVY)
            pdf.cell(0, 8, heading)
            pdf.set_text_color(*BLACK)
            pdf.ln(3)
            i += 1
            continue

        # ── H3 ───────────────────────────────────────────────────────────────
        if re.match(r"^### ", text):
            heading = strip_md(text[4:])
            pdf.ln(3)
            pdf.set_font("Serif", "B", 10.5)
            pdf.set_text_color(*NAVY)
            pdf.multi_cell(0, 6, heading)
            pdf.set_text_color(*BLACK)
            pdf.ln(0.5)
            i += 1
            continue

        # ── Table ────────────────────────────────────────────────────────────
        if text.startswith("|"):
            rows = []
            rows.append([c.strip() for c in text.strip("|").split("|")])
            i += 1
            # skip separator
            if i < len(lines) and re.match(r"^[\|\s\-:]+$", lines[i].strip()):
                i += 1
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            render_table(pdf, rows)
            continue

        # ── Bullet list ──────────────────────────────────────────────────────
        if text.startswith("- "):
            body = strip_md(text[2:])
            pdf.set_font("Serif", "", 10)
            x0 = pdf.l_margin + 7
            pdf.set_x(x0 - 5)
            pdf.cell(5, 5.5, "\u2022")
            pdf.multi_cell(pdf.epw - 7, 5.5, body)
            i += 1
            continue

        # ── Numbered list ────────────────────────────────────────────────────
        m = re.match(r"^(\d+)\.\s+(.+)$", text)
        if m:
            num  = m.group(1)
            body = strip_md(m.group(2))
            pdf.set_font("Serif", "", 10)
            pdf.set_x(pdf.l_margin + 4)
            pdf.cell(8, 5.5, f"{num}.")
            pdf.multi_cell(pdf.epw - 8, 5.5, body)
            i += 1
            continue

        # ── Blank line ───────────────────────────────────────────────────────
        if text == "":
            pdf.ln(2.5)
            i += 1
            continue

        # ── Italic-only line ─────────────────────────────────────────────────
        if re.match(r"^\*[^*].+[^*]\*$", text):
            pdf.set_font("Serif", "I", 9)
            pdf.set_text_color(*GRAY)
            pdf.multi_cell(0, 5, text[1:-1])
            pdf.set_text_color(*BLACK)
            i += 1
            continue

        # ── Signature blank lines (\_\_\_\_) ─────────────────────────────────
        if re.match(r"^[_\\]+$", text):
            pdf.set_font("Serif", "", 10)
            clean = text.replace("\\", "").replace("_", "")
            # Draw an actual line instead
            y = pdf.get_y() + 4
            pdf.set_draw_color(80, 80, 80)
            pdf.set_line_width(0.3)
            pdf.line(pdf.l_margin, y, pdf.l_margin + 120, y)
            pdf.ln(6)
            i += 1
            continue

        # ── Regular paragraph (may have inline bold) ─────────────────────────
        pdf.set_font("Serif", "", 10)
        if "**" in text:
            render_inline(pdf, text, line_h=5.5)
            pdf.ln(5.5)
        else:
            pdf.multi_cell(0, 5.5, strip_md(text))
        pdf.ln(1)
        i += 1

    pdf.output(PDF_FILE)
    print(f"PDF created: {PDF_FILE}")


def strip_md(text):
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"\*(.+?)\*",     r"\1", text)
    text = re.sub(r"__(.+?)__",     r"\1", text)
    text = re.sub(r"_(.+?)_",       r"\1", text)
    text = text.replace("\\_", "_")
    return text


def render_inline(pdf, text, line_h=5.5):
    """Write a line that may contain **bold** segments."""
    parts = re.split(r"(\*\*.*?\*\*)", text)
    for part in parts:
        if part.startswith("**") and part.endswith("**"):
            pdf.set_font("Serif", "B", 10)
            pdf.write(line_h, part[2:-2])
        else:
            pdf.set_font("Serif", "", 10)
            pdf.write(line_h, strip_md(part))


def render_table(pdf, rows):
    if not rows:
        return
    pdf.ln(3)
    ncols  = len(rows[0])
    col_w  = pdf.epw / ncols

    # Header row
    pdf.set_fill_color(*NAVY)
    pdf.set_text_color(*WHITE)
    pdf.set_font("Sans", "B", 9)
    for cell in rows[0]:
        pdf.cell(col_w, 8, strip_md(cell), border=0, fill=True, align="L")
    pdf.ln()

    # Data rows — alternating shading
    pdf.set_text_color(*BLACK)
    pdf.set_font("Serif", "", 9.5)
    for idx, row in enumerate(rows[1:]):
        bg = (247, 250, 255) if idx % 2 == 0 else WHITE
        pdf.set_fill_color(*bg)
        for cell in row:
            pdf.cell(col_w, 7.5, strip_md(cell), border="B", fill=True)
        pdf.ln()

    # Bottom border
    pdf.set_draw_color(*NAVY)
    pdf.set_line_width(0.4)
    pdf.line(pdf.l_margin, pdf.get_y(), pdf.l_margin + pdf.epw, pdf.get_y())
    pdf.set_line_width(0.2)
    pdf.ln(3)


if __name__ == "__main__":
    with open(MD_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
    build_pdf(lines)
