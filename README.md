# macOS Siri TTS OpenAI-Compatible API Wrapper

This project exposes the native macOS speech synthesizer (`NSSpeechSynthesizer`) as a local, OpenAI-compatible text-to-speech (TTS) API endpoint. 

It allows you to plug native macOS voices directly into tools and applications that expect the OpenAI `/v1/audio/speech` API format.

---

## Features
* **OpenAI Compatible:** Implements the `/v1/audio/speech` POST endpoint.
* **Ultra-low Latency:** Leverages native Cocoa `AppKit` APIs without needing cloud dependencies.
* **Stand-alone Executable:** Can be compiled into a single binary via PyInstaller for zero-config deployments on other Mac machines.

---

## Prerequisites
This wrapper **requires macOS** to run, as it relies heavily on the native Apple `AppKit` framework via `pyobjc`.

---

## Installation & Setup

1. **Clone or save the script** as `siri_oai_api.py`.
2. **Install dependencies** using `uv` (or regular `pip`):

```bash
uv pip install fastapi uvicorn pyobjc-framework-Cocoa

```

> **Note:** The `AppKit` module is part of the `pyobjc-framework-Cocoa` package. If you try to run or package the app without it, python won't be able to find `AppKit`.

---

## Running the API

Start the local server by running:

```bash
python siri_oai_api.py

```

The server will spin up at `http://localhost:8000`.

### Example Usage (cURL)

```bash
curl http://localhost:8000/v1/audio/speech \
  -H "Content-Type: application/json" \
  -d '{
    "model": "tts-1",
    "input": "Hello! This is Siri reading text straight from a local OpenAI API clone.",
    "voice": "alloy"
  }' \
  --output speech.aiff

```

> **Audio Format Note:** This API returns native Apple **AIFF** audio data instead of MP3 to maintain absolute speed without heavy transcoding overhead. Most modern players (and LLM frameworks) can stream or read AIFF natively.

---

## Compiling to a Standalone Executable

If you want to package this API into a single executable file that you can run without installing Python or dependencies everywhere, use **PyInstaller**.

Because `AppKit` is a dynamically bound Objective-C framework, you must explicitly tell PyInstaller to collect its metadata hooks using `--collect-all`.

### 1. Install PyInstaller

```bash
uv pip install pyinstaller

```

### 2. Build the Binary

Run the following build command:

```bash
pyinstaller --onefile --collect-all AppKit siri_oai_api.py

```

### 3. Run the Binary

Once completed, you will find your standalone application in the `dist/` directory:

```bash
./dist/siri_oai_api

```
