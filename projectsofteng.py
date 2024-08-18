import cv2
from PIL import Image
from pytesseract import pytesseract
from gtts import gTTS
import pygame
import io

# Mengatur jalur eksekusi Tesseract
path_to_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
pytesseract.tesseract_cmd = path_to_tesseract

# Konfigurasi Tesseract untuk menggunakan bahasa Indonesia
language = 'ind'

# Inisialisasi pygame untuk audio
pygame.mixer.init()

# Inisialisasi kamera
camera = cv2.VideoCapture('http://192.168.1.4:8080/video')

while True:
    ret, frame = camera.read()
    if not ret:
        print("Failed to grab frame")
        break

    # cuma ngatur resolusi aja biar kualitas gambar dan framenya oke
    resized = cv2.resize(frame, (600, 400))
    cv2.imshow("Frame", resized)
    
    key = cv2.waitKey(1)
    
    if key == ord('c'):  # Menekan 'c' untuk ss gambar dari webcam
        pil_image = Image.fromarray(cv2.cvtColor(resized, cv2.COLOR_BGR2RGB))
        text = pytesseract.image_to_string(pil_image, lang=language)
        print("Detected Text:", text)

        # Baca teks yang dideteksi dalam bahasa Indonesia
        if text:
            tts = gTTS(text=text, lang='id')
            mp3_fp = io.BytesIO()
            tts.write_to_fp(mp3_fp)
            mp3_fp.seek(0)
            pygame.mixer.music.load(mp3_fp)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():  # Kita menunggu sampai audio selesai
                pygame.time.Clock().tick(10)
    
    if key == ord('q'):  # Tekan 'q' untuk keluar dari webcam
        break

camera.release()
cv2.destroyAllWindows()