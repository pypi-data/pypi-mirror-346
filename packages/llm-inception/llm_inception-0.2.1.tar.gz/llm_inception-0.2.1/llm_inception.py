import click
from httpx_sse import connect_sse, aconnect_sse
import httpx
import json
import llm
from pydantic import Field
from typing import Optional
import sys
try:
    from rich.live import Live
    from rich.text import Text
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False


def fetch_models(key=None):
    key = llm.get_key(key or "", "inception", "LLM_INCEPTION_KEY")
    if not key:
        raise click.ClickException(
            "You must set the 'inception' key or the LLM_INCEPTION_KEY environment variable."
        )
    try:
        response = httpx.get(
            "https://api.inceptionlabs.ai/v1/models",
            headers={"Authorization": f"Bearer {key}"},
            timeout=30,
        )
        response.raise_for_status()
        return response.json()["data"]
    except httpx.HTTPStatusError as e:
        raise click.ClickException(f"Error fetching models: {e.response.text}")


def get_model_details(key=None, force_fetch=False):
    user_dir = llm.user_dir()
    inception_models = user_dir / "inception_models.json"
    if inception_models.exists() and not force_fetch:
        models = json.loads(inception_models.read_text())
    else:
        models = fetch_models(key=key)
        inception_models.write_text(json.dumps(models, indent=2))
    return models


@llm.hookimpl
def register_models(register):
    for model in get_model_details():
        model_id = model["id"]
        our_model_id = "inception/" + model_id
        register(
            InceptionLabs(our_model_id, model_id), AsyncInceptionLabs(our_model_id, model_id)
        )


def get_model_ids(key):
    return [model["id"] for model in get_model_details(key)]


@llm.hookimpl
def register_commands(cli):
    @cli.group()
    def inception():
        "Commands relating to the llm-inception plugin"

    @inception.command()
    @click.option("--key", help="Inception Labs API key")
    def refresh(key):
        "Refresh the list of available Inception Labs models"
        before = set(get_model_ids(key=key))
        get_model_details(key=key, force_fetch=True)
        after = set(get_model_ids(key=key))
        added = after - before
        removed = before - after
        if added:
            click.echo(f"Added models: {', '.join(added)}", err=True)
        if removed:
            click.echo(f"Removed models: {', '.join(removed)}", err=True)
        if added or removed:
            click.echo("New list of models:", err=True)
            for model_id in get_model_ids(key=key):
                click.echo(model_id, err=True)
        else:
            click.echo("No changes", err=True)

    @inception.command()
    @click.option("--key", help="Inception Labs API key")
    def models(key):
        "List available Inception Labs models"
        details = get_model_details(key)
        click.echo(json.dumps(details, indent=2))


class _SharedInceptionLabs:
    can_stream = True
    needs_key = "inception"
    key_env_var = "LLM_INCEPTION_KEY"

    class Options(llm.Options):
        max_tokens: Optional[int] = Field(
            description="The maximum number of tokens to generate in the completion.",
            ge=0,
            default=None,
        )
        no_diffusion: bool = Field(
            description="Set to true to disable diffusing mode (API call and animation). Diffusion is ON by default.",
            default=False,
        )

    def __init__(self, our_model_id, inception_id):
        self.model_id = our_model_id
        self.inception_id = inception_id

    def __str__(self):
        return "Inception Labs: {}".format(self.model_id)

    def build_messages(self, prompt, conversation):
        messages = []
        latest_message = {"role": "user", "content": prompt.prompt}
        if not conversation:
            if prompt.system:
                messages.append({"role": "system", "content": prompt.system})
            messages.append(latest_message)
            return messages

        system_from_conversation = None
        for prev_response in conversation.responses:
            if not prompt.system and prev_response.prompt.system:
                system_from_conversation = prev_response.prompt.system
            messages.append({"role": "user", "content": prev_response.prompt.prompt})
            messages.append({"role": "assistant", "content": prev_response.text()})

        if system_from_conversation:
            messages = [{"role": "system", "content": prompt.system}] + messages

        messages.append(latest_message)
        return messages

    def build_request_body(self, prompt, conversation):
        messages = self.build_messages(prompt, conversation)
        body = {
            "model": self.inception_id,
            "messages": messages,
            "diffusing": not prompt.options.no_diffusion,
        }
        if prompt.options.max_tokens:
            body["max_tokens"] = prompt.options.max_tokens
        return body

    def set_usage(self, response, usage):
        if usage:
            response.set_usage(
                input=usage["prompt_tokens"],
                output=usage["completion_tokens"],
            )


