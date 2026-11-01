from datetime import datetime, timezone
from typing import Optional, List, Dict, Any

from sqlmodel import SQLModel, Field
from sqlalchemy import Column, JSON


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Story(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    raw_text: str
    target_role: Optional[str] = None
    target_level: Optional[str] = None
    jd_keywords: Optional[str] = None
    facts_json: Dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))
    optimized_bullets_json: List[Dict[str, Any]] = Field(default_factory=list, sa_column=Column(JSON))
    questions_json: List[str] = Field(default_factory=list, sa_column=Column(JSON))
    tags: List[str] = Field(default_factory=list, sa_column=Column(JSON))
    created_at: datetime = Field(default_factory=_utcnow)
    updated_at: datetime = Field(default_factory=_utcnow)


class Job(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    company: Optional[str] = None
    title: Optional[str] = None
    jd_text: str
    parsed_json: Dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))
    created_at: datetime = Field(default_factory=_utcnow)


class InterviewPack(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    job_id: Optional[int] = Field(default=None, foreign_key="job.id")
    story_ids: List[int] = Field(default_factory=list, sa_column=Column(JSON))
    pack_json: Dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))
    created_at: datetime = Field(default_factory=_utcnow)


class Version(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    job_id: Optional[int] = Field(default=None, foreign_key="job.id")
    story_ids: List[int] = Field(default_factory=list, sa_column=Column(JSON))
    bullet_optimization_json: List[Dict[str, Any]] = Field(default_factory=list, sa_column=Column(JSON))
    parsed_jd_json: Dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))
    interview_pack_json: Dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=_utcnow)
