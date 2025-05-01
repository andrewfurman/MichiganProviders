"""
upload_provider/markdown_to_individual_provider_gpt.py
──────────────────────────────────────────────────────
Single-branch flow: markdown ➜ GPT tool-call ➜ DB update.

DEBUG_GPT=1  → verbose logs.
"""

from __future__ import annotations

import json
import logging
import os
from typing import Any, Mapping

from flask import current_app
from openai import OpenAI, pydantic_function_tool
from pydantic import BaseModel, Field, ValidationError
from sqlalchemy.exc import SQLAlchemyError

from models.provider import IndividualProvider
from models.provider_audit import ProviderAudit
from models.db import db

DEBUG = bool(int(os.getenv("DEBUG_GPT", "0")))
client = OpenAI()

# ── Pydantic schema (provider_id *not* included) ─────────────────
class ProviderUpdateIn(BaseModel):
    npi: str
    first_name: str
    last_name: str
    gender: str | None = None
    phone: str | None = None
    provider_type: str | None = None
    accepting_new_patients: bool
    specialties: str | None = None
    board_certifications: str | None = None
    languages: str | None = None
    address_line: str | None = None
    city: str | None = None
    state: str | None = None
    zip: str | None = None


# Build function schema with strict mode
_base_tool = pydantic_function_tool(ProviderUpdateIn)
provider_update_tool = {
    **_base_tool,
    "function": {**_base_tool["function"], "name": "provider_update", "strict": True},
}


def _save_provider(
    provider: IndividualProvider,
    updates: Mapping[str, Any],
    *,
    user_id: int | None,
    logger: logging.Logger,
) -> None:
    audits = []
    for fld, new in updates.items():
        old = getattr(provider, fld)
        if str(old) != str(new):
            setattr(provider, fld, new)
            audits.append(
                ProviderAudit(
                    provider_id=provider.provider_id,
                    field_updated=fld,
                    old_value=str(old) if old is not None else None,
                    new_value=str(new) if new is not None else None,
                    change_description=f"Updated {fld}",
                    user_id=user_id,
                )
            )

    if audits:
        db.session.add_all(audits)
    db.session.commit()
    logger.info("✓ Provider %s saved (%d fields)", provider.provider_id, len(audits))


def markdown_to_individual_provider_gpt(provider_id: int) -> bool:
    """Run GPT once; expect a strict provider_update tool-call."""
    log = current_app.logger

    provider: IndividualProvider | None = db.session.get(IndividualProvider, provider_id)
    if not provider:
        log.error("✖ Provider %s not found", provider_id)
        return False

    md_text = provider.provider_enrollment_form_markdown_text
    if not md_text:
        log.error("✖ No markdown for provider %s", provider_id)
        return False

    messages = [
        {
            "role": "system",
            "content": (
                "Extract provider information from the markdown. "
                "Call the function `provider_update` **without** the field "
                "`provider_id`; the caller will supply it. "
                "Return booleans as true/false. Use null when data is missing."
            ),
        },
        {"role": "user", "content": md_text},
    ]

    try:
        # Log the request
        log.info("Making GPT API request:")
        log.info("Model: gpt-4.1-mini")
        log.info("Messages: %s", json.dumps(messages, indent=2))
        log.info("Tools: %s", json.dumps([provider_update_tool], indent=2))

        completion = client.chat.completions.create(
            model="gpt-4.1-mini",            # supports function calling
            messages=messages,
            tools=[provider_update_tool],
            tool_choice="auto",
            parallel_tool_calls=False,
        )

        # Log the response
        log.info("GPT API response:")
        log.info("Response: %s", completion.model_dump_json(indent=2))
    except Exception:
        log.exception("✖ OpenAI call failed (provider %s)", provider_id)
        return False

    msg = completion.choices[0].message
    if DEBUG:
        log.info("[GPT] full assistant msg:\n%s", msg.model_dump_json(indent=2)[:2000])

    if not msg.tool_calls:
        log.error("✖ No tool call returned (provider %s)", provider_id)
        return False

    call = msg.tool_calls[0]
    if DEBUG:
        log.info("[GPT] raw args: %s", call.function.arguments)

    # Inject provider_id then validate
    try:
        payload = json.loads(call.function.arguments)
        payload["provider_id"] = provider_id
        extracted = ProviderUpdateIn.model_validate(payload)
    except (json.JSONDecodeError, ValidationError) as e:
        log.error("✖ Validation failed: %s", e)
        return False

    try:
        _save_provider(
            provider,
            updates=extracted.model_dump(),
            user_id=None,
            logger=log,
        )
        return True
    except SQLAlchemyError:
        log.exception("✖ DB error while saving provider %s", provider_id)
        db.session.rollback()
        return False
