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

## 📈 What is a Spectrogram?

A **spectrogram** is a visual representation of how the **frequency content** of a signal changes over **time**. It’s one of the most powerful tools in audio signal analysis. It’s like a movie of the **audio’s frequency energy** — showing not just how loud a signal is, but **which frequencies** are present and **when**.

### 🔍 How to Read a Spectrogram

- **X-axis** → Time (seconds)
- **Y-axis** → Frequency (Hz)
- **Color Intensity** → Amplitude or power of the signal at that time and frequency

Think of it as a movie of your sound, showing **what frequencies** are present **and when**.

### 🎵 Example Interpretation

| Time → | | |
|--------|--|--|
| 🔊 **Low frequencies** (bottom) | bass, hum |
| 🎶 **Mid frequencies** | voice, instruments |
| 🔔 **High frequencies** (top) | hiss, cymbals, sibilance |

- Bright colors = strong/loud signal
- Dark colors = soft/quiet signal

---

## 🔬 How Spectrograms are Generated

Internally, the signal is split into small chunks (windows), and each chunk is transformed using the **Short-Time Fourier Transform (STFT)**:

1. Chop signal into overlapping frames
2. Apply a **Fast Fourier Transform (FFT)** on each frame
3. Stack the results to build a time-frequency map

### 🖼️ Visualization

Plots are rendered live using `matplotlib` and embedded in the PyQt5 GUI using `FigureCanvasQTAgg`. We refresh the canvas approximately every 50 milliseconds using a `QTimer`.

---

## 🧩 Dependencies

Install everything with:

```bash
pip install numpy scipy matplotlib pyqt5 pyaudio noisereduce
```
---

## How To Run

```bash
python audio_gui.py
```
---

Once it launches: 
- Select your microphone from the dropdown
- Toggle "**Enable Noise Suppression**" if you like
- Click **Start** to begin visualizing
- You can switch between **Waveform** and **Spectrogram** tabs

---

## 📚 Learning Goals

This project is a great way to learn:
1. Audio signal processing (time domain + frequency domain)
2. Realtime plotting with Matplotlib
3. GUI development with PyQt5
4. Spectral noise reduction
5. Working with streaming audio data (PyAudio)
6. Multimodal visualization (waveform + spectrogram)

---

## ✨ Author

Shubham Sahu

---
