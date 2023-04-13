import pyaudio
import speech_recognition as sr
import openai
import pyttsx3

# Set up OpenAI API credentials
openai.api_key = "TOKEN"

engine = pyttsx3.init()

engine.setProperty('rate', 155)  # Set the rate of speech to 150 words per minute
engine.setProperty('voice', 'english-us')

#engine.setProperty('rate', 150)  # Set the rate of speech to 150 words per minute

# Set up audio input parameters
chunk = 1024
sample_rate = 44100
duration = 5  # in seconds

# Record audio input
audio = pyaudio.PyAudio()
stream = audio.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=sample_rate,
                    input=True,
                    frames_per_buffer=chunk)
print("Recording audio...")
frames = []
for i in range(int(sample_rate / chunk * duration)):
    data = stream.read(chunk)
    frames.append(data)
print("Audio recorded!")
stream.stop_stream()
stream.close()
audio.terminate()

# Recognize speech from audio input
r = sr.Recognizer()
audio_data = sr.AudioData(b''.join(frames), sample_rate=sample_rate, sample_width=2)
text = r.recognize_google(audio_data)
print(f"Recognized speech: {text}")

# Generate text response from OpenAI GPT-3
prompt = f"Q: {text}\nA:"
model_engine = "text-davinci-002"  # choose the GPT-3 model engine
temperature = 0.5  # controls the randomness of the generated text
max_tokens = 1024  # controls the length of the generated text
response = openai.Completion.create(
    engine=model_engine,
    prompt=prompt,
    temperature=temperature,
    max_tokens=max_tokens
)
generated_text = response.choices[0].text.strip()
print(f"Generated text: {generated_text}")



engine.say(generated_text)
engine.runAndWait()
