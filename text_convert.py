import speech_recognition as sr
import os

class TextConvert:
    def __init__(self, recorded_files):
        recorded_files = "./recorded_files"
        self.recorded_files = recorded_files
        self.recognizer = sr.Recognizer()

    def RecordProcess(self):
        
        wav_files = [file for file in os.listdir(self.recorded_files) if file.endswith('.wav')]

        for wav_file in wav_files:
            wav_path = os.path.join(self.recorded_files, wav_file)
            print("Record:", wav_path)

            recorded_file = sr.AudioFile(wav_path)

            try:
                with recorded_file as source:
                    record = self.recognizer.record(source)
                text = self.recognizer.recognize_google(record)
                segments = text.split(".")
                for segment in segments:
                    print(segment.strip())  
            except sr.UnknownValueError:
                print("\n unknown value error.")
            except sr.RequestError as e:
                print("\n server request error: {0}".format(e))
        print("\n All record have been converted.")