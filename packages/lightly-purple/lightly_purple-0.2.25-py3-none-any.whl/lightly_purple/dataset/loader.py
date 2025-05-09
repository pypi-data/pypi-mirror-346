"""Dataset functionality module."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from uuid import UUID

from labelformat.formats import (
    COCOInstanceSegmentationInput,
    COCOObjectDetectionInput,
    YOLOv8ObjectDetectionInput,
)
from labelformat.model.binary_mask_segmentation import BinaryMaskSegmentation
from labelformat.model.bounding_box import BoundingBoxFormat
from labelformat.model.image import Image
from labelformat.model.instance_segmentation import (
    ImageInstanceSegmentation,
    InstanceSegmentationInput,
)
from labelformat.model.multipolygon import MultiPolygon
from labelformat.model.object_detection import (
    ImageObjectDetection,
    ObjectDetectionInput,
)
from tqdm import tqdm

from lightly_purple.dataset.embedding_generator import EmbeddingGenerator
from lightly_purple.dataset.embedding_manager import EmbeddingManagerProvider
from lightly_purple.dataset.env import APP_URL, PURPLE_HOST, PURPLE_PORT
from lightly_purple.server.db import db_manager
from lightly_purple.server.features import purple_active_features
from lightly_purple.server.models import Dataset
from lightly_purple.server.models.annotation_label import AnnotationLabelInput
from lightly_purple.server.models.annotation_task import (
    AnnotationTask,
    AnnotationType,
)
from lightly_purple.server.models.bounding_box_annotation import (
    BoundingBoxAnnotationInput,
)
from lightly_purple.server.models.dataset import DatasetInput
from lightly_purple.server.models.sample import SampleInput
from lightly_purple.server.models.tag import TagInput
from lightly_purple.server.resolvers.annotation import (
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
from lightly_purple.server.resolvers.tag import TagResolver
from lightly_purple.server.server import Server

# Constants
ANNOTATION_BATCH_SIZE = 64  # Number of annotations to process in a single batch
EMBEDDING_BATCH_SIZE = 64  # Number of embeddings to process in a single batch


@dataclass
class AnnotationProcessingContext:
    """Context for processing annotations for a single sample."""

    dataset_id: UUID
    sample_id: UUID
    label_map: dict[int, UUID]
    annotation_task_id: UUID


class DatasetLoader:
    """Class responsible for loading datasets from various sources."""

    def __init__(self) -> None:
        """Initialize the dataset loader."""
        with db_manager.session() as session:
            self.dataset_resolver = DatasetResolver(session)
            self.tag_resolver = TagResolver(session)
            self.sample_resolver = SampleResolver(session)
            self.annotation_resolver = BoundingBoxAnnotationResolver(session)
            self.embedding_manager = (
                EmbeddingManagerProvider.get_embedding_manager(session=session)
            )
            self.annotation_label_resolver = AnnotationLabelResolver(session)
            self.annotation_task_resolver = AnnotationTaskResolver(session)

    def _create_dataset(self, name: str, directory: str) -> Dataset:
        """Creates a new dataset."""
        with db_manager.session() as session:  # noqa: F841
            # Create dataset record
            dataset = DatasetInput(
                name=name,
                directory=directory,
            )
            return self.dataset_resolver.create(dataset)

    def _create_example_tags(self, dataset: Dataset) -> None:
        """Create example tags for samples and annotations."""
        self.tag_resolver.create(
            TagInput(
                dataset_id=dataset.dataset_id,
                name="label_mistakes",
                kind="sample",
            )
        )
        self.tag_resolver.create(
            TagInput(
                dataset_id=dataset.dataset_id,
                name="label_mistakes",
                kind="annotation",
            )
        )

    def _create_label_map(
        self, input_labels: ObjectDetectionInput | InstanceSegmentationInput
    ) -> dict[int, UUID]:
        """Create a mapping of category IDs to annotation label IDs."""
        label_map = {}
        for category in tqdm(
            input_labels.get_categories(),
            desc="Processing categories",
            unit=" categories",
        ):
            label = AnnotationLabelInput(annotation_label_name=category.name)
            stored_label = self.annotation_label_resolver.create(label)
            label_map[category.id] = stored_label.annotation_label_id
        return label_map

    def _process_object_detection_annotations(
        self,
        context: AnnotationProcessingContext,
        image_data: ImageObjectDetection,
    ) -> list[BoundingBoxAnnotationInput]:
        """Process object detection annotations for a single image."""
        new_annotations = []
        for obj in image_data.objects:
            box = obj.box.to_format(BoundingBoxFormat.XYWH)
            x, y, width, height = box

            new_annotations.append(
                BoundingBoxAnnotationInput(
                    dataset_id=context.dataset_id,
                    sample_id=context.sample_id,
                    annotation_label_id=context.label_map[obj.category.id],
                    x=x,
                    y=y,
                    width=width,
                    height=height,
                    confidence=obj.confidence,
                    annotation_task_id=context.annotation_task_id,
                )
            )
        return new_annotations

    def _process_instance_segmentation_annotations(
        self,
        context: AnnotationProcessingContext,
        image_data: ImageInstanceSegmentation,
    ) -> list[BoundingBoxAnnotationInput]:
        """Process instance segmentation annotations for a single image."""
        new_annotations = []
        for obj in image_data.objects:
            segmentation_rle: None | list[int] = None
            if isinstance(obj.segmentation, MultiPolygon):
                box = obj.segmentation.bounding_box().to_format(
                    BoundingBoxFormat.XYWH
                )
            elif isinstance(obj.segmentation, BinaryMaskSegmentation):
                box = obj.segmentation.bounding_box.to_format(
                    BoundingBoxFormat.XYWH
                )
                segmentation_rle = obj.segmentation._rle_row_wise  # noqa: SLF001
            else:
                raise ValueError(
                    f"Unsupported segmentation type: {type(obj.segmentation)}"
                )

            x, y, width, height = box

            new_annotations.append(
                BoundingBoxAnnotationInput(
                    dataset_id=context.dataset_id,
                    sample_id=context.sample_id,
                    annotation_label_id=context.label_map[obj.category.id],
                    x=x,
                    y=y,
                    width=width,
                    height=height,
                    segmentation__binary_mask__rle_row_wise=segmentation_rle,
                    annotation_task_id=context.annotation_task_id,
                )
            )
        return new_annotations

    def _load_into_dataset(
        self,
        dataset: Dataset,
        input_labels: ObjectDetectionInput | InstanceSegmentationInput,
        img_dir: Path,
        annotation_task_id: UUID,
    ) -> None:
        """Store a loaded dataset in database."""
        # Create label mapping
        label_map = self._create_label_map(input_labels)

        # Create example tags.
        self._create_example_tags(dataset=dataset)

        annotations_to_create: list[BoundingBoxAnnotationInput] = []
        sample_ids_for_embeddings = []

        # Load an embedding generator and register the model.
        embedding_generator = _load_embedding_generator()

        # Set feature flag if embedding_generator is available.
        if embedding_generator:
            purple_active_features.append("embeddingSearchEnabled")
            embedding_model = self.embedding_manager.register_embedding_model(
                dataset_id=dataset.dataset_id,
                embedding_generator=embedding_generator,
            )

        # Process images and annotations
        for image_data in tqdm(
            input_labels.get_labels(),
            desc="Processing images",
            unit=" images",
        ):
            # Mypy does not get that .image exists in both cases.
            image: Image = image_data.image  # type: ignore[attr-defined]
            # Create sample record
            sample = SampleInput(
                file_name=str(image.filename),
                file_path_abs=str(img_dir / image.filename),
                width=image.width,
                height=image.height,
                dataset_id=dataset.dataset_id,
            )
            stored_sample = self.sample_resolver.create(sample)
            sample_ids_for_embeddings.append(stored_sample.sample_id)
            # Process embedding batch if needed
            if (
                embedding_generator
                and len(sample_ids_for_embeddings) >= EMBEDDING_BATCH_SIZE
            ):
                self.embedding_manager.embed_images(
                    sample_ids=sample_ids_for_embeddings,
                    embedding_model_id=embedding_model.embedding_model_id,
                )
                sample_ids_for_embeddings = []

            # Create context for processing annotations for this sample
            context = AnnotationProcessingContext(
                dataset_id=dataset.dataset_id,
                sample_id=stored_sample.sample_id,
                label_map=label_map,
                annotation_task_id=annotation_task_id,
            )

            # Process annotations.
            new_annotations: list[BoundingBoxAnnotationInput] = []
            if isinstance(image_data, ImageInstanceSegmentation):
                new_annotations = (
                    self._process_instance_segmentation_annotations(
                        context=context,
                        image_data=image_data,
                    )
                )
            elif isinstance(image_data, ImageObjectDetection):
                new_annotations = self._process_object_detection_annotations(
                    context=context,
                    image_data=image_data,
                )
            else:
                raise ValueError(
                    f"Unsupported annotation type: {type(image_data)}"
                )

            annotations_to_create.extend(new_annotations)

            if len(annotations_to_create) >= ANNOTATION_BATCH_SIZE:
                self.annotation_resolver.create_many(annotations_to_create)
                annotations_to_create = []

        # Insert any remaining embeddings
        if embedding_generator and sample_ids_for_embeddings:
            self.embedding_manager.embed_images(
                sample_ids=sample_ids_for_embeddings,
                embedding_model_id=embedding_model.embedding_model_id,
            )
            sample_ids_for_embeddings = []

        # Insert any remaining annotations
        if annotations_to_create:
            self.annotation_resolver.create_many(annotations_to_create)

    def from_yolo(
        self,
        data_yaml_path: str,
        input_split: str = "train",
        task_name: str | None = None,
    ) -> None:
        """Load a dataset in YOLO format and store in DB.

        Args:
            data_yaml_path: Path to the YOLO data.yaml file.
            input_split: The split to load (e.g., 'train', 'val').
            task_name: Optional name for the annotation task. If None, a
                default name is generated.
        """
        data_yaml = Path(data_yaml_path).absolute()
        dataset_name = data_yaml.parent.name

        if task_name is None:
            task_name = (
                f"Loaded from YOLO: {data_yaml.name} ({input_split} split)"
            )

        # Load the dataset using labelformat.
        label_input = YOLOv8ObjectDetectionInput(
            input_file=data_yaml,
            input_split=input_split,
        )
        img_dir = label_input._images_dir()  # noqa: SLF001

        self.from_labelformat(
            input_labels=label_input,
            dataset_name=dataset_name,
            input_images_folder=str(img_dir),
            is_prediction=False,
            task_name=task_name,
        )

    def from_coco_object_detections(
        self,
        annotations_json_path: str,
        input_images_folder: str,
        task_name: str | None = None,
    ) -> None:
        """Load a dataset in COCO Object Detection format and store in DB.

        Args:
            annotations_json_path: Path to the COCO annotations JSON file.
            input_images_folder: Path to the folder containing the images.
            task_name: Optional name for the annotation task. If None, a
                default name is generated.
        """
        annotations_json = Path(annotations_json_path)
        dataset_name = annotations_json.parent.name

        if task_name is None:
            task_name = (
                f"Loaded from COCO Object Detection: {annotations_json.name}"
            )

        label_input = COCOObjectDetectionInput(
            input_file=annotations_json,
        )
        img_dir = Path(input_images_folder).absolute()

        self.from_labelformat(
            input_labels=label_input,
            dataset_name=dataset_name,
            input_images_folder=str(img_dir),
            is_prediction=False,
            task_name=task_name,
        )

    def from_coco_instance_segmentations(
        self,
        annotations_json_path: str,
        input_images_folder: str,
        task_name: str | None = None,
    ) -> None:
        """Load a dataset in COCO Instance Segmentation format and store in DB.

        Args:
            annotations_json_path: Path to the COCO annotations JSON file.
            input_images_folder: Path to the folder containing the images.
            task_name: Optional name for the annotation task. If None, a
                default name is generated.
        """
        annotations_json = Path(annotations_json_path)
        dataset_name = annotations_json.parent.name

        if task_name is None:
            task_name = f"Loaded from COCO Instance Segmentation: {annotations_json.name}"  # noqa: E501

        label_input = COCOInstanceSegmentationInput(
            input_file=annotations_json,
        )
        img_dir = Path(input_images_folder).absolute()

        self.from_labelformat(
            input_labels=label_input,
            dataset_name=dataset_name,
            input_images_folder=str(img_dir),
            is_prediction=False,
            task_name=task_name,
        )

    def from_labelformat(
        self,
        input_labels: ObjectDetectionInput | InstanceSegmentationInput,
        dataset_name: str,
        input_images_folder: str,
        is_prediction: bool = True,
        task_name: str | None = None,
    ) -> None:
        """Load a dataset from a labelformat object and store in database.

        Args:
            input_labels: The labelformat input object.
            dataset_name: The name for the new dataset.
            input_images_folder: Path to the folder containing the images.
            is_prediction: Whether the task is for prediction or labels.
            task_name: Optional name for the annotation task. If None, a
                default name is generated.
        """
        img_dir = Path(input_images_folder).absolute()

        # Determine annotation type based on input.
        # Currently, we always create BBOX tasks, even for segmentation,
        # as segmentation data is stored alongside bounding boxes.
        annotation_type = AnnotationType.BBOX

        # Generate a default task name if none is provided.
        if task_name is None:
            task_name = f"Loaded from labelformat: {dataset_name}"

        # Create dataset and annotation task.
        dataset = self._create_dataset(
            name=dataset_name,
            directory=str(img_dir),
        )
        new_annotation_task = self.annotation_task_resolver.create(
            AnnotationTask(
                name=task_name,
                annotation_type=annotation_type,
                is_prediction=is_prediction,
            )
        )

        img_dir = Path(input_images_folder).absolute()
        self._load_into_dataset(
            dataset=dataset,
            input_labels=input_labels,
            img_dir=img_dir,
            annotation_task_id=new_annotation_task.annotation_task_id,
        )

    def launch(self) -> None:
        """Launch the web interface for the loaded dataset."""
        server = Server(host=PURPLE_HOST, port=PURPLE_PORT)

        print(f"Open the Purple GUI under: {APP_URL}")

        server.start()


def _load_embedding_generator() -> EmbeddingGenerator | None:
    """Load the embedding generator.

    Use MobileCLIP if its dependencies have been installed,
    otherwise return None.
    """
    try:
        from lightly_purple.dataset.mobileclip_embedding_generator import (
            MobileCLIPEmbeddingGenerator,
        )

        print("Using MobileCLIP embedding generator.")
        return MobileCLIPEmbeddingGenerator()
    except ImportError:
        print("Embedding functionality is disabled.")
        return None
