"""Example: index a YOLO dataset **and** add model predictions.

Workflow
--------
1. Load the ground truth YOLO dataset (same loader call as `example.py`).
2. Create a second annotation task flagged `is_prediction=True`.
3. For every ground truth box we fabricate a “prediction” (copy the box,
   give it a random confidence); insert them in a single bulk call.
4. Compute mAP (overall + per class) in Python and print it.
5. Launch the Purple UI so you can inspect both tasks.

Environment
-----------
• DATASET_PATH: path to your YOLO `data.yaml`
• PURPLE_DATASET_SPLIT: dataset split to load (train / val / test)
"""

from __future__ import annotations

import os
import random
from pathlib import Path
from uuid import UUID

from lightly_purple.dataset.loader import DatasetLoader
from lightly_purple.metrics.detection.map import calculate_map_metric
from lightly_purple.server.db import db_manager
from lightly_purple.server.models.annotation_task import (
    AnnotationTask,
    AnnotationType,
)
from lightly_purple.server.models.bounding_box_annotation import (
    BoundingBoxAnnotationInput,
)
from lightly_purple.server.models.tag import TagInput
from lightly_purple.server.resolvers.annotation import (
    AnnotationsFilterParams,
    BoundingBoxAnnotationResolver,
)
from lightly_purple.server.resolvers.annotation_label import (
    AnnotationLabelResolver,
)
from lightly_purple.server.resolvers.annotation_task import (
    AnnotationTaskResolver,
)
from lightly_purple.server.resolvers.dataset import DatasetResolver
from lightly_purple.server.resolvers.sample import SampleResolver

# Tag imports for train/test split
from lightly_purple.server.resolvers.tag import TagResolver

# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #
DATASET_PATH = Path(
    os.getenv(
        "DATASET_PATH",
        "/path/to/your/yolo/dataset/data.yaml",
    )
).expanduser()
INPUT_SPLIT = os.getenv("PURPLE_DATASET_SPLIT", "train")  # train / val / test
CONF_RANGE = (0.5, 0.95)  # random confidence for mock predictions


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
def _random_confidence() -> float:
    return random.uniform(*CONF_RANGE)


# --------------------------------------------------------------------------- #
# Inference stub — replace with your own model call
# --------------------------------------------------------------------------- #
def _run_inference(
    image_files: list[Path],
) -> dict[str, list[tuple[float, float, float, float, float]]]:
    """Mock detector.

    Returns a mapping: image filename -> list of (x, y, w, h, confidence)

    Replace this with your actual batch inference implementation.
    The coordinates must be absolute pixel values (XYWH).
    """
    preds: dict[str, list[tuple[float, float, float, float, float]]] = {}
    for img in image_files:
        # fabricate 0 to 3 random boxes per image
        num_boxes = random.randint(0, 3)
        pred_boxes = []
        for _ in range(num_boxes):
            x = random.uniform(0, 400)
            y = random.uniform(0, 400)
            w = random.uniform(20, 150)
            h = random.uniform(20, 150)
            conf = _random_confidence()
            pred_boxes.append((x, y, w, h, conf))
        preds[img.name] = pred_boxes
    return preds


def _latest_dataset_id(resolver: DatasetResolver):
    """Return the newest dataset (assumes each run starts fresh)."""
    datasets = resolver.get_all()
    return datasets[0].dataset_id  # type: ignore[attr-defined]


def _latest_gt_task_id(resolver: AnnotationTaskResolver):
    """Return the newest *ground truth* task (is_prediction = False)."""
    for task in reversed(resolver.get_all()):
        if (
            not task.is_prediction
            and task.annotation_type == AnnotationType.BBOX
        ):
            return task.annotation_task_id
    raise RuntimeError("No ground truth task found.")


# --------------------------------------------------------------------------- #
# 1. Load ground truth YOLO labels
# --------------------------------------------------------------------------- #
print("▶ Loading YOLO dataset…")
loader = DatasetLoader()
loader.from_yolo(
    str(DATASET_PATH), input_split=INPUT_SPLIT, task_name="Labelbox Annotations"
)

