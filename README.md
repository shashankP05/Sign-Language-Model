# ASL Sign Language Recognition

This project provides a GUI for American Sign Language (ASL) sign prediction using a MobileNetV2-based model trained with TensorFlow 2.10.1.

## Features
- Upload an image or use your webcam to predict ASL signs.
- Model is operational only between 6pm and 10pm (customizable in code).
- User-friendly Tkinter interface.

## Setup

1. **Clone or download this repository.**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Download the trained model:**
   - [Download the model from Google Drive](https://drive.google.com/drive/folders/1KNl-eraWztNUTyKHrfU3Jpcmd5pEGK6N?usp=drive_link)
   - Place the downloaded `.keras` model file in the project directory and update the `MODEL_PATH` in the code if needed.

## Usage

Run the GUI:
```bash
python GUI.py
```

- Click "Upload Image" to select an image for prediction.
- Click "Start Webcam" to use your webcam for real-time prediction.
- The model will only work between 6pm and 10pm. Outside this window, you will be notified.

## Notes
- The model was trained with images resized to 200x200 and pixel values scaled to [0, 1].
- If you want to change the operational hours, edit the `is_operational_time()` function in `GUI.py`.

## License
This project is for educational purposes.
