import pyaudio
import wave
import whisper

def record_audio():
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
    frames = []

    print("Recording...")

    try:
        while True:
            data = stream.read(1024)
            frames.append(data)
    except KeyboardInterrupt:
        print("Recording stopped")

    stream.stop_stream()
    stream.close()
    audio.terminate()

    return frames

def save_audio(frames, filename):
    recording = wave.open(filename, "wb")
    recording.setnchannels(1)
    recording.setsampwidth(pyaudio.get_sample_size(pyaudio.paInt16))
    recording.setframerate(44100)
    recording.writeframes(b''.join(frames))
    recording.close()

def transcribe_audio(audio_file, model):
    transcription = model.transcribe(audio_file)
    return transcription

def save_transcription(transcription, filename):
    with open(filename, "w") as file:
        file.write(transcription['text'])

def main():
    model = whisper.load_model("base")
    audio_frames = record_audio()
    audio_filename = "recording.wav"
    save_audio(audio_frames, audio_filename)
    print(f"File saved as {audio_filename}")

    transcription = transcribe_audio(audio_filename, model)
    print("Transcription: ", transcription['text'])

    transcription_filename = "transcription.txt"
    save_transcription(transcription, transcription_filename)

if __name__ == "__main__":
    main()