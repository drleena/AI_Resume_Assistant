# AI Resume Screening Assistant

An AI-powered resume screening application built using Python, LangChain, Google Gemini, FAISS, and Streamlit. The application helps users compare multiple PDF resumes against a job description and generates structured, evidence-based candidate assessments.

## Project Overview

Recruitment teams often need to review large numbers of resumes to identify candidates whose skills and experience align with a job description. Manual screening can be time-consuming and inconsistent.

The AI Resume Screening Assistant uses Large Language Models (LLMs) and Retrieval-Augmented Generation (RAG) to extract relevant information from resumes and evaluate it against job requirements.

Users can upload multiple PDF resumes, enter a job description, and review AI-generated assessments through an interactive web interface.

The application is intended to support human decision-making rather than automate hiring decisions.

## Key Features

- **Multiple Resume Uploads:** Upload multiple PDF resumes through the Streamlit interface.
- **PDF Text Extraction:** Extract text from resumes using PyPDF.
- **Text Chunking:** Split resume text into smaller chunks for efficient retrieval.
- **Text Embeddings:** Generate vector embeddings using Google's embedding model.
- **Semantic Search:** Retrieve relevant resume passages using FAISS vector search.
- **AI-Powered Evaluation:** Use Google Gemini to compare resume evidence with job requirements.
- **Indicative Match Score:** Generate a match score between 0 and 100.
- **Skill Identification:** Identify matching skills and missing or unverified skills.
- **Experience Assessment:** Summarize relevant professional experience.
- **Strengths and Gaps:** Present evidence-based observations about each resume.
- **Candidate Comparison:** Display assessment summaries in a comparison table.
- **Downloadable Results:** Export summary results as CSV and detailed evaluations as JSON.
- **Interactive Interface:** Access the application through a Streamlit web interface.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application development |
| Streamlit | Interactive web interface |
| LangChain | LLM integration and document processing |
| Google Gemini | Resume evaluation and natural language generation |
| Google Generative AI Embeddings | Text embedding generation |
| FAISS | Vector storage and similarity search |
| PyPDF | PDF text extraction |
| Pandas | Tabular results and CSV export |
| python-dotenv | Local environment variable management |
| Git and GitHub | Version control and source code hosting |
| Streamlit Community Cloud | Application deployment |

## Application Workflow

The application follows these steps:

1. **Upload Resumes:** Users upload one or more PDF resumes.
2. **Extract Text:** Resume text is extracted from the uploaded PDF files.
3. **Split Documents:** Extracted text is divided into smaller chunks.
4. **Generate Embeddings:** Text chunks are converted into vector embeddings.
5. **Build Vector Index:** FAISS creates a searchable vector index for the resume.
6. **Retrieve Relevant Evidence:** The application retrieves resume passages relevant to the job description.
7. **Evaluate the Resume:** Google Gemini assesses the retrieved evidence against the job requirements.
8. **Generate Results:** The application produces a match score, matching skills, missing or unverified skills, relevant experience, strengths, gaps, and a recommendation for human review.
9. **Compare Candidates:** Results are presented in a structured comparison table.
10. **Export Results:** Users can download summary results in CSV format and detailed assessments in JSON format.

## Project Structure

