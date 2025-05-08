<div align="center">
<p align="center">

<!-- prettier-ignore -->
<img src="https://cdn.prod.website-files.com/62cd5ce03261cba217188442/66dac501a8e9a90495970876_Logo%20dark-short-p-800.png" height="50px">

**The open-source tool curating datasets**

---

[![PyPI python](https://img.shields.io/pypi/pyversions/lightly-purple)](https://pypi.org/project/lightly-purple)
[![PyPI version](https://badge.fury.io/py/lightly-purple.svg)](https://pypi.org/project/lightly-purple)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

</p>
</div>

# 🚀 Aloha!

We at **[Lightly](https://lightly.ai)** created **Lightly Purple**, an open-source tool designed to supercharge your data curation workflows for computer vision datasets. Explore your data, visualize annotations and crops, tag samples, and export curated lists to improve your machine learning pipelines.

Lightly Purple runs entirely locally on your machine, keeping your data private. It consists of a Python library for indexing your data and a web-based UI for visualization and curation.

## ✨ Core Workflow

Using Lightly Purple typically involves these steps:

1.  **Index Your Dataset:** Run a Python script using the `lightly-purple` library to process your local dataset (images and annotations) and save metadata into a local `purple.db` file.
2.  **Launch the UI:** The script then starts a local web server.
3.  **Explore & Curate:** Use the UI to visualize images, annotations, and object crops. Filter and search your data (experimental text search available). Apply tags to interesting samples (e.g., "mislabeled", "review").
4.  **Export Curated Data:** Export information (like filenames) for your tagged samples from the UI to use downstream.
5.  **Stop the Server:** Close the terminal running the script (Ctrl+C) when done.

<p align="center">
  <img alt="Lightly Purple Sample Grid View" src="https://storage.googleapis.com/lightly-public/purple/screenshot_grid_view.jpg" width="70%">
  <br/>
  <em>Visualize your dataset samples with annotations in the grid view.</em>
</p>
<p align="center">
  <img alt="Lightly Purple Annotation Crop View" src="https://storage.googleapis.com/lightly-public/purple/screenshot_annotation_view.jpg" width="70%">
  <br/>
  <em>Switch to the annotation view to inspect individual object crops easily.</em>
</p>
<p align="center">
  <img alt="Lightly Purple Sample Detail View" src="https://storage.googleapis.com/lightly-public/purple/screenshot_detail_view.jpg" width="70%">
  <br/>
  <em>Inspect individual samples in detail, viewing all annotations and metadata.</em>
</p>

## 💻 Installation

Ensure you have **Python 3.8 or higher**. We strongly recommend using a virtual environment.

The library is OS-independent and works on Windows, Linux, and macOS.

```shell
# 1. Create and activate a virtual environment (Recommended)
# On Linux/macOS:
python3 -m venv venv
source venv/bin/activate

# On Windows:
python -m venv venv
.\venv\Scripts\activate

# 2. Install Lightly Purple
pip install lightly-purple

# 3. Verify installation (Optional)
pip show lightly-purple
```

## **Quickstart**

Download the dataset and run a quickstart script to load your dataset and launch the app.

### YOLO Object Detection

To run an example using a yolo dataset, clone the example repository and run the example script:

```shell
git clone https://github.com/lightly-ai/datasets_examples_purple dataset_examples_purple
python dataset_examples_purple/road_signs_yolo/example_yolo.py
```

<details>
<summary>The YOLO format details:</summary>

```
road_signs_yolo/
├── train/
│   ├── images/
│   │   ├── image1.jpg
│   │   ├── image2.jpg
│   │   └── ...
│   └── labels/
│       ├── image1.txt
│       ├── image2.txt
│       └── ...
├── valid/  (optional)
│   ├── images/
│   │   └── ...
│   └── labels/
│       └── ...
└── data.yaml
```

Each label file should contain YOLO format annotations (one per line):

```
<class> <x_center> <y_center> <width> <height>
```

Where coordinates are normalized between 0 and 1.

</details>


<details>
<summary>Let's break down the `example_yolo.py` script to explore the dataset:</summary>

```python
# We import the DatasetLoader class from the lightly_purple module
from lightly_purple import DatasetLoader
from pathlib import Path

# Create a DatasetLoader instance
loader = DatasetLoader()

data_yaml_path = Path(__file__).resolve().parent / "data.yaml"
loader.from_yolo(
    data_yaml_path=str(data_yaml_path),
    input_split="test",
)

# We start the UI application on port 8001
loader.launch()
```
</details>

</details>

### COCO Instance Segmentation

To run an instance segmentation example using a COCO dataset, clone the example repository and run the example script:

```shell
git clone https://github.com/lightly-ai/datasets_examples_purple dataset_examples_purple
python dataset_examples_purple/coco_subset_128_images/example_coco.py
```

<details>
<summary>The COCO format details:</summary>

```
coco_subset_128_images/
├── images/
│   ├── image1.jpg
│   ├── image2.jpg
│   └── ...
└── instances_train2017.json        # Single JSON file containing all annotations
```

COCO uses a single JSON file containing all annotations. The format consists of three main components:

- Images: Defines metadata for each image in the dataset.
- Categories: Defines the object classes.
- Annotations: Defines object instances.

</details>

<details>
<summary>Let's break down the `example_coco.py` script to explore the dataset:</summary>

```python
# We import the DatasetLoader class from the lightly_purple module
from lightly_purple import DatasetLoader
from pathlib import Path

# Create a DatasetLoader instance
loader = DatasetLoader()

current_dir = Path(__file__).resolve().parent
loader.from_coco_instance_segmentations(
    annotations_json_path=str(current_dir / "instances_train2017.json"),
    input_images_folder=str(current_dir / "images"),
)

# We start the UI application on port 8001
loader.launch()

```
</details>

</details>

## 🔍 How It Works

1.  Your **Python script** uses the `lightly-purple` **Dataset Loader**.
2.  The Loader reads your images and annotations, calculates embeddings, and saves metadata to a local **`purple.db`** file (using DuckDB).
3.  `loader.launch()` starts a **local Backend API** server.
4.  This server reads from `purple.db` and serves data to the **UI Application** running in your browser (`http://localhost:8001`).
5.  Images are streamed directly from your disk for display in the UI.

## 📦 Supported Dataset Formats & Annotations

The `DatasetLoader` currently supports:

- **YOLOv8 Object Detection:** Reads `.yaml` file. Supports bounding boxes ✅.
- **COCO Object Detection:** Reads `.json` annotations. Supports bounding boxes ✅.
- **COCO Instance Segmentation:** Reads `.json` annotations. Supports instance masks in RLE (Run-Length Encoding) format ✅.

**Limitations:**

- Requires datasets _with_ annotations. Cannot index image folders alone ❌.
- No direct support for classification datasets yet ❌.
- Cannot add custom metadata during the loading step ❌.

## 📚 **FAQ**

### Are the datasets persistent?

Yes, the information about datasets is persistent and stored in the db file. You can see it after the dataset is processed.
If you rerun the loader it will create a new dataset representing the same dataset, keeping the previous dataset information untouched.

### Can I change the database path?

Not yet. The database is stored in the working directory by default.

### Can I launch in another Python script or do I have to do it in the same script?

It is possible to use only one script at the same time because we lock the db file for the duration of the script.

### Can I change the API backend port?

Currently, the API always runs on port 8001, and this cannot be changed yet.

### Can I process datasets that do not have annotations?

No, we support only datasets with annotations now.

### What dataset annotations are supported?

Bounding boxes are supported ✅

Instance segmentation is supported ✅

Custom metadata is NOT yet supported ❌
