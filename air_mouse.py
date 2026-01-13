import cv2
import mediapipe as mp
import pyautogui
import math

# Initialize tracking
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.8)
mp_draw = mp.solutions.drawing_utils
screen_width, screen_height = pyautogui.size()

# Smoothing & Toggle variables
plocX, plocY = 0, 0
smooth_factor = 5
boss_key_active = False

cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, img = cap.read()
    if not success: break
    img = cv2.flip(img, 1)
    h, w, _ = img.shape
    results = hands.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

    if results.multi_hand_landmarks:
        for hand_lms in results.multi_hand_landmarks:
            lms = hand_lms.landmark
            
            # 1. Finger Counting Logic
            # Tips: Index(8), Middle(12), Ring(16), Pinky(20)
            # Joints: Index(6), Middle(10), Ring(14), Pinky(18)
            fingers = []
            for tip, joint in [(8, 6), (12, 10), (16, 14), (20, 18)]:
                if lms[tip].y < lms[joint].y:
                    fingers.append(1)
                else:
                    fingers.append(0)

            total_fingers = sum(fingers)

            # 2. Boss Key (4 Fingers Up)
            if total_fingers == 4:
                cv2.putText(img, "BOSS KEY ACTIVATED", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                pyautogui.hotkey('win', 'd') # For Windows. Use ('command', 'm') for Mac
                pyautogui.sleep(1.0) # Pause to avoid flickering windows

            # 3. Air Mouse Logic (Only if 1 finger is up - the index)
            elif total_fingers == 1 and fingers[0] == 1:
                target_x = screen_width * lms[8].x
                target_y = screen_height * lms[8].y
                
                clocX = plocX + (target_x - plocX) / smooth_factor
                clocY = plocY + (target_y - plocY) / smooth_factor
                pyautogui.moveTo(clocX, clocY)
                plocX, plocY = clocX, clocY

                # Pinch to click
                dist = math.sqrt((lms[8].x - lms[4].x)**2 + (lms[8].y - lms[4].y)**2)
                if dist < 0.05:
                    pyautogui.click()
                    cv2.circle(img, (int(lms[8].x*w), int(lms[8].y*h)), 15, (0,255,0), cv2.FILLED)

            mp_draw.draw_landmarks(img, hand_lms, mp_hands.HAND_CONNECTIONS)

    cv2.imshow("AuraLink Boss Edition", img)
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()