```text
AI_Resume_Assistant/
│
├── app.py
├── resume_rag.py
├── resume_evaluator.py
├── requirements.txt
├── README.md
├── .gitignore
└── .env

File Descriptions
File	Description
app.py	Streamlit application interface, resume uploads, evaluation workflow, results display, and downloads
resume_rag.py	PDF text extraction, document splitting, embedding generation, FAISS indexing, and evidence retrieval
resume_evaluator.py	Gemini integration and structured resume evaluation
requirements.txt	Python dependencies required to run the application
.gitignore	Excludes sensitive files, virtual environments, and local data from Git tracking
.env	Stores the local Gemini API key; must not be committed to GitHub
README.md	Project documentation and setup instructions


Installation and Setup
Prerequisites
- Python 3.11
- Git
- A Google Gemini API key
- A GitHub account for source code hosting
- A Streamlit Community Cloud account for deployment
Step 1: Clone the Repository
git clone https://github.com/YOUR_USERNAME/AI_Resume_Assistant.git
Replace YOUR_USERNAME with your GitHub username.
Navigate to the project directory:
cd AI_Resume_Assistant
Step 2: Create a Virtual Environment
python3.11 -m venv .venv
Activate the environment on macOS or Linux:
source .venv/bin/activate
Step 3: Install Dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt
Step 4: Configure the Gemini API Key
Create a .env file in the project root directory.
Add the following configuration:
GOOGLE_API_KEY=your_gemini_api_key
Replace your_gemini_api_key with your actual Google Gemini API key.
Security: Never commit .env to GitHub or expose your API key in application code.
Step 5: Run the Application
Start the Streamlit application:
python -m streamlit run app.py
Open the local URL displayed in the terminal, usually:
http://localhost:8501
How to Use the Application
1. Open the application in your browser.
2. Enter or paste the job description.
3. Upload one or more PDF resumes.
4. Click Evaluate Resumes.
5. Review the candidate comparison table.
6. Expand individual evaluations to inspect detailed assessments.
7. Download the summary as CSV or detailed results as JSON.
Evaluation Output
For each resume, the application generates the following information:
Output	Description
Match Score	An indicative score from 0 to 100 representing alignment with the job description
Matching Skills	Skills supported by the available resume evidence
Missing or Unverified Skills	Job requirements not sufficiently evidenced in the retrieved text
Relevant Experience	Professional experience relevant to the position
Strengths	Evidence-based observations about relevant qualifications
Gaps	Requirements for which the available evidence is limited or absent
Recommendation	Strong match, potential match, or limited match
Recommendation Reason	Explanation of the assessment
Human Review Required	Indicates that a person must review the assessment


The generated score is not a validated probability of job performance and should not be interpreted as an objective measure of candidate quality.
Deployment
The application can be deployed using Streamlit Community Cloud.
Deployment Steps
1. Push the application source code to GitHub.
2. Sign in to Streamlit Community Cloud.
3. Create a new application and select the GitHub repository.
4. Select the main branch.
5. Set the main file path to app.py.
6. Configure the Gemini API key in the application's Secrets settings.
7. Deploy the application.
Add the following to Streamlit Cloud Secrets:
GOOGLE_API_KEY = "your_gemini_api_key"
The API key should be stored only in the Secrets configuration, not in GitHub.
Limitations
- The application supports PDF resumes containing extractable text.
- Scanned PDFs may require OCR processing, which is not currently included.
- Evaluation quality depends on the completeness and clarity of the resume and job description.
- Retrieval may omit relevant information when it is not present in the selected passages.
- LLM-generated scores and recommendations can vary and may contain errors.
- The current scoring approach is not a validated recruitment assessment instrument.
- API availability, usage limits, and charges depend on the Google Gemini service and account configuration.
- The application requires human verification before any employment-related decision.
Responsible Use
This application is designed as a decision-support tool.
- Evaluate only job-related qualifications and evidence.
- Do not use protected characteristics or unrelated personal information in screening.
- Review the original resume before making employment decisions.
- Do not automatically reject or select candidates based solely on AI-generated scores.
- Verify important qualifications and claims independently.
- Handle candidate information confidentially and in accordance with applicable data protection requirements.
Future Enhancements
Potential improvements include:
- More structured, requirement-by-requirement scoring.
- Configurable job-related evaluation criteria.
- Evidence citations linked to resume pages and passages.
- OCR support for scanned resumes.
- Improved evaluation consistency and validation.
- Batch processing and improved error handling.
- Downloadable PDF evaluation reports.
- Candidate review history and evaluation tracking.
- User authentication and access controls.
- Testing across diverse resumes to identify and reduce potential bias.
Author
Leena Gaikwad
GitHub: https://github.com/YOUR_USERNAME
Disclaimer
This project demonstrates the application of Large Language Models, Retrieval-Augmented Generation, vector search, and interactive web development to resume screening.
It is intended for educational and decision-support purposes only. AI-generated assessments should not be used as the sole basis for employment decisions.
