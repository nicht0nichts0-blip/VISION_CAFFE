from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.selectioncontrol import MDSwitch
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField

from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivy.clock import Clock
from kivy.utils import platform

import cv2
import numpy as np

# --- 1. Модуль Векторного поиска (Visual Search) ---
class VectorSearchEngine:
    def __init__(self):
        # База данных: {"Имя товара": [список_векторов]}
        self.db = {}

    def extract_features(self, frame):
        """
        Преобразует кадр с едой в вектор (эмбеддинг).
        Для MVP используем HSV-гистограмму.
        """
        resized = cv2.resize(frame, (128, 128))
        hsv = cv2.cvtColor(resized, cv2.COLOR_BGR2HSV)
        hist = cv2.calcHist([hsv], [0, 1, 2], None, [8, 8, 8], [0, 180, 0, 256, 0, 256])
        return cv2.normalize(hist, hist).flatten()

    def add_product(self, name, frame):
        vec = self.extract_features(frame)
        if name not in self.db:
            self.db[name] = []
        self.db[name].append(vec)

    def find_similar(self, frame):
        if not self.db:
            return None, 0.0
        
        target_vec = self.extract_features(frame)
        best_name = None
        best_score = -1.0

        for name, vectors in self.db.items():
            for v in vectors:
                # Косинусное сходство / Dot product
                score = float(np.dot(target_vec, v))
                if score > best_score:
                    best_score = score
                    best_name = name

        return best_name, best_score

# --- 2. Модуль Считывания Весов ---
class ScaleReader:
    @staticmethod
    def read_weight(frame):
        # Предобработка кадра для 7-сегментного табло весов M-ER 327
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Заглушка для теста: возвращаем зафиксированный вес для MVP
        # В следующем шаге подключим Tesseract/EasyOCR
        return 0.350

# --- 3. Главный Интерфейс Приложения ---
class FoodScaleApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.engine = VectorSearchEngine()
        self.capture = None
        self.dialog = None

        screen = MDScreen()
        main_layout = MDBoxLayout(orientation='vertical', padding=10, spacing=10)

        # 1. Поток видео с камеры
        self.image_widget = Image()
        main_layout.add_widget(self.image_widget)

        # 2. Панель статуса и результатов
        self.label_status = MDLabel(
            text="Инициализация приложения...", 
            halign="center",
            font_style="Subtitle1",
            size_hint_y=0.1
        )
        main_layout.add_widget(self.label_status)

        # 3. Переключатель режима (Тест с 1 камеры / Поток 2 IP-камер)
        switch_layout = MDBoxLayout(orientation='horizontal', size_hint_y=0.08, spacing=10)
        switch_label = MDLabel(text="Тестовый режим (1 Камера телефона)", halign="right")
        self.test_mode_switch = MDSwitch(active=True)
        switch_layout.add_widget(switch_label)
        switch_layout.add_widget(self.test_mode_switch)
        main_layout.add_widget(switch_layout)

        # 4. Кнопки управления
        btn_layout = MDBoxLayout(spacing=10, size_hint_y=0.15)
        
        btn_scan_food = MDRaisedButton(text="1. Распознать еду", on_release=self.scan_food)
        btn_scan_weight = MDRaisedButton(text="2. Считывать вес", on_release=self.scan_weight)
        btn_add_product = MDRaisedButton(text="+ Добавить блюдо", on_release=self.open_add_dialog)

        btn_layout.add_widget(btn_scan_food)
        btn_layout.add_widget(btn_scan_weight)
        btn_layout.add_widget(btn_add_product)

        main_layout.add_widget(btn_layout)
        screen.add_widget(main_layout)
        return screen

    def on_start(self):
        # Запрос прав в runtime под Android
        if platform == 'android':
            from android.permissions import request_permissions, Permission
            request_permissions(
                [Permission.CAMERA, Permission.INTERNET],
                self.permission_callback
            )
        else:
            self.start_camera()

    def permission_callback(self, permissions, grants):
        if all(grants):
            Clock.schedule_once(lambda dt: self.start_camera(), 0.5)
        else:
            self.label_status.text = "Ошибка: Не даны разрешения на камеру!"

    def start_camera(self):
        try:
            # Открываем локальную камеру смартфона
            self.capture = cv2.VideoCapture(0)
            if not self.capture.isOpened():
                self.capture = cv2.VideoCapture(1)

            Clock.schedule_interval(self.update_frame, 1.0 / 30.0)
            self.label_status.text = "Камера готова к работе"
        except Exception as e:
            self.label_status.text = f"Ошибка камеры: {str(e)}"

    def update_frame(self, dt):
        if self.capture and self.capture.isOpened():
            ret, frame = self.capture.read()
            if ret:
                self.current_frame = frame
                # Конвертируем кадр под текстуру Kivy
                buf = cv2.flip(frame, 0).tobytes()
                texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
                texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='unsigned byte')
                self.image_widget.texture = texture

    # --- Функционал сканирования и добавления ---
    def scan_food(self, instance):
        if hasattr(self, 'current_frame'):
            name, score = self.engine.find_similar(self.current_frame)
            if name and score > 0.6:
                self.label_status.text = f"Блюдо: {name} (Уверенность: {int(score*100)}%)"
            else:
                self.label_status.text = "Блюдо не найдено в базе! Добавьте его."

    def scan_weight(self, instance):
        if hasattr(self, 'current_frame'):
            weight = ScaleReader.read_weight(self.current_frame)
            self.label_status.text = f"Вес с весов M-ER 327: {weight} кг"

    def open_add_dialog(self, instance):
        if not hasattr(self, 'current_frame'):
            return

        self.input_field = MDTextField(hint_text="Название блюда (напр. Плов)")
        self.dialog = MDDialog(
            title="Добавление блюда в векторную базу",
            type="custom",
            content_cls=self.input_field,
            buttons=[
                MDFlatButton(text="Отмена", on_release=lambda x: self.dialog.dismiss()),
                MDRaisedButton(text="Сохранить вектор", on_release=self.save_product)
            ],
        )
        self.dialog.open()

    def save_product(self, instance):
        prod_name = self.input_field.text.strip()
        if prod_name:
            self.engine.add_product(prod_name, self.current_frame)
            self.label_status.text = f"Товар '{prod_name}' сохранен в базу!"
        self.dialog.dismiss()

if __name__ == '__main__':
    FoodScaleApp().run()
