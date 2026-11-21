"""Monkey patch for LangChain OpenAI client to preserve Google Gemini thought signatures.

Resolves Google AI Studio 400 BadRequestError:
"Function call is missing a thought_signature in functionCall parts".
Preserves `extra_content` on `AIMessage.tool_calls` across multi-turn reasoning loops.
"""

from langchain_openai.chat_models import base as _lc_openai_base

_orig_convert = _lc_openai_base._convert_dict_to_message
_orig_serialize = _lc_openai_base._lc_tool_call_to_openai_tool_call


def _patched_convert(_dict):
    msg = _orig_convert(_dict)
    raw_calls = _dict.get("tool_calls") or []
    for i, raw in enumerate(raw_calls):
        if "extra_content" in raw and i < len(msg.tool_calls):
            msg.tool_calls[i]["extra_content"] = raw["extra_content"]
    return msg


def _patched_serialize(tool_call):
    d = _orig_serialize(tool_call)
    if "extra_content" in tool_call:
        d["extra_content"] = tool_call["extra_content"]
    return d


def apply_patch():
    """Applies the thought signature preservation patch to LangChain."""
    _lc_openai_base._convert_dict_to_message = _patched_convert
    _lc_openai_base._lc_tool_call_to_openai_tool_call = _patched_serialize
    print("Google Gemini thought_signature patch successfully applied to LangChain!")
