import numpy as np
import cv2
import math


# --- 1. Модуль Векторизации и Поиска (Visual Search) ---
class VectorSearchEngine:
    def __init__(self):
        # Локальная база: {"Имя товара": [список_векторов]}
        self.db = {}

    def extract_features(self, frame):
        """
        Простая заглушка векторайзера на базе гистограммы цветов OpenCV (для MVP).
        В боевой версии замените на PyTorch MobileNetV3 / ONNX Runtime.
        """
        resized = cv2.resize(frame, (128, 128))
        hsv = cv2.cvtColor(resized, cv2.COLOR_BGR2HSV)
        # Считаем цветовой профиль еды как простой вектор из 512 значений
        hist = cv2.calcHist([hsv], [0, 1, 2], None, [8, 8, 8], [0, 180, 0, 256, 0, 256])
        vector = cv2.normalize(hist, hist).flatten()
        return vector

    def add_product(self, name, frame):
        vector = self.extract_features(frame)
        if name not in self.db:
            self.db[name] = []
        self.db[name].append(vector)

    def find_similar(self, frame, top_k=3):
        if not self.db:
            return []

        target_vec = self.extract_features(frame)
        scores = []

        for name, vectors in self.db.items():
            # Находим наилучшее совпадение среди сохраненных фото товара
            max_sim = max([np.dot(target_vec, v) for v in vectors])
            scores.append((name, float(max_sim)))

        # Сортируем по убыванию сходства
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]


# --- 2. Модуль Распознавания Весов M-ER 327 ---
class ScaleReader:
    @staticmethod
    def read_weight(frame, crop_box=None):
        """
        crop_box: (x1, y1, x2, y2) — область табло весов
        """
        if crop_box:
            x1, y1, x2, y2 = crop_box
            frame = frame[y1:y2, x1:x2]

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Бинаризация для контрастности 7-сегментного табло
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # На ПК/Android передаем кадр в легкий движок Tesseract / EasyOCR
        # Для теста возвращаем mock-структуру
        return thresh