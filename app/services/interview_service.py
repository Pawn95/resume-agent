from typing import List, Optional
from sqlmodel import select

from app.db import get_session
from app.models import InterviewPack


def create_pack(job_id: Optional[int], story_ids: List[int], pack_json: dict) -> InterviewPack:
    with get_session() as session:
        pack = InterviewPack(
            job_id=job_id,
            story_ids=story_ids or [],
            pack_json=pack_json or {},
        )
        session.add(pack)
        session.commit()
        session.refresh(pack)
        return pack


def list_packs() -> List[InterviewPack]:
    with get_session() as session:
        return list(session.exec(select(InterviewPack).order_by(InterviewPack.created_at.desc())).all())


def get_pack(pack_id: int) -> Optional[InterviewPack]:
    with get_session() as session:
        return session.get(InterviewPack, pack_id)


def delete_pack(pack_id: int) -> bool:
    with get_session() as session:
        pack = session.get(InterviewPack, pack_id)
        if not pack:
            return False
        session.delete(pack)
        session.commit()
        return True
