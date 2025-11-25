import streamlit as st
from src.new_main import run_main

st.set_page_config(page_title="AI Resume Builder", page_icon="📄", layout="centered")

st.title("📄 AI Resume Builder")
st.caption("Upload resume PDFs, generate professional templates for PGi or Mindmaps, and send them via email instantly.")

st.divider()

# --- Upload Section ---
st.subheader("📎 Upload one or more resume PDFs")
uploaded_files = st.file_uploader(
    "Upload Resumes",
    type=["pdf","docx"],
    accept_multiple_files=True,
    help="You can upload multiple PDF resumes at once."
)

# --- Template Selection ---
st.subheader("🏢 Select Organization")
company_choice = st.radio(
    "Choose company template:",
    ["PGi", "Mindmaps Technologies"],
    help="Select which company's resume format to use."
)

# --- Email Section ---
st.subheader("📬 Recipient Details")
recipient_emails = st.text_input(
    "Recipient Email(s)",
    placeholder="Enter comma-separated email addresses",
    help="Example: person1@gmail.com, person2@company.com"
)

st.divider()

# --- Button ---
process_button = st.button("🚀 Start Processing & Send Results")

# --- Status Container ---
status_box = st.container()

if process_button:
    if not uploaded_files:
        st.error("❌ Please upload at least one PDF file.")
    elif not recipient_emails.strip():
        st.error("❌ Please enter at least one recipient email address.")
    else:
        # Process emails and run the main function
        email_list = [email.strip() for email in recipient_emails.split(",") if email.strip()]

        st.info(f"📤 Sending results to: {', '.join(email_list)}")
        st.info(f"🏢 Using template: {company_choice}")

        with st.spinner("⏳ Processing resumes..."):
            run_main(uploaded_files, email_list, company_choice)

        st.success("✅ All resumes processed and sent successfully!")
