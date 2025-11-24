import speech_recognition as sr

for index, name in enumerate(sr.Microphone.list_microphone_names()):
    print(index, name)
