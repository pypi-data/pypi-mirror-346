from __future__ import annotations

import os
from functools import cache

from agents import ModelSettings
from agents import OpenAIChatCompletionsModel
from loguru import logger
from openai import AsyncAzureOpenAI
from openai import AsyncOpenAI


@cache
def get_openai_client() -> AsyncOpenAI:
    # OpenAI-compatible endpoints
    openai_proxy_api_key = os.getenv("OPENAI_PROXY_API_KEY")
    openai_proxy_base_url = os.getenv("OPENAI_PROXY_BASE_URL")
    if openai_proxy_api_key:
        logger.info("Using OpenAI proxy API key")
        return AsyncOpenAI(base_url=openai_proxy_base_url, api_key=openai_proxy_api_key)

    # Azure OpenAI-comatible endpoints
    azure_api_key = os.getenv("AZURE_OPENAI_API_KEY")
    if azure_api_key:
        logger.info("Using Azure OpenAI API key")
        return AsyncAzureOpenAI(api_key=azure_api_key)

    logger.info("Using OpenAI API key")
    return AsyncOpenAI()


@cache
def get_openai_model() -> OpenAIChatCompletionsModel:
    model_name = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    client = get_openai_client()
    return OpenAIChatCompletionsModel(model_name, openai_client=client)


@cache
def get_openai_model_settings():
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    temperature = None if model == "o3-mini" else float(os.getenv("OPENAI_TEMPERATURE", 0.0))
    return ModelSettings(temperature=temperature)
