"""This module defines the AnnotationTaskResolver."""

from typing import List, Optional, Sequence
from uuid import UUID

from sqlmodel import Session, select

from lightly_purple.server.models.annotation_task import AnnotationTask


class AnnotationTaskResolver:
    """Resolver class for AnnotationTask models."""

    def __init__(self, session: Session) -> None:
        """Initialize the resolver with a database session."""
        self.session = session

    def create(self, annotation_task: AnnotationTask) -> AnnotationTask:
        """Create a new annotation task."""
        self.session.add(annotation_task)
        self.session.commit()
        self.session.refresh(annotation_task)
        return annotation_task

    def get_by_id(self, annotation_task_id: UUID) -> Optional[AnnotationTask]:
        """Get an annotation task by ID."""
        statement = select(AnnotationTask).where(
            AnnotationTask.annotation_task_id == annotation_task_id
        )
        return self.session.exec(statement).first()

    def get_all(self) -> List[AnnotationTask]:
        """Get all annotation tasks."""
        statement = select(AnnotationTask)
        results: Sequence[AnnotationTask] = self.session.exec(statement).all()
        return list(results)
