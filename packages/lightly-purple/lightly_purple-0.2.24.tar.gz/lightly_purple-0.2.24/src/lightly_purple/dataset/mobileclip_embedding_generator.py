"""MobileCLIP embedding generator."""

from __future__ import annotations

import tempfile
from pathlib import Path
from uuid import UUID

import mobileclip  # type: ignore[import-untyped]
import torch
from PIL import Image

from lightly_purple.server.models.embedding_model import EmbeddingModelInput

from . import file_utils
from .embedding_generator import EmbeddingGenerator

MODEL_NAME = "mobileclip_s0"
MOBILECLIP_DOWNLOAD_URL = f"https://docs-assets.developer.apple.com/ml-research/datasets/mobileclip/{MODEL_NAME}.pt"


class MobileCLIPEmbeddingGenerator(EmbeddingGenerator):
    """MobileCLIP embedding model."""

    def __init__(self) -> None:
        """Initialize the MobileCLIP embedding model.

        This method loads the MobileCLIP model and its tokenizer. The model
        checkpoint is downloaded and cached locally for future use.
        """
        model_path = _get_cached_mobileclip_checkpoint()
        self._model, _, self._preprocess = (
            mobileclip.create_model_and_transforms(
                model_name=MODEL_NAME, pretrained=model_path
            )
        )
        self._tokenizer = mobileclip.get_tokenizer(model_name=MODEL_NAME)
        self._model_hash = file_utils.get_file_xxhash(model_path)

    def get_embedding_model_input(
        self, dataset_id: UUID
    ) -> EmbeddingModelInput:
        """Generate an EmbeddingModelInput instance.

        Args:
            dataset_id: The ID of the dataset.

        Returns:
            An EmbeddingModelInput instance with the model details.
        """
        return EmbeddingModelInput(
            name=MODEL_NAME,
            embedding_model_hash=self._model_hash,
            embedding_dimension=512,
            dataset_id=dataset_id,
        )

    def embed_text(self, text: str) -> list[float]:
        """Embed a text with MobileCLIP.

        Args:
            text: The text to embed.

        Returns:
            A list of floats representing the generated embedding.
        """
        tokenized = self._tokenizer([text])
        with torch.no_grad():
            embedding = self._model.encode_text(tokenized)[0]
            # Convert embedding to list of floats.
            embedding_list: list[float] = (
                embedding.cpu().numpy().flatten().tolist()
            )
        return embedding_list

    def embed_images(self, filepaths: list[Path]) -> list[list[float]]:
        """Embed images with MobileCLIP.

        Args:
            filepaths: A list of file paths to the images to embed.

        Returns:
            A list of lists of floats representing the generated embeddings
            in the same order as the input file paths.
        """
        images = [
            self._preprocess(Image.open(filepath).convert("RGB"))
            for filepath in filepaths
        ]
        images_tensor = torch.stack(images)
        with torch.no_grad():
            embeddings = self._model.encode_image(images_tensor)
            # Convert embedding to list of floats.
            embeddings_list: list[list[float]] = (
                embeddings.cpu().numpy().tolist()
            )
        return embeddings_list


def _get_cached_mobileclip_checkpoint() -> Path:
    file_path = Path(tempfile.gettempdir()) / "mobileclip_s0.pt"
    file_utils.download_file_if_does_not_exist(
        url=MOBILECLIP_DOWNLOAD_URL,
        local_filename=file_path,
    )
    return file_path
