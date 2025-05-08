"""Example of how to use the DatasetLoader class."""

import math
import os

from lightly_purple import DatasetLoader
from lightly_purple.server.models.tag import TagInput

# Create a DatasetLoader instance
loader = DatasetLoader()

# Define the path to the dataset (folder containing data.yaml)
dataset_path = os.getenv("DATASET_PATH", "/path/to/your/yolo/dataset/data.yaml")

# Load YOLO dataset using data.yaml path
loader.from_yolo(
    dataset_path,
    input_split=os.getenv("PURPLE_DATASET_SPLIT", "test"),
)

# Define the reviewers
# This should be a comma-separated list of reviewers
# we will then create a tag for each reviewer and assign them samples
# to work on.
reviewers = os.getenv("DATASET_REVIEWERS", "Alice, Bob, Charlie, David")

# Get the first dataset from the list of datasets
datasets = loader.dataset_resolver.get_all()
latest_dataset = datasets[0] if datasets else None
if not latest_dataset:
    raise ValueError("No dataset found")
dataset_id = latest_dataset.dataset_id

# Get all samples from the db
samples = loader.sample_resolver.get_all_by_dataset_id(
    dataset_id=dataset_id,
    limit=-1,
)

# Create a tag for each reviewer to work on
tags = []
for reviewer in reviewers.split(","):
    tags.append(
        loader.tag_resolver.create(
            TagInput(
                dataset_id=dataset_id,
                name=f"""{reviewer.strip()} tasks""",
                kind="sample",
            )
        )
    )

# Chunk the samples into portions equally divided among the reviewers.
chunk_size = math.ceil(len(samples) / len(tags))
for i, tag in enumerate(tags):
    # allocate all samples for this tag
    sample_ids = [
        sample.sample_id
        for sample in samples[i * chunk_size : (i + 1) * chunk_size]
    ]

    # Add sample_ids to the tag
    loader.tag_resolver.add_sample_ids_to_tag_id(
        tag_id=tag.tag_id,
        sample_ids=sample_ids,
    )


# Launch the server to load data
loader.launch()
