from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.label import MDLabel
from kivy.graphics.texture import Texture
from kivy.uix.image import Image
from kivy.clock import Clock
import cv2

from main import VectorSearchEngine, ScaleReader


class FoodScaleApp(MDApp):
    def build(self):
        self.engine = VectorSearchEngine()
        self.capture = cv2.VideoCapture(0)  # 0 = встроенная камера / веб-камера

        layout = MDBoxLayout(orientation='vertical', padding=10, spacing=10)

        # Виджет видеопотока
        self.image_widget = Image()
        layout.add_widget(self.image_widget)

        # Результаты
        self.label_result = MDLabel(
            text="Наведите камеру на еду или весы",
            halign="center",
            theme_text_color="Primary"
        )
        layout.add_widget(self.label_result)

        # Кнопки управления
        btn_layout = MDBoxLayout(spacing=10, size_hint_y=0.2)

        # Исправленные кнопки для KivyMD 2.0+
        btn_scan_food = MDButton(
            style="elevated",  # Заменяет MDRaisedButton
            on_release=self.scan_food,
            size_hint=(0.5, 1)  # Устанавливаем размер
        )
        btn_scan_food.add_widget(MDButtonText(text="1. Сканировать еду"))

        btn_add_food = MDButton(
            style="elevated",
            on_release=self.add_food_dialog,
            size_hint=(0.5, 1)
        )
        btn_add_food.add_widget(MDButtonText(text="+ Добавить товар"))

        btn_layout.add_widget(btn_scan_food)
        btn_layout.add_widget(btn_add_food)

        layout.add_widget(btn_layout)

        # Обновление кадров (30 FPS)
        Clock.schedule_interval(self.update_frame, 1.0 / 30.0)
        return layout

    def update_frame(self, dt):
        ret, frame = self.capture.read()
        if ret:
            self.current_frame = frame
            # Конвертация кадра OpenCV для отображения в Kivy UI
            buf = cv2.flip(frame, 0).tobytes()
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='unsigned byte')
            self.image_widget.texture = texture

    def scan_food(self, instance):
        if hasattr(self, 'current_frame'):
            results = self.engine.find_similar(self.current_frame)
            if results:
                top_name, score = results[0]
                self.label_result.text = f"Распознано: {top_name} (Точность: {int(score * 100)}%)"
            else:
                self.label_result.text = "База пуста! Добавьте первый товар."

    def add_food_dialog(self, instance):
        # Для теста сохраняем базовый товар
        if hasattr(self, 'current_frame'):
            self.engine.add_product("Тестовое Блюдо", self.current_frame)
            self.label_result.text = "Сохранено 1 фото для 'Тестовое Блюдо'"


if __name__ == '__main__':
    FoodScaleApp().run()