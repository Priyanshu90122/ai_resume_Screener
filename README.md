# ai_resume_Screener
# Graph-Based LLM Resume Evaluation System (LangGraph-Inspired)

- An AI-powered resume screening system that evaluates resumes against internship/job descriptions using a graph-based LLM pipeline inspired by LangGraph.
-  The system performs skill extraction, skill-to-job comparison, ATS-style scoring, and delivers explainable AI hiring decisions using Google Gemini (LLM).

- This project demonstrates how LangGraph-style state-driven workflows can be applied to real-world AI hiring systems.

  # Key Features

- Resume upload support (PDF & DOCX)
  LLM-based skill extraction using Google Gemini
- LangGraph-inspired graph architecture (state → node → node → decision)
-  ATS-style resume scoring
-  Explainable AI with skill-wise reasoning
-  Skill gap analysis for candidates
-   Recruiter-style interactive UI
-    Cloud deployable (Render / Streamlit Cloud)

# Graph-Based Architecture (LangGraph Inspired)
The system is designed using LangGraph principles, where the AI workflow is modeled as a state-driven graph.
Initial State
(resume_text, job_description)
        ↓
Skill Extraction Node (LLM)
        ↓
Skill Comparison Node (LLM)
        ↓
Scoring & Decision Node
        ↓
Final Hiring Verdic
# LangGraph Concepts Used
State Object → shared data passed across nodes
Graph Nodes → independent AI tasks (extract, compare, score)
Deterministic Transitions → fixed execution order
Explainability → each node produces interpretable output
Although implemented manually for SDK stability, the architecture strictly follows LangGraph-style graph execution and reasoning principles.

# Technology used
• Python
• Google Gemini (LLM)
• Large Language Models (LLMs)
• LangGraph (Conceptual / Graph-based AI orchestration)
• Graph-based AI Pipelines
• Explainable AI
• Streamlit
• ATS-style Scoring
• PyPDF2
• python-docx

# Local Setup
- Clone repository
git clone https://github.com/your-username/ai-resume-screener.git
cd ai-resume-screener

- Install dependencies
pip install -r requirements.txt

- Set Gemini API Key
export GEMINI_API_KEY="your_api_key_here"

- Run Locally
python -m streamlit run frontend.py

#  Explainable AI
- Each decision includes:
- Skill match status
- AI-generated justification
- Transparent reasoning path across graph nodes
- This avoids black-box predictions and aligns with responsible AI principles.
