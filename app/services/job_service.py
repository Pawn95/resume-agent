from typing import List, Optional
from sqlmodel import select

from app.db import get_session
from app.models import Job


def create_job(jd_text: str, parsed_json: dict) -> Job:
    with get_session() as session:
        job = Job(
            jd_text=jd_text,
            parsed_json=parsed_json or {},
            company=(parsed_json.get("company") or None) if parsed_json else None,
            title=(parsed_json.get("title") or None) if parsed_json else None,
        )
        session.add(job)
        session.commit()
        session.refresh(job)
        return job


def list_jobs() -> List[Job]:
    with get_session() as session:
        return list(session.exec(select(Job).order_by(Job.created_at.desc())).all())


def get_job(job_id: int) -> Optional[Job]:
    with get_session() as session:
        return session.get(Job, job_id)


def delete_job(job_id: int) -> bool:
    with get_session() as session:
        job = session.get(Job, job_id)
        if not job:
            return False
        session.delete(job)
        session.commit()
        return True
