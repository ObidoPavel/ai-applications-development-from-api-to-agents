"""
Task-specific configuration for t1_llm_api.

Re-exports commons.constants and overrides OpenAI endpoints so this task can use
Open Router by setting OPENAI_HOST=https://openrouter.ai/api in the environment.
"""

import os

from commons import constants as _commons

OPENAI_HOST = os.getenv("OPENAI_HOST", "https://api.openai.com")
OPENAI_CHAT_COMPLETIONS_ENDPOINT = f"{OPENAI_HOST}/v1/chat/completions"
OPENAI_RESPONSES_ENDPOINT = f"{OPENAI_HOST}/v1/responses"

OPENAI_API_KEY = _commons.OPENAI_API_KEY
DEFAULT_SYSTEM_PROMPT = _commons.DEFAULT_SYSTEM_PROMPT
ANTHROPIC_ENDPOINT = _commons.ANTHROPIC_ENDPOINT
ANTHROPIC_API_KEY = _commons.ANTHROPIC_API_KEY
GEMINI_ENDPOINT = _commons.GEMINI_ENDPOINT
GEMINI_API_KEY = _commons.GEMINI_API_KEY
