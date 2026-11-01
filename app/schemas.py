from typing import List, Dict, Any
from pydantic import BaseModel, Field


class BulletFacts(BaseModel):
    action: List[str] = Field(default_factory=list)
    object: List[str] = Field(default_factory=list)
    method: List[str] = Field(default_factory=list)
    result: List[str] = Field(default_factory=list)
    missing: List[str] = Field(default_factory=list)


class BulletVersion(BaseModel):
    tone: str
    bullets: List[str] = Field(default_factory=list)


class BulletOptimization(BaseModel):
    facts: BulletFacts
    versions: List[BulletVersion] = Field(default_factory=list)
    questions: List[str] = Field(default_factory=list)


class ParsedJD(BaseModel):
    company: str = ""
    title: str = ""
    must_have: List[str] = Field(default_factory=list)
    nice_to_have: List[str] = Field(default_factory=list)
    responsibilities: List[str] = Field(default_factory=list)
    keywords: List[str] = Field(default_factory=list)
    tone: str = ""
    seniority: str = ""
    domain: str = ""


class InterviewQuestion(BaseModel):
    category: str
    question: str
    intent: str = ""
    answer_framework: str = ""
    related_story_ids: List[int] = Field(default_factory=list)
    followups: List[str] = Field(default_factory=list)
    red_flags: List[str] = Field(default_factory=list)


class InterviewCategory(BaseModel):
    name: str
    questions: List[InterviewQuestion] = Field(default_factory=list)


class InterviewPack(BaseModel):
    total_questions: int = 0
    categories: List[InterviewCategory] = Field(default_factory=list)