class InceptionLabs(_SharedInceptionLabs, llm.KeyModel):
    def execute(self, prompt, stream, response, conversation, key=None):
        messages = self.build_messages(prompt, conversation)
        response._prompt_json = {"messages": messages}
        body_params = self.build_request_body(prompt, conversation)

        if stream:
            body_params["stream"] = True

        should_run_rich_animation = stream and (not prompt.options.no_diffusion) and RICH_AVAILABLE and sys.stdout.isatty()

        if should_run_rich_animation:
            live_display_text = Text()
            last_sse_data = None
            displayed_final_content = False
            
            with Live(live_display_text, refresh_per_second=10, transient=False) as live:
                try:
                    with httpx.Client() as client:
                        with connect_sse(
                            client, "POST", "https://api.inceptionlabs.ai/v1/chat/completions",
                            headers={"Content-Type": "application/json", "Accept": "application/json", "Authorization": f"Bearer {key}"},
                            json=body_params,
                            timeout=None
                        ) as event_source:
                            for sse in event_source.iter_sse():
                                if not last_sse_data and event_source.response.is_error:
                                    error_body_preview = b""
                                    try: error_body_preview = event_source.response.read()
                                    except Exception: pass
                                    error_text = error_body_preview.decode(errors='replace')[:500] if error_body_preview else event_source.response.reason_phrase
                                    live.stop()
                                    raise llm.ModelError(f"API Error: {event_source.response.status_code} - {error_text}")
                                event_source.response.raise_for_status()

                                if sse.event == "error":
                                    live.stop()
                                    raise llm.ModelError(f"API SSE Error: {sse.data}")
                                if sse.data == "[DONE]":
                                    break
                                
                                try:
                                    data = sse.json()
                                    last_sse_data = data 
                                except json.JSONDecodeError:
                                    continue

                                if data.get("choices") and data["choices"][0].get("delta") and "content" in data["choices"][0]["delta"]:
                                    content_chunk = data["choices"][0]["delta"]["content"]
                                    live_display_text.plain = content_chunk

                                    if data.get("diffusion_meta", {}).get("diffusion_progress", 0.0) >= 1.0:
                                        live_display_text.plain = content_chunk 
                                        displayed_final_content = True
                                
                except httpx.HTTPStatusError as e:
                    live.stop()
                    error_detail = e.response.text if e.response and hasattr(e.response, 'text') and not e.response.is_stream_consumed else e.response.reason_phrase if e.response else "Unknown"
                    if e.response and not e.response.is_stream_consumed:
                         try: e.response.read(); error_detail = e.response.text
                         except Exception: pass 
                    raise llm.ModelError(f"API HTTP Error: {e.request.method} {e.request.url} - Status {e.response.status_code} - {error_detail}")
                except Exception as e: 
                    live.stop()
                    raise llm.ModelError(f"Error during streaming: {str(e)}")
            
            if live_display_text.plain.strip() or displayed_final_content:
                yield ""
            
            if last_sse_data: 
                usage_info = last_sse_data.pop("usage", None)
                if 'choices' in last_sse_data and isinstance(last_sse_data['choices'], list) and len(last_sse_data['choices']) > 0:
                    choice = last_sse_data['choices'][0]
                    if 'delta' in choice: del choice['delta']
                    if 'message' in choice and choice.get('message', {}).get('content'):
                        pass
                    elif not choice:
                        del last_sse_data['choices'][0]
                if 'choices' in last_sse_data and not last_sse_data['choices']:
                    del last_sse_data['choices']
                
                self.set_usage(response, usage_info)
                response.response_json = last_sse_data

        elif stream: 
            final_content_parts = []
            last_sse_data = None
            try:
                with httpx.Client() as client:
                    with connect_sse(
                        client, "POST", "https://api.inceptionlabs.ai/v1/chat/completions",
                        headers={"Content-Type": "application/json", "Accept": "application/json", "Authorization": f"Bearer {key}"},
                        json=body_params, 
                        timeout=None
                    ) as event_source:
                        for sse in event_source.iter_sse():
                            if not last_sse_data and event_source.response.is_error:
                                error_body_preview = b""
                                try:
                                    error_body_preview = event_source.response.read()
                                except Exception:
                                    pass
                                error_text = error_body_preview.decode(errors='replace')[:500] if error_body_preview else event_source.response.reason_phrase
                                raise llm.ModelError(f"API Error: {event_source.response.status_code} - {error_text}")
                            event_source.response.raise_for_status()

                            if sse.event == "error":
                                raise llm.ModelError(f"API SSE Error: {sse.data}")
                            if sse.data == "[DONE]":
                                break
                            
                            try:
                                data = sse.json()
                                last_sse_data = data
                            except json.JSONDecodeError:
                                continue

                            if data.get("choices") and data["choices"][0].get("delta") and "content" in data["choices"][0]["delta"]:
                                content_chunk = data["choices"][0]["delta"]["content"]
                                final_content_parts.append(content_chunk)
                                yield content_chunk
            except httpx.HTTPStatusError as e:
                error_detail = e.response.text if e.response and hasattr(e.response, 'text') and not e.response.is_stream_consumed else e.response.reason_phrase if e.response else "Unknown HTTP error"
                if e.response and not e.response.is_stream_consumed:
                     try:
                        e.response.read()
                        error_detail = e.response.text
                     except Exception:
                        pass
                raise llm.ModelError(f"API HTTP Error: {e.request.method} {e.request.url} - Status {e.response.status_code} - {error_detail}")
            except Exception as e:
                 raise llm.ModelError(f"Error during streaming: {str(e)}")

            if last_sse_data: 
                usage_info = last_sse_data.pop("usage", None)
                last_sse_data.pop("choices", None)
                self.set_usage(response, usage_info)
                response.response_json = last_sse_data
        
        else:
            with httpx.Client() as client:
                api_response = client.post(
                    "https://api.inceptionlabs.ai/v1/chat/completions",
                    headers={
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                        "Authorization": f"Bearer {key}",
                    },
                    json=body_params, 
                    timeout=None,
                )
                try:
                    api_response.raise_for_status()
                except httpx.HTTPStatusError as e:
                    raise llm.ModelError(f"API HTTP Error (non-stream): {e.request.method} {e.request.url} - Status {e.response.status_code} - {e.response.text}")

                response_json = api_response.json()
                yield response_json["choices"][0]["message"]["content"]
                self.set_usage(response, response_json.pop("usage", None))
                response.response_json = response_json


