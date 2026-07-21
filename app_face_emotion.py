import cv2
import mediapipe as mp
import math
import sys

# ========================= تنظیمات اولیه =========================
mp_face_mesh = mp.solutions.face_mesh
mp_draw = mp.solutions.drawing_utils
face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1)

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ Error: Could not open camera.")
    sys.exit(1)

# ========================= توابع =========================
def euclidean_distance(point1, point2):
    """Calculate Euclidean distance between two points"""
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

def detect_emotion(landmarks):
    """
    Detect facial emotion based on MediaPipe FaceMesh landmarks
    Returns: (emotion, color)
    """
    # ===== نقاط لب (برای تشخیص خوشحالی و تعجب) =====
    upper_lip = landmarks[13]
    lower_lip = landmarks[14]
    left_mouth = landmarks[61]
    right_mouth = landmarks[291]

    # ===== نقاط ابرو (برای تشخیص عصبانیت و ناراحتی) =====
    left_eyebrow_inner = landmarks[46]
    right_eyebrow_inner = landmarks[276]
    left_eye_inner = landmarks[133]
    right_eye_inner = landmarks[362]

    # ===== نقاط چشم (برای تشخیص پلک زدن و خستگی) =====
    left_eye_top = landmarks[159]
    left_eye_bottom = landmarks[145]
    right_eye_top = landmarks[386]
    right_eye_bottom = landmarks[374]

    # ===== محاسبه نسبت‌ها =====
    mouth_height = euclidean_distance(upper_lip, lower_lip)
    mouth_width = euclidean_distance(left_mouth, right_mouth)
    mouth_ratio = mouth_height / mouth_width if mouth_width > 0 else 0

    left_brow_to_eye = euclidean_distance(left_eyebrow_inner, left_eye_inner)
    right_brow_to_eye = euclidean_distance(right_eyebrow_inner, right_eye_inner)
    brow_eye_ratio = (left_brow_to_eye + right_brow_to_eye) / 2

    left_eye_height = euclidean_distance(left_eye_top, left_eye_bottom)
    right_eye_height = euclidean_distance(right_eye_top, right_eye_bottom)
    avg_eye_height = (left_eye_height + right_eye_height) / 2

    # ===== تشخیص حالت‌ها =====
    if mouth_ratio > 0.35:
        return "😊 Happy", (0, 255, 0)
    elif mouth_ratio > 0.25 and avg_eye_height > 0.03:
        return "😮 Surprise", (255, 255, 0)
    elif brow_eye_ratio < 0.04:
        return "😠 Angry", (0, 0, 255)
    elif mouth_ratio > 0.15 and brow_eye_ratio > 0.07:
        return "😢 sad", (255, 0, 0)
    else:
        return "😐 Neutral", (255, 255, 255)

# ========================= حلقه اصلی =========================
print("🔄 press 'q' to quit.")

while True:
    ret, frame = cap.read()

    if not ret or frame is None:
        print("⚠️  Warning: Entry frame, skipping...")
        continue

    frame = cv2.flip(frame, 1)  # آینه‌ای کردن تصویر
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = face_mesh.process(rgb)

    emotion_text = "😐 No Face"
    color = (128, 128, 128)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            # رسم نقاط کلیدی روی صورت
            mp_draw.draw_landmarks(
                frame,
                face_landmarks,
                mp_face_mesh.FACEMESH_CONTOURS,
                landmark_drawing_spec=mp_draw.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=1),
                connection_drawing_spec=mp_draw.DrawingSpec(color=(255, 255, 255), thickness=1)
            )

            # تشخیص حالت چهره
            emotion_text, color = detect_emotion(face_landmarks.landmark)

    # نمایش حالت روی صفحه
    cv2.putText(
        frame,
        emotion_text,
        (30, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.2,
        color,
        3
    )

    cv2.imshow("Facial Emotion Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# ========================= پاکسازی =========================
cap.release()
cv2.destroyAllWindows()
print("👋 closed program.")