import streamlit as st
import PIL.Image

if not hasattr(PIL.Image, 'ANTIALIAS'):
    PIL.Image.ANTIALIAS = PIL.Image.LANCZOS

import os
import io
import json
from .extract_text import extract_text_from_pdf
from .llm_parser import extract_resume_info
from .create_docx1 import fill_template
from .send_email import send_mail_with_files
# from .create_docx_test import generate_resume_files


def run_main(files, email_list, company_choice):
    """
    Main entry: process uploaded resumes -> generate DOCX & PDF -> email both.
    """
    try:
        st.write(f"📦 Processing {len(files)} file(s) using **{company_choice}** template...")
        processed_files = []

        for f in files:
            filename = f.name
            st.info(f"📄 Extracting text from {filename}...")

            # Read file bytes
            file_stream = io.BytesIO(f.read())
            file_stream.seek(0)

            # Step 1: Extract text
            # resume_text = extract_text_from_pdf(file_stream)
            resume_text = extract_text_from_pdf(file_stream)
            # print(f"text {resume_text}")

            # Step 2: Parse resume using LLM
            st.info("🤖 Extracting structured data using LLM...")
            resume_json = extract_resume_info(resume_text)
            # print(resume_json)
            print('Calling the test function')
            # generate_resume_files(resume_json)

            # Step 3: Choose template
            base_dir = os.path.dirname(os.path.abspath(__file__))
            data_dir = os.path.join(base_dir, "..", "data")
            output_docx_dir = os.path.join(data_dir, "output", "doc")
            output_pdf_dir = os.path.join(data_dir, "output", "pdf")

            os.makedirs(output_docx_dir, exist_ok=True)
            os.makedirs(output_pdf_dir, exist_ok=True)

            if company_choice == "PGi":
                template_path = os.path.join(data_dir, "template", "Resume_Template_PGI.docx")
                output_docx_path = os.path.join(output_docx_dir, f"{filename}_PGI.docx")
                output_pdf_path = os.path.join(output_pdf_dir, f"{filename}_PGI.pdf")
            else:
                template_path = os.path.join(data_dir, "template", "MindMap.docx")
                output_docx_path = os.path.join(output_docx_dir, f"{filename}_Mindmap.docx")
                output_pdf_path = os.path.join(output_pdf_dir, f"{filename}_Mindmap.pdf")

            

            st.info(f"📝 Creating files using template: {os.path.basename(template_path)}")
            fill_template(template_path, output_docx_path, output_pdf_path, resume_json)
            # generate_resume_files(resume_json)

            processed_files.append((output_docx_path, output_pdf_path))
            st.success(f"✅ {filename} processed successfully!")

        # Step 4: Send both DOCX & PDF to recipient(s)
        st.info(f"📧 Sending results to {', '.join(email_list)}...")

        attachments = []
        for docx_path, pdf_path in processed_files:
            attachments.append(docx_path)
            attachments.append(pdf_path)

        send_mail_with_files(recipients=email_list, attachments=attachments)

        st.success("🎉 All files processed and sent successfully!")

    except Exception as e:
        st.error(f"❌ Unexpected error during processing: {e}")

