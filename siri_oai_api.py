import os
import tempfile
from fastapi import FastAPI, Request, Response
from AppKit import NSSpeechSynthesizer, NSURL
import uvicorn

app = FastAPI()

def synthesize_text(text: str) -> bytes:
    # 1. Create a temporary file path to store the AIFF audio
    # macOS native speech synthesizer outputs AIFF, not MP3
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, "siri_output.aiff")
    file_url = NSURL.fileURLWithPath_(file_path)
    
    # 2. Initialize the macOS Speech Synthesizer
    synthesizer = NSSpeechSynthesizer.alloc().init()
    
    # 3. Direct the speech to the file instead of the speakers
    synthesizer.startSpeakingString_toURL_(text, file_url)
    
    # 4. Because NSSpeechSynthesizer runs asynchronously, we must wait
    # for it to finish writing the file before reading it.
    while synthesizer.isSpeaking():
        pass  # Small busy-wait loop for computational completeness
    
    # 5. Read the generated audio bytes
    audio_bytes = b""
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            audio_bytes = f.read()
        os.remove(file_path) # Clean up the temp file
        
    return audio_bytes

@app.post("/v1/audio/speech")
async def generate_speech(request: Request):
    data = await request.json()
    text = data.get("input")
    
    if not text:
        return Response(content="Missing input text", status_code=400)
    
    audio_data = synthesize_text(text)
    
    # Note: macOS natively generates AIFF/CAF data. 
    # To strictly match OpenAI's MP3 spec, we return audio/aiff here,
    # or you can use a library like ffmpeg to convert it to MP3.
    return Response(content=audio_data, media_type="audio/aiff")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)