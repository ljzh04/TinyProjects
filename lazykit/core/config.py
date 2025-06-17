"""Handles global/user config, paths"""
import json

DEFAULT_CONFIG = {
    "default_license": "MIT",
    "llm_provider": "openai",
    "llm_model": "gpt-4",
}


def write_default_config(path: str):
    with open(path, "w") as f:
        json.dump(DEFAULT_CONFIG, f, indent=2)
