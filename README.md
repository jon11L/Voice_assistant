
# AI Voice Assistant


### Main logic:

    - Speech-to-Text (Audio input → Text)  --> Google Speech Recognition
    - AI Chat Response (Text → AI Response) -> Facebook/BlenderBot  with Pytorch 
    - Text-to-Speech (AI Response → Audio output) --> Microsoft edge-tts


I am working on creating a small, local, free virtual assistant using the technologies mentioned above. Which hopefully should be able to be used without any Authentication or Apikeys.
only an active internet connection is required to use the speech recognitions. As Blendorbot 400 should be able to run locally.

The speech recognition works, but have a hard time getting different key words,  set as "good morning" at the moment, as it was recognizing the Wake word more accurately.