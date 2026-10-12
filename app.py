import json
import pandas as pd
import streamlit as st

from resume_rag import (
    extract_resume_text,
    build_resume_vector_store,
    retrieve_relevant_resume_content,
)

from resume_evaluator import evaluate_resume


st.set_page_config(
    page_title="AI Resume Screening Assistant",
    page_icon="📄",
    layout="wide",
)


st.title("📄 AI Resume Screening Assistant")

st.write(
    "Compare resumes against a job description using "
    "AI-assisted evidence retrieval and evaluation."
)

st.info(
    "This tool provides indicative, job-related assessments "
    "for human review. It does not make hiring decisions."
)


# Sidebar
with st.sidebar:
    st.header("About the application")

    st.write(
        """
        **Technology stack**
        - Python
        - LangChain
        - Gemini
        - FAISS vector search
        - Streamlit

        **Supported input:** PDF resumes
        """
    )


# Job description
st.subheader("1. Enter the job description")

job_description = st.text_area(
    "Job Description",
    height=250,
    placeholder=(
        "Paste the complete job description here, "
        "including required skills and experience."
    ),
)


# Resume upload
st.subheader("2. Upload resumes")

uploaded_files = st.file_uploader(
    "Upload one or more PDF resumes",
    type=["pdf"],
    accept_multiple_files=True,
)


if uploaded_files:
    st.write(f"**Resumes uploaded:** {len(uploaded_files)}")

    for uploaded_file in uploaded_files:
        st.write(f"📄 {uploaded_file.name}")


# Evaluation
if st.button(
    "Evaluate Resumes",
    type="primary",
    use_container_width=True,
):

    if not job_description.strip():
        st.error("Please enter a job description.")

    elif not uploaded_files:
        st.error("Please upload at least one PDF resume.")

    else:

        results = []

        progress_bar = st.progress(0)
        status_text = st.empty()

        total_files = len(uploaded_files)

        for index, uploaded_file in enumerate(uploaded_files):

            status_text.write(
                f"Processing {uploaded_file.name}..."
            )

            try:
                # Step 1: Extract resume text
                resume_documents = extract_resume_text(
                    uploaded_file,
                    uploaded_file.name,
                )

                # Step 2: Create vector store for this resume
                vector_store = build_resume_vector_store(
                    resume_documents
                )

                # Step 3: Retrieve relevant resume evidence
                retrieved_documents = (
                    retrieve_relevant_resume_content(
                        vector_store,
                        job_description,
                        k=5,
                    )
                )

                resume_context = "\n\n".join(
                    [
                        (
                            f"Page {document.metadata.get('page')}:\n"
                            f"{document.page_content}"
                        )
                        for document in retrieved_documents
                    ]
                )

                # Step 4: Evaluate the resume
                evaluation = evaluate_resume(
                    resume_context=resume_context,
                    job_description=job_description,
                    resume_filename=uploaded_file.name,
                )

                results.append(evaluation)

            except Exception as error:
                st.error(
                    f"Could not evaluate {uploaded_file.name}: "
                    f"{error}"
                )

            progress_bar.progress(
                (index + 1) / total_files
            )

        status_text.empty()
        progress_bar.empty()

        if results:

            st.session_state["resume_results"] = results
            st.session_state["job_description"] = job_description

            st.success(
                f"Successfully evaluated {len(results)} resume(s)."
            )


# Display results
if "resume_results" in st.session_state:

    results = st.session_state["resume_results"]

    st.divider()
    st.header("3. Evaluation Results")

    # Summary table
    summary_rows = []

    for result in results:
        summary_rows.append(
            {
                "Resume": result.get("resume_filename", ""),
                "Match Score": result.get("match_score", 0),
                "Recommendation": result.get(
                    "recommendation", ""
                ),
                "Human Review Required": True,
            }
        )

    summary_df = pd.DataFrame(summary_rows)

    st.subheader("Candidate comparison")

    st.dataframe(
        summary_df,
        use_container_width=True,
        hide_index=True,
    )

    # Download CSV
    csv_data = summary_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download comparison as CSV",
        data=csv_data,
        file_name="resume_screening_results.csv",
        mime="text/csv",
    )

    # Detailed results
    st.subheader("Detailed evaluations")

    for result in results:

        filename = result.get(
            "resume_filename",
            "Resume",
        )

        score = result.get("match_score", 0)

        with st.expander(
            f"{filename} — {score}/100"
        ):

            st.metric(
                "Indicative match score",
                f"{score}/100",
            )

            st.caption(
                "This score is model-generated decision support, "
                "not a validated probability of job performance."
            )

            st.write("**Recommendation for human review**")
            st.write(result.get("recommendation", ""))

            st.write("**Reasoning**")
            st.write(result.get("recommendation_reason", ""))

            st.write("**Matching skills**")
            st.write(
                result.get("matching_skills", [])
            )

            st.write("**Missing or unverified skills**")
            st.write(
                result.get(
                    "missing_or_unverified_skills",
                    [],
                )
            )

            st.write("**Relevant experience**")
            st.write(
                result.get("relevant_experience", [])
            )

            st.write("**Strengths**")
            st.write(result.get("strengths", []))

            st.write("**Gaps**")
            st.write(result.get("gaps", []))

            st.write("**Evidence**")
            st.write(result.get("evidence", []))

            st.warning(
                "Review the original resume and verify all "
                "important qualifications before making "
                "any employment decision."
            )

    # Download complete evaluations
    detailed_json = json.dumps(
        results,
        indent=2,
        ensure_ascii=False,
    )

    st.download_button(
        label="Download detailed evaluations as JSON",
        data=detailed_json,
        file_name="resume_screening_details.json",
        mime="application/json",
    )