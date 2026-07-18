import streamlit as st
import time
import json
from datetime import datetime

# Import project modules
import database
import ai_analyzer
import utils
from models import SkillAssessment

# Set page config first
st.set_page_config(
    page_title="SkillProof — AI-Assessed Micro-Portfolio",
    page_icon="🏅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Database
database.init_db()

# Inject CSS styles
utils.inject_custom_css()

# Session State Initialization
if "wizard_step" not in st.session_state:
    st.session_state.wizard_step = "submit_work"

if "selected_category" not in st.session_state:
    st.session_state.selected_category = "Coding"

if "submitted_work" not in st.session_state:
    st.session_state.submitted_work = ""

if "explanation" not in st.session_state:
    st.session_state.explanation = ""

if "explanation_start_time" not in st.session_state:
    st.session_state.explanation_start_time = None

if "last_result" not in st.session_state:
    st.session_state.last_result = None

if "last_proof_id" not in st.session_state:
    st.session_state.last_proof_id = None

# Pre-packaged sample submissions for easy testing/demo
SAMPLES = {
    "Coding": {
        "title": "Quicksort Algorithm in Python",
        "content": """def quicksort(arr):
    # Standard quicksort implementation with pivot selection
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)

# Test cases
test_data = [3, 6, 8, 10, 1, 2, 1]
print("Sorted array:", quicksort(test_data))""",
        "explanation": "I implemented a recursive quicksort algorithm in Python. It picks the middle element as a pivot, then partitions the list into elements smaller than, equal to, and larger than the pivot, and recursively sorts the sub-arrays. I used list comprehensions for partition readability."
    },
    "Writing": {
        "title": "AI in Education Essay Snippet",
        "content": "Artificial intelligence is fundamentally reshaping the educational landscape, moving from a novel research topic to an active agent in classrooms worldwide. Personalized tutoring systems, adaptive assessments, and automated administrative tasks represent a major shift. However, this transformation raises critical questions regarding cognitive agency. If learners rely entirely on AI assistants to formulate arguments or solve complex equations, do they risk atrophy of baseline critical thinking skills? The goal must be integration that scaffolds, rather than replaces, human intellectual effort.",
        "explanation": "This is a short essay arguing that while AI in classrooms provides personalized scaffolding for students, over-reliance poses a risk to critical thinking skills. I wrote it to highlight the tension between automation and cognitive development in modern schools."
    },
    "Design": {
        "title": "UX Case Study: FinGuard Mobile Wallet",
        "content": "FinGuard is a mobile wallet targeted at elderly users to prevent financial scams. The design language prioritizes readability and cognitive ease. The layout uses high-contrast colors (Navy #0F172A and Orange #EA580C for primary alerts) and a typography scale starting at 18px to assist visibility. Interactive cards feature clear micro-copy indicating security state, and buttons are designed with large touch targets (minimum 48x48dp) to account for motor skill declines. Navigation is strictly linear to reduce memory load.",
        "explanation": "I designed FinGuard to solve financial security issues for elderly citizens. I focused on contrast levels, larger typography, and simple linear flows to keep accessibility high and cognitive load low. The visual choices reflect physical accessibility needs."
    }
}

# Sidebar Layout
with st.sidebar:
    st.markdown("""
        <div style='text-align: center; padding: 10px 0;'>
            <svg width="52" height="52" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
                <defs>
                    <linearGradient id="badgeGradSidebar" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stop-color="#B99CFF"/>
                        <stop offset="100%" stop-color="#FFA8C9"/>
                    </linearGradient>
                </defs>
                <circle cx="24" cy="24" r="21" fill="url(#badgeGradSidebar)"/>
                <path d="M24 12l3 6.6 7.2 1-5.2 5.1 1.2 7.2L24 28.4l-6.2 3.5 1.2-7.2-5.2-5.1 7.2-1z" fill="#1E1233"/>
            </svg>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; margin-top: 0; color: #F5EFFF;'>SkillProof</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #B8A8D9; font-size: 0.85rem; margin-top: -10px;'>AI-Assessed Micro-Portfolio</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Navigation Modes
    app_mode = st.radio("Navigation", ["Create Assessment", "History Dashboard"], label_visibility="collapsed")
    
    st.markdown("---")
    
    # API Key Management
    st.markdown("### Gemini API Setup")
    api_key_input = st.text_input(
        "API Key Override (Optional)",
        type="password",
        help="If not set in your environmental variables or .env file, paste your API key here.",
        value=""
    )
    
    if api_key_input:
        st.session_state.GEMINI_API_KEY_OVERRIDE = api_key_input
        # Inject into env for the current session
        import os
        os.environ["GEMINI_API_KEY"] = api_key_input
    
    # Simple check indicator
    configured_key = ai_analyzer.get_api_key()
    if configured_key:
        st.success("API Key Detected & Configured")
    else:
        st.warning("API Key Missing! Setup required.")

    st.markdown("---")
    st.markdown(
        """
        <div style='font-size: 0.75rem; color: #9A87C2; line-height: 1.4;'>
            <b>Disclaimer:</b> SkillProof assessments are evidence-based estimations generated using Gemini. 
            It is not an official academic certificate or a definitive test of human/AI authorship.
        </div>
        """,
        unsafe_allow_html=True
    )

# ----------------- MAIN APP CONTROLLER -----------------

if app_mode == "History Dashboard":
    st.markdown("<h1 class='glowing-title'>Assessment Archive</h1>", unsafe_allow_html=True)
    st.markdown("<p class='glowing-subtitle'>Review and verify your historical Proof Cards</p>", unsafe_allow_html=True)
    
    records = database.get_all_assessments()
    
    if not records:
        st.info("No assessments found. Create your first assessment to generate a Proof Card!")
    else:
        # Create grid layout
        for record in records:
            with st.container():
                st.markdown(f"""
                <div class='glass-card' style='padding: 20px;'>
                    <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;'>
                        <span style='font-family: Fredoka, sans-serif; font-weight: 700; font-size: 1.25rem; color: #F5EFFF;'>
                            {record['skill_tier']} - {record['category']} Assessment
                        </span>
                        <span class='proof-id-badge'>{record['proof_id']}</span>
                    </div>
                    <div style='display: flex; gap: 24px; margin-bottom: 12px; font-size: 0.9rem;'>
                        <div>Score: <strong style='color: #B99CFF;'>{record['score']}/5</strong></div>
                        <div>Confidence: <strong>{record['verification_confidence']}</strong></div>
                        <div>AI Likelihood: <strong>{record['ai_assistance_level']}</strong></div>
                        <div>Consistency: <strong>{record['explanation_consistency']}</strong></div>
                    </div>
                    <div style='color: #B8A8D9; font-size: 0.8rem; margin-bottom: 16px;'>
                        Assessed on: {datetime.fromisoformat(record['assessment_date']).strftime("%Y-%m-%d %H:%M:%S")}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Expandable details
                with st.expander("View Full Verification & Proof Card"):
                    try:
                        assessment_data = json.loads(record['assessment_json'])
                        # Render Proof Card HTML
                        html_code = utils.render_proof_card_html(
                            assessment_data,
                            record['proof_id'],
                            record['category'],
                            record['assessment_date']
                        )
                        st.components.v1.html(html_code, height=620, scrolling=True)
                        
                        # Download button — reliable printing happens from the standalone file
                        standalone_html = utils.render_standalone_proof_card_page(
                            assessment_data,
                            record['proof_id'],
                            record['category'],
                            record['assessment_date']
                        )
                        st.download_button(
                            label="⬇️ Download Proof Card",
                            data=standalone_html,
                            file_name=f"skillproof_{record['proof_id']}.html",
                            mime="text/html",
                            use_container_width=True,
                            key=f"download_{record['proof_id']}",
                        )
                        st.markdown(
                            """
                            > **Tip**: Open the downloaded file in your browser, then press **Ctrl+P** / **Cmd+P** and save as PDF (enable Background Graphics for full color).
                            """
                        )
                    except Exception as e:
                        st.error(f"Could not render archived card: {e}")
                st.markdown("<br>", unsafe_allow_html=True)

else:
    # assessment wizard flow
    
    # Step 1: Submit Work
    if st.session_state.wizard_step == "submit_work":
        st.markdown("<h1 class='glowing-title'>SkillProof Assessment</h1>", unsafe_allow_html=True)
        st.markdown("<p class='glowing-subtitle'>Upload your work for an objective, evidence-based evaluation</p>", unsafe_allow_html=True)
        
        st.markdown(
            """
            <div class='glass-card'>
                <h4>About SkillProof</h4>
                <p style='color: #B8A8D9; font-size: 0.9rem; line-height: 1.5;'>
                    Traditional resumes and certificates rely on self-claims or static institutional degrees. 
                    SkillProof evaluates your actual contribution using an <b>evidence-based framework</b>:
                </p>
                <ol style='color: #B8A8D9; font-size: 0.9rem; padding-left: 20px; line-height: 1.6;'>
                    <li><b>Work Quality:</b> Deep structural analysis of the content for domain-specific mastery.</li>
                    <li><b>AI Likelihood:</b> An analysis of formatting structures and patterns pointing to templates or generator assistance.</li>
                    <li><b>Explanation Consistency:</b> Evaluating how well you explain the technical choices and motivations behind your work.</li>
                </ol>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Form Container
        with st.container():
            st.markdown("### Step 1: Select Your Category")
            category = st.selectbox(
                "Category",
                ["Coding", "Writing", "Design"],
                label_visibility="collapsed"
            )
            st.session_state.selected_category = category
            
            st.markdown("### Step 2: Paste Your Work")
            
            # Helper buttons to inject demo samples
            st.markdown("<div style='font-size: 0.85rem; color: #B8A8D9;'>Load a Demo Sample to Test:</div>", unsafe_allow_html=True)
            col_s1, col_s2, col_s3 = st.columns(3)
            with col_s1:
                if st.button("💻 Python Quicksort (Coding)", use_container_width=True):
                    st.session_state.submitted_work = SAMPLES["Coding"]["content"]
                    st.rerun()
            with col_s2:
                if st.button("📝 AI in Education (Writing)", use_container_width=True):
                    st.session_state.submitted_work = SAMPLES["Writing"]["content"]
                    st.rerun()
            with col_s3:
                if st.button("🎨 Mobile Case Study (Design)", use_container_width=True):
                    st.session_state.submitted_work = SAMPLES["Design"]["content"]
                    st.rerun()

            # The text area
            placeholder_text = {
                "Coding": "Paste your code here...",
                "Writing": "Paste your article, essay, or blog post here...",
                "Design": "Paste your design spec, case study description, or text representation of your creative work..."
            }[category]
            
            work_text = st.text_area(
                "Submission Content",
                value=st.session_state.submitted_work,
                placeholder=placeholder_text,
                height=250,
                label_visibility="collapsed"
            )
            st.session_state.submitted_work = work_text
            
            # Next trigger button
            if st.button("Analyze My Skill"):
                if not work_text.strip():
                    st.error("Please enter or paste your work first before continuing!")
                elif not configured_key:
                    st.error("API Key is missing. Please add a GEMINI_API_KEY to continue.")
                else:
                    # Switch to explanation step and trigger timer
                    st.session_state.explanation_start_time = time.time()
                    st.session_state.wizard_step = "explanation"
                    st.rerun()

    # Step 2: Explanation & Controlled Timer
    elif st.session_state.wizard_step == "explanation":
        st.markdown("<h1 class='glowing-title'>Controlled Explanation</h1>", unsafe_allow_html=True)
        st.markdown("<p class='glowing-subtitle'>Explain the creation process and structure of your work</p>", unsafe_allow_html=True)
        
        # Display JavaScript timer (must use components.v1.html — st.markdown does not execute <script> tags)
        st.components.v1.html(
            """
            <div style="font-family: 'Fredoka', sans-serif; text-align: center; margin-bottom: 10px; padding: 16px; background: rgba(17, 24, 39, 0.7); border: 1px solid rgba(239, 68, 68, 0.2); border-radius: 16px;">
                <div id="timer-display" style="font-size: 2.5rem; font-weight: 800; color: #FFA8C9;">60s</div>
                <div style="font-size: 0.85rem; color: #B8A8D9; text-transform: uppercase; letter-spacing: 0.05em; font-family: sans-serif;">Controlled Window remaining</div>
            </div>
            <script>
                let timeLeft = 60;
                const display = document.getElementById("timer-display");
                const countdown = setInterval(() => {
                    timeLeft--;
                    if (timeLeft <= 0) {
                        clearInterval(countdown);
                        display.innerText = "TIME OUT";
                        display.style.color = "#FF6F91";
                    } else {
                        display.innerText = timeLeft + "s";
                        if (timeLeft <= 15) {
                            display.style.color = "#FF6F91";
                        }
                    }
                }, 1000);
            </script>
            """,
            height=130,
        )
        
        st.markdown(
            """
            <div class='glass-card'>
                <h4>Instructions</h4>
                <p style='color: #B8A8D9; font-size: 0.9rem;'>
                    You have <b>60 seconds</b> to write a brief explanation of your work. 
                    Detail your architectural decisions, technical approaches, challenges faced, or key thematic choices. 
                    This step acts as an authenticity signal matching your cognitive understanding with the work.
                </p>
                <p style='font-size: 0.8rem; color: #B99CFF;'>
                    Note: The timer serves as a controlled baseline. It is not an absolute human detector, but it helps calibrate the verification confidence.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Prepopulate demo helper
        st.markdown("<div style='font-size: 0.85rem; color: #B8A8D9;'>Load Demo Explanation (Optional):</div>", unsafe_allow_html=True)
        if st.button("Load Matching Demo Explanation"):
            cat = st.session_state.selected_category
            st.session_state.explanation = SAMPLES[cat]["explanation"]
            st.rerun()

        explanation_input = st.text_area(
            "Write your explanation here...",
            value=st.session_state.explanation,
            placeholder="E.g., I built this sorting logic to handle small datasets efficiently. The pivot strategy was chosen because...",
            height=150
        )
        st.session_state.explanation = explanation_input
        
        # Buttons
        col_b1, col_b2 = st.columns(2)
        with col_b1:
            if st.button("Cancel / Go Back"):
                st.session_state.wizard_step = "submit_work"
                st.rerun()
        with col_b2:
            if st.button("Submit Explanation"):
                if not explanation_input.strip():
                    st.error("Please provide a short explanation first!")
                else:
                    # Switch to loading state
                    st.session_state.wizard_step = "loading"
                    st.rerun()

    # Step 3: Analysis Loading Screen
    elif st.session_state.wizard_step == "loading":
        st.markdown("<h1 class='glowing-title'>Analyzing Submission...</h1>", unsafe_allow_html=True)
        st.markdown("<p class='glowing-subtitle'>Extracting contribution signals and validating metrics</p>", unsafe_allow_html=True)
        
        # Nice loading graphic container
        with st.container():
            st.markdown(
                """
                <div class='glass-card' style='text-align: center; padding: 40px;'>
                    <div style='display: inline-block; margin-bottom: 20px; animation: pulse 2s infinite;'>
                        <svg width="56" height="56" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
                            <defs>
                                <linearGradient id="badgeGradLoading" x1="0%" y1="0%" x2="100%" y2="100%">
                                    <stop offset="0%" stop-color="#B99CFF"/>
                                    <stop offset="100%" stop-color="#FFA8C9"/>
                                </linearGradient>
                            </defs>
                            <circle cx="24" cy="24" r="21" fill="url(#badgeGradLoading)"/>
                            <path d="M24 12l3 6.6 7.2 1-5.2 5.1 1.2 7.2L24 28.4l-6.2 3.5 1.2-7.2-5.2-5.1 7.2-1z" fill="#1E1233"/>
                        </svg>
                    </div>
                    <h3>Conducting AI & Human Contribution Analysis</h3>
                    <p style='color: #B8A8D9;'>Contacting Gemini API and validating the response schema...</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # API analysis call
            try:
                with st.spinner("Parsing structure and comparing explanation patterns..."):
                    # Call analyzer
                    assessment: SkillAssessment = ai_analyzer.analyze_submission(
                        category=st.session_state.selected_category,
                        work_content=st.session_state.submitted_work,
                        explanation_content=st.session_state.explanation
                    )
                    
                    # Store model result in session
                    st.session_state.last_result = assessment.model_dump()
                    
                    # Generate ID and save to DB
                    proof_id = utils.generate_proof_id()
                    st.session_state.last_proof_id = proof_id
                    
                    database.save_assessment(
                        proof_id=proof_id,
                        category=st.session_state.selected_category,
                        submitted_work=st.session_state.submitted_work,
                        explanation=st.session_state.explanation,
                        score=assessment.score,
                        skill_tier=assessment.skill_tier,
                        verification_confidence=assessment.verification_confidence,
                        ai_assistance_level=assessment.ai_assistance_level,
                        explanation_consistency=assessment.explanation_consistency,
                        assessment_json=json.dumps(assessment.model_dump())
                    )
                    
                    # Advance to results
                    st.session_state.wizard_step = "results"
                    st.rerun()
                    
            except Exception as e:
                st.error(f"Analysis failed: {e}")
                if st.button("Back to Work Submission"):
                    st.session_state.wizard_step = "submit_work"
                    st.rerun()

    # Step 4: Results Presentation
    elif st.session_state.wizard_step == "results":
        st.markdown("<h1 class='glowing-title'>Assessment Results</h1>", unsafe_allow_html=True)
        st.markdown("<p class='glowing-subtitle'>Evidence-based signals extracted from your micro-portfolio</p>", unsafe_allow_html=True)
        
        res = st.session_state.last_result
        if not res:
            st.error("No results stored. Please restart the assessment.")
            if st.button("Restart"):
                st.session_state.wizard_step = "submit_work"
                st.rerun()
        else:
            # Score and status grids
            col_r1, col_r2 = st.columns([1, 2])
            
            with col_r1:
                # Score box
                score = res["score"]
                st.markdown(f"""
                <div class='glass-card' style='text-align: center;'>
                    <h5 style='margin: 0; color: #B8A8D9;'>Skill Score</h5>
                    <div style='font-size: 4rem; font-weight: 800; color: #B99CFF; line-height: 1.2;'>{score}</div>
                    <div style='font-size: 1rem; color: #B8A8D9; margin-bottom: 12px;'>Out of 5</div>
                    <div style='display: flex; justify-content: center; gap: 6px; margin-bottom: 16px;'>
                        {''.join(['<div class="score-dot active"></div>' if i <= score else '<div class="score-dot"></div>' for i in range(1, 6)])}
                    </div>
                    <span style='font-weight: 700; color: #D9A6FF; background: rgba(192, 132, 252, 0.12); padding: 4px 12px; border-radius: 6px;'>
                        {res['skill_tier']}
                    </span>
                </div>
                """, unsafe_allow_html=True)
                
                # Signal details
                st.markdown(f"""
                <div class='glass-card'>
                    <h4>Assessed Signals</h4>
                    <div style='margin-bottom: 12px;'>
                        <div style='font-size: 0.75rem; color: #B8A8D9; text-transform: uppercase;'>Verification Confidence</div>
                        <span class='badge badge-{"strong" if res["verification_confidence"] == "Strong" else ("moderate" if res["verification_confidence"] == "Moderate" else "limited")}'>
                            {res["verification_confidence"]}
                        </span>
                    </div>
                    <div style='margin-bottom: 12px;'>
                        <div style='font-size: 0.75rem; color: #B8A8D9; text-transform: uppercase;'>AI Assistance Level</div>
                        <span class='badge badge-{"low" if res["ai_assistance_level"] == "Low" else ("moderate" if res["ai_assistance_level"] == "Moderate" else "high")}'>
                            {res["ai_assistance_level"]}
                        </span>
                    </div>
                    <div>
                        <div style='font-size: 0.75rem; color: #B8A8D9; text-transform: uppercase;'>Explanation Consistency</div>
                        <span class='badge badge-{"strong" if res["explanation_consistency"] == "Strong" else ("moderate" if res["explanation_consistency"] == "Moderate" else "limited")}'>
                            {res["explanation_consistency"]}
                        </span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
            with col_r2:
                # Skill Tags and details
                st.markdown(f"""
                <div class='glass-card'>
                    <h4>Detected Skills</h4>
                    <div class='pill-container'>
                        {''.join([f'<span class="pill">{tag}</span>' for tag in res["skill_tags"]])}
                    </div>
                    
                    <h4>Technical & Conceptual Quality</h4>
                    <p style='color: #D9CCF0; font-size: 0.95rem; line-height: 1.5; margin-bottom: 16px;'>{res['technical_quality']}</p>
                    
                    <h4>Work Evidence</h4>
                    <p style='color: #B8A8D9; font-size: 0.85rem; line-height: 1.5; border-left: 3px solid #B99CFF; padding-left: 12px; font-style: italic;'>
                        "{res['work_evidence']}"
                    </p>
                </div>
                """, unsafe_allow_html=True)

            # Details
            col_d1, col_d2 = st.columns(2)
            with col_d1:
                st.markdown(f"""
                <div class='glass-card'>
                    <h4 style='color: #7EEBB8;'>Key Strengths</h4>
                    <ul style='color: #D9CCF0; padding-left: 20px; font-size: 0.9rem;'>
                        {"".join([f"<li style='margin-bottom: 6px;'>{s}</li>" for s in res["strengths"]])}
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            with col_d2:
                st.markdown(f"""
                <div class='glass-card'>
                    <h4 style='color: #FFA8C9;'>Growth Directions</h4>
                    <ul style='color: #D9CCF0; padding-left: 20px; font-size: 0.9rem;'>
                        {"".join([f"<li style='margin-bottom: 6px;'>{g}</li>" for g in res["growth_areas"]])}
                    </ul>
                </div>
                """, unsafe_allow_html=True)

            # AI & Consistency Explanations
            st.markdown(f"""
            <div class='glass-card'>
                <h4>AI Assistance Likelihood Rationale</h4>
                <p style='color: #B8A8D9; font-size: 0.9rem; line-height: 1.5; margin-bottom: 14px;'>{res['ai_assistance_explanation']}</p>
                <div style='font-size: 0.8rem; color: #B8A8D9;'><b>Signals Detected:</b></div>
                <ul style='color: #B8A8D9; font-size: 0.85rem; padding-left: 20px; margin-top: 4px;'>
                    {"".join([f"<li>{sig}</li>" for sig in res.get("ai_assistance_signals", [])])}
                </ul>
                
                <h4 style='margin-top: 20px;'>Explanation Matching Analysis</h4>
                <p style='color: #B8A8D9; font-size: 0.9rem; line-height: 1.5;'>{res['explanation_consistency_explanation']}</p>
            </div>
            """, unsafe_allow_html=True)

            # Action buttons
            col_a1, col_a2 = st.columns(2)
            with col_a1:
                if st.button("Generate Proof Card"):
                    st.session_state.wizard_step = "proof_card"
                    st.rerun()
            with col_a2:
                if st.button("New Assessment"):
                    st.session_state.wizard_step = "submit_work"
                    st.session_state.submitted_work = ""
                    st.session_state.explanation = ""
                    st.session_state.last_result = None
                    st.session_state.last_proof_id = None
                    st.rerun()

    # Step 5: Proof Card View
    elif st.session_state.wizard_step == "proof_card":
        st.markdown("<h1 class='glowing-title'>Verification Card</h1>", unsafe_allow_html=True)
        st.markdown("<p class='glowing-subtitle'>Share this credential to prove your practical contribution signals</p>", unsafe_allow_html=True)
        
        res = st.session_state.last_result
        proof_id = st.session_state.last_proof_id
        category = st.session_state.selected_category
        date_str = datetime.now().isoformat()
        
        if not res:
            st.error("No results stored. Please restart.")
            if st.button("Restart"):
                st.session_state.wizard_step = "submit_work"
                st.rerun()
        else:
            # Render HTML Card
            html_code = utils.render_proof_card_html(res, proof_id, category, date_str)
            st.components.v1.html(html_code, height=620, scrolling=True)
            
            # Download button for standalone, print-reliable version
            standalone_html = utils.render_standalone_proof_card_page(res, proof_id, category, date_str)
            st.download_button(
                label="⬇️ Download Proof Card",
                data=standalone_html,
                file_name=f"skillproof_{proof_id}.html",
                mime="text/html",
                use_container_width=True,
            )
            
            # Guidelines & Export Tips
            st.markdown(
                """
                <div class='glass-card'>
                    <h4>Exporting & Sharing</h4>
                    <p style='color: #B8A8D9; font-size: 0.9rem; line-height: 1.5;'>
                    </p>
                    <ol style='color: #B8A8D9; font-size: 0.9rem; padding-left: 20px; line-height: 1.6;'>
                        <li>Click <b>Download Proof Card</b> above, then open the downloaded file in your browser.</li>
                        <li>Make sure <b>Background Graphics</b> is enabled in your browser's print options, so the dark card styling and colors are captured correctly.</li>
                    </ol>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Navigation back/reset
            col_p1, col_p2 = st.columns(2)
            with col_p1:
                if st.button("Back to Results"):
                    st.session_state.wizard_step = "results"
                    st.rerun()
            with col_p2:
                if st.button("New Assessment"):
                    st.session_state.wizard_step = "submit_work"
                    st.session_state.submitted_work = ""
                    st.session_state.explanation = ""
                    st.session_state.last_result = None
                    st.session_state.last_proof_id = None
                    st.rerun()
