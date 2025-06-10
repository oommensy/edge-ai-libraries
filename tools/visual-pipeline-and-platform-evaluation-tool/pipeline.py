import math
from pathlib import Path
from typing import List
import os
import yaml
import importlib


class GstPipeline:
    def __init__(self):
        pass

    def pipeline(self) -> str:
        if not hasattr(self, "_pipeline"):
            raise ValueError("Pipeline is not defined")

        return self._pipeline

    def evaluate(
        self,
        constants: dict,
        parameters: dict,
        regular_channels: int,
        inference_channels,
    ) -> str:
        raise NotImplementedError(
            "The evaluate method must be implemented by subclasses"
        )

    def diagram(self) -> Path:
        if not hasattr(self, "_diagram"):
            raise ValueError("Diagram is not defined")

        return self._diagram

    def bounding_boxes(self) -> List:
        if not hasattr(self, "_bounding_boxes"):
            raise ValueError("Bounding Boxes is not defined")

        return self._bounding_boxes
    
class PipelineLoader:
    @staticmethod
    def list():
        """Return available pipeline folder names (not display names)."""
        pipelines_dir = Path("pipelines")
        return [
            name for name in pipelines_dir.iterdir()
            if name.is_dir() and not name.name.startswith("_")
        ]
    @staticmethod
    def config(pipeline_name: str) -> dict:
        """Return full config dict for a pipeline."""
        config_path = Path("pipelines") / pipeline_name / "config.yaml"
        if not config_path.exists():
            raise FileNotFoundError(f"{config_path} not found")
        return yaml.safe_load(config_path.read_text()) #TODO - validate it has description etc.
    @staticmethod
    def load(pipeline_name: str, metadata_only: bool = False):
        """Load pipeline class and config, or just metadata.name"""
        config = PipelineLoader.config(pipeline_name)
        if metadata_only:
            return config.get("metadata", {}).get("name", pipeline_name)
        #class_name = "".join(word.capitalize() for word in pipeline_name.split("_")) + "Pipeline"
        class_name = config.get("metadata", {}).get("class")
        if not class_name:
            raise ValueError(f"Pipeline {pipeline_name} does not have a class defined in config.yaml")
        module = importlib.import_module(f"pipelines.{pipeline_name}.pipeline")
        pipeline_cls = getattr(module, class_name)
        return pipeline_cls(), config