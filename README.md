# Language-Carrier

First Push : 
  Tasks Done so far:
      <br>1. Video/Audio to .wav form converted using ffmpeg in videoToAudio.py file.
        <br>1.1 Basic Exceptions such as File not found handled.
        <br>1.2 Other audio conversion exceptions handled.
      <br>2. From this file, audio.wav is created from the source and the file, audioToText.py is called.
      <br>3. silenceBasedConversion method is invoked. The audio source path is hardcoded.
      <br>4. Necessary text files are created to store results.
      <br>5. The audio.wav file is broken into smaller chunks, so that, it will be easy for the audio to be converted.
      <br>6. This also reduces the audio size and length.
      <br>7. Chunks are then converted into slow playback to make efficient audio to text conversion.
      <br>8. Each Audio file is converted to text. Exception is handled.
      <br>9. Text converted to other languages.
      <br>10.Audio developed from text in translated_audio directory.
  <br>Tasks to be done:
      <br>1. UI Development using Tkinter.
      <br>2. Integration.
      <br>3. Unrecognized files handling.
      <br>4. Retry files handling.
      <br>5. Male/Female versions for the audio files should be added.
