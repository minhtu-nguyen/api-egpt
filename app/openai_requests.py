import os
import openai
#from decouple import config
from dotenv import load_dotenv
from pathlib import Path

dotenv_path = Path('../.env')
load_dotenv(dotenv_path=dotenv_path)

openai.organization = os.getenv("OPEN_AI_ORG")
openai.api_key = os.getenv("OPEN_AI_KEY")

from app.database import get_recent_messages

#Audio to Text
def convert_audio_to_text(audio_file):
  try:
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    message_text = transcript["text"]
    return message_text
  except Exception as e:
    return
  
#Get response
def get_chat_response(message_input):
  messages = get_recent_messages()
  user_message = {"role": "user", "content": message_input}
  messages.append(user_message)
  print(messages)

  try:
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=messages
    )
    message_text = response["choices"][0]["message"]["content"]
    return message_text
  except Exception as e:
    return