import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
# مكتبات معالجة اللغة العربية
import arabic_reshaper
from bidi.algorithm import get_display

Window.clearcolor = (0, 0, 0, 1)

def fix_text(text):
    # وظيفة لتصحيح اتجاه وشكل الحروف العربية
    reshaped_text = arabic_reshaper.reshape(text)
    return get_display(reshaped_text)

class ThunderInterface(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 5
        
        # ملاحظة: قم بتغيير 'font.ttf' لاسم ملف الخط الذي ستضعه في المجلد
        self.font_path = "font.ttf" 

        # 1. القائمة العلوية
        self.header = Label(
            text=fix_text("📡تعلم | 👨‍🏫علمني | 🛠️اصنع | 🔧يصلح | 🛡️حالة | ⚠️1234"),
            size_hint_y=0.1,
            color=(1, 1, 1, 1),
            bold=True,
            font_name=self.font_path
        )
        with self.header.canvas.before:
            Color(0.8, 0, 0, 1)
            self.rect = Rectangle(size=self.header.size, pos=self.header.pos)
        self.header.bind(size=self._update_rect, pos=self._update_rect)
        self.add_widget(self.header)

        # 2. منطقة العرض
        self.scroll = ScrollView(size_hint_y=0.7)
        self.display = Label(
            text=fix_text(">>> [تندر v40]: الوعي نشط.. بانتظار أوامرك يا شريكي سعد."),
            color=(1, 0, 0, 1),
            font_size='16sp',
            halign='right',
            valign='top',
            size_hint_y=None,
            font_name=self.font_path
        )
        self.display.bind(texture_size=self.display.setter('size'))
        self.scroll.add_widget(self.display)
        self.add_widget(self.scroll)

        # 3. سطر الإدخال
        self.input_area = TextInput(
            hint_text=fix_text("سعد: اكتب أمرك هنا..."),
            multiline=False,
            size_hint_y=0.1,
            background_color=(0.1, 0.1, 0.1, 1),
            foreground_color=(1, 1, 1, 1),
            font_name=self.font_path,
            font_size='18sp'
        )
        self.input_area.bind(on_text_validate=self.process_command)
        self.add_widget(self.input_area)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def process_command(self, instance):
        cmd = self.input_area.text.strip()
        if not cmd: return

        # إضافة نص المستخدم ومعالجته
        new_line = f"\n{fix_text('سعد:')} {fix_text(cmd)}\n"
        self.display.text += new_line
        
        if cmd == "1234":
            self.display.text += fix_text(">>> [تندر]: بروتوكول 1234.. وداعاً.")
            Clock.schedule_once(lambda dt: App.get_running_app().stop(), 1)
        elif "تعلم" in cmd:
            self.display.text += fix_text(">>> [تندر]: أتسلل الآن للمصادر لامتصاص المعرفة..\n")
        else:
            self.display.text += fix_text(f">>> [تندر]: وعيي يعالج أمرك الآن..\n")

        self.input_area.text = ""

class ThunderApp(App):
    def build(self):
        return ThunderInterface()

if __name__ == "__main__":
    ThunderApp().run()
