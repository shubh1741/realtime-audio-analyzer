import sys
import numpy as np
import pyaudio
import noisereduce as nr
from scipy.signal import spectrogram
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QComboBox, QCheckBox, QLabel, QTabWidget
)
from PyQt5.QtCore import QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class AudioVisualizer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Real-Time Audio Analyzer 🎧")
        self.setGeometry(200, 200, 900, 600)

        # Audio setup
        self.chunk = 1024
        self.rate = 44100
        self.channels = 1
        self.format = pyaudio.paInt16
        self.buffer_size = 40
        self.raw_audio_buffer = np.zeros(self.chunk * self.buffer_size, dtype=np.int16)
        self.p = pyaudio.PyAudio()
        self.stream = None

        # Main layout
        main_layout = QVBoxLayout()
        control_layout = QHBoxLayout()

        # Controls
        self.device_selector = QComboBox()
        self.device_selector.addItems(self.get_input_devices())
        self.noise_checkbox = QCheckBox("Enable Noise Suppression")
        self.start_button = QPushButton("Start")
        self.stop_button = QPushButton("Stop")

        control_layout.addWidget(QLabel("Select Microphone:"))
        control_layout.addWidget(self.device_selector)
        control_layout.addWidget(self.noise_checkbox)
        control_layout.addWidget(self.start_button)
        control_layout.addWidget(self.stop_button)
        main_layout.addLayout(control_layout)

        # Tabs for Waveform & Spectrogram
        self.tabs = QTabWidget()
        self.waveform_tab = QWidget()
        self.spectrogram_tab = QWidget()

        self.tabs.addTab(self.waveform_tab, "Waveform")
        self.tabs.addTab(self.spectrogram_tab, "Spectrogram")
        main_layout.addWidget(self.tabs)
        self.setLayout(main_layout)

        # Waveform Plot
        self.waveform_fig = Figure()
        self.waveform_canvas = FigureCanvas(self.waveform_fig)
        self.ax_waveform = self.waveform_fig.add_subplot(111)
        self.line_waveform, = self.ax_waveform.plot(np.zeros(self.chunk))
        self.ax_waveform.set_ylim(-32768, 32767)
        self.ax_waveform.set_title("Live Waveform")
        self.ax_waveform.set_xlabel("Samples")
        self.ax_waveform.set_ylabel("Amplitude")
        self.waveform_tab.setLayout(QVBoxLayout())
        self.waveform_tab.layout().addWidget(self.waveform_canvas)

        # Spectrogram Plot
        self.spec_fig = Figure()
        self.spec_canvas = FigureCanvas(self.spec_fig)
        self.ax_spec = self.spec_fig.add_subplot(111)
        self.spec_img = self.ax_spec.imshow(np.zeros((256, 10)), aspect='auto',
                                            origin='lower', extent=[0, 1, 0, self.rate / 2])
        self.ax_spec.set_title("Live Spectrogram")
        self.ax_spec.set_xlabel("Time")
        self.ax_spec.set_ylabel("Frequency (Hz)")
        self.spectrogram_tab.setLayout(QVBoxLayout())
        self.spectrogram_tab.layout().addWidget(self.spec_canvas)

        # Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plots)

        # Button connections
        self.start_button.clicked.connect(self.start_stream)
        self.stop_button.clicked.connect(self.stop_stream)

    def get_input_devices(self):
        devices = []
        for i in range(self.p.get_device_count()):
            info = self.p.get_device_info_by_index(i)
            if info["maxInputChannels"] > 0:
                devices.append(f"{i}: {info['name']}")
        return devices

    def start_stream(self):
        index = int(self.device_selector.currentText().split(":")[0])
        self.stream = self.p.open(format=self.format,
                                  channels=self.channels,
                                  rate=self.rate,
                                  input=True,
                                  input_device_index=index,
                                  frames_per_buffer=self.chunk)
        self.timer.start(50)

    def stop_stream(self):
        self.timer.stop()
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None

    def update_plots(self):
        if not self.stream:
            return

        raw = self.stream.read(self.chunk, exception_on_overflow=False)
        audio = np.frombuffer(raw, dtype=np.int16)

        # Update rolling buffer
        self.raw_audio_buffer = np.roll(self.raw_audio_buffer, -self.chunk)
        self.raw_audio_buffer[-self.chunk:] = audio

        # Apply noise suppression if enabled
        if self.noise_checkbox.isChecked():
            audio_proc = nr.reduce_noise(y=self.raw_audio_buffer.astype(float), sr=self.rate).astype(np.int16)
        else:
            audio_proc = self.raw_audio_buffer

        # Update waveform
        self.line_waveform.set_ydata(audio)
        self.line_waveform.set_xdata(np.arange(len(audio)))
        self.waveform_canvas.draw()

        # Update spectrogram
        # Update spectrogram
        f, t, Sxx = spectrogram(audio_proc, fs=self.rate, nperseg=512, noverlap=256)
        Sxx_log = 10 * np.log10(Sxx + 1e-8)

        # Update data if it's 2D
        if Sxx_log.ndim == 2:
            self.spec_img.set_data(Sxx_log)
            self.spec_img.set_extent([0, t[-1] if len(t) else 1, 0, f[-1] if len(f) else self.rate / 2])
            self.spec_img.set_clim(np.min(Sxx_log), np.max(Sxx_log))
            self.spec_canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AudioVisualizer()
    window.show()
    sys.exit(app.exec_())
