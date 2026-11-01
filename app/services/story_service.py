from typing import List, Optional
from sqlmodel import select

from app.db import get_session
from app.models import Story


def create_story(
    title: str,
    raw_text: str,
    target_role: str = "",
    target_level: str = "",
    jd_keywords: str = "",
    facts_json: Optional[dict] = None,
    optimized_bullets_json: Optional[list] = None,
    questions_json: Optional[list] = None,
    tags: Optional[list] = None,
) -> Story:
    with get_session() as session:
        story = Story(
            title=title,
            raw_text=raw_text,
            target_role=target_role or None,
            target_level=target_level or None,
            jd_keywords=jd_keywords or None,
            facts_json=facts_json or {},
            optimized_bullets_json=optimized_bullets_json or [],
            questions_json=questions_json or [],
            tags=tags or [],
        )
        session.add(story)
        session.commit()
        session.refresh(story)
        return story


def list_stories() -> List[Story]:
    with get_session() as session:
        return list(session.exec(select(Story).order_by(Story.created_at.desc())).all())


def get_story(story_id: int) -> Optional[Story]:
    with get_session() as session:
        return session.get(Story, story_id)


def update_story(story_id: int, **kwargs) -> Optional[Story]:
    with get_session() as session:
        story = session.get(Story, story_id)
        if not story:
            return None
        for k, v in kwargs.items():
            setattr(story, k, v)
        session.add(story)
        session.commit()
        session.refresh(story)
        return story


def delete_story(story_id: int) -> bool:
    with get_session() as session:
        story = session.get(Story, story_id)
        if not story:
            return False
        session.delete(story)
        session.commit()
        return True
