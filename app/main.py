from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
#from decouple import config
import openai
import uvicorn

#App Initialization
app = FastAPI()


#Functions
from functions.openai_requests import convert_audio_to_text, get_chat_response
from functions.database import store_messages, reset_messages
from functions.text_to_speech import convert_text_to_speech

'''
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:4173",
    "http://localhost:3000",
'''

#CORS
origins = [
    "https://superlative-gnome-f096d1.netlify.app/",
    "http://chat-demo.minhtu-nguyen.dev/",     
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:4173",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def read_main():
    return { "message" : "Hello World of FastAPI HTTPS"}

@app.get("/test")
async def test():
    return {"message": "Hello World"}

@app.get("/reset")
async def reset_conversation():
    reset_messages()
    return {"response": "conversation reset"}

@app.get("/get-audio")
async def get_audio():
    audio_input = open("voice.mp3", "rb")

    message_decoded = convert_audio_to_text(audio_input)

    if not message_decoded:
        return HTTPException(status_code=400, detail="Failed to decode audio")
    
    chat_response = get_chat_response(message_decoded)
    store_messages(message_decoded, chat_response)
    #print(chat_response)
    
    # Convert chat response to audio
    audio_output = convert_text_to_speech(chat_response)

    # Guard: Ensure output
    if not audio_output:
        raise HTTPException(status_code=400, detail="Failed audio output")

    # Create a generator that yields chunks of data
    def iterfile():
        yield audio_output

    # Use for Post: Return output audio
    return StreamingResponse(iterfile(), media_type="application/octet-stream")

@app.post("/post-audio/")
async def post_audio(file: UploadFile = File(...)):

    # Convert audio to text - production
    # Save the file temporarily
    with open(file.filename, "wb") as buffer:
        buffer.write(file.file.read())
    audio_input = open(file.filename, "rb")

    # Decode audio
    message_decoded = convert_audio_to_text(audio_input)

    # Guard: Ensure output
    if not message_decoded:
        raise HTTPException(status_code=400, detail="Failed to decode audio")

    # Get chat response
    chat_response = get_chat_response(message_decoded)

    # Store messages
    store_messages(message_decoded, chat_response)

    # Guard: Ensure output
    if not chat_response:
        raise HTTPException(status_code=400, detail="Failed chat response")

    # Convert chat response to audio
    audio_output = convert_text_to_speech(chat_response)

    # Guard: Ensure output
    if not audio_output:
        raise HTTPException(status_code=400, detail="Failed audio output")

    # Create a generator that yields chunks of data
    def iterfile():
        yield audio_output

    # Use for Post: Return output audio
    return StreamingResponse(iterfile(), media_type="application/octet-stream")

if __name__ == "__main__":
    uvicorn.run("main:app", host='0.0.0.0', port=8000, ssl_keyfile="./localhost+2-key.pem", 
                ssl_certfile="./localhost+2.pem"
                )