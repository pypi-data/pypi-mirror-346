"""API endpoints for annotation tasks."""

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from lightly_purple.server.db import get_session
from lightly_purple.server.models.annotation_task import AnnotationTask
from lightly_purple.server.resolvers.annotation_task import (
    AnnotationTaskResolver,
)

router = APIRouter(prefix="/annotationtasks", tags=["annotationtasks"])


@router.get("/", response_model=List[AnnotationTask])
def get_annotation_tasks(
    session: Session = Depends(get_session),  # noqa: B008
) -> List[AnnotationTask]:
    """Get all annotation tasks."""
    resolver = AnnotationTaskResolver(session)
    return resolver.get_all()


@router.get("/{annotation_task_id}", response_model=AnnotationTask)
def get_annotation_task(
    annotation_task_id: UUID,
    session: Session = Depends(get_session),  # noqa: B008
) -> AnnotationTask:
    """Get an annotation task by ID."""
    resolver = AnnotationTaskResolver(session)
    task = resolver.get_by_id(annotation_task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Annotation task with ID {annotation_task_id} not found",
        )
    return task
