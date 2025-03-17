import cv2
import os
import time

# Path video input
video_path = 'dataset.mp4'  # Ganti dengan path video yang sesuai
output_folder = 'captured_frames'  # Folder untuk menyimpan gambar 4K

# Target resolusi 4K
TARGET_WIDTH = 3840
TARGET_HEIGHT = 2160

# Fungsi untuk menangkap dan menyimpan frame dengan resolusi 4K
def capture_and_save_frames_4k(video_path, output_folder, fps_target=100):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Tidak dapat membuka video")
        return

    # Mendapatkan resolusi asli video
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(f"Resolusi Video Asli: {width}x{height}")

    video_fps = cap.get(cv2.CAP_PROP_FPS) or 30  # Default jika tidak terdeteksi
    frame_interval = int(video_fps * 60 / fps_target)

    os.makedirs(output_folder, exist_ok=True)

    frame_count = 0
    saved_count = 0
    start_time = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % frame_interval == 0:
            # Upscale ke 4K menggunakan Lanczos interpolation untuk kualitas terbaik
            frame_4k = cv2.resize(frame, (TARGET_WIDTH, TARGET_HEIGHT), interpolation=cv2.INTER_LANCZOS4)

            filename = os.path.join(output_folder, f"frame_{saved_count:04d}_4k.jpg")
            cv2.imwrite(filename, frame_4k)
            saved_count += 1
            print(f"Disimpan: {filename}")

        frame_count += 1
        if time.time() - start_time > 60:
            break

    cap.release()
    print(f"Total gambar yang disimpan dalam resolusi 4K: {saved_count}")

# Jalankan fungsi
capture_and_save_frames_4k(video_path, output_folder)
