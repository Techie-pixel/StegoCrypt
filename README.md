# 🔐 Steganography Tool - Image | Audio | Video

Complete Python-based Steganography application with GUI for hiding secret messages in multimedia files.

## ✨ Features

- **Image Steganography**: Hide messages in PNG, JPG, JPEG, BMP images
- **Audio Steganography**: Hide messages in WAV audio files
- **Video Steganography**: Hide messages in MP4, AVI, MKV video files
- **User-friendly GUI**: Easy-to-use interface with tabs
- **LSB Encoding**: Uses Least Significant Bit technique
- **Secure**: Messages hidden imperceptibly

## 🚀 Installation

### Step 1: Install Python
Make sure you have Python 3.8 or higher installed.

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

Or install individually:
```bash
pip install Pillow opencv-python numpy pydub
```

### Step 3: Run the Application
```bash
python app.py
```

## 📖 How to Use

### Image Steganography

#### Encoding:
1. Go to the "🖼️ Image" tab
2. Click "Select Image" and choose your image file
3. Type your secret message in the text box
4. Click "Encode & Save"
5. Choose where to save the encoded image (PNG format)

#### Decoding:
1. Scroll down to the decode section
2. Click "Select Encoded Image"
3. Click "Decode Message"
4. Your secret message will be revealed!

### Audio Steganography

#### Encoding:
1. Go to the "🎵 Audio" tab
2. Click "Select Audio File (WAV)" and choose your WAV file
3. Type your secret message
4. Click "Encode & Save"
5. Save the encoded audio file

**Note**: Only WAV files are supported for audio steganography.

#### Decoding:
1. Click "Select Encoded Audio"
2. Click "Decode Message"
3. View your hidden message!

### Video Steganography

#### Encoding:
1. Go to the "🎬 Video" tab
2. Click "Select Video File"
3. Enter your secret message
4. Click "Encode & Save"
5. Save as AVI file

**Note**: Message is hidden in the first frame of the video.

#### Decoding:
1. Click "Select Encoded Video"
2. Click "Decode Message"
3. Extract your hidden message!

## 🛠️ Technical Details

### LSB (Least Significant Bit) Technique
The application uses LSB steganography which modifies the least significant bit of pixel/audio/video data to hide information. This makes changes imperceptible to human eyes/ears.

### Supported Formats

**Images**: PNG, JPG, JPEG, BMP (Output: PNG)
**Audio**: WAV (Input and Output)
**Video**: MP4, AVI, MKV (Input: Multiple, Output: AVI)

### Delimiter
Uses binary delimiter `1111111111111110` to mark the end of hidden message.

## 📊 Project Structure

## ⚠️ Important Notes

1. **Image**: Always save encoded images as PNG to preserve data
2. **Audio**: Only WAV format supported for best quality
3. **Video**: Encoded video saved as AVI format
4. **Message Size**: Message should be smaller than the media file capacity
5. **Original Files**: Keep original files safe, encoded files may be larger

## 🎓 For Academic Projects

This tool is perfect for:
- Computer Science microprojects
- Cybersecurity assignments
- Data hiding demonstrations
- Information security coursework

## 🐛 Troubleshooting

### Error: "Message too large"
- Use a larger image/audio/video file
- Or reduce your message length

### Video encoding takes time
- Normal behavior, especially for large videos
- First frame encoding is used for faster processing

### Audio not working
- Make sure audio file is in WAV format
- Convert MP3/other formats to WAV first

## 📝 Example Usage

```python
# Simple example of how the encoding works
message = "Hello Secret World!"
# Converts to binary: 01001000 01100101 01101100 01101100 01101111...
# Hides in LSB of pixels/audio samples
```

## 🎨 GUI Features

- **Dark Theme**: Easy on the eyes
- **Tabbed Interface**: Separate tabs for each media type
- **File Selection**: Visual feedback for selected files
- **Progress Messages**: Success/error notifications
- **Intuitive Design**: Simple and clean layout

## 💡 Tips

1. Use PNG for images (lossless format)
2. Larger files can hide longer messages
3. Keep original files as backup
4. Test with small messages first
5. Encoded files look identical to originals

## 🔒 Security Note

This is for educational purposes. For real security needs:
- Add encryption before steganography
- Use password protection
- Implement additional security layers

## 📞 Support

For issues or questions:
1. Check the error message
2. Verify file formats
3. Ensure all dependencies are installed
4. Check file permissions

## 🌟 Credits

Developed for educational and research purposes.
Uses standard steganography techniques taught in computer science.

---

**Happy Hiding! 🔐**
