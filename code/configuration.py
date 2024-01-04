from pathlib import Path
import yaml
from typing import List


class Configuration:
    def __init__(self, urls: List[str], maximum_depth: int):
        self.urls = urls
        self.maximum_depth = maximum_depth

    def to_dict(self) -> dict[str, list[str] | int]:
        return {"urls": self.urls, "maximum_depth": self.maximum_depth}

    @classmethod
    def from_dict(cls, config_dict: dict[str, list[str] | int]):
        return cls(
            urls=config_dict.get("urls", []),  # type: ignore
            maximum_depth=config_dict.get("maximum_depth", 0),  # type: ignore
        )

    @classmethod
    def random_cfg(cls):
        return cls(urls=["https://www.google.de"], maximum_depth=5)
