# import json
# import os
# import platform
# from docx import Document
# from docx.text.paragraph import Paragraph
# from docx.shared import Pt

# # PDF helpers
# from fpdf import FPDF  # fpdf2 (pure Python)

# # Optional: docx2pdf (Windows/Mac) — used if available
# try:
#     from docx2pdf import convert as docx2pdf_convert
#     _HAS_DOCX2PDF = True
# except Exception:
#     _HAS_DOCX2PDF = False


# def fill_template(template_path, output_docx_path, output_pdf_path, resume_json):
#     """
#     Fill the DOCX template (python-docx) and generate a readable PDF.

#     Strategy:
#     1. Save DOCX using python-docx (existing behavior).
#     2. Try docx2pdf.convert (best fidelity) if available and platform supports it.
#     3. Fallback to a plain-text rendering using fpdf with a registered Unicode TTF (DejaVuSans) if available.
#     """
#     print("▶ fill_template start")
#     if isinstance(resume_json, dict):
#         data = resume_json
#     else:
#         data = json.loads(resume_json or "{}")

#     doc = Document(template_path)

#     def join_list(values):
#         return " | ".join(values) if values else ""

#     def find_heading_idx(heading_text):
#         for idx, para in enumerate(doc.paragraphs):
#             if para.text.strip().lower() == heading_text.lower():
#                 return idx
#         return None

#     def clear_paragraph(para: Paragraph):
#         for run in para.runs:
#             run.text = ""
#         para.text = ""

#     def add_after_heading(heading, lines, bullet=False):
#         idx = find_heading_idx(heading)
#         if idx is not None:
#             # skip placeholder empty paragraphs
#             while idx + 1 < len(doc.paragraphs) and not doc.paragraphs[idx + 1].text.strip():
#                 idx += 1
#             for line in lines:
#                 new_para = doc.add_paragraph(line, style="List Bullet" if bullet else None)
#                 doc.paragraphs[idx]._element.addnext(new_para._element)
#                 idx += 1

#     # ==== Fill core fields (keeps your original behavior) ====
#     # Full name
#     for para in doc.paragraphs:
#         if "full name" in para.text.lower():
#             full_name = f"{data.get('first_name', '')} {data.get('last_name', '')}".strip()
#             clear_paragraph(para)
#             para.add_run(full_name)
#             break

#     # Career summary
#     summary_text = data.get("career_summary", "")
#     if summary_text:
#         summary_lines = [s.strip() for s in summary_text.replace("\n", " ").split(". ") if s.strip()]
#         idx = find_heading_idx("Career Summary")
#         if idx is not None:
#             if idx + 1 < len(doc.paragraphs):
#                 clear_paragraph(doc.paragraphs[idx + 1])
#             for line in summary_lines:
#                 if not line.endswith("."):
#                     line += "."
#                 new_para = doc.add_paragraph(line, style="List Bullet")
#                 doc.paragraphs[idx]._element.addnext(new_para._element)
#                 idx += 1

#     # Expertise
#     idx = find_heading_idx("Expertise")
#     if idx is not None and idx + 1 < len(doc.paragraphs):
#         clear_paragraph(doc.paragraphs[idx + 1])
#         doc.paragraphs[idx + 1].add_run(join_list(data.get("expertise", [])))

#     # Technical Skills
#     idx = find_heading_idx("Technical Skills")
#     if idx is not None and idx + 1 < len(doc.paragraphs):
#         clear_paragraph(doc.paragraphs[idx + 1])
#         doc.paragraphs[idx + 1].add_run(join_list(data.get("technical_skills", [])))

#     # Professional Experience (simple version)
#     idx = find_heading_idx("Professional Experience")
#     if idx is not None:
#         for exp in data.get("professional_experience", []):
#             header_parts = [exp.get("title", ""), exp.get("company", ""), exp.get("location", "")]
#             header_parts = [p for p in header_parts if p]
#             if header_parts:
#                 hp = doc.add_paragraph(" | ".join(header_parts))
#                 try:
#                     hp.runs[0].bold = True
#                 except Exception:
#                     pass
#                 doc.paragraphs[idx]._element.addnext(hp._element)
#                 idx += 1

