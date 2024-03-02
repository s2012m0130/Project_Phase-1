import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QLabel, QLineEdit, QSlider
from PyQt5.QtCore import Qt
from pydub import AudioSegment

class AudioEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.original_audio = None
        self.new_audio = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Basic Audio Editor')
        self.setGeometry(100, 100, 600, 300)  # Adjusted window size for extra controls

        self.loadAudioBtn = QPushButton('Load Original Audio', self)
        self.loadAudioBtn.clicked.connect(self.loadOriginalAudio)
        self.loadAudioBtn.resize(200, 40)
        self.loadAudioBtn.move(50, 30)

        # UI elements for specifying trim start and end times
        self.trimStartInput = QLineEdit(self)
        self.trimStartInput.setPlaceholderText('Trim Start Time (s)')
        self.trimStartInput.move(260, 30)
        self.trimStartInput.resize(200, 40)

        self.trimEndInput = QLineEdit(self)
        self.trimEndInput.setPlaceholderText('Trim End Time (s)')
        self.trimEndInput.move(260, 80)
        self.trimEndInput.resize(200, 40)

        self.trimAudioBtn = QPushButton('Trim Audio', self)
        self.trimAudioBtn.clicked.connect(self.trimAudio)
        self.trimAudioBtn.resize(200, 40)
        self.trimAudioBtn.move(50, 130)

        self.statusLabel = QLabel('Status: Waiting for input...', self)
        self.statusLabel.move(50, 230)
        self.statusLabel.resize(500, 40)

        # Slider for start
        self.trimStartSlider = QSlider(Qt.Horizontal, self)
        self.trimStartSlider.setFocusPolicy(Qt.StrongFocus)
        self.trimStartSlider.setTickPosition(QSlider.TicksBothSides)
        self.trimStartSlider.setTickInterval(10)  # 根据需要调整
        self.trimStartSlider.setSingleStep(1)
        self.trimStartSlider.move(260, 130)
        self.trimStartSlider.resize(200, 40) # max = 30s
        self.trimStartSlider.valueChanged[int].connect(self.updateTrimStartInput)
        
        # Slider for end
        self.trimEndSlider = QSlider(Qt.Horizontal, self)
        self.trimEndSlider.setFocusPolicy(Qt.StrongFocus)
        self.trimEndSlider.setTickPosition(QSlider.TicksBothSides)
        self.trimEndSlider.setTickInterval(10)  
        self.trimEndSlider.setSingleStep(1)
        self.trimEndSlider.move(260, 180)
        self.trimEndSlider.resize(200, 40) 
        self.trimEndSlider.valueChanged[int].connect(self.updateTrimEndInput)

    def loadOriginalAudio(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'Open file', './recorded_files')
        if fname:
            self.original_audio = AudioSegment.from_file(fname)
            self.statusLabel.setText('Original audio loaded.')
        self.updateSliders()  

    def updateSliders(self):
        if self.original_audio:
            max_value = len(self.original_audio) // 1000 
            self.trimStartSlider.setMaximum(max_value)
            self.trimEndSlider.setMaximum(max_value)

    def updateTrimStartInput(self, value):
        self.trimStartInput.setText(str(value))
        
    def updateTrimEndInput(self, value):
        self.trimEndInput.setText(str(value))

    def trimAudio(self):
        start_time = int(self.trimStartInput.text()) * 1000 if self.trimStartInput.text() else 0
        end_time = int(self.trimEndInput.text()) * 1000 if self.trimEndInput.text() else len(self.original_audio)
        if self.original_audio:
            trimmed_audio = self.original_audio[start_time:end_time]
            trimmed_audio.export("./trim/trimmed_audio.wav", format="wav")
            self.statusLabel.setText(f'Audio trimmed and saved as trimmed_audio.wav in ./trim.')
        else:
            self.statusLabel.setText('No original audio loaded.')


def main():
    app = QApplication(sys.argv)
    ex = AudioEditor()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
