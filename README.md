# 🔐 StegoCrypt - Advanced Steganography Tool

Complete Python-based Steganography application with a modern Web GUI for hiding secret messages in multimedia files using Flask.

## ✨ Features

- **Image Steganography**: Hide messages in PNG, JPG, JPEG, BMP images
- **Audio Steganography**: Hide messages in WAV audio files
- **Video Steganography**: Hide messages in MP4, AVI, MKV video files
- **Modern Web Interface**: Sleek, glassmorphic UI with Day/Night modes
- **LSB Encoding**: Uses Least Significant Bit technique
- **Secure**: Messages hidden imperceptibly with binary delimiters

## 🚀 Installation

### Step 1: Install Python
Make sure you have Python 3.8 or higher installed.

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

Or install individually:
```bash
pip install Flask Pillow opencv-python numpy
```

### Step 3: Run the Application
```bash
python app.py
```

Open `http://localhost:5000` in your browser.

## 📖 How to Use

### Image Steganography

#### Encoding:
1. Go to the "🖼️ Image" tab.
2. Drag and drop or click to browse for an image file.
3. Type your secret message in the "Secret Message" box.
4. Click "Encode & Download".
5. The encoded image will be downloaded in PNG format.

#### Decoding:
1. Go to the "Reveal Message" section in the Image tab.
2. Upload the encoded PNG image.
3. Click "Decode Message".
4. Your secret message will be revealed in the result box!

### Audio Steganography

#### Encoding:
1. Go to the "🎵 Audio" tab.
2. Select a WAV audio file.
3. Enter your secret message.
4. Click "Encode & Download".
5. Save the resulting WAV file.

**Note**: WAV files are recommended for best results.

#### Decoding:
1. Upload the encoded WAV file in the Decode section.
2. Click "Decode Message".
3. View your hidden message!

### Video Steganography

#### Encoding:
1. Go to the "🎬 Video" tab.
2. Upload a video file (MP4, AVI, MKV).
3. Enter your secret message.
4. Click "Encode & Download".
5. The encoded video is saved in AVI format (lossless).

**Note**: Message is hidden in the first frame of the video for efficiency.

#### Decoding:
1. Upload the encoded AVI video in the Decode section.
2. Click "Decode Message".
3. Extract your hidden message!

## 🛠️ Technical Details

### LSB (Least Significant Bit) Technique
The application uses LSB steganography which modifies the least significant bit of pixel/audio/video data to hide information. This makes changes imperceptible to human eyes/ears.

### Supported Formats

- **Images**: PNG, JPG, JPEG, BMP (Output: PNG)
- **Audio**: WAV, MP3, OGG (Input), WAV (Output)
- **Video**: MP4, AVI, MKV (Input), AVI (Output)

### Delimiter
Uses binary delimiter `1111111111111110` to mark the end of the hidden message.

## 📊 Project Structure

```
steganography-project/
│
├── app.py    # Main application
├── requirements.txt         # Dependencies
└── README.md               # Documentation
```

## ⚠️ Important Notes

1. **Image**: Always use the downloaded PNG to preserve hidden data.
2. **Audio**: WAV format is preferred for high-fidelity data hiding.
3. **Video**: Encoded video is saved as AVI to avoid compression artifacts.
4. **Message Size**: Ensure the message fits within the media's capacity.
5. **Original Files**: Keep backups of your original media files.

## 🎓 For Academic Projects

This tool is perfect for:
- Computer Science microprojects
- Cybersecurity assignments
- Data hiding demonstrations
- Information security coursework

## 🐛 Troubleshooting

### Error: "Message too large"
- Use a larger image/audio/video file or shorten your message.

### Video encoding takes time
- This is normal for video processing; the message is hidden in the first frame to save time.

### Audio not working
- Ensure the file is a valid audio format. Convert to WAV if necessary.

## 📝 Example Usage

```python
# Simple example of how the encoding works
message = "Hello Secret World!"
# Converts to binary: 01001000 01100101 01101100 01101100 01101111...
# Hides in LSB of pixels/audio samples
```

## 🎨 UI Features

- **Glassmorphism Design**: Modern, frosted-glass look.
- **Day/Night Modes**: Switch themes easily with a toggle.
- **Interactive Dropzones**: Drag and drop support with visual feedback.
- **Toast Notifications**: Clean success/error alerts.
- **Animated Background**: Cyberpunk-style Matrix animation.

## 💡 Tips

1. Use PNG for images to avoid data loss from compression.
2. Larger media files provide more "space" for longer messages.
3. Test with short messages first to understand the flow.
4. Encoded files look identical to the originals to the naked eye.

## 🔒 Security Note

This is for educational purposes. For real security needs:
- Encrypt your message before hiding it.
- Use strong passwords and additional security layers.

## 🌟 Credits

Developed for educational and research purposes.
Uses standard steganography techniques taught in computer science.

---

**Happy Hiding! 🔐**
