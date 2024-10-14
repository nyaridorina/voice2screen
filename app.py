import speech_recognition as sr

recognizer = sr.Recognizer()

def recognize_from_file(audio_file):
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Google Speech Recognition could not understand the audio."
    except sr.RequestError:
        return "Could not request results from Google Speech Recognition service."

# Example usage:
print(recognize_from_file("your_audio_file.wav"))
