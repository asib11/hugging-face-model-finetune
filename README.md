# FastAPI Hugging Face

A FastAPI service for running local Hugging Face language and speech models.
The application loads Gemma 3 1B Instruct and Llama 3.2 3B Instruct for text
generation, plus OpenAI Whisper Small for speech-to-text transcription.

## What It Does

- Loads the downloaded Gemma and Llama models with Transformers.
- Loads the downloaded Whisper Small model for automatic speech recognition.
- Applies each model's chat template to incoming prompts.
- Generates up to 128 new tokens per request.
- Downloads audio from a supplied URL and transcribes it with Whisper.
- Returns generated text or transcriptions as JSON.

Models are loaded when the application starts, so startup can take time and
requires enough CPU/GPU memory for the selected models.

## Requirements

- Python 3.14 or newer
- `uv`
- Hugging Face access to the gated model repositories
- Enough disk space for the model weights
- A CUDA-capable GPU is recommended, but Transformers can use CPU if needed

## Setup

Clone the repository and enter the project directory:

```bash
git clone <repository-url>
cd fastapi-hugging-face
```

Create the virtual environment and install dependencies:

```bash
uv sync
```

Log in to Hugging Face:

```bash
uv run hf auth login
```

Before downloading a gated model, accept its license and access terms while
logged in to the same Hugging Face account:

- [Google Gemma 3 1B Instruct](https://huggingface.co/google/gemma-3-1b-it)
- [Meta Llama 3.2 3B Instruct](https://huggingface.co/meta-llama/Llama-3.2-3B-Instruct)
- [OpenAI Whisper Small](https://huggingface.co/openai/whisper-small)

Download the models from the project root:

```bash
uv run python GoogleGemmaDownload.py
uv run python MetaLlamaDownload.py
uv run python WhisperDownload.py
```

The files are saved in `AIModels/gemma`, `AIModels/llama`, and
`AIModels/whisper`. Model weights are large and are excluded from Git by
`.gitignore`.

## Run the API

Start the development server:

```bash
uv run python main.py
```

The API is available at <http://localhost:8000>. Interactive API documentation
is available at <http://localhost:8000/docs>.

## Endpoints

Health check:

```bash
curl http://localhost:8000/
```

Gemma:

```bash
curl -X POST http://localhost:8000/chat-gemma \
	-H "Content-Type: application/json" \
	-d '{"prompt":"Explain machine learning in one paragraph."}'
```

Llama:

```bash
curl -X POST http://localhost:8000/chat-llama \
	-H "Content-Type: application/json" \
	-d '{"prompt":"Write a short welcome message."}'
```

	Whisper transcription:

	```bash
	curl -X POST http://localhost:8000/transcribe-whisper \
		-H "Content-Type: application/json" \
		-d '{"audio_url":"https://example.com/audio.mp3"}'
	```

Both chat endpoints accept:

```json
{
	"prompt": "Your question or instruction"
}
```

and return:

```json
{
	"content": "Generated model response"
}
```

The Whisper endpoint accepts:

```json
{
	"audio_url": "https://example.com/audio.mp3"
}
```

The server downloads the file from `audio_url` temporarily, transcribes it,
deletes the temporary file, and returns:

```json
{
	"transcription": "Transcribed audio text"
}
```

## Project Structure

```text
main.py                    FastAPI application entrypoint
app/gemma_api.py           Gemma model loading and endpoint
app/llama_api.py           Llama model loading and endpoint
app/whisper_api.py         Whisper model loading and transcription endpoint
GoogleGemmaDownload.py     Gemma model download script
MetaLlamaDownload.py       Llama model download script
WhisperDownload.py         Whisper model download script
AIModels/                  Local model files, ignored by Git
pyproject.toml             Project dependencies and metadata
```

## Troubleshooting

If Hugging Face returns `403 Forbidden`, the logged-in account has not been
approved for the gated model. Accept the model terms and authenticate again:

```bash
uv run hf auth login --force
```

If startup reports a missing tokenizer backend, update the environment:

```bash
uv sync
```
