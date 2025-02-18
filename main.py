import speech_recognition as sr
# from transformers import pipeline
import edge_tts
import asyncio

from queue import Queue
import time
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize recognizer
recognizer = sr.Recognizer()

# Initialize AI model (using a small model for Q&A) from huggingface
# qa_pipeline = pipeline(
#     "conversational",
#     model="facebook/blenderbot-400M-distill",
#     tokenizer="facebook/blenderbot-400M-distill"
# )


WAKE_WORD = "good morning"
def listen_for_wake_word():
    while True:
        with sr.Microphone(device_index=2) as source:
            print("Waiting for wake word...")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source)
            
        try:
            text = recognizer.recognize_google(audio).lower()
            if WAKE_WORD in text:
                print("Wake word detected!")
                return True

        except sr.WaitTimeoutError:
            continue
        except sr.UnknownValueError as e:
            print("Didn't catch that, listening again...", e)
            continue
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            # time.sleep(1)
            continue
        except Exception as e:
            print(f"Error: {e}")
            continue
    return False

async def text_to_speech(text, voice="en-US-ChristopherNeural", output_file="output.mp3"):
    '''Convert the given text into speech.Saves the audio file using the edge-tts module'''
    communicate = edge_tts.Communicate(text, voice, rate="+0%", pitch="+0Hz", volume="+0%")
    await communicate.save(output_file)


def listen_to_microphone(language='en-US'): # or 'fr-FR' for French
    '''Listen to the microphone and convert audio to text'''
    while True:
        with sr.Microphone(device_index=2) as source: #device_index: 2 when my headphones is connected,  0 for default internal microphone
            print(f"Listening in {language}...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
            # recognizer.recogn
            text = ""

        try:
            text = recognizer.recognize_google(audio, language=language).lower()
            print(f"You said: {text}")
            return text
    
        except sr.UnknownValueError:
            print("Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            return None


async def main():
    while True:

        if not listen_for_wake_word():
            continue
        # Get audio input and convert to text
        text_input = listen_to_microphone()
        
        if text_input:
            # store the user's text in new file
            with open('input.txt', 'w') as file:
                file.write(text_input)
            
            time.sleep(1)
            # Convert user's text to speech using edge-tts
            await text_to_speech(text_input)
            
            
if __name__ == "__main__":
    asyncio.run(main())



            # Get AI response
            # response = qa_pipeline(text_input)
            # ai_response = response.generated_responses[0]
            # print(f"AI: {ai_response}")
            
            # Convert response to speech using edge-tts
            # await text_to_speech(ai_response)
            






















# aai.settings.api_key = os.getenv('ASSEMBLYAI_API_KEY')
# # openai.api_key = ""
# # elevenlabs.set_api_key()

# # -------- Take from Assemblyai docs --------
# def on_open(session_opened: aai.RealtimeSessionOpened):
#     print("Session opened with ID:", session_opened.session_id)

# def on_close():
#     print("Session closed")

# # --------  END Take from Assemblyai docs --------


# transcript_queue =  Queue()

# def on_data(transcript: aai.RealtimeTranscript):
#     if not transcript.text:
#         return
#     if isinstance(transcript, aai.RealtimeFinalTranscript):
#         transcript_queue.put(transcript.text + "")
#         # Add new line after final transcript.
#         print(transcript.text, end="\r\n")
#     else:
#         print(transcript.text, end="\r")


# def on_error(error: aai.RealtimeError):
#     print("Error:", error)


# # Conversation loop
# def on_conversation():

#     while True:
#         transcriber = aai.RealtimeTranscriber(
#             sample_rate=16_000,
#             on_data=on_data,
#             on_error=on_error,
#             on_open=on_open,
#             on_close=on_close,
#         )

#         # start connection
#         transcriber.connect()

#         # open microphone
#         microphone_stream = aai.extras.MicrophoneStream(sample_rate=16_000)

#         # stream audio
#         transcriber.stream(microphone_stream)

#         # close audio
#         transcriber.close()

#         # retrieve data from Queue
#         transcript_result = transcript_queue.get()


#         # send transcript to openai for response.
#         print(f"Transcript, Result audio:", transcript_result)