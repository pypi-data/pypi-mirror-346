"""This module contains the API routes for computing detection metrics."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlmodel import Session
from typing_extensions import Annotated

from lightly_purple.metrics.detection.map import (
    DetectionMetricsMAP,
    calculate_map_metric,
)
from lightly_purple.server.db import get_session
from lightly_purple.server.resolvers.annotation import (
    AnnotationsFilterParams,
    BoundingBoxAnnotationResolver,
)
from lightly_purple.server.resolvers.annotation_label import (
    AnnotationLabelResolver,
)
from lightly_purple.server.routes.api.annotation import get_annotation_resolver
from lightly_purple.server.routes.api.annotation_label import (
    get_annotation_label_resolver,
)

metrics_router = APIRouter()

SessionDep = Annotated[Session, Depends(get_session)]


class DetectionMetricsMAPRequest(BaseModel):
    """Request for computing the MAP detection metric."""

    dataset_id: UUID
    ground_truth_task_id: UUID
    prediction_task_id: UUID
    tag_id: UUID | None = None


@metrics_router.post(
    "/metrics/compute/detection/map", response_model=DetectionMetricsMAP
)
def compute_detection_map(
    request_body: DetectionMetricsMAPRequest,
    resolver: Annotated[
        BoundingBoxAnnotationResolver, Depends(get_annotation_resolver)
    ],
    label_resolver: Annotated[
        AnnotationLabelResolver, Depends(get_annotation_label_resolver)
    ],
) -> DetectionMetricsMAP:
    """Compute the MAP detection metric."""
    ground_truth_annotations = resolver.get_all(
        filters=AnnotationsFilterParams(
            dataset_ids=[request_body.dataset_id],
            annotation_task_ids=[request_body.ground_truth_task_id],
            sample_tag_ids=[request_body.tag_id]
            if request_body.tag_id
            else None,
        ),
    )
    prediction_annotations = resolver.get_all(
        filters=AnnotationsFilterParams(
            dataset_ids=[request_body.dataset_id],
            annotation_task_ids=[request_body.prediction_task_id],
            sample_tag_ids=[request_body.tag_id]
            if request_body.tag_id
            else None,
        ),
    )

    metrics_result = calculate_map_metric(
        pred_annotations=prediction_annotations,
        gt_annotations=ground_truth_annotations,
    )

    # Rename per-class metrics to use label names
    raw_map_pc = metrics_result.map_per_class
    if raw_map_pc:
        id2name = label_resolver.names_by_ids([UUID(k) for k in raw_map_pc])
        metrics_result.map_per_class = {
            id2name.get(k, k): v for k, v in raw_map_pc.items()
        }
    raw_mar100_pc = metrics_result.mar_100_per_class
    if raw_mar100_pc:
        id2name = label_resolver.names_by_ids([UUID(k) for k in raw_mar100_pc])
        metrics_result.mar_100_per_class = {
            id2name.get(k, k): v for k, v in raw_mar100_pc.items()
        }
    return metrics_result
