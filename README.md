# 🖐️ MediaPipe Hand & Face Detection

## 📌 معرفی
این پروژه با استفاده از **MediaPipe** و **OpenCV** قابلیت‌های زیر رو پیاده‌سازی کرده:
- تشخیص دست و شمارش انگشتان
- تشخیص حالت مشت و Victory
- تشخیص حالت چهره (خوشحالی، عصبانیت، ناراحتی، تعجب)

## 🛠️ تکنولوژی‌های استفاده‌شده
- Python 3.10+
- OpenCV
- MediaPipe
- NumPy

## 📂 ساختار پروژه


MediaPipe_project/
│
├── app_count_fingers.py          # شمارش انگشتان
├── app_fist_detection.py         # تشخیص مشت
├── app_victory.py                # تشخیص حالت Victory
├── app_face_emotion.py           # تشخیص حالت چهره
├── show_hand_landmark.py         # نمایش نقاط دست
└── requirements.txt              # لیست کتابخونه‌ها



## 🚀 نصب و اجرا


bash
# ۱. کلون کردن پروژه
git clone https://github.com/mohammadmarani2002/MediaPipe_project.git
cd MediaPipe_project

# ۲. ایجاد محیط مجازی
python -m venv venv
source venv/bin/activate  # برای لینوکس/مک
.\venv\Scripts\activate   # برای ویندوز

# ۳. نصب کتابخونه‌ها
pip install -r requirements.txt

# ۴. اجرا (مثال)
python app_count_fingers.py


📸 نمونه خروجی

(اسکرین‌شات به‌زودی اضافه می‌شود)

👨‍💻 نویسنده

محمد مرانی
                                                                                                      https://github.com/mohammadmarani2002

📝 نکات

· برای خروج از هر برنامه، کلید q رو بزنید.
· دوربین باید به‌درستی متصل باشه.
