import tkinter as tk
from tkinter import filedialog, Label, Button, messagebox
from PIL import Image, ImageTk
import numpy as np
import cv2
import threading
from datetime import datetime
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array

# Load model and class labels
MODEL_PATH = r"C:\Users\shash\Desktop\sign\asl_model_final_mobilenet.keras"
model = load_model(MODEL_PATH)
# Update this list to match your class order
class_labels = [
    'A','B','C','D','del','E','F','G','H','I','J','K','L','M','N','nothing','O','P','Q','R','S','space','T','U','V','W','X','Y','Z'
]
IMG_SIZE = (200, 200)

# Check if current time is within allowed hours (6pm to 10pm)
def is_operational_time():
    now = datetime.now().time()
    start = now.replace(hour=18, minute=0, second=0, microsecond=0)
    end = now.replace(hour=22, minute=0, second=0, microsecond=0)
    return start <= now <= end

# Prediction function
def predict_image(img):
    img = img.resize(IMG_SIZE)
    arr = img_to_array(img) / 255.0
    arr = np.expand_dims(arr, axis=0)
    preds = model.predict(arr)
    idx = np.argmax(preds)
    return class_labels[idx]

# GUI class
class ASLApp:
    def __init__(self, master):
        self.master = master
        master.title("ASL Sign Prediction")
        self.label = Label(master, text="Upload an image or use webcam to predict ASL sign.")
        self.label.pack()
        self.img_label = Label(master)
        self.img_label.pack()
        self.result_label = Label(master, text="Prediction: ")
        self.result_label.pack()
        self.upload_btn = Button(master, text="Upload Image", command=self.upload_image)
        self.upload_btn.pack()
        self.webcam_btn = Button(master, text="Start Webcam", command=self.start_webcam)
        self.webcam_btn.pack()
        self.stop_btn = Button(master, text="Stop Webcam", command=self.stop_webcam, state=tk.DISABLED)
        self.stop_btn.pack()
        self.cap = None
        self.webcam_running = False

    def notify_time(self):
        messagebox.showinfo("Not Operational", "Model is only operational from 6pm to 10pm. Please come back later.")

    def upload_image(self):
        if not is_operational_time():
            self.notify_time()
            return
        file_path = filedialog.askopenfilename()
        if file_path:
            img = Image.open(file_path).convert('RGB')
            pred = predict_image(img)
            img_disp = img.resize((150, 150))
            img_tk = ImageTk.PhotoImage(img_disp)
            self.img_label.configure(image=img_tk)
            self.img_label.image = img_tk
            self.result_label.config(text=f"Prediction: {pred}")

    def start_webcam(self):
        if not is_operational_time():
            self.notify_time()
            return
        self.cap = cv2.VideoCapture(0)
        self.webcam_running = True
        self.webcam_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        threading.Thread(target=self.webcam_loop).start()

    def stop_webcam(self):
        self.webcam_running = False
        self.webcam_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        if self.cap:
            self.cap.release()
            self.cap = None
        self.img_label.config(image='')
        self.result_label.config(text="Prediction: ")

    def webcam_loop(self):
        while self.webcam_running and self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img_pil = Image.fromarray(img)
            pred = predict_image(img_pil)
            img_disp = img_pil.resize((150, 150))
            img_tk = ImageTk.PhotoImage(img_disp)
            self.img_label.configure(image=img_tk)
            self.img_label.image = img_tk
            self.result_label.config(text=f"Prediction: {pred}")
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        self.stop_webcam()

if __name__ == "__main__":
    root = tk.Tk()
    app = ASLApp(root)
    root.mainloop()