class AsyncInceptionLabs(_SharedInceptionLabs, llm.AsyncKeyModel):
    async def execute(self, prompt, stream, response, conversation, key=None):
        messages = self.build_messages(prompt, conversation)
        response._prompt_json = {"messages": messages}
        body_params = self.build_request_body(prompt, conversation)

        if stream:
            body_params["stream"] = True

        if stream:
            final_content_parts = []
            last_sse_data = None
            try:
                async with httpx.AsyncClient() as client:
                    async with aconnect_sse(
                            client, "POST", "https://api.inceptionlabs.ai/v1/chat/completions",
                            headers={"Content-Type": "application/json", "Accept": "application/json", "Authorization": f"Bearer {key}"},
                            json=body_params, 
                            timeout=None
                    ) as event_source:
                        async for sse in event_source.aiter_sse():
                            if not last_sse_data and event_source.response.is_error:
                                error_body_preview = b""
                                try:
                                    error_body_preview = await event_source.response.aread()
                                except Exception:
                                    pass
                                error_text = error_body_preview.decode(errors='replace')[:500] if error_body_preview else event_source.response.reason_phrase
                                raise llm.ModelError(f"API Error: {event_source.response.status_code} - {error_text}")
                            event_source.response.raise_for_status()

                            if sse.event == "error":
                                raise llm.ModelError(f"API SSE Error: {sse.data}")
                            if sse.data == "[DONE]":
                                break
                            
                            try:
                                data = sse.json()
                                last_sse_data = data
                            except json.JSONDecodeError:
                                continue

                            if data.get("choices") and data["choices"][0].get("delta") and "content" in data["choices"][0]["delta"]:
                                content_chunk = data["choices"][0]["delta"]["content"]
                                final_content_parts.append(content_chunk)
                                yield content_chunk
            except httpx.HTTPStatusError as e:
                error_detail = e.response.reason_phrase if e.response else "Unknown HTTP error"
                if e.response and not e.response.is_stream_consumed:
                    try:
                        await e.response.aread() 
                        error_detail = e.response.text
                    except Exception:
                        pass 
                raise llm.ModelError(f"API HTTP Error: {e.request.method} {e.request.url} - Status {e.response.status_code} - {error_detail}")

            except Exception as e:
                raise llm.ModelError(f"Error during async streaming: {str(e)}")

            if last_sse_data: 
                usage_info = last_sse_data.pop("usage", None)
                last_sse_data.pop("choices", None)
                self.set_usage(response, usage_info)
                response.response_json = last_sse_data
        else:
            async with httpx.AsyncClient() as client:
                api_response = await client.post(
                    "https://api.inceptionlabs.ai/v1/chat/completions",
                    headers={
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                        "Authorization": f"Bearer {key}",
                    },
                    json=body_params,
                    timeout=None,
                )
                try:
                    api_response.raise_for_status()
                except httpx.HTTPStatusError as e:
                    raise llm.ModelError(f"API HTTP Error (async non-stream): {e.request.method} {e.request.url} - Status {e.response.status_code} - {e.response.text}")

                response_json = api_response.json()
                yield response_json["choices"][0]["message"]["content"]
                self.set_usage(response, response_json.pop("usage", None))
                response.response_json = response_json