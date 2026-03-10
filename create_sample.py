import wave
import math
import struct

# Audio parameters
sample_rate = 44100
duration = 5.0  # seconds
frequency = 440.0  # Hz

# Generate audio frames
print("Generating 5-second sample audio...")
with wave.open('sample_audio.wav', 'w') as wav_file:
    wav_file.setnchannels(1)  # Mono
    wav_file.setsampwidth(2)  # 2 bytes per sample
    wav_file.setframerate(sample_rate)
    
    for i in range(int(duration * sample_rate)):
        value = int(32767.0 * math.sin(2.0 * math.pi * frequency * i / sample_rate))
        data = struct.pack('<h', value)
        wav_file.writeframes(data)

print(f"✅ sample_audio.wav created successfully!")
