"""
Advanced Steganography Web Application
Flask backend with Image, Audio & Video steganography
"""

from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
from PIL import Image
import cv2
import numpy as np
import wave
import struct
import os
import io
import tempfile
import uuid
import subprocess
import shutil

app = Flask(__name__)
CORS(app)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100 MB max upload

# Ensure temp directory exists
UPLOAD_FOLDER = os.path.join(tempfile.gettempdir(), 'stegano_uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ─────────────────────────────────────────────
#  Helper functions
# ─────────────────────────────────────────────

def text_to_binary(text):
    """Convert text to binary string"""
    return ''.join(format(ord(char), '08b') for char in text)


def binary_to_text(binary):
    """Convert binary string to text"""
    text = ""
    for i in range(0, len(binary), 8):
        byte = binary[i:i+8]
        if len(byte) == 8:
            text += chr(int(byte, 2))
    return text


DELIMITER = '1111111111111110'


# ─────────────────────────────────────────────
#  Page route
# ─────────────────────────────────────────────

@app.route('/')
def index():
    return render_template('index.html')


# ─────────────────────────────────────────────
#  IMAGE steganography
# ─────────────────────────────────────────────

@app.route('/encode/image', methods=['POST'])
def encode_image():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        file = request.files['file']
        message = request.form.get('message', '').strip()
        if not message:
            return jsonify({'error': 'No message provided'}), 400

        # Load image
        img = Image.open(file.stream).convert('RGB')
        encoded_img = img.copy()
        width, height = img.size

        # Binary message with delimiter
        binary_msg = text_to_binary(message) + DELIMITER

        # Capacity check
        capacity = width * height * 3
        if len(binary_msg) > capacity:
            return jsonify({'error': f'Message too large! Needs {len(binary_msg)} bits, image capacity is {capacity} bits.'}), 400

        # LSB encode
        data_idx = 0
        for y in range(height):
            for x in range(width):
                if data_idx < len(binary_msg):
                    pixel = list(img.getpixel((x, y)))
                    for i in range(3):
                        if data_idx < len(binary_msg):
                            pixel[i] = pixel[i] & ~1 | int(binary_msg[data_idx])
                            data_idx += 1
                    encoded_img.putpixel((x, y), tuple(pixel))
                else:
                    break
            if data_idx >= len(binary_msg):
                break

        # Save to buffer
        buf = io.BytesIO()
        encoded_img.save(buf, format='PNG')
        buf.seek(0)

        return send_file(buf, mimetype='image/png', as_attachment=True,
                         download_name='encoded_image.png')

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/decode/image', methods=['POST'])
def decode_image():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        file = request.files['file']

        img = Image.open(file.stream)
        width, height = img.size

        binary_msg = ""
        for y in range(height):
            for x in range(width):
                pixel = img.getpixel((x, y))
                for i in range(min(len(pixel), 3)):
                    binary_msg += str(pixel[i] & 1)

        idx = binary_msg.find(DELIMITER)
        if idx == -1:
            return jsonify({'error': 'No hidden message found in this image!'}), 404

        message = binary_to_text(binary_msg[:idx])
        return jsonify({'message': message, 'length': len(message)})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ─────────────────────────────────────────────
#  AUDIO steganography
# ─────────────────────────────────────────────

def _convert_to_wav(input_path):
    """Convert any audio file to WAV using ffmpeg if available, otherwise try direct open."""
    wav_path = os.path.join(UPLOAD_FOLDER, f'{uuid.uuid4()}.wav')
    ffmpeg_path = shutil.which('ffmpeg')
    if ffmpeg_path:
        try:
            subprocess.run(
                [ffmpeg_path, '-y', '-i', input_path, '-acodec', 'pcm_s16le', '-ar', '44100', wav_path],
                check=True, capture_output=True, timeout=60
            )
            return wav_path
        except Exception:
            pass
    # If ffmpeg not available or failed, try using the file directly
    # (only works if the file is already WAV)
    return input_path


@app.route('/encode/audio', methods=['POST'])
def encode_audio():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        file = request.files['file']
        message = request.form.get('message', '').strip()
        if not message:
            return jsonify({'error': 'No message provided'}), 400

        # Save uploaded file temporarily
        original_ext = os.path.splitext(file.filename or '')[1] or '.wav'
        tmp_in = os.path.join(UPLOAD_FOLDER, f'{uuid.uuid4()}{original_ext}')
        file.save(tmp_in)

        # Convert to WAV if needed
        wav_in = _convert_to_wav(tmp_in)

        try:
            audio = wave.open(wav_in, mode='rb')
        except wave.Error:
            _cleanup_files(tmp_in, wav_in)
            return jsonify({'error': 'Unsupported audio format! Please upload a WAV file, or install ffmpeg for automatic conversion.'}), 400

        params = audio.getparams()
        frame_bytes = bytearray(list(audio.readframes(audio.getnframes())))
        audio.close()

        binary_msg = text_to_binary(message) + DELIMITER

        if len(binary_msg) > len(frame_bytes):
            _cleanup_files(tmp_in, wav_in)
            return jsonify({'error': f'Message too large! Needs {len(binary_msg)} bits, audio capacity is {len(frame_bytes)} bits.'}), 400

        for i in range(len(binary_msg)):
            frame_bytes[i] = (frame_bytes[i] & 254) | int(binary_msg[i])

        tmp_out = os.path.join(UPLOAD_FOLDER, f'{uuid.uuid4()}.wav')
        with wave.open(tmp_out, 'wb') as new_audio:
            new_audio.setparams(params)
            new_audio.writeframes(bytes(frame_bytes))

        _cleanup_files(tmp_in, wav_in)

        response = send_file(tmp_out, mimetype='audio/wav', as_attachment=True,
                             download_name='encoded_audio.wav')

        @response.call_on_close
        def cleanup():
            try:
                os.remove(tmp_out)
            except OSError:
                pass

        return response

    except Exception as e:
        return jsonify({'error': str(e)}), 500


def _cleanup_files(*paths):
    """Safely remove temp files."""
    for p in paths:
        if p and os.path.exists(p):
            try:
                os.remove(p)
            except OSError:
                pass


@app.route('/decode/audio', methods=['POST'])
def decode_audio():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        file = request.files['file']

        original_ext = os.path.splitext(file.filename or '')[1] or '.wav'
        tmp_in = os.path.join(UPLOAD_FOLDER, f'{uuid.uuid4()}{original_ext}')
        file.save(tmp_in)

        # Convert to WAV if needed
        wav_in = _convert_to_wav(tmp_in)

        try:
            audio = wave.open(wav_in, mode='rb')
        except wave.Error:
            _cleanup_files(tmp_in, wav_in)
            return jsonify({'error': 'Unsupported audio format! Please upload a WAV file, or install ffmpeg for automatic conversion.'}), 400

        frame_bytes = bytearray(list(audio.readframes(audio.getnframes())))
        audio.close()
        _cleanup_files(tmp_in, wav_in)

        binary_msg = ""
        for byte in frame_bytes:
            binary_msg += str(byte & 1)

        idx = binary_msg.find(DELIMITER)
        if idx == -1:
            return jsonify({'error': 'No hidden message found in this audio!'}), 404

        message = binary_to_text(binary_msg[:idx])
        return jsonify({'message': message, 'length': len(message)})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ─────────────────────────────────────────────
#  VIDEO steganography
# ─────────────────────────────────────────────

@app.route('/encode/video', methods=['POST'])
def encode_video():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        file = request.files['file']
        message = request.form.get('message', '').strip()
        if not message:
            return jsonify({'error': 'No message provided'}), 400

        # Save uploaded video, preserve original extension for OpenCV compatibility
        original_ext = os.path.splitext(file.filename or '')[1] or '.avi'
        tmp_in = os.path.join(UPLOAD_FOLDER, f'{uuid.uuid4()}{original_ext}')
        file.save(tmp_in)

        cap = cv2.VideoCapture(tmp_in)
        if not cap.isOpened():
            _cleanup_files(tmp_in)
            return jsonify({'error': 'Could not open video file! Please try a different format (AVI, MP4).'}), 400

        fps = int(cap.get(cv2.CAP_PROP_FPS)) or 30
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        binary_msg = text_to_binary(message) + DELIMITER

        if len(binary_msg) > width * height * 3:
            cap.release()
            _cleanup_files(tmp_in)
            return jsonify({'error': 'Message too large for this video frame! Use a higher resolution video or shorter message.'}), 400

        # Output as AVI with lossless codec FFV1 to preserve LSB data
        tmp_out = os.path.join(UPLOAD_FOLDER, f'{uuid.uuid4()}.avi')
        fourcc = cv2.VideoWriter_fourcc(*'FFV1')
        out = cv2.VideoWriter(tmp_out, fourcc, fps, (width, height))

        if not out.isOpened():
            cap.release()
            _cleanup_files(tmp_in)
            return jsonify({'error': 'Could not create output video. Codec issue on this system.'}), 500

        data_idx = 0
        frame_count = 0

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Encode in first frame only
            if frame_count == 0:
                for i in range(height):
                    for j in range(width):
                        if data_idx < len(binary_msg):
                            for k in range(3):
                                if data_idx < len(binary_msg):
                                    val = int(frame[i, j, k])
                                    val = (val & 0xFE) | int(binary_msg[data_idx])
                                    frame[i, j, k] = np.uint8(val)
                                    data_idx += 1
                        else:
                            break
                    if data_idx >= len(binary_msg):
                        break

            out.write(frame)
            frame_count += 1

        cap.release()
        out.release()
        _cleanup_files(tmp_in)

        if frame_count == 0:
            _cleanup_files(tmp_out)
            return jsonify({'error': 'No frames could be read from the video!'}), 400

        response = send_file(tmp_out, mimetype='video/x-msvideo', as_attachment=True,
                             download_name='encoded_video.avi')

        @response.call_on_close
        def cleanup():
            try:
                os.remove(tmp_out)
            except OSError:
                pass

        return response

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/decode/video', methods=['POST'])
def decode_video():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        file = request.files['file']

        original_ext = os.path.splitext(file.filename or '')[1] or '.avi'
        tmp_in = os.path.join(UPLOAD_FOLDER, f'{uuid.uuid4()}{original_ext}')
        file.save(tmp_in)

        cap = cv2.VideoCapture(tmp_in)
        ret, frame = cap.read()
        cap.release()
        _cleanup_files(tmp_in)

        if not ret:
            return jsonify({'error': 'Could not read video file!'}), 400

        height, width = frame.shape[:2]
        binary_msg = ""

        for i in range(height):
            for j in range(width):
                for k in range(3):
                    binary_msg += str(int(frame[i, j, k]) & 1)

        idx = binary_msg.find(DELIMITER)
        if idx == -1:
            return jsonify({'error': 'No hidden message found in this video!'}), 404

        message = binary_to_text(binary_msg[:idx])
        return jsonify({'message': message, 'length': len(message)})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ─────────────────────────────────────────────
#  Run
# ─────────────────────────────────────────────

if __name__ == '__main__':
    print("\n🔐 Steganography Web App starting on port 10000...")
    app.run(host='0.0.0.0', port=10000)
