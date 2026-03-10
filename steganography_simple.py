"""
Advanced Steganography Application
Image, Video & Audio Steganography with Modern UI
Hide and reveal secret messages in multimedia files!
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from PIL import Image
import cv2
import numpy as np
import wave
import os


class ModernSteganographyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🔐 Advanced Steganography Tool")
        self.root.geometry("900x750")
        self.root.configure(bg="#0a0e27")
        
        # Variables
        self.selected_file = None
        self.decode_file = None
        
        # Style configuration
        self.setup_styles()
        
        # Create UI
        self.create_ui()
    
    def setup_styles(self):
        """Configure modern ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure Notebook style
        style.configure(
            'TNotebook',
            background='#0a0e27',
            borderwidth=0
        )
        style.configure(
            'TNotebook.Tab',
            background='#1e2749',
            foreground='#a6b8e8',
            padding=[20, 10],
            font=('Arial', 11, 'bold')
        )
        style.map(
            'TNotebook.Tab',
            background=[('selected', '#2d3561')],
            foreground=[('selected', '#ffffff')]
        )
    
    def create_ui(self):
        # Header
        header_frame = tk.Frame(self.root, bg="#0a0e27")
        header_frame.pack(fill="x", pady=(20, 10))
        
        title = tk.Label(
            header_frame,
            text="🔐 ADVANCED STEGANOGRAPHY",
            font=("Arial", 26, "bold"),
            bg="#0a0e27",
            fg="#00d9ff"
        )
        title.pack()
        
        subtitle = tk.Label(
            header_frame,
            text="Hide & Reveal Secret Messages • Image • Video • Audio",
            font=("Arial", 12),
            bg="#0a0e27",
            fg="#7b8bb6"
        )
        subtitle.pack(pady=5)
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Create tabs
        self.image_tab = tk.Frame(self.notebook, bg="#1a1f3a")
        self.video_tab = tk.Frame(self.notebook, bg="#1a1f3a")
        self.audio_tab = tk.Frame(self.notebook, bg="#1a1f3a")
        
        self.notebook.add(self.image_tab, text="🖼️  IMAGE")
        self.notebook.add(self.video_tab, text="🎬  VIDEO")
        self.notebook.add(self.audio_tab, text="🎵  AUDIO")
        
        # Setup each tab
        self.setup_image_tab()
        self.setup_video_tab()
        self.setup_audio_tab()
        
        # Footer
        footer = tk.Label(
            self.root,
            text="Secure • Private • Undetectable",
            font=("Arial", 9),
            bg="#0a0e27",
            fg="#4a5578"
        )
        footer.pack(pady=10)
    
    def create_encode_section(self, parent, file_type):
        """Create reusable encode section"""
        # Encode Section Container
        encode_frame = tk.Frame(parent, bg="#1a1f3a")
        encode_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Encode Header
        encode_header = tk.Label(
            encode_frame,
            text="📥 ENCODE - HIDE MESSAGE",
            font=("Arial", 15, "bold"),
            bg="#1a1f3a",
            fg="#00ff88"
        )
        encode_header.pack(pady=(0, 20))
        
        # File Selection Button
        select_btn = tk.Button(
            encode_frame,
            text=f"📁 Select {file_type.upper()} File",
            command=lambda: self.select_file(f"encode_{file_type}"),
            bg="#00d9ff",
            fg="#000000",
            font=("Arial", 12, "bold"),
            cursor="hand2",
            padx=30,
            pady=15,
            relief="flat",
            borderwidth=0
        )
        select_btn.pack(pady=10)
        
        # File label
        file_label = tk.Label(
            encode_frame,
            text="No file selected",
            bg="#1a1f3a",
            fg="#7b8bb6",
            font=("Arial", 10)
        )
        file_label.pack(pady=5)
        
        # Message Input
        msg_label = tk.Label(
            encode_frame,
            text="✍️ Secret Message:",
            bg="#1a1f3a",
            fg="#ffffff",
            font=("Arial", 12, "bold")
        )
        msg_label.pack(pady=(20, 8))
        
        message_text = tk.Text(
            encode_frame,
            height=5,
            width=75,
            font=("Consolas", 11),
            bg="#2d3561",
            fg="#ffffff",
            insertbackground="#00ff88",
            relief="flat",
            padx=15,
            pady=15
        )
        message_text.pack(pady=5)
        
        # Encode Button
        encode_btn = tk.Button(
            encode_frame,
            text=f"🔒 ENCODE & SAVE {file_type.upper()}",
            command=lambda: self.encode_dispatch(file_type),
            bg="#00ff88",
            fg="#000000",
            font=("Arial", 13, "bold"),
            cursor="hand2",
            padx=35,
            pady=15,
            relief="flat",
            borderwidth=0
        )
        encode_btn.pack(pady=20)
        
        # Progress Label
        progress_label = tk.Label(
            encode_frame,
            text="",
            bg="#1a1f3a",
            fg="#ffd700",
            font=("Arial", 10, "italic")
        )
        progress_label.pack(pady=5)
        
        return file_label, message_text, progress_label
    
    def create_decode_section(self, parent, file_type):
        """Create reusable decode section"""
        # Separator
        separator = tk.Frame(parent, height=3, bg="#2d3561")
        separator.pack(fill="x", padx=30, pady=20)
        
        # Decode Section Container
        decode_frame = tk.Frame(parent, bg="#1a1f3a")
        decode_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Decode Header
        decode_header = tk.Label(
            decode_frame,
            text="📤 DECODE - REVEAL MESSAGE",
            font=("Arial", 15, "bold"),
            bg="#1a1f3a",
            fg="#ff6b9d"
        )
        decode_header.pack(pady=(0, 20))
        
        # Button Container
        btn_container = tk.Frame(decode_frame, bg="#1a1f3a")
        btn_container.pack(pady=10)
        
        # Select Encoded File Button
        select_decode_btn = tk.Button(
            btn_container,
            text=f"📁 Select Encoded {file_type.upper()}",
            command=lambda: self.select_file(f"decode_{file_type}"),
            bg="#7b8bb6",
            fg="#000000",
            font=("Arial", 11, "bold"),
            cursor="hand2",
            padx=25,
            pady=12,
            relief="flat",
            borderwidth=0
        )
        select_decode_btn.pack(side="left", padx=8)
        
        # Decode Button
        decode_btn = tk.Button(
            btn_container,
            text=f"🔓 DECODE MESSAGE",
            command=lambda: self.decode_dispatch(file_type),
            bg="#ff6b9d",
            fg="#000000",
            font=("Arial", 11, "bold"),
            cursor="hand2",
            padx=25,
            pady=12,
            relief="flat",
            borderwidth=0
        )
        decode_btn.pack(side="left", padx=8)
        
        # Decoded Message Display
        result_label = tk.Label(
            decode_frame,
            text="📝 Decoded Message:",
            bg="#1a1f3a",
            fg="#ffffff",
            font=("Arial", 12, "bold")
        )
        result_label.pack(pady=(25, 8))
        
        # ScrolledText for decoded message
        decoded_text = scrolledtext.ScrolledText(
            decode_frame,
            height=6,
            width=75,
            font=("Consolas", 11),
            bg="#2d3561",
            fg="#00ff88",
            relief="flat",
            padx=15,
            pady=15,
            wrap=tk.WORD
        )
        decoded_text.pack(pady=5)
        decoded_text.config(state='disabled')  # Read-only initially
        
        return decoded_text
    
    def setup_image_tab(self):
        """Setup Image Steganography Tab"""
        self.img_file_label, self.img_message_text, self.img_progress = \
            self.create_encode_section(self.image_tab, "image")
        self.img_decoded_text = self.create_decode_section(self.image_tab, "image")
    
    def setup_video_tab(self):
        """Setup Video Steganography Tab"""
        self.vid_file_label, self.vid_message_text, self.vid_progress = \
            self.create_encode_section(self.video_tab, "video")
        self.vid_decoded_text = self.create_decode_section(self.video_tab, "video")
    
    def setup_audio_tab(self):
        """Setup Audio Steganography Tab"""
        self.aud_file_label, self.aud_message_text, self.aud_progress = \
            self.create_encode_section(self.audio_tab, "audio")
        self.aud_decoded_text = self.create_decode_section(self.audio_tab, "audio")
    
    def select_file(self, file_type):
        """Handle file selection for different types"""
        if file_type == "encode_image":
            file_path = filedialog.askopenfilename(
                title="Select Image",
                filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp")]
            )
            if file_path:
                self.selected_file = file_path
                self.img_file_label.config(
                    text=f"✓ Selected: {os.path.basename(file_path)}",
                    fg="#00ff88"
                )
        
        elif file_type == "decode_image":
            file_path = filedialog.askopenfilename(
                title="Select Encoded Image",
                filetypes=[("PNG files", "*.png")]
            )
            if file_path:
                self.decode_file = file_path
                messagebox.showinfo("✓ File Selected", 
                    f"Ready to decode:\n{os.path.basename(file_path)}")
        
        elif file_type == "encode_video":
            file_path = filedialog.askopenfilename(
                title="Select Video",
                filetypes=[("Video files", "*.mp4 *.avi *.mkv *.mov")]
            )
            if file_path:
                self.selected_file = file_path
                self.vid_file_label.config(
                    text=f"✓ Selected: {os.path.basename(file_path)}",
                    fg="#00ff88"
                )
        
        elif file_type == "decode_video":
            file_path = filedialog.askopenfilename(
                title="Select Encoded Video",
                filetypes=[("Video files", "*.avi *.mp4")]
            )
            if file_path:
                self.decode_file = file_path
                messagebox.showinfo("✓ File Selected", 
                    f"Ready to decode:\n{os.path.basename(file_path)}")
        
        elif file_type == "encode_audio":
            file_path = filedialog.askopenfilename(
                title="Select Audio",
                filetypes=[("WAV files", "*.wav")]
            )
            if file_path:
                self.selected_file = file_path
                self.aud_file_label.config(
                    text=f"✓ Selected: {os.path.basename(file_path)}",
                    fg="#00ff88"
                )
        
        elif file_type == "decode_audio":
            file_path = filedialog.askopenfilename(
                title="Select Encoded Audio",
                filetypes=[("WAV files", "*.wav")]
            )
            if file_path:
                self.decode_file = file_path
                messagebox.showinfo("✓ File Selected", 
                    f"Ready to decode:\n{os.path.basename(file_path)}")
    
    def encode_dispatch(self, file_type):
        """Dispatch encoding to appropriate handler"""
        if file_type == "image":
            self.encode_image()
        elif file_type == "video":
            self.encode_video()
        elif file_type == "audio":
            self.encode_audio()
    
    def decode_dispatch(self, file_type):
        """Dispatch decoding to appropriate handler"""
        if file_type == "image":
            self.decode_image()
        elif file_type == "video":
            self.decode_video()
        elif file_type == "audio":
            self.decode_audio()
    
    # ==================== IMAGE STEGANOGRAPHY ====================
    def encode_image(self):
        if not self.selected_file:
            messagebox.showerror("❌ Error", "Please select an image first!")
            return
        
        message = self.img_message_text.get("1.0", "end-1c").strip()
        if not message:
            messagebox.showerror("❌ Error", "Please enter a message to hide!")
            return
        
        try:
            self.img_progress.config(text="⏳ Encoding in progress...")
            self.root.update()
            
            # Load image
            img = Image.open(self.selected_file)
            img = img.convert('RGB')
            encoded_img = img.copy()
            width, height = img.size
            
            # Convert message to binary with delimiter
            binary_message = ''.join(format(ord(char), '08b') for char in message)
            binary_message += '1111111111111110'  # Delimiter
            
            # Check capacity
            if len(binary_message) > width * height * 3:
                self.img_progress.config(text="")
                messagebox.showerror("❌ Error", 
                    f"Message too large!\n\n"
                    f"Message size: {len(binary_message)} bits\n"
                    f"Image capacity: {width * height * 3} bits\n\n"
                    f"Use a larger image or shorter message.")
                return
            
            # Encode message in LSB
            data_index = 0
            for y in range(height):
                for x in range(width):
                    if data_index < len(binary_message):
                        pixel = list(img.getpixel((x, y)))
                        
                        for i in range(3):  # RGB channels
                            if data_index < len(binary_message):
                                pixel[i] = pixel[i] & ~1 | int(binary_message[data_index])
                                data_index += 1
                        
                        encoded_img.putpixel((x, y), tuple(pixel))
                    else:
                        break
                if data_index >= len(binary_message):
                    break
            
            # Save encoded image
            save_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png")],
                initialfile="encoded_image.png"
            )
            
            if save_path:
                encoded_img.save(save_path, "PNG")
                self.img_progress.config(text="✓ Encoding complete!", fg="#00ff88")
                messagebox.showinfo("🎉 Success!", 
                    f"Message hidden successfully!\n\n"
                    f"📁 Saved: {os.path.basename(save_path)}\n"
                    f"📝 Message: {len(message)} characters\n"
                    f"🔒 Status: Encrypted & Hidden")
                self.img_message_text.delete("1.0", "end")
            else:
                self.img_progress.config(text="")
        
        except Exception as e:
            self.img_progress.config(text="")
            messagebox.showerror("❌ Error", f"Encoding failed:\n{str(e)}")
    
    def decode_image(self):
        if not self.decode_file:
            messagebox.showerror("❌ Error", "Please select an encoded image first!")
            return
        
        try:
            img = Image.open(self.decode_file)
            width, height = img.size
            
            binary_message = ""
            
            # Extract LSB from each pixel
            for y in range(height):
                for x in range(width):
                    pixel = img.getpixel((x, y))
                    
                    for i in range(3):  # RGB channels
                        binary_message += str(pixel[i] & 1)
            
            # Find delimiter
            delimiter = '1111111111111110'
            delimiter_index = binary_message.find(delimiter)
            
            if delimiter_index == -1:
                self.display_decoded_message(self.img_decoded_text, 
                    "❌ NO MESSAGE FOUND\n\nThis image does not contain any hidden message.")
                messagebox.showerror("❌ Error", 
                    "No hidden message found in this image!")
                return
            
            binary_message = binary_message[:delimiter_index]
            
            # Convert binary to text
            message = ""
            for i in range(0, len(binary_message), 8):
                byte = binary_message[i:i+8]
                if len(byte) == 8:
                    message += chr(int(byte, 2))
            
            # Display decoded message
            self.display_decoded_message(self.img_decoded_text, message)
            messagebox.showinfo("🎉 Success!", 
                f"Message revealed successfully!\n\n"
                f"📝 Length: {len(message)} characters")
        
        except Exception as e:
            messagebox.showerror("❌ Error", f"Decoding failed:\n{str(e)}")
    
    # ==================== VIDEO STEGANOGRAPHY ====================
    def encode_video(self):
        if not self.selected_file:
            messagebox.showerror("❌ Error", "Please select a video first!")
            return
        
        message = self.vid_message_text.get("1.0", "end-1c").strip()
        if not message:
            messagebox.showerror("❌ Error", "Please enter a message to hide!")
            return
        
        try:
            self.vid_progress.config(text="⏳ Encoding video... This may take a while...")
            self.root.update()
            
            cap = cv2.VideoCapture(self.selected_file)
            
            # Get video properties
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            # Save path
            save_path = filedialog.asksaveasfilename(
                defaultextension=".avi",
                filetypes=[("AVI files", "*.avi")],
                initialfile="encoded_video.avi"
            )
            
            if not save_path:
                cap.release()
                self.vid_progress.config(text="")
                return
            
            # Video writer
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            out = cv2.VideoWriter(save_path, fourcc, fps, (width, height))
            
            # Convert message to binary
            binary_message = ''.join(format(ord(char), '08b') for char in message)
            binary_message += '1111111111111110'  # Delimiter
            
            # Check capacity
            if len(binary_message) > width * height * 3:
                cap.release()
                out.release()
                self.vid_progress.config(text="")
                messagebox.showerror("❌ Error", 
                    "Message too large for video frame!\n"
                    "Use a higher resolution video or shorter message.")
                return
            
            data_index = 0
            frame_count = 0
            
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Encode in first frame only
                if frame_count == 0:
                    for i in range(height):
                        for j in range(width):
                            if data_index < len(binary_message):
                                pixel = frame[i, j]
                                
                                for k in range(3):  # BGR channels
                                    if data_index < len(binary_message):
                                        pixel[k] = pixel[k] & ~1 | int(binary_message[data_index])
                                        data_index += 1
                                
                                frame[i, j] = pixel
                            else:
                                break
                        if data_index >= len(binary_message):
                            break
                
                out.write(frame)
                frame_count += 1
                
                # Update progress
                if frame_count % 30 == 0:
                    progress = (frame_count / total_frames) * 100
                    self.vid_progress.config(
                        text=f"⏳ Processing: {progress:.1f}% ({frame_count}/{total_frames} frames)")
                    self.root.update()
            
            cap.release()
            out.release()
            
            self.vid_progress.config(text="✓ Encoding complete!", fg="#00ff88")
            messagebox.showinfo("🎉 Success!", 
                f"Message hidden in video!\n\n"
                f"📁 Saved: {os.path.basename(save_path)}\n"
                f"📝 Message: {len(message)} characters\n"
                f"🎬 Frames: {total_frames}")
            self.vid_message_text.delete("1.0", "end")
        
        except Exception as e:
            self.vid_progress.config(text="")
            messagebox.showerror("❌ Error", f"Encoding failed:\n{str(e)}")
    
    def decode_video(self):
        if not self.decode_file:
            messagebox.showerror("❌ Error", "Please select an encoded video first!")
            return
        
        try:
            cap = cv2.VideoCapture(self.decode_file)
            
            ret, frame = cap.read()
            if not ret:
                messagebox.showerror("❌ Error", "Could not read video file!")
                cap.release()
                return
            
            height, width = frame.shape[:2]
            binary_message = ""
            
            # Extract LSB from first frame
            for i in range(height):
                for j in range(width):
                    pixel = frame[i, j]
                    
                    for k in range(3):  # BGR channels
                        binary_message += str(pixel[k] & 1)
            
            cap.release()
            
            # Find delimiter
            delimiter = '1111111111111110'
            delimiter_index = binary_message.find(delimiter)
            
            if delimiter_index == -1:
                self.display_decoded_message(self.vid_decoded_text, 
                    "❌ NO MESSAGE FOUND\n\nThis video does not contain any hidden message.")
                messagebox.showerror("❌ Error", 
                    "No hidden message found in this video!")
                return
            
            binary_message = binary_message[:delimiter_index]
            
            # Convert binary to text
            message = ""
            for i in range(0, len(binary_message), 8):
                byte = binary_message[i:i+8]
                if len(byte) == 8:
                    message += chr(int(byte, 2))
            
            # Display decoded message
            self.display_decoded_message(self.vid_decoded_text, message)
            messagebox.showinfo("🎉 Success!", 
                f"Message revealed from video!\n\n"
                f"📝 Length: {len(message)} characters")
        
        except Exception as e:
            messagebox.showerror("❌ Error", f"Decoding failed:\n{str(e)}")
    
    # ==================== AUDIO STEGANOGRAPHY ====================
    def encode_audio(self):
        if not self.selected_file:
            messagebox.showerror("❌ Error", "Please select an audio file first!")
            return
        
        message = self.aud_message_text.get("1.0", "end-1c").strip()
        if not message:
            messagebox.showerror("❌ Error", "Please enter a message to hide!")
            return
        
        try:
            self.aud_progress.config(text="⏳ Encoding audio...")
            self.root.update()
            
            # Read audio file
            audio = wave.open(self.selected_file, mode='rb')
            frame_bytes = bytearray(list(audio.readframes(audio.getnframes())))
            
            # Convert message to binary
            binary_message = ''.join(format(ord(char), '08b') for char in message)
            binary_message += '1111111111111110'  # Delimiter
            
            # Check capacity
            if len(binary_message) > len(frame_bytes):
                audio.close()
                self.aud_progress.config(text="")
                messagebox.showerror("❌ Error", 
                    f"Message too large!\n\n"
                    f"Message size: {len(binary_message)} bits\n"
                    f"Audio capacity: {len(frame_bytes)} bits\n\n"
                    f"Use a longer audio file or shorter message.")
                return
            
            # Encode message in LSB of audio frames
            for i in range(len(binary_message)):
                frame_bytes[i] = (frame_bytes[i] & 254) | int(binary_message[i])
            
            # Save encoded audio
            save_path = filedialog.asksaveasfilename(
                defaultextension=".wav",
                filetypes=[("WAV files", "*.wav")],
                initialfile="encoded_audio.wav"
            )
            
            if save_path:
                frame_modified = bytes(frame_bytes)
                
                # Write new audio file
                with wave.open(save_path, 'wb') as new_audio:
                    new_audio.setparams(audio.getparams())
                    new_audio.writeframes(frame_modified)
                
                audio.close()
                
                self.aud_progress.config(text="✓ Encoding complete!", fg="#00ff88")
                messagebox.showinfo("🎉 Success!", 
                    f"Message hidden in audio!\n\n"
                    f"📁 Saved: {os.path.basename(save_path)}\n"
                    f"📝 Message: {len(message)} characters\n"
                    f"🔒 Status: Encrypted & Hidden")
                self.aud_message_text.delete("1.0", "end")
            else:
                audio.close()
                self.aud_progress.config(text="")
        
        except Exception as e:
            self.aud_progress.config(text="")
            messagebox.showerror("❌ Error", f"Encoding failed:\n{str(e)}")
    
    def decode_audio(self):
        if not self.decode_file:
            messagebox.showerror("❌ Error", "Please select an encoded audio file first!")
            return
        
        try:
            # Read audio file
            audio = wave.open(self.decode_file, mode='rb')
            frame_bytes = bytearray(list(audio.readframes(audio.getnframes())))
            audio.close()
            
            # Extract LSB
            binary_message = ""
            for byte in frame_bytes:
                binary_message += str(byte & 1)
            
            # Find delimiter
            delimiter = '1111111111111110'
            delimiter_index = binary_message.find(delimiter)
            
            if delimiter_index == -1:
                self.display_decoded_message(self.aud_decoded_text, 
                    "❌ NO MESSAGE FOUND\n\nThis audio file does not contain any hidden message.")
                messagebox.showerror("❌ Error", 
                    "No hidden message found in this audio!")
                return
            
            binary_message = binary_message[:delimiter_index]
            
            # Convert binary to text
            message = ""
            for i in range(0, len(binary_message), 8):
                byte = binary_message[i:i+8]
                if len(byte) == 8:
                    message += chr(int(byte, 2))
            
            # Display decoded message
            self.display_decoded_message(self.aud_decoded_text, message)
            messagebox.showinfo("🎉 Success!", 
                f"Message revealed from audio!\n\n"
                f"📝 Length: {len(message)} characters")
        
        except Exception as e:
            messagebox.showerror("❌ Error", f"Decoding failed:\n{str(e)}")
    
    def display_decoded_message(self, text_widget, message):
        """Display decoded message in text widget"""
        text_widget.config(state='normal')
        text_widget.delete(1.0, tk.END)
        text_widget.insert(1.0, message)
        text_widget.config(state='disabled')


def main():
    root = tk.Tk()
    app = ModernSteganographyApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()