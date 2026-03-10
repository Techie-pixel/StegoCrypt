"""
Simple Command-Line Demo of Image Steganography
Use this for quick testing without GUI
"""

from PIL import Image
import os


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


def encode_image_simple(image_path, message, output_path):
    """Encode message in image using LSB"""
    print(f"\n🔒 Encoding message in image...")
    
    # Load image
    img = Image.open(image_path)
    img = img.convert('RGB')
    encoded = img.copy()
    width, height = img.size
    
    # Convert message to binary with delimiter
    binary_msg = text_to_binary(message)
    binary_msg += '1111111111111110'  # Delimiter
    
    # Check if message fits
    max_bytes = width * height * 3
    if len(binary_msg) > max_bytes:
        print(f"❌ Error: Message too large!")
        print(f"   Message: {len(binary_msg)} bits")
        print(f"   Capacity: {max_bytes} bits")
        return False
    
    # Encode message
    data_index = 0
    for y in range(height):
        for x in range(width):
            if data_index < len(binary_msg):
                pixel = list(img.getpixel((x, y)))
                
                # Modify RGB channels
                for i in range(3):
                    if data_index < len(binary_msg):
                        pixel[i] = pixel[i] & ~1 | int(binary_msg[data_index])
                        data_index += 1
                
                encoded.putpixel((x, y), tuple(pixel))
            else:
                break
        if data_index >= len(binary_msg):
            break
    
    # Save
    encoded.save(output_path, "PNG")
    print(f"✅ Message encoded successfully!")
    print(f"   Original: {image_path}")
    print(f"   Encoded: {output_path}")
    print(f"   Message length: {len(message)} characters")
    return True


def decode_image_simple(image_path):
    """Decode message from image"""
    print(f"\n🔓 Decoding message from image...")
    
    # Load image
    img = Image.open(image_path)
    width, height = img.size
    
    # Extract binary data
    binary_msg = ""
    for y in range(height):
        for x in range(width):
            pixel = img.getpixel((x, y))
            
            # Extract from RGB channels
            for i in range(3):
                binary_msg += str(pixel[i] & 1)
    
    # Find delimiter
    delimiter = '1111111111111110'
    delimiter_pos = binary_msg.find(delimiter)
    
    if delimiter_pos == -1:
        print("❌ No hidden message found!")
        return None
    
    # Convert to text
    binary_msg = binary_msg[:delimiter_pos]
    message = binary_to_text(binary_msg)
    
    print(f"✅ Message decoded successfully!")
    print(f"   Message: {message}")
    return message


def demo():
    """Run a complete demo"""
    print("="*60)
    print("       STEGANOGRAPHY DEMO - IMAGE ENCODING/DECODING")
    print("="*60)
    
    # Check if test image exists
    if not os.path.exists("test_image.png"):
        print("\n📝 Creating test image...")
        # Create a simple test image
        from PIL import Image
        img = Image.new('RGB', (100, 100), color='lightblue')
        img.save("test_image.png")
        print("✅ Test image created: test_image.png")
    
    # Demo message
    message = "Hello! This is a secret message hidden in the image! 🔐"
    
    print(f"\n📨 Message to hide: {message}")
    print(f"   Length: {len(message)} characters")
    
    # Encode
    success = encode_image_simple("test_image.png", message, "encoded_image.png")
    
    if success:
        # Decode
        decoded = decode_image_simple("encoded_image.png")
        
        # Verify
        if decoded == message:
            print("\n" + "="*60)
            print("✅ SUCCESS! Message encoded and decoded correctly!")
            print("="*60)
        else:
            print("\n❌ ERROR: Decoded message doesn't match!")
    
    print("\n💡 Files created:")
    print("   - test_image.png (original)")
    print("   - encoded_image.png (with hidden message)")
    print("\n🚀 Now try the GUI: python steganography_app.py")


def interactive_mode():
    """Interactive command-line mode"""
    print("\n" + "="*60)
    print("           INTERACTIVE STEGANOGRAPHY MODE")
    print("="*60)
    
    while True:
        print("\nOptions:")
        print("1. Encode message in image")
        print("2. Decode message from image")
        print("3. Run demo")
        print("4. Exit")
        
        choice = input("\nEnter choice (1-4): ").strip()
        
        if choice == "1":
            img_path = input("Enter image path: ").strip()
            if not os.path.exists(img_path):
                print("❌ Image not found!")
                continue
            
            message = input("Enter secret message: ").strip()
            output = input("Enter output path (e.g., encoded.png): ").strip()
            
            encode_image_simple(img_path, message, output)
        
        elif choice == "2":
            img_path = input("Enter encoded image path: ").strip()
            if not os.path.exists(img_path):
                print("❌ Image not found!")
                continue
            
            decode_image_simple(img_path)
        
        elif choice == "3":
            demo()
        
        elif choice == "4":
            print("\n👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid choice!")


if __name__ == "__main__":
    print("\n🎯 STEGANOGRAPHY - QUICK DEMO")
    print("\nChoose mode:")
    print("1. Run automatic demo")
    print("2. Interactive mode")
    
    mode = input("\nEnter choice (1 or 2): ").strip()
    
    if mode == "1":
        demo()
    elif mode == "2":
        interactive_mode()
    else:
        print("Invalid choice! Running demo...")
        demo()