#             date_parts = [exp.get("start_date", ""), exp.get("end_date", "")]
#             date_parts = [d for d in date_parts if d]
#             if date_parts:
#                 dp = doc.add_paragraph(" – ".join(date_parts))
#                 try:
#                     dp.runs[0].italic = True
#                 except Exception:
#                     pass
#                 doc.paragraphs[idx]._element.addnext(dp._element)
#                 idx += 1

#             if exp.get("description"):
#                 dp2 = doc.add_paragraph(exp["description"])
#                 doc.paragraphs[idx]._element.addnext(dp2._element)
#                 idx += 1

#             for ach in exp.get("achievements", []):
#                 if ach.strip():
#                     a = doc.add_paragraph(ach, style="List Bullet")
#                     doc.paragraphs[idx]._element.addnext(a._element)
#                     idx += 1
            
#             for _ in range(2):
#                 spacer = doc.add_paragraph("")
#                 doc.paragraphs[idx]._element.addnext(spacer._element)
#                 idx += 1

#     # Education
#     edu_lines = []
#     for edu in data.get("education", []):
#         parts = []
#         if edu.get("degree"):
#             parts.append(edu["degree"])
#         if edu.get("field"):
#             parts.append(edu["field"])
#         if edu.get("institution"):
#             parts.append(edu["institution"])
#         header = " | ".join([p for p in parts if p])
#         date_range = " – ".join([p for p in [edu.get("start_year", ""), edu.get("end_year", "")] if p])
#         if header and date_range:
#             edu_lines.append(f"{header}    {date_range}")
#         elif header:
#             edu_lines.append(header)
#         elif date_range:
#             edu_lines.append(date_range)
#     add_after_heading("Education", edu_lines)

#     # Certifications
#     # cert_lines = [c for c in data.get("certifications", []) if c.strip()]
#     # if cert_lines:
#     #     add_after_heading("Certifications", cert_lines, bullet=True)

#     def remove_certification_block(doc):
#         indices_to_remove = []
#         for i, p in enumerate(doc.paragraphs):
#             if p.text.strip().lower() == "certification":
#                 indices_to_remove.append(i)
#                 # also remove the next paragraph if empty placeholder
#                 if i + 1 < len(doc.paragraphs) and not doc.paragraphs[i+1].text.strip():
#                     indices_to_remove.append(i+1)
#                 break

#         # remove in reverse order to avoid index shift
#         for idx in sorted(indices_to_remove, reverse=True):
#             p = doc.paragraphs[idx]._element
#             p.getparent().remove(p)

#     remove_certification_block(doc)
#     certifications = data.get("certifications", [])

#     # Keep only non-empty, non-null names
#     cert_lines = [c.strip() for c in certifications if c and c.strip()]

#     # Add header + bullets ONLY if list is not empty
#     if cert_lines:
#         add_after_heading("CERTIFICATION", cert_lines, bullet=True)
    
#     # ==== Save DOCX ====
#     os.makedirs(os.path.dirname(output_docx_path), exist_ok=True)
#     doc.save(output_docx_path)
#     print(f"✅ DOCX saved: {output_docx_path}")

#     # ==== Create PDF (try docx2pdf first, fallback to fpdf Unicode rendering) ====
#     try:
#         create_pdf_from_docx(output_docx_path, output_pdf_path)
#         if os.path.exists(output_pdf_path) and os.path.getsize(output_pdf_path) > 0:
#             print(f"✅ PDF saved: {output_pdf_path} (size={os.path.getsize(output_pdf_path)} bytes)")
#         else:
#             print(f"❌ PDF not created or zero size: {output_pdf_path}")
#     except Exception as e:
#         print(f"❌ PDF generation failed: {e}")


# def find_dejavu_ttf():
#     """Return a path to a DejaVuSans.ttf if present on the system or None."""
#     candidates = [
#         # Linux common
#         "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
#         "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
#         # macOS common
#         "/Library/Fonts/DejaVuSans.ttf",
#         # Windows common locations (may vary)
#         "C:\\Windows\\Fonts\\DejaVuSans.ttf",
#         # Local project fallback
#         os.path.join(os.getcwd(), "DejaVuSans.ttf"),
#     ]
#     for p in candidates:
#         if p and os.path.exists(p):
#             return p
#     return None


# def create_pdf_from_docx(docx_path: str, output_pdf_path: str):
#     """
#     Create a PDF from a DOCX file.

