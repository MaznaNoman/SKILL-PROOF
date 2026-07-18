# SkillProof — Prove Your Skill, Not Your Pedigree

> Built for **IEEE BuildByte Hackathon**

SkillProof is an evidence-based skill verification platform. A user submits real work (code, writing, or design) along with their own short explanation of their approach. AI evaluates both — producing a **Proof Card**: a free, instant, credential-free way to demonstrate real ability, without needing a degree or paid certification.

LIVE DEMO: https://skill-proof-zkyb6g8xgdbwtjjmvbecdl.streamlit.app/

---

## The Problem We're Solving

Two barriers keep talented people from being recognized:

- **Recognition & Visibility** — contributions often go unseen or uncredited, especially for people without institutional backing.
- **Opportunity Without Wealth** — proving skill usually requires paid certifications, degrees, or bootcamps that many can't afford.

SkillProof addresses both: anyone can submit real work and walk away with a free, verifiable proof of skill — no gatekeeping required.

---

## Our Core Feature — Explanation, Not Just Output

The main thing that makes SkillProof different from "just another AI grader" is this: **the user doesn't just submit their work — they explain their own approach to it, in their own words, under a short time window.**

That explanation is what actually gets evaluated alongside the submission. A person who genuinely understands their own work can explain it naturally and specifically. Someone who can't explain what they submitted has a much weaker case for skill — regardless of how good the submission itself looks.

**On the "AI Assistance Level" / "Verification Confidence" labels:** these are intentionally *not* presented as a reliable AI-content detector. AI-generated-text detection is a well-known hard problem, and no tool (ours included) can claim to reliably tell whether specific text was AI-written. We don't try to. Instead, these labels reflect how well the user's *own explanation* lines up with what they submitted — coherence and specificity, not a forensic AI-detection verdict. They should be read as a **soft signal**, not a definitive judgment, and we say this explicitly in the app itself.

This is a deliberate design choice: rather than over-promising a detection capability we can't guarantee, SkillProof's real value is giving people a structured way to *demonstrate* understanding — which is a more honest and more durable signal than a quality score alone.

---

## Features

- Submit work across 3 categories: Coding, Writing, Design
- AI-generated skill score, tier, and detected skill tags
- 60-second timed explanation step, encouraging in-the-moment, authentic reasoning
- Verification Confidence & AI Assistance signals based on explanation coherence (explicitly framed as a soft signal, not a definitive AI detector)
- Submission history — a trust profile that builds over time, not a single snapshot
- Downloadable Proof Card (standalone HTML, print/save-as-PDF ready)

---

## Tech Stack

- **Frontend/App:** Python, Streamlit
- **AI:** Google Gemini API (`gemini-flash-latest`), structured output via Pydantic schemas
- **Database:** SQLite
- **Deployment:** Streamlit Community Cloud

---

## File Structure & Responsibility

- **`app.py`** — Streamlit UI and wizard flow (Submit → 60s Explanation → Loading → Results → Proof Card → History).
- **`ai_analyzer.py`** — Gemini API integration (modern `google-genai` SDK with legacy fallback), structured schema generation.
- **`models.py`** — Pydantic schemas validating score ranges and allowed values.
- **`prompts.py`** — Prompt instructions defining evidence-based scoring and explanation-coherence evaluation.
- **`database.py`** — SQLite storage for archiving past assessments.
- **`utils.py`** — Global CSS/theme, typography, and the Proof Card HTML template (including the standalone downloadable version).

---

## How It Works

```
User selects category + submits work
        │
        ▼
User explains their approach (60-second window)
        │
        ▼
Gemini analyzes: submission quality + explanation coherence
        │
        ▼
Returns: score, tier, skill tags, verification confidence
        │
        ▼
Proof Card generated + saved to history
```

---

## Setup & Local Execution

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Get a Gemini API key
1. Go to [Google AI Studio](https://aistudio.google.com/)
2. Log in and click **Create API Key**
3. Copy the key

### 3. Add your key locally
Create `.streamlit/secrets.toml` in the project root:
```toml
GEMINI_API_KEY = "your_actual_key_here"
```
This file is git-ignored and will never be committed.

### 4. Run the app
```bash
streamlit run app.py
```
Opens at `http://localhost:8501`.

---

## Deployment (Streamlit Community Cloud)

1. Push this repo to GitHub (`.streamlit/secrets.toml` stays out of git — already handled by `.gitignore`).
2. Go to [share.streamlit.io](https://share.streamlit.io/), log in, click **New app**, and select this repo with `app.py` as the entry point.
3. Before/after deploying, open **Settings → Secrets** and add:
   ```toml
   GEMINI_API_KEY = "your_actual_key_here"
   ```
4. Save — Streamlit loads this into `st.secrets` automatically.

---

## Demo Script (for judges / walkthrough)

1. Confirm the sidebar shows **API Key Detected & Configured**.
2. Select **Coding**, click the sample submission button to load a demo snippet.
3. Click **Analyze My Skill**.
4. On the explanation screen, write (or load the demo) explanation within the 60-second window.
5. Submit — review the score, skill tags, and verification confidence.
6. Click **Generate Proof Card** to see the final credential.
7. Click **Download Proof Card**, open the downloaded file in your browser, and print/save as PDF from there (enable Background Graphics for full color).
8. Open **History** in the sidebar to see the assessment archived.

---

## Challenge Alignment

- **Recognition & Visibility:** Gives people a way to demonstrate skill through actual, explained work rather than relying on credentials that reward existing privilege.
- **Opportunity Without Wealth:** Free, instant, and requires no paid certification, bootcamp, or degree — just the work and the ability to explain it.

---

## Known Limitations & Roadmap

- **AI Assistance / Verification Confidence is a soft signal, not a guarantee.** It's based on explanation-to-submission coherence, not forensic AI-content detection — no such detector is fully reliable, and we don't claim otherwise.
- Verification is currently single-submission-based.
- **Planned:** peer/community validation layer, dynamic live-challenge mode (instead of static submission), and long-term trust profiles built from patterns across multiple submissions rather than one-off scoring.

