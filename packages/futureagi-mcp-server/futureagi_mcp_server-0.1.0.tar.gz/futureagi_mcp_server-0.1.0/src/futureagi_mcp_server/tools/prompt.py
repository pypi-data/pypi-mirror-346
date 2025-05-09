import os
import json

from fi.api.auth import APIKeyAuth
from fi.api.types import HttpMethod, RequestConfig

from ..logger import get_logger
from .routes import Routes

logger = get_logger()

LIST_OF_PROMPTS_DESCRIPTION = """
    Get the list of prompts from the database

    Args:
        None

    Returns:
        list: A list of prompts
"""


def get_list_of_prompts():
    """
    Get the list of prompts from the database
    """
    request_handler = APIKeyAuth()

    request_config = RequestConfig(
        method=HttpMethod.GET,
        url=Routes.PROMPT_EXECUTIONS.value,
        auth=request_handler,
    )

    response = request_handler.request(request_config)
    
    if response.status_code == 200:
        return response.json()
    else:
        logger.error(f"Failed to get list of prompts: {response.status_code}")
        return {"error": "Failed to get list of prompts"}
    

def generate_prompt(requirements: str):
    """
    Generate a prompt based on the requirements
    """
    request_handler = APIKeyAuth()

    request_config = RequestConfig(
        method=HttpMethod.POST,
        url=Routes.PROMPT_GENERATE.value,
        auth=request_handler,
        data={"statement": requirements},
    )

    response = request_handler.request(request_config)

    if response.status_code == 200:
        return response.json()
    else:
        logger.error(f"Failed to generate prompt: {response.status_code}")
        return {"error": "Failed to generate prompt"}
    

def improve_prompt(existing_prompt: str, improvements: str):
    """
    Improve a prompt based on the feedback
    """
    request_handler = APIKeyAuth()

    request_config = RequestConfig(
        method=HttpMethod.POST,
        url=Routes.PROMPT_IMPROVE.value,
        auth=request_handler,
        data={"existing_prompt": existing_prompt, "improvement_requirements": improvements},
    )

    response = request_handler.request(request_config)

    if response.status_code == 200:
        return response.json()
    else:
        logger.error(f"Failed to improve prompt: {response.status_code}")
        return {"error": "Failed to improve prompt"}
