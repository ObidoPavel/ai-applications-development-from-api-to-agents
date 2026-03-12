# Getting API Keys from Open Router

[Open Router](https://openrouter.ai) provides a single API that routes to many models (OpenAI, Anthropic, Google, etc.). You can use one API key instead of managing separate keys per provider.

## Get your Open Router API key

1. Go to **https://openrouter.ai/keys**
2. Sign in (e.g. with Google or GitHub)
3. Click **Create Key**
4. Name the key (e.g. "t1_llm_api") and optionally set a credit limit
5. Copy the key (it starts with `sk-or-v1-...`). Store it securely.

## Use the key in this project

This task uses **each provider’s API directly** (OpenAI, Anthropic, Gemini). You have two options:

### Option A – Use Open Router only for OpenAI-compatible calls

You can use your Open Router key for the **OpenAI** entry points (Chat Completions and Responses) so you can try many models (e.g. GPT, Llama, Mistral) with one key:

1. Set in `.env` (or export in your shell):
   - `OPENAI_API_KEY=<your Open Router key>`
   - `OPENAI_HOST=https://openrouter.ai/api`
2. When running the **OpenAI** apps in this task (`t1_llm_api`), the client uses `t1_llm_api.constants`, which builds the OpenAI base URL from the `OPENAI_HOST` environment variable. So you can use Open Router for those apps without changing any shared code.
3. In the app, you can change the `model_name` to any [Open Router model ID](https://openrouter.ai/docs/features/models) (e.g. `openai/gpt-4o`, `anthropic/claude-3.5-sonnet`, `google/gemini-pro`).

For **Anthropic** and **Gemini** apps, you still need separate keys from [Claude](https://platform.claude.com/settings/keys) and [Google AI Studio](https://aistudio.google.com/app/api-keys), or run those apps only when you have added credits and keys.

### Option B – Use direct provider keys only

Ignore Open Router and set all three in `.env`:

- `OPENAI_API_KEY` – from [OpenAI API keys](https://platform.openai.com/settings/organization/api-keys)
- `ANTHROPIC_API_KEY` – from [Claude API keys](https://platform.claude.com/settings/keys)
- `GEMINI_API_KEY` – from [Google AI Studio](https://aistudio.google.com/app/api-keys)

## Loading `.env` when you run

Python does not load `.env` by default. Do one of the following:

- **Unix/macOS:**  
  `export $(grep -v '^#' .env | xargs)`  
  then run your script from the same shell.

- **PowerShell:**  
  `Get-Content .env | ForEach-Object { if ($_ -match '^([^#][^=]+)=(.*)$') { [Environment]::SetEnvironmentVariable($matches[1].Trim(), $matches[2].Trim(), 'Process') } }`  
  then run your script.

- **Optional:** Install `python-dotenv` and call `load_dotenv()` at the start of the app so variables from `.env` are loaded automatically.
