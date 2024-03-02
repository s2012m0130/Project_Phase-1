import tkinter as tk
import os
from text_convert import TextConvert
from recorder import AudioRecorder
from playback import SoundPlayer, WAVReader, SoundPlayer_update
from trim_gui import AudioEditor
import threading

class RecorderApp:
    def __init__(self):
        self.playing = False
        self.root = tk.Tk()
        self.root.title("Audio Recorder")
        self.root.resizable(False, False)

        self.listbox = tk.Listbox(self.root)
        self.listbox.pack()
        self.load_recorded_files()

        self.label = tk.Label(text= "00:00:00")
        self.label.pack()

        self.record_button = tk.Button(self.root, text="⏺", font=("Arial", 40, "bold"), command=self.toggle_recording)
        self.record_button.pack()

        self.play_button = tk.Button(self.root, text="▶", font=("Arial", 40, "bold"), command=self.play_audio)
        self.play_button.pack()

        self.recorder = AudioRecorder()
        self.WAVReader = WAVReader(None)
        
         
        self.player = SoundPlayer_update(self.WAVReader, self.playback_finished)
        self.root.mainloop()
    
    def load_recorded_files(self):
        recorded_files = [file for file in os.listdir("recorded_files") if file.endswith(".wav")]
        recorded_files = sorted(recorded_files)
        
        text_converter = TextConvert(recorded_files)
        text_converter.RecordProcess()
        
        self.listbox.delete(0, tk.END)

        for file in recorded_files:
            self.listbox.insert(tk.END, file)

    def toggle_recording(self):
        if not self.recorder.recording:  # Start recording if not already recording
            self.record_button.config(text="⏹",fg="red")
            threading.Thread(target=self.recorder.record_audio).start()
        else:  # Stop recording if already recording
            self.record_button.config(text="⏺", fg="black")
            self.recorder.stop_recording()
            self.recorder.save_as_wav()  
            self.load_recorded_files()

    def play_audio(self):
        if not self.listbox.curselection():
            return
        selected_file = self.listbox.get(self.listbox.curselection())
        self.WAVReader.set_filename(f"recorded_files/{selected_file}")
        if self.WAVReader.get_filename() is None:
            return

        if not self.playing:
            self.play_button.config(text="⏸")  
            self.WAVReader.read_wav_file()
            self.player.play_sound()  
            self.playing = True
        elif self.player.paused:  
            self.play_button.config(text="⏸")  
            self.player.pause()  
        else:
            self.play_button.config(text="▶")  
            self.player.pause()
    
    def playback_finished(self):
        self.update_ui_after_playback()

    def update_ui_after_playback(self):
        self.play_button.config(text="▶")  
        self.playing = False  

RecorderApp()

    