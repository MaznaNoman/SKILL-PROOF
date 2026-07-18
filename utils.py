import random
import string
from datetime import datetime
import streamlit as st

def generate_proof_id() -> str:
    """Generates a random unique ID for the proof card (e.g., SP-7D3E-9A2C)."""
    chars = string.ascii_uppercase + string.digits
    part1 = "".join(random.choices(chars, k=4))
    part2 = "".join(random.choices(chars, k=4))
    return f"SP-{part1}-{part2}"

def inject_custom_css():
    """Injects high-fidelity glassmorphism CSS and custom modern font families into Streamlit."""
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Fredoka:wght@500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

        /* Animations */
        @keyframes pulse {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.6; transform: scale(1.08); }
        }
        @keyframes dotPop {
            0% { transform: scale(0.4); opacity: 0; }
            60% { transform: scale(1.25); }
            100% { transform: scale(1); opacity: 1; }
        }
        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(8px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        /* Apply fonts globally */
        html, body, [class*="css"], .stMarkdown {
            font-family: 'Inter', sans-serif;
        }
        
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Fredoka', sans-serif !important;
            font-weight: 700;
        }

        /* Customize main streamlit background */
        .stApp {
            background: radial-gradient(circle at 50% 50%, #2F1D4D 0%, #150a26 100%);
            color: #F5EFFF;
        }

        /* Force sidebar dark regardless of system/browser light-mode preference */
        [data-testid="stSidebar"], [data-testid="stSidebarContent"] {
            background: #1E1233 !important;
            color: #F5EFFF !important;
        }
        [data-testid="stSidebar"] * {
            color: #F5EFFF !important;
        }

        /* Force base html/body dark as a fallback so no light flash occurs anywhere */
        html, body {
            background-color: #150a26 !important;
            color: #F5EFFF !important;
        }

        /* Title styling with glowing text gradient */
        .glowing-title {
            font-family: 'Fredoka', sans-serif;
            background: linear-gradient(135deg, #B99CFF 0%, #D9A6FF 50%, #FFA8C9 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
            font-size: 2.8rem;
            text-align: center;
            margin-bottom: 0.2rem;
            letter-spacing: -0.03em;
            text-shadow: 0 0 40px rgba(129, 140, 248, 0.15);
        }

        .glowing-subtitle {
            font-family: 'Inter', sans-serif;
            font-size: 1.1rem;
            color: #B8A8D9;
            text-align: center;
            margin-bottom: 2rem;
            font-weight: 300;
        }

        /* Glassmorphic Container */
        .glass-card {
            background: rgba(17, 24, 39, 0.7);
            backdrop-filter: blur(16px) saturate(180%);
            -webkit-backdrop-filter: blur(16px) saturate(180%);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            padding: 28px;
            margin-bottom: 24px;
            box-shadow: 0 10px 40px 0 rgba(0, 0, 0, 0.5);
            transition: transform 0.3s ease, border-color 0.3s ease;
            animation: fadeInUp 0.4s ease-out;
        }
        
        .glass-card:hover {
            border-color: rgba(129, 140, 248, 0.3);
            transform: translateY(-2px);
        }

        /* Category Cards Selector */
        .category-container {
            display: flex;
            gap: 16px;
            margin-bottom: 24px;
        }

        /* Custom Status Badges */
        .badge {
            display: inline-block;
            padding: 6px 12px;
            border-radius: 9999px;
            font-size: 0.85rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        .badge-strong {
            background: rgba(16, 185, 129, 0.15);
            color: #7EEBB8;
            border: 1px solid rgba(16, 185, 129, 0.3);
        }
        .badge-moderate {
            background: rgba(245, 158, 11, 0.15);
            color: #FFD98A;
            border: 1px solid rgba(245, 158, 11, 0.3);
        }
        .badge-limited {
            background: rgba(239, 68, 68, 0.15);
            color: #FF6F91;
            border: 1px solid rgba(239, 68, 68, 0.3);
        }

        .badge-high {
            background: rgba(239, 68, 68, 0.15);
            color: #FF6F91;
            border: 1px solid rgba(239, 68, 68, 0.3);
        }
        .badge-low {
            background: rgba(16, 185, 129, 0.15);
            color: #7EEBB8;
            border: 1px solid rgba(16, 185, 129, 0.3);
        }

        /* Custom Pill List */
        .pill-container {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 8px;
            margin-bottom: 16px;
        }
        .pill {
            background: rgba(99, 102, 241, 0.15);
            color: #D8C7FF;
            border: 1px solid rgba(99, 102, 241, 0.3);
            padding: 4px 10px;
            border-radius: 8px;
            font-size: 0.8rem;
            font-weight: 500;
        }

        /* Elegant metrics grid */
        .metric-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
            gap: 16px;
            margin-bottom: 24px;
        }

        .metric-box {
            background: rgba(31, 41, 55, 0.5);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            padding: 16px;
            text-align: center;
        }

        .metric-label {
            font-size: 0.75rem;
            color: #B8A8D9;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 4px;
        }

        .metric-value {
            font-size: 1.25rem;
            font-weight: 700;
            color: #F5EFFF;
        }

        /* Score rating circles */
        .score-indicator {
            display: flex;
            justify-content: center;
            gap: 8px;
            margin: 12px 0;
        }
        .score-dot {
            width: 14px;
            height: 14px;
            border-radius: 50%;
            background-color: #3D2A5C;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        .score-dot.active {
            background-color: #B99CFF;
            box-shadow: 0 0 10px rgba(129, 140, 248, 0.6);
            animation: dotPop 0.4s ease-out;
        }

        /* Interactive buttons animation */
        div.stButton > button {
            background: linear-gradient(135deg, #A87FFF 0%, #FF8FD1 100%) !important;
            color: #F5EFFF !important;
            font-weight: 600 !important;
            border: none !important;
            padding: 10px 24px !important;
            border-radius: 8px !important;
            box-shadow: 0 4px 15px rgba(99, 102, 241, 0.2) !important;
            transition: all 0.25s ease-in-out !important;
            width: 100%;
        }

        div.stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 25px rgba(99, 102, 241, 0.4) !important;
            border: none !important;
        }

        /* Secondary actions link style */
        .secondary-btn {
            background: rgba(31, 41, 55, 0.6);
            border: 1px solid rgba(255, 255, 255, 0.1);
            color: #F5EFFF;
            padding: 8px 16px;
            border-radius: 8px;
            text-align: center;
            font-weight: 500;
            display: block;
            text-decoration: none;
            margin-top: 10px;
            transition: background 0.2s;
        }
        .secondary-btn:hover {
            background: rgba(55, 65, 81, 0.8);
            color: #F5EFFF;
        }

        /* Custom Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        ::-webkit-scrollbar-track {
            background: #1E1233;
        }
        ::-webkit-scrollbar-thumb {
            background: #2F1D4D;
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #3D2A5C;
        }
        </style>
    """, unsafe_allow_html=True)

def render_proof_card_html(assessment_data: dict, proof_id: str, category: str, date_str: str) -> str:
    """
    Renders the custom SkillProof Proof Card in beautiful HTML with glassmorphic styles,
    neon accents, credential details, holographic watermarks, and verification signatures.
    """
    # Parse date to prettier format
    try:
        dt = datetime.fromisoformat(date_str)
        formatted_date = dt.strftime("%B %d, %Y")
    except Exception:
        formatted_date = date_str

    score = assessment_data.get("score", 3)
    tier = assessment_data.get("skill_tier", "Intermediate")
    confidence = assessment_data.get("verification_confidence", "Moderate")
    ai_level = assessment_data.get("ai_assistance_level", "Moderate")
    consistency = assessment_data.get("explanation_consistency", "Moderate")
    tags = assessment_data.get("skill_tags", [])
    strengths = assessment_data.get("strengths", [])
    growth_areas = assessment_data.get("growth_areas", [])
    technical_quality = assessment_data.get("technical_quality", "")

    # Generate stars / dots HTML for score
    dots_html = ""
    for i in range(1, 6):
        active_class = "active" if i <= score else ""
        dots_html += f'<div class="score-dot {active_class}"></div>'

    # Pill tags HTML
    pills_html = ""
    for tag in tags[:5]: # Cap at 5 tags for layout space
        pills_html += f'<span class="proof-tag">{tag}</span>'

    # Highlights HTML
    strengths_html = ""
    for strength in strengths[:2]:
        strengths_html += f'<li>{strength}</li>'

    growth_html = ""
    for growth in growth_areas[:2]:
        growth_html += f'<li>{growth}</li>'

    # Color class for tier / confidence
    confidence_color = "#7EEBB8" if confidence == "Strong" else ("#FFD98A" if confidence == "Moderate" else "#FF6F91")
    ai_color = "#7EEBB8" if ai_level == "Low" else ("#FFD98A" if ai_level == "Moderate" else "#FF6F91")
    consistency_color = "#7EEBB8" if consistency == "Strong" else ("#FFD98A" if consistency == "Moderate" else "#FF6F91")

    # Full HTML markup
    html_content = f"""
    <div class="proof-card-container">
        <style>
            @keyframes dotPop {{
                0% {{ transform: scale(0.4); opacity: 0; }}
                60% {{ transform: scale(1.25); }}
                100% {{ transform: scale(1); opacity: 1; }}
            }}
            .proof-card-container {{
                display: flex;
                justify-content: center;
                margin: 20px 0;
            }}
            .proof-card {{
                width: 100%;
                max-width: 650px;
                background: linear-gradient(145deg, #1E1233 0%, #2F1D4D 100%);
                border: 2px solid rgba(129, 140, 248, 0.25);
                border-radius: 20px;
                box-shadow: 0 15px 45px rgba(0, 0, 0, 0.6), 0 0 30px rgba(129, 140, 248, 0.05);
                padding: 30px;
                position: relative;
                overflow: hidden;
                color: #F0E8FF;
                font-family: 'Inter', sans-serif;
                -webkit-print-color-adjust: exact !important;
                print-color-adjust: exact !important;
                color-adjust: exact !important;
                transition: box-shadow 0.3s ease, border-color 0.3s ease;
            }}
            .proof-card:hover {{
                border-color: rgba(129, 140, 248, 0.45);
                box-shadow: 0 15px 45px rgba(0, 0, 0, 0.6), 0 0 40px rgba(129, 140, 248, 0.15);
            }}
            @media print {{
                html, body {{
                    -webkit-print-color-adjust: exact !important;
                    print-color-adjust: exact !important;
                    background: #1E1233 !important;
                }}
            }}
            /* Glow effects */
            .proof-card::before {{
                content: '';
                position: absolute;
                top: -50%;
                right: -50%;
                width: 100%;
                height: 100%;
                background: radial-gradient(circle, rgba(168, 85, 247, 0.08) 0%, transparent 70%);
                z-index: 0;
                pointer-events: none;
            }}
            .proof-card::after {{
                content: '';
                position: absolute;
                bottom: -50%;
                left: -50%;
                width: 100%;
                height: 100%;
                background: radial-gradient(circle, rgba(99, 102, 241, 0.08) 0%, transparent 70%);
                z-index: 0;
                pointer-events: none;
            }}
            /* Brand Header */
            .proof-header {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                border-bottom: 1px solid rgba(255, 255, 255, 0.08);
                padding-bottom: 16px;
                margin-bottom: 20px;
                position: relative;
                z-index: 1;
            }}
            .brand-name {{
                font-family: 'Fredoka', sans-serif;
                font-weight: 800;
                font-size: 1.5rem;
                background: linear-gradient(135deg, #B99CFF 0%, #D9A6FF 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                letter-spacing: -0.02em;
            }}
            .proof-id-badge {{
                font-family: 'JetBrains Mono', monospace;
                background: rgba(255, 255, 255, 0.06);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 6px;
                padding: 4px 10px;
                font-size: 0.75rem;
                color: #B8A8D9;
                letter-spacing: 0.05em;
            }}
            /* Core Stats */
            .proof-body {{
                position: relative;
                z-index: 1;
            }}
            .work-title {{
                font-family: 'Fredoka', sans-serif;
                font-size: 1.6rem;
                font-weight: 700;
                color: #F5EFFF;
                margin: 0 0 6px 0;
            }}
            .category-tag {{
                font-size: 0.75rem;
                text-transform: uppercase;
                letter-spacing: 0.1em;
                color: #B99CFF;
                font-weight: 700;
                margin-bottom: 16px;
                display: inline-block;
            }}
            /* Stars block */
            .score-section {{
                display: flex;
                align-items: center;
                gap: 12px;
                margin-bottom: 20px;
            }}
            .score-stars {{
                display: flex;
                gap: 6px;
            }}
            .score-dot {{
                width: 12px;
                height: 12px;
                border-radius: 50%;
                background-color: #3D2A5C;
                border: 1px solid rgba(255, 255, 255, 0.05);
            }}
            .score-dot.active {{
                background-color: #B99CFF;
                box-shadow: 0 0 8px rgba(129, 140, 248, 0.6);
                animation: dotPop 0.4s ease-out;
            }}
            .score-label {{
                font-family: 'Fredoka', sans-serif;
                font-size: 1rem;
                font-weight: 600;
                color: #F5EFFF;
                background: rgba(129, 140, 248, 0.12);
                border: 1px solid rgba(129, 140, 248, 0.2);
                padding: 2px 10px;
                border-radius: 6px;
            }}
            .tier-pill {{
                font-family: 'Fredoka', sans-serif;
                font-size: 0.85rem;
                font-weight: 700;
                color: #D9A6FF;
                background: rgba(192, 132, 252, 0.12);
                border: 1px solid rgba(192, 132, 252, 0.2);
                padding: 2px 10px;
                border-radius: 6px;
                margin-left: 6px;
            }}
            /* Tags Container */
            .proof-tag-container {{
                display: flex;
                flex-wrap: wrap;
                gap: 6px;
                margin-bottom: 22px;
            }}
            .proof-tag {{
                background: rgba(255, 255, 255, 0.04);
                border: 1px solid rgba(255, 255, 255, 0.08);
                color: #D9CCF0;
                padding: 4px 10px;
                border-radius: 6px;
                font-size: 0.75rem;
                font-weight: 500;
            }}
            /* Verification Indicators */
            .metrics-panel {{
                background: rgba(10, 15, 28, 0.5);
                border: 1px solid rgba(255, 255, 255, 0.04);
                border-radius: 12px;
                padding: 16px;
                margin-bottom: 22px;
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 12px;
            }}
            .metric-item {{
                text-align: center;
            }}
            .metric-title {{
                font-size: 0.65rem;
                color: #B8A8D9;
                text-transform: uppercase;
                letter-spacing: 0.05em;
                margin-bottom: 4px;
            }}
            .metric-stat {{
                font-weight: 700;
                font-size: 0.9rem;
            }}
            /* Subsections */
            .bullets-section {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 20px;
                margin-bottom: 20px;
            }}
            .bullets-col h4 {{
                margin: 0 0 8px 0;
                font-size: 0.85rem;
                color: #F5EFFF;
                text-transform: uppercase;
                letter-spacing: 0.05em;
                font-family: 'Fredoka', sans-serif;
            }}
            .bullets-col ul {{
                margin: 0;
                padding-left: 16px;
                font-size: 0.8rem;
                color: #B8A8D9;
                line-height: 1.4;
            }}
            .bullets-col li {{
                margin-bottom: 6px;
            }}
            .quality-summary {{
                font-size: 0.8rem;
                color: #B8A8D9;
                line-height: 1.4;
                border-left: 2px solid #B99CFF;
                padding-left: 10px;
                margin-bottom: 20px;
            }}
            /* Footer Disclaimer */
            .proof-footer {{
                border-top: 1px solid rgba(255, 255, 255, 0.08);
                padding-top: 14px;
                display: flex;
                justify-content: space-between;
                align-items: flex-end;
                font-size: 0.65rem;
                color: #9A87C2;
                position: relative;
                z-index: 1;
            }}
            .disclaimer-text {{
                max-width: 70%;
                line-height: 1.3;
            }}
            .date-badge {{
                font-family: 'JetBrains Mono', monospace;
            }}
            .verified-badge {{
                position: absolute;
                bottom: 60px;
                right: 30px;
                border: 2px dashed rgba(168, 85, 247, 0.3);
                color: rgba(168, 85, 247, 0.5);
                font-family: 'Fredoka', sans-serif;
                font-size: 0.85rem;
                font-weight: 800;
                text-transform: uppercase;
                letter-spacing: 0.15em;
                padding: 6px 12px;
                transform: rotate(-12deg);
                border-radius: 6px;
                pointer-events: none;
                z-index: 0;
            }}
        </style>
        <div class="proof-card">
            <div class="verified-badge">Verified Signal</div>
            <div class="proof-header">
                <span class="brand-name">SkillProof</span>
                <span class="proof-id-badge">{proof_id}</span>
            </div>
            <div class="proof-body">
                <span class="category-tag">{category} Assessment</span>
                <h3 class="work-title">{tier} Contribution</h3>
                
                <div class="score-section">
                    <div class="score-stars">
                        {dots_html}
                    </div>
                    <span class="score-label">Score {score}/5</span>
                    <span class="tier-pill">{tier}</span>
                </div>

                <div class="proof-tag-container">
                    {pills_html}
                </div>

                <div class="quality-summary">
                    {technical_quality}
                </div>

                <div class="metrics-panel">
                    <div class="metric-item">
                        <div class="metric-title">Verification Confidence</div>
                        <div class="metric-stat" style="color: {confidence_color};">{confidence}</div>
                    </div>
                    <div class="metric-item">
                        <div class="metric-title">AI Assistance</div>
                        <div class="metric-stat" style="color: {ai_color};">{ai_level}</div>
                    </div>
                    <div class="metric-item">
                        <div class="metric-title">Explanation Consistency</div>
                        <div class="metric-stat" style="color: {consistency_color};">{consistency}</div>
                    </div>
                </div>

                <div class="bullets-section">
                    <div class="bullets-col">
                        <h4>Assessed Strengths</h4>
                        <ul>{strengths_html}</ul>
                    </div>
                    <div class="bullets-col">
                        <h4>Growth Directions</h4>
                        <ul>{growth_html}</ul>
                    </div>
                </div>
            </div>
            <div class="proof-footer">
                <div class="disclaimer-text">
                    AI-assisted assessment based on submitted work and explanation. This is not a definitive determination of human or AI authorship.
                </div>
                <div class="date-badge">
                    ISSUED: {formatted_date}
                </div>
            </div>
        </div>
    </div>
    """
    return html_content


def render_standalone_proof_card_page(assessment_data: dict, proof_id: str, category: str, date_str: str) -> str:
    """
    Wraps the proof card HTML into a complete, self-contained HTML document
    (with Google Fonts + full styling embedded) that can be downloaded and
    opened directly in a browser. This is the reliable path for printing/saving
    as PDF, since printing content that lives inside an iframe is inconsistent
    across browsers — a standalone page prints exactly as shown, every time.
    """
    card_html = render_proof_card_html(assessment_data, proof_id, category, date_str)
    tier = assessment_data.get("skill_tier", "Assessment")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>SkillProof — {proof_id} — {tier}</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Fredoka:wght@500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
    body {{
        margin: 0;
        padding: 32px;
        background: #150a26;
        display: flex;
        justify-content: center;
        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
    }}
    @media print {{
        body {{
            padding: 0;
            background: #150a26 !important;
            -webkit-print-color-adjust: exact !important;
            print-color-adjust: exact !important;
        }}
        @page {{
            margin: 0.5cm;
        }}
    }}
</style>
</head>
<body>
{card_html}
</body>
</html>"""
