import streamlit as st
import google.generativeai as genai
import io, json
import PyPDF2
from docx import Document

# ==================================================
# 🔑 GEMINI API KEY
# ==================================================
# ⚠️ Demo ke baad API key regenerate kar lena
genai.configure(api_key="PASTE_YOUR_GEMINI_API_KEY_HERE")

# ✅ Stable model for google-generativeai SDK
model = genai.GenerativeModel("gemini-pro")

# ==================================================
# 📄 Resume text extraction
# ==================================================
def extract_text(file_bytes, filename):
    text = ""
    if filename.lower().endswith(".pdf"):
        reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
        for page in reader.pages:
            if page.extract_text():
                text += page.extract_text()
    elif filename.lower().endswith(".docx"):
        doc = Document(io.BytesIO(file_bytes))
        for p in doc.paragraphs:
            text += p.text + "\n"
    return text.strip()

# ==================================================
# 🤖 Gemini call helper
# ==================================================
def llm(prompt: str) -> str:
    response = model.generate_content(prompt)
    return response.text

# ==================================================
# 🔷 GRAPH NODES (Internship-oriented AI pipeline)
# ==================================================
def extract_skills_node(state):
    prompt = f"""
    Extract ONLY technical skills (languages, frameworks, tools).
    Return STRICT JSON list of strings only.

    Resume Text:
    {state['resume_text']}
    """
    try:
        state["skills"] = json.loads(llm(prompt))
    except:
        state["skills"] = []
    return state


def compare_skills_node(state):
    prompt = f"""
    Compare candidate skills with job requirements.

    Candidate Skills: {state['skills']}
    Job Description: {state['job_description']}

    Return STRICT JSON:
    [
      {{
        "skill": "Python",
        "status": true,
        "reason": "Mentioned clearly in resume"
      }}
    ]
    """
    try:
        state["trace"] = json.loads(llm(prompt))
    except:
        state["trace"] = []
    return state


def scoring_node(state):
    matched = sum(1 for t in state["trace"] if t.get("status"))
    total = len(state["trace"])
    state["score"] = int((matched / total) * 100) if total else 0

    if state["score"] >= 80:
        state["verdict"] = "Strong Internship Candidate"
    elif state["score"] >= 60:
        state["verdict"] = "Potential Candidate (Needs Improvement)"
    else:
        state["verdict"] = "Not Ready for Internship"

    state["decision"] = "SELECTED ✅" if state["score"] >= 70 else "REJECTED ❌"
    return state

# ==================================================
# 🔷 GRAPH EXECUTOR (Manual LangGraph-style)
# ==================================================
def run_graph(state):
    state = extract_skills_node(state)
    state = compare_skills_node(state)
    state = scoring_node(state)
    return state

# ==================================================
# 🖥️ STREAMLIT UI
# ==================================================
st.set_page_config(page_title="AI Resume Screener", layout="centered")
st.title("🤖 AI Internship Resume Screener")
st.caption("Graph-based AI • Explainable • ATS-style Evaluation")

resume = st.file_uploader("📄 Upload Resume (PDF / DOCX)", type=["pdf", "docx"])
job_desc = st.text_area("🧾 Internship Job Description", height=150)

if st.button("🚀 Analyze Resume"):
    if not resume or not job_desc:
        st.warning("Please upload resume and enter job description")
    else:
        with st.spinner("Running AI graph-based evaluation..."):
            resume_text = extract_text(resume.getvalue(), resume.name)

            # Initial STATE
            state = {
                "resume_text": resume_text,
                "job_description": job_desc,
                "skills": [],
                "trace": [],
                "score": 0,
                "decision": "",
                "verdict": ""
            }

            result = run_graph(state)

        # ==================================================
        # 🎯 OUTPUT (INTERNSHIP-ORIENTED)
        # ==================================================
        st.markdown("---")

        # AI Hiring Verdict
        if result["score"] >= 80:
            st.success(f"🎉 **AI Hiring Verdict: {result['verdict']}**")
        elif result["score"] >= 60:
            st.warning(f"⚠️ **AI Hiring Verdict: {result['verdict']}**")
        else:
            st.error(f"🚫 **AI Hiring Verdict: {result['verdict']}**")

        # ATS-Style Match Score
        st.subheader("📊 ATS Match Score")
        st.progress(result["score"] / 100)
        st.markdown(f"### **{result['score']}% Skill Match**")

        # AI Summary
        matched_skills = sum(1 for t in result["trace"] if t.get("status"))
        total_skills = len(result["trace"])

        st.info(
            f"🤖 **AI Summary:** Resume matched **{matched_skills} / {total_skills}** "
            f"key skills required for this internship role."
        )

        # Skill-wise Evaluation
        st.subheader("🧩 Skill-wise Evaluation (Explainable AI)")
        for t in result["trace"]:
            if t.get("status"):
                st.markdown(
                    f"""
                    <div style="padding:10px; border-radius:8px; background:#e8fff4; margin-bottom:8px;">
                    ✅ <b>{t['skill']}</b><br>
                    <small>{t['reason']}</small>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f"""
                    <div style="padding:10px; border-radius:8px; background:#ffecec; margin-bottom:8px;">
                    ❌ <b>{t['skill']}</b><br>
                    <small>{t['reason']}</small>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        # Skill Gap Analysis
        missing_skills = [t["skill"] for t in result["trace"] if not t.get("status")]
        st.subheader("🚧 Skill Gap Analysis")
        if missing_skills:
            st.warning("The following skills need improvement:")
            for s in missing_skills:
                st.write(f"• {s}")
        else:
            st.success("No major skill gaps detected.")

        # Resume Improvement Suggestions
        with st.expander("🧠 AI Resume Improvement Suggestions"):
            if missing_skills:
                st.write(
                    "To improve internship shortlisting chances:\n"
                    "- Add projects related to missing skills\n"
                    "- Mention tools/framework usage clearly\n"
                    "- Quantify results (accuracy, performance, impact)\n"
                    "- Include GitHub or project links"
                )
            else:
                st.write(
                    "Your resume is well-aligned for this internship role.\n"
                    "Focus on interview preparation and problem-solving skills."
                )

        # Explainable AI (Interview-friendly)
        with st.expander("🔍 How the AI made this decision"):
            st.write("""
            This system follows a **graph-based AI reasoning pipeline**:
            1. Resume text extraction (PDF/DOCX)
            2. Skill identification using Gemini (LLM)
            3. Skill-to-job requirement comparison
            4. ATS-style scoring and hiring verdict

            Each step is transparent and explainable, making the system
            suitable for real-world AI-assisted hiring.
            """)