# --------------------------------------------------------------------------- #
# 2. Open a DB session: create prediction task & insert fake boxes
# --------------------------------------------------------------------------- #
with db_manager.session() as session:
    dataset_resolver = DatasetResolver(session)
    task_resolver = AnnotationTaskResolver(session)
    ann_resolver = BoundingBoxAnnotationResolver(session)

    dataset_id = _latest_dataset_id(dataset_resolver)
    gt_task_id = _latest_gt_task_id(task_resolver)
    # --- fetch all GT boxes (needed for metrics & label pool) ------------- #
    gt_boxes = ann_resolver.get_all(
        filters=AnnotationsFilterParams(annotation_task_ids=[gt_task_id])
    )

    # Use all distinct label ids from the GT set
    label_id_pool = list({box.annotation_label_id for box in gt_boxes})

    # --- create prediction task ------------------------------------------- #
    pred_task = task_resolver.create(
        AnnotationTask(
            name="YOLOv8 predictions",
            annotation_type=AnnotationType.BBOX,
            is_prediction=True,
        )
    )
    pred_task_id = pred_task.annotation_task_id
    print(f"▶ Created prediction task {pred_task_id}")

    # --- gather sample records to map filename -> sample_id --------------- #
    sample_resolver = SampleResolver(session)
    # Fetch *all* samples for this dataset (single call with large limit)
    samples = sample_resolver.get_all_by_dataset_id(
        dataset_id=dataset_id,
        offset=0,
        limit=100_000,  # adjust if you expect >100k images
    )
    # Create train/test split tags (60/40) and assign samples
    tag_resolver = TagResolver(session)
    sample_ids = [s.sample_id for s in samples]
    random.shuffle(sample_ids)
    split_idx = int(0.6 * len(sample_ids))
    train_ids = sample_ids[:split_idx]
    test_ids = sample_ids[split_idx:]

    train_tag = tag_resolver.create(
        TagInput(dataset_id=dataset_id, name="train", kind="sample")
    )
    test_tag = tag_resolver.create(
        TagInput(dataset_id=dataset_id, name="test", kind="sample")
    )
    tag_resolver.add_sample_ids_to_tag_id(train_tag.tag_id, train_ids)
    tag_resolver.add_sample_ids_to_tag_id(test_tag.tag_id, test_ids)
    filename_to_sample: dict[str, UUID] = {}
    for s in samples:
        # Sample model stores the absolute path in `file_path_abs`
        fname = Path(getattr(s, "file_path_abs", s.file_name)).name
        filename_to_sample[fname] = s.sample_id

    # --- call user defined inference -------------------------------------- #
    image_paths = [
        Path(getattr(s, "file_path_abs", s.file_name)) for s in samples
    ]
    pred_dict = _run_inference(image_paths)

    # --- convert predictions to DB inputs --------------------------------- #
    pred_inputs: list[BoundingBoxAnnotationInput] = []
    for fname, boxes in pred_dict.items():
        sample_id = filename_to_sample.get(fname)
        if sample_id is None:
            continue  # skip files that are not in our DB
        for x, y, w, h, conf in boxes:
            pred_inputs.append(
                BoundingBoxAnnotationInput(
                    dataset_id=dataset_id,
                    sample_id=sample_id,
                    annotation_label_id=random.choice(label_id_pool),
                    annotation_task_id=pred_task_id,
                    x=x,
                    y=y,
                    width=w,
                    height=h,
                    confidence=conf,
                )
            )

    # Add jittered ground-truth boxes as pseudo-predictions for some positives
    for gt in gt_boxes:
        if random.random() < 0.8:  # noqa: PLR2004
            pred_inputs.append(
                BoundingBoxAnnotationInput(
                    dataset_id=gt.dataset_id,
                    sample_id=gt.sample_id,
                    annotation_label_id=gt.annotation_label_id,
                    annotation_task_id=pred_task_id,
                    x=gt.x + random.uniform(-5, 5),
                    y=gt.y + random.uniform(-5, 5),
                    width=gt.width * random.uniform(0.9, 1.1),
                    height=gt.height * random.uniform(0.9, 1.1),
                    confidence=random.uniform(0.8, 1.0),
                )
            )

    ann_resolver.create_many(pred_inputs)
    print(f"▶ Inserted {len(pred_inputs)} predictions")

    # --------------------------------------------------------------------- #
    # 3. Compute metrics locally
    # --------------------------------------------------------------------- #
    metrics = calculate_map_metric(pred_inputs, gt_boxes)
    print("\n=== mAP ===")
    print(f"Overall: {metrics.map:.3f}")
    if metrics.map_per_class:
        id2name = AnnotationLabelResolver(session).names_by_ids(
            [UUID(k) for k in metrics.map_per_class]
        )
        for label_id, val in metrics.map_per_class.items():
            print(f"  {id2name.get(label_id, label_id)}: {val:.3f}")
    print(f"mAP@0.50 (IoU=0.50): {metrics.map_50:.3f}")
    print(f"mAP@0.75 (IoU=0.75): {metrics.map_75:.3f}")
    print(f"mAP small objects (<32^2 px): {metrics.map_small:.3f}")
    print(f"mAP medium objects (32^2-96^2 px): {metrics.map_medium:.3f}")
    print(f"mAP large objects (>96^2 px): {metrics.map_large:.3f}")
    print(f"Recall@100 detections per image: {metrics.mar_100:.3f}")
    print("============\n")

# --------------------------------------------------------------------------- #
# 4. Launch UI
# --------------------------------------------------------------------------- #
loader.launch()
