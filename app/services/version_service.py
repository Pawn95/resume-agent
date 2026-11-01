from typing import List, Optional
from sqlmodel import select

from app.db import get_session
from app.models import Version


def create_version(
    name: str,
    job_id: Optional[int] = None,
    story_ids: Optional[List[int]] = None,
    bullet_optimization_json: Optional[list] = None,
    parsed_jd_json: Optional[dict] = None,
    interview_pack_json: Optional[dict] = None,
    notes: str = "",
) -> Version:
    with get_session() as session:
        v = Version(
            name=name,
            job_id=job_id,
            story_ids=story_ids or [],
            bullet_optimization_json=bullet_optimization_json or [],
            parsed_jd_json=parsed_jd_json or {},
            interview_pack_json=interview_pack_json or {},
            notes=notes or None,
        )
        session.add(v)
        session.commit()
        session.refresh(v)
        return v


def list_versions() -> List[Version]:
    with get_session() as session:
        return list(session.exec(select(Version).order_by(Version.created_at.desc())).all())


def get_version(version_id: int) -> Optional[Version]:
    with get_session() as session:
        return session.get(Version, version_id)


def delete_version(version_id: int) -> bool:
    with get_session() as session:
        v = session.get(Version, version_id)
        if not v:
            return False
        session.delete(v)
        session.commit()
        return True
