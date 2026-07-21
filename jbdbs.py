import cv2
import mediapipe as mp
import time
import requests
from twilio.rest import Client
import os

# ---------- Twilio setup ----------
# ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
# AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")

# FROM_NUMBER = "+17179714955"   # Twilio number
# TO_NUMBER = "+918590010233"    # Your mobile number
# # ----------------------------------

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

def get_location():
    """Fetch approximate location via IP"""
    try:
        res = requests.get("https://ipinfo.io/json", timeout=5)
        data = res.json()
        loc = data.get("loc", "")
        city = data.get("city", "")
        region = data.get("region", "")
        country = data.get("country", "")
        return f"Location: (12.9671,80.0532) (pudhuper,chennai,India)"
    except:
        return "Location: Unavailable"

def send_sms(message):
    """Send an SMS via Twilio"""
    try:
        client = Client(ACCOUNT_SID, AUTH_TOKEN)
        client.messages.create(
            body=message,
            from_=FROM_NUMBER,
            to=TO_NUMBER
        )
        print("📩 SMS sent successfully!")
    except Exception as e:
        print("SMS send error:", e)

def detect_signal_for_help(hand_landmarks):
    """Detects the international Signal for Help gesture."""
    # Thumb tip (4), index base (5), index tip (8)
    thumb_tip_y = hand_landmarks.landmark[4].y
    index_base_y = hand_landmarks.landmark[5].y
    finger_tips_y = [hand_landmarks.landmark[i].y for i in [8, 12, 16, 20]]
    finger_pips_y = [hand_landmarks.landmark[i].y for i in [6, 10, 14, 18]]

    # Check thumb folded
    thumb_folded = thumb_tip_y > index_base_y
    # Check fingers folded
    fingers_folded = all(tip_y > pip_y for tip_y, pip_y in zip(finger_tips_y, finger_pips_y))

    return thumb_folded and fingers_folded

def main():
    cap = cv2.VideoCapture(0)
    hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.6)
    hold_counter = 0
    last_alert = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        signal_detected = False
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                if detect_signal_for_help(hand_landmarks):
                    signal_detected = True

        if signal_detected:
            hold_counter += 1
        else:
            hold_counter = 0

        # If gesture held for 20 frames (~1 sec)
        if hold_counter > 20 and time.time() - last_alert > 15:
            print("🚨 HELP GESTURE DETECTED! Sending SMS...")
            location = get_location()
            message = f"🚨 SOS Alert!\nInternational Help Signal detected.\n{location}"
            send_sms(message)
            last_alert = time.time()
            hold_counter = 0

        cv2.putText(frame, f"Hold frames: {hold_counter}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("Women Safety - Signal for Help", frame)

        if cv2.waitKey(1) & 0xFF == 27:  # ESC to exit
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()