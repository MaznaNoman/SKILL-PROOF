import sqlite3
import os
import json
from datetime import datetime

DEFAULT_DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "skillproof.db")

def init_db(db_path=DEFAULT_DB_PATH):
    """Initializes the database and creates the assessments table if it doesn't exist."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS assessments (
            proof_id TEXT PRIMARY KEY,
            category TEXT NOT NULL,
            submitted_work TEXT NOT NULL,
            explanation TEXT NOT NULL,
            assessment_date TEXT NOT NULL,
            score INTEGER NOT NULL,
            skill_tier TEXT NOT NULL,
            verification_confidence TEXT NOT NULL,
            ai_assistance_level TEXT NOT NULL,
            explanation_consistency TEXT NOT NULL,
            assessment_json TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def save_assessment(
    proof_id,
    category,
    submitted_work,
    explanation,
    score,
    skill_tier,
    verification_confidence,
    ai_assistance_level,
    explanation_consistency,
    assessment_json,
    db_path=DEFAULT_DB_PATH,
    assessment_date=None
):
    """Saves a new skill assessment to the database."""
    if assessment_date is None:
        assessment_date = datetime.now().isoformat()
        
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO assessments (
                proof_id, category, submitted_work, explanation, assessment_date,
                score, skill_tier, verification_confidence, ai_assistance_level,
                explanation_consistency, assessment_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                proof_id,
                category,
                submitted_work,
                explanation,
                assessment_date,
                score,
                skill_tier,
                verification_confidence,
                ai_assistance_level,
                explanation_consistency,
                assessment_json
            )
        )
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error while saving assessment: {e}")
        conn.rollback()
        raise e
    finally:
        conn.close()

def get_all_assessments(db_path=DEFAULT_DB_PATH):
    """Retrieves all saved assessments sorted by date descending."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM assessments ORDER BY assessment_date DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_assessment_by_id(proof_id, db_path=DEFAULT_DB_PATH):
    """Retrieves a single assessment by proof_id."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM assessments WHERE proof_id = ?", (proof_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None
