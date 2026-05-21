import cv2
import mediapipe as mp
import time
import serial

# ====== CONNECT TO ARDUINO ======
arduino_port = "COM9"
arduino = serial.Serial(arduino_port, 9600)
time.sleep(2)

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)


def fingers_up(hand_landmarks):
    tips_ids = [8, 12, 16, 20]
    pips_ids = [6, 10, 14, 18]

    fingers = []
    for tip, pip in zip(tips_ids, pips_ids):
        fingers.append(
            1 if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[pip].y else 0
        )
    return fingers


def main():

    # ===== STATE MACHINE =====
    stable_gesture = "none"
    gesture_frames = 0
    GESTURE_LIMIT = 6

    last_sent = "none"

    with mp_hands.Hands(
        max_num_hands=1,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.5,
    ) as hands:

        while True:
            ret, frame = cap.read()

            if not ret:
                print("Camera failed.")
                break

            frame = cv2.flip(frame, 1)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb)

            current_gesture = "none"

            # ===== DETECT HAND =====
            if results.multi_hand_landmarks:
                hand_landmarks = results.multi_hand_landmarks[0]

                mp_draw.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                )

                fingers = fingers_up(hand_landmarks)

                # cleaner matching (more stable than exact lists)
                index_up = fingers[0] == 1 and sum(fingers[1:]) == 0
                index_middle_up = fingers[0] == 1 and fingers[1] == 1 and sum(fingers[2:]) == 0
                middle_ring_pinky_up = fingers[0] == 0 and fingers[1:] == [1, 1, 1]

                if index_up:
                    current_gesture = "spray1"
                elif index_middle_up:
                    current_gesture = "spray2"
                elif middle_ring_pinky_up:
                    current_gesture = "spray3"
                else:
                    current_gesture = "none"

                cv2.putText(frame, f"fingers={fingers}", (50, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

            # ===== STABILITY CHECK =====
            if current_gesture == stable_gesture:
                gesture_frames += 1
            else:
                stable_gesture = current_gesture
                gesture_frames = 0

            # ===== ONLY TRIGGER WHEN STABLE =====
            if gesture_frames >= GESTURE_LIMIT:

                # only send once per gesture change
                if stable_gesture != last_sent:

                    if stable_gesture == "spray1":
                        arduino.write(b'1')

                    elif stable_gesture == "spray2":
                        arduino.write(b'2')

                    elif stable_gesture == "spray3":
                        arduino.write(b'3')

                    elif stable_gesture == "none":
                        arduino.write(b'0')  # return to start

                    last_sent = stable_gesture

            # ===== UI =====
            cv2.putText(frame, f"Gesture: {stable_gesture}", (50, 120),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            cv2.putText(frame, f"Frames: {gesture_frames}", (50, 170),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

            cv2.imshow("Hand + Finger Tracking", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()
    arduino.close()


if __name__ == "__main__":
    main()
