# 🎧 Real-Time Audio Analyzer (Waveform + Spectrogram + Noise Suppression)

A Python-based GUI tool that captures and visualizes live audio input from a microphone. The app displays both a **waveform** and a **spectrogram** of your voice or sound environment, and includes a toggle to apply **real-time noise suppression**.

This is ideal for learning audio processing, signal visualization, and GUI design in Python.

---

## 🚀 Features

- 🎙️ Microphone selector (choose from available input devices)
- 📊 Real-time waveform plot (amplitude vs time)
- 📈 Real-time spectrogram view (frequency vs time)
- 🎛 Optional noise suppression using spectral gating
- 🧼 Smoother display with automatic amplitude scaling
- 🧠 Built with PyQt5 and Matplotlib
- ✅ Easy to use, beginner friendly

---

## 🧠 How It Works

### 🎤 Audio Input
Audio is captured using the `pyaudio` library in real-time from the selected microphone device. It reads small chunks of samples (`CHUNK = 1024`) at a standard sampling rate (`RATE = 44100` Hz).

### 📉 Noise Suppression
When enabled, we pass the signal through the [`noisereduce`](https://github.com/timsainb/noisereduce) library. It applies **spectral gating** based on a noise profile estimated from the input signal itself. This helps reduce background noise like fan hum, static, etc.

### 📈 Spectrogram
The `scipy.signal.spectrogram` function is used to compute a time-frequency representation of the audio. We apply a logarithmic scale (`10 * log10`) for better contrast in the display.

### 🖼️ Visualization
Plots are rendered live using `matplotlib` and embedded in the PyQt5 GUI using `FigureCanvasQTAgg`. We refresh the canvas approximately every 50 milliseconds using a `QTimer`.

---

## 🧩 Dependencies

Install everything with:

```bash
pip install numpy scipy matplotlib pyqt5 pyaudio noisereduce

---

# Project Structure
├── audio_gui.py       # Main application
├── README.md          # Project documentation
└── requirements.txt   # (Optional) for pip install
---

# How To Run

```bash
python audio_gui.py

Once it launches:
Select your microphone from the dropdown
Toggle "Enable Noise Suppression" if you like
Click Start to begin visualizing
You can switch between Waveform and Spectrogram tabs

---

# 📚 Learning Goals
This project is a great way to learn:
Audio signal processing (time domain + frequency domain)
Realtime plotting with Matplotlib
GUI development with PyQt5
Spectral noise reduction
Working with streaming audio data (PyAudio)
Multimodal visualization (waveform + spectrogram)

---
#✨ Author
Shubham Sahu