#     1) If docx2pdf is available and platform is Windows/macOS, use that (best fidelity).
#     2) Otherwise, render paragraphs into a plain-text PDF using fpdf with a Unicode TTF if available.
#     """
#     # Try docx2pdf when available and supported
#     if _HAS_DOCX2PDF and platform.system() in ("Windows", "Darwin"):
#         try:
#             print("ℹ Using docx2pdf for conversion (best fidelity)")
#             # Ensure output directory exists
#             os.makedirs(os.path.dirname(output_pdf_path), exist_ok=True)
#             docx2pdf_convert(docx_path, output_pdf_path)
#             return
#         except Exception as e:
#             print(f"⚠ docx2pdf conversion failed: {e} — falling back to text-render PDF")

#     # Fallback: use fpdf to render text. This is plain-text and won't keep layout.
#     print("ℹ Falling back to fpdf text-render conversion")
#     doc = Document(docx_path)

#     pdf = FPDF(format='A4', unit='mm')
#     pdf.set_auto_page_break(auto=True, margin=15)
#     pdf.add_page()

#     # Try to register DejaVuSans (unicode-capable). If not found, use built-in Arial (may not render unicode).
#     dejavu = find_dejavu_ttf()
#     if dejavu:
#         try:
#             pdf.add_font("DejaVu", "", dejavu, uni=True)
#             pdf.set_font("DejaVu", size=11)
#             print(f"ℹ Registered DejaVu font at: {dejavu}")
#         except Exception as e:
#             print(f"⚠ Failed to register DejaVu font: {e} — using built-in font")
#             pdf.set_font("Arial", size=11)
#     else:
#         print("⚠ DejaVuSans.ttf not found on system — unicode characters may not render correctly in PDF")
#         pdf.set_font("Arial", size=11)

#     for para in doc.paragraphs:
#         text = para.text.strip()
#         if not text:
#             pdf.ln(4)
#             continue
#         pdf.multi_cell(0, 6, txt=text)
#         pdf.ln(1)

#     os.makedirs(os.path.dirname(output_pdf_path), exist_ok=True)
#     pdf.output(output_pdf_path)


# # If module is executed as script (for quick manual testing)
# if __name__ == '__main__':
#     # Example usage (adjust paths)
#     tpl = 'data/template/Resume_Template_PGI.docx'
#     out_docx = 'data/output/doc/test.docx'
#     out_pdf = 'data/output/pdf/test.pdf'
#     sample_json = {}
#     if os.path.exists(tpl):
#         fill_template(tpl, out_docx, out_pdf, sample_json)
#     else:
#         print('Template not found — update the path for manual testing')


import json
import os
from docx import Document
from docx.text.paragraph import Paragraph
from fpdf import FPDF


# ======================================================
# Utility: Find embedded Unicode font
# ======================================================
def get_font_path():
    local_font = os.path.join(os.path.dirname(__file__), "fonts", "DejaVuSans.ttf")
    if os.path.exists(local_font):
        return local_font

    # Fallback system paths (rarely needed on Streamlit Cloud)
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/Library/Fonts/DejaVuSans.ttf",
    ]
    for p in candidates:
        if os.path.exists(p):
            return p

    return None


