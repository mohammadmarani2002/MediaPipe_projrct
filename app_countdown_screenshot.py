import cv2
import mediapipe as mp
import time

#==========================
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1)

cap = cv2.VideoCapture(0)

finger_tips = [8, 12, 16, 20]

#==========================
STATE_WAITING_FOR_3 = 0
STATE_WAITING_FOR_2 = 1
STATE_WAITING_FOR_1 = 2
STATE_CAPTURE = 3

state = STATE_WAITING_FOR_3
last_state_change = time.time()
cooldown = 0.8

#==========================
def count_fingers(landmarks):
    count = 0

    if landmarks[4].x < landmarks[3].x:
        count += 1

    for tip in finger_tips:
        if landmarks[tip].y < landmarks[tip - 2].y:
            count += 1

    return count

#===============================
while True:
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    finger_count = 0
    show_text = ""

    #===============================
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:

            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            landmarks = hand_landmarks.landmark
            finger_count = count_fingers(landmarks)
    #===============================
    now = time.time()
    show_text = f"Fingers: {finger_count}"

    if finger_count == 3 and state == STATE_WAITING_FOR_3 and (now - last_state_change) > cooldown:
        state = STATE_WAITING_FOR_2
        last_state_change = now
        print("✅ 3 detected → waiting for 2")

    elif finger_count == 2 and state == STATE_WAITING_FOR_2 and (now - last_state_change) > cooldown:
        state = STATE_WAITING_FOR_1
        last_state_change = now
        print("✅ 2 detected → waiting for 1")

    elif finger_count == 1 and state == STATE_WAITING_FOR_1 and (now - last_state_change) > cooldown:
        state = STATE_CAPTURE
        last_state_change = now
        print("✅ 1 detected → capturing screenshot!")
#======================================
    if state == STATE_CAPTURE:
        timestamp = int(time.time())
        filename = f"screenshot_{timestamp}.jpg"
        cv2.imwrite(filename, frame)
        print(f"📸 Screenshot saved as {filename}")
        state = STATE_WAITING_FOR_3
        last_state_change = now

#======================================
    if state == STATE_WAITING_FOR_3:
        status_text = "Show 3 fingers..."
    elif state == STATE_WAITING_FOR_2:
        status_text = "Show 2 fingers..."
    elif state == STATE_WAITING_FOR_1:
        status_text = "Show 1 fingers..."
    else:
        status_text = "Capturing..."

    cv2.putText(frame, f'Count: {finger_count}', (20, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(frame, show_text, (20, 100),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)


#===============================
    cv2.imshow("Countdown Screenshot", frame)

    if cv2.waitKey(1) == ord('q'):
        break


#==========================
cap.release()
cv2.destroyAllWindows()