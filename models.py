from pydantic import BaseModel, Field, field_validator
from typing import List, Literal

class SkillAssessment(BaseModel):
    score: int = Field(..., description="Skill Score from 1 to 5 based on technical or conceptual quality.")
    skill_tags: List[str] = Field(..., description="List of specific technical/conceptual skills detected in the work.")
    skill_tier: Literal["Beginner", "Intermediate", "Advanced"] = Field(..., description="The tier of the assessed skill level.")
    verification_confidence: Literal["Strong", "Moderate", "Limited"] = Field(..., description="Verification confidence for contribution authenticity based on explanation and work consistency.")
    ai_assistance_level: Literal["Low", "Moderate", "High"] = Field(..., description="Likelihood of AI usage in the submitted work.")
    ai_assistance_explanation: str = Field(..., description="Short explanation of the AI-likelihood analysis and assistance signals detected.")
    ai_assistance_signals: List[str] = Field(..., description="Key features of the work that indicate AI assistance or human elements.")
    explanation_consistency: Literal["Strong", "Moderate", "Limited"] = Field(..., description="How well the user's explanation matches the concepts and execution in the submitted work.")
    explanation_consistency_explanation: str = Field(..., description="Detailed reasoning comparing the explanation and the work.")
    strengths: List[str] = Field(..., description="List of concrete, evidence-backed strengths in the submitted work.")
    weaknesses: List[str] = Field(..., description="List of areas that need refinement or show limitations in the submitted work.")
    growth_areas: List[str] = Field(..., description="Actionable suggestions for learning or development.")
    technical_quality: str = Field(..., description="Summary of the technical or conceptual quality of the work.")
    work_evidence: str = Field(..., description="Direct citation or specific analysis points from the submitted work illustrating the skills.")

    @field_validator('score')
    @classmethod
    def check_score(cls, v: int) -> int:
        if not (1 <= v <= 5):
            raise ValueError('Score must be between 1 and 5')
        return v