# ======================================================
# Main Template Fill Function
# ======================================================
def fill_template(template_path, output_docx_path, output_pdf_path, resume_json):
    print("▶ fill_template start")

    if not isinstance(resume_json, dict):
        data = json.loads(resume_json or "{}")
    else:
        data = resume_json

    doc = Document(template_path)

    def join_list(values):
        return " | ".join(values) if values else ""

    def clear_paragraph(para: Paragraph):
        for run in para.runs:
            run.text = ""
        para.text = ""

    def find_heading_idx(text):
        for i, p in enumerate(doc.paragraphs):
            if p.text.strip().lower() == text.lower():
                return i
        return None

    def add_after_heading(heading, lines, bullet=False):
        idx = find_heading_idx(heading)
        if idx is not None:
            for line in lines:
                new_p = doc.add_paragraph(
                    line,
                    style="List Bullet" if bullet else None
                )
                doc.paragraphs[idx]._element.addnext(new_p._element)
                idx += 1

    # ======================================================
    # Fill template content
    # ======================================================

    # Full Name
    for para in doc.paragraphs:
        if "full name" in para.text.lower():
            full_name = f"{data.get('first_name', '')} {data.get('last_name', '')}".strip()
            clear_paragraph(para)
            para.add_run(full_name)
            break

    # Career Summary
    summary = data.get("career_summary", "")
    if summary:
        lines = [s.strip() + "." for s in summary.replace("\n", " ").split(". ") if s.strip()]
        idx = find_heading_idx("Career Summary")
        if idx is not None and idx + 1 < len(doc.paragraphs):
            clear_paragraph(doc.paragraphs[idx + 1])
        for line in lines:
            p = doc.add_paragraph(line, style="List Bullet")
            doc.paragraphs[idx]._element.addnext(p._element)
            idx += 1

    # Expertise
    idx = find_heading_idx("Expertise")
    if idx is not None:
        clear_paragraph(doc.paragraphs[idx + 1])
        doc.paragraphs[idx + 1].add_run(join_list(data.get("expertise", [])))

    # Technical Skills
    idx = find_heading_idx("Technical Skills")
    if idx is not None:
        clear_paragraph(doc.paragraphs[idx + 1])
        doc.paragraphs[idx + 1].add_run(join_list(data.get("technical_skills", [])))

    # Professional Experience
    idx = find_heading_idx("Professional Experience")
    if idx is not None:
        for exp in data.get("professional_experience", []):
            # Title | Company | Location
            header = " | ".join(filter(None, [
                exp.get("title", ""),
                exp.get("company", ""),
                exp.get("location", "")
            ]))
            if header:
                p = doc.add_paragraph(header)
                p.runs[0].bold = True
                doc.paragraphs[idx]._element.addnext(p._element)
                idx += 1

            # Dates
            date_text = " – ".join(filter(None, [exp.get("start_date", ""), exp.get("end_date", "")]))
            if date_text:
                p = doc.add_paragraph(date_text)
                p.runs[0].italic = True
                doc.paragraphs[idx]._element.addnext(p._element)
                idx += 1

            # Description
            if exp.get("description"):
                p = doc.add_paragraph(exp["description"])
                doc.paragraphs[idx]._element.addnext(p._element)
                idx += 1

            # Achievements
            for ach in exp.get("achievements", []):
                if ach.strip():
                    p = doc.add_paragraph(ach, style="List Bullet")
                    doc.paragraphs[idx]._element.addnext(p._element)
                    idx += 1

            # Spacer
            spacer = doc.add_paragraph("")
            doc.paragraphs[idx]._element.addnext(spacer._element)
            idx += 1

    # Education
    edu_lines = []
    for edu in data.get("education", []):
        header = " | ".join(filter(None, [
            edu.get("degree", ""),
            edu.get("field", ""),
            edu.get("institution", "")
        ]))
        dates = " – ".join(filter(None, [
            edu.get("start_year", ""),
            edu.get("end_year", "")
        ]))
        edu_lines.append(f"{header}    {dates}")

    add_after_heading("Education", edu_lines)

    # Certifications
    certs = [c.strip() for c in data.get("certifications", []) if c and c.strip()]
    if certs:
        add_after_heading("CERTIFICATION", certs, bullet=True)

    # ======================================================
    # Save DOCX
    # ======================================================
    os.makedirs(os.path.dirname(output_docx_path), exist_ok=True)
    doc.save(output_docx_path)
    print("✅ DOCX saved")

    # ======================================================
    # Generate PDF (FPDF + Unicode)
    # ======================================================
    create_pdf(output_docx_path, output_pdf_path)


# ======================================================
# PDF Writing (FPDF Unicode)
# ======================================================
def create_pdf(docx_path, pdf_path):
    print("→ Creating PDF (Unicode safe)…")

    font_path = get_font_path()
    if not font_path:
        raise RuntimeError(
            "❌ Missing DejaVuSans.ttf. Add it under src/fonts/DejaVuSans.ttf"
        )

    doc = Document(docx_path)

    pdf = FPDF("P", "mm", "A4")
    pdf.add_page()
    pdf.add_font("DejaVu", "", font_path, uni=True)
    pdf.set_font("DejaVu", size=11)
    pdf.set_auto_page_break(auto=True, margin=12)

    for p in doc.paragraphs:
        text = p.text.strip()
        if not text:
            pdf.ln(4)
        else:
            pdf.multi_cell(0, 6, txt=text)
            pdf.ln(1)

    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
    pdf.output(pdf_path)

    print(f"✅ PDF saved: {pdf_path}")

