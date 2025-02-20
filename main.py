import speech_recognition as sr
# from transformers import pipeline
import edge_tts
import asyncio

from queue import Queue
import time
import os
from dotenv import load_dotenv
import tkinter as tk
import threading
load_dotenv()


# Initialize AI model (using a small model for Q&A) from huggingface
# qa_pipeline = pipeline(
#     "conversational",
#     model="facebook/blenderbot-400M-distill",
#     tokenizer="facebook/blenderbot-400M-distill"
# )


class VoiceAssistant:

    def __init__(self):

        self.WAKE_WORD = "good morning"

        # Initialize recognizer
        self.recognizer = sr.Recognizer()

        # Set a Gui interface for the Voice Assistant
        self.window = tk.Tk()
        self.window.title("Voice Assistant")
        self.window.geometry("300x250")
        self.label = tk.Label(self.window, text="🤖" ,font=("Arial", 120, "bold"))
        self.label.pack()

        # --- creating a exit button to quit the interface ---  
        exit_button = tk.Button(self.window,
                                text='Exit',
                                command=lambda: self.window.quit()
                                )
        exit_button.pack(side=tk.BOTTOM, expand=True, anchor="s")

        threading.Thread(target=self.start_assistant_thread, daemon=True).start()
        self.window.mainloop()

    def start_assistant_thread(self):
        """Creates a new event loop in this thread and runs the assistant"""
        asyncio.new_event_loop().run_until_complete(self.run_assistant())


    async def run_assistant(self, language="en-US"):  # or 'en-US' for French or "en-US" for english
        """Continuously listens to the microphone and responds to user commands when Key Worsd are heard"""
        while True:
            # Update GUI (use thread-safe method
            self.window.after(0, lambda: self.label.config(fg="blue"))

            try:
                with sr.Microphone(device_index=2) as source: # device_index=2 , in my case when headphones connected
                    print("Waiting for wake word...")
                    self.recognizer.adjust_for_ambient_noise(source, duration=1)
                    audio = self.recognizer.listen(source)
                    text = self.recognizer.recognize_google(audio, language=language).lower()

                    if self.WAKE_WORD in text:
                        print("Wake word detected!")
                        self.window.after(0, lambda: self.label.config(fg="red"))

                        self.recognizer.adjust_for_ambient_noise(source, duration=1)
                        audio = self.recognizer.listen(source)
                        text = self.recognizer.recognize_google(audio, language=language).lower()
                        print(f"You said: {text}")

                        # Convert the given text into speech
                        await self.text_to_speech(text)

                    # quit the program if user say "Stop"
                    if "stop" in text:
                        print("Exiting...")
                        self.window.after(0, self.window.quit)
                        return

            except sr.WaitTimeoutError:
                print("Timeout error")
            except sr.UnknownValueError:
                print("Could not understand audio")
            except sr.RequestError as e:
                print(f"Could not request results; {e}")
            except Exception as e:
                print(f"Error: {e}")

            # Small pause to prevent CPU overuse
            await asyncio.sleep(0.2)


    async def text_to_speech(self, text, voice="en-US-ChristopherNeural", output_file="output.mp3"):
        '''Convert the given text into speech.Saves the audio file using the edge-tts module'''
        communicate = edge_tts.Communicate(text, voice, rate="+0%", pitch="+0Hz", volume="+0%")
        await communicate.save(output_file)

            
if __name__ == "__main__":
    VoiceAssistant()


            # Get AI response
            # response = qa_pipeline(text_input)
            # ai_response = response.generated_responses[0]
            # print(f"AI: {ai_response}")
            
            # Convert response to speech using edge-tts
            # await text_to_speech(ai_response)
