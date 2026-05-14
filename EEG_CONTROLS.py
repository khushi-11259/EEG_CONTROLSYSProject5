import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
import cv2
import serial
import time

# arduino part
arduino = serial.Serial('COM5', 9600)
time.sleep(2)

# matplotlib

import matplotlib

matplotlib.use('TkAgg')  # graph


# Generate EEG Signals
def generate_eeg(state):
    if state == "focus":
        return np.sin(np.linspace(0, 20, 100)) + np.random.rand(100) * 0.5
    else:
        return np.sin(np.linspace(0, 5, 100)) + np.random.rand(100) * 0.5


# PLOT PART
plt.ion()  # interaction point


def live_plot():
    plt.clf()
    plt.title("Real-Time EEG Signal")
    plt.xlabel("Time")
    plt.ylabel("Signal")

    signal = generate_eeg("focus")  # simulated signal
    plt.plot(signal)

    plt.pause(0.1)

    if not plt.fignum_exists(1):
        raise Exception("Graph closed")


X = []
y = []

for _ in range(100):
    X.append(generate_eeg("focus"))
    y.append(1)

    X.append(generate_eeg("relax"))
    y.append(0)

model = RandomForestClassifier()
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model.fit(X_train,y_train)

y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test,y_pred)
print(f"Model Accuracy: {accuracy * 100:.2f}%")

print("AI Model Ready!")


def detect_focus():
    cap = cv2.VideoCapture(0)

    print("Press 'q' to stop camera")

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            face_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            )

            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            if len(faces) > 0:
                state = "focus"
                cv2.putText(frame, "FOCUS", (50, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 8)
            else:
                state = "relax"
                cv2.putText(frame, "RELAX", (50, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 8)

            cv2.imshow("Brain Detection", frame)

            # Graph
            live_plot()

            # AI Prediction
            signal = generate_eeg(state)
            prediction = model.predict([signal])
            if prediction == 1:
                print("LED ON")
                arduino.write(b'1')
            else:
                print("LED OFF")
                arduino.write(b'0')

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                print("Exiting...")
                break

    except:
        print("Closed manually")

    finally:
        cap.release()
        cv2.destroyAllWindows()
        plt.close('all')


detect_focus()
