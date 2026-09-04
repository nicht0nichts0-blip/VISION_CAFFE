from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout

class FoodScaleApp(MDApp):
    def build(self):
        # Создаем главный экран
        screen = MDScreen()
        
        layout = MDBoxLayout(
            orientation='vertical', 
            spacing=20, 
            padding=20,
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        
        label = MDLabel(
            text="Food Scale Vision MVP", 
            halign="center",
            font_style="H4"
        )
        
        button = MDRaisedButton(
            text="Работает!", 
            pos_hint={'center_x': 0.5}
        )
        
        layout.add_widget(label)
        layout.add_widget(button)
        screen.add_widget(layout)
        
        return screen

if __name__ == '__main__':
    FoodScaleApp().run()
