import sys
import click
import json
import yaml
from typing import TypedDict
import os
from pydantic import BaseModel, Field


class LanggraphConfig(BaseModel):
    """graph.yaml 파일의 구조를 정의합니다."""

    package_directory: str = Field(
        description="Root Directory of your package(module)."
    )
    graph_path: str = Field(
        description="Path to the langgraph module.",
        examples=["./react_agent/graph.py:graph"],
    )
    env_file: str | None = None
    requirements_file: str | None = None


def validate_graph_yaml(graph_yaml: str) -> LanggraphConfig:
    with open(graph_yaml, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    try:
        return LanggraphConfig.model_validate(config)
    except Exception as e:
        raise click.UsageError(
            f"Invalid graph.yaml. {graph_yaml} 파일을 확인해주세요. : {e}"
        )
