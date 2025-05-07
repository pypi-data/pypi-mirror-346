# llm-inception

[![PyPI](https://img.shields.io/pypi/v/llm-inception.svg)](https://pypi.org/project/llm-inception/)
[![Changelog](https://img.shields.io/github/v/release/ghostofpokemon/llm-inception?include_prereleases&label=changelog)](https://github.com/ghostofpokemon/llm-inception/releases)
[![Tests](https://github.com/ghostofpokemon/llm-inception/actions/workflows/test.yml/badge.svg)](https://github.com/ghostofpokemon/llm-inception/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/ghostofpokemon/llm-inception/blob/main/LICENSE)

Run prompts against LLMs hosted by [Inception Labs](https://inceptionlabs.ai/) with support for their unique diffusing animation feature.

## Installation

Install this plugin in the same environment as [LLM](https://llm.datasette.io/).
```bash
llm install llm-inception
```
This plugin uses [Rich](https://rich.readthedocs.io/) to display diffusing animations.

## Usage

First, obtain an API key for Inception Labs and set it using the `llm` command-line tool:

```bash
llm keys set inception
# Paste your INCEPTION_API_KEY here
```
Alternatively, the plugin will use the `LLM_INCEPTION_KEY` environment variable if set.

### Available Models

To see a list of available Inception Labs models that `llm` can use, run:
```bash
llm models list
```
The list of models is fetched from the API and cached. You can refresh this cache by running:
```bash
llm inception refresh
```
To see the detailed JSON information for all cached Inception Labs models:
```bash
llm inception models
```

### Running Prompts

Run prompts against Inception Labs models like this:
```bash
llm -m inception/mercury-coder-small "Tell me a short story about a brave avocado."
```

### Diffusing Animation

This plugin supports Inception Labs' "diffusing" feature, which shows an animation as the model generates its response. This is enabled by default when using the plugin in an interactive terminal.

**Example:**
```bash
llm chat -m inception/mercury-coder-small
> Write a haiku about a robot falling in love.
(Animation will play here)
Whispering wind chills,
Leaves dance under moonlit sky,
Night's soft embrace holds.
>
```

You can control this feature using the `-o no_diffusion true` option (note the underscore):
```bash
llm -m inception/mercury-coder-small "Why is the sky blue?" -o no_diffusion true
```

Other model options like `max_tokens` can also be set:
```bash
llm -m inception/mercury-coder-small "Explain quantum entanglement simply." -o max_tokens 150
```

## Development

To set up this plugin locally, first check out the code. Then create a new virtual environment:
```bash
cd llm-inception
python -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
pip install -e '.[test]'
```
To run the tests (you'll need to create some!):
```bash
pytest
```

<!-- Optional: If you set up API key for tests
To run tests that might interact with the live API (use with caution or mock appropriately):
Set your API key as an environment variable:
export LLM_INCEPTION_KEY="your_actual_api_key"
Then run pytest.
-->
