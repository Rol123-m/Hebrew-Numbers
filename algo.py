from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.core.text import LabelBase
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.animation import Animation
from kivy.core.audio import SoundLoader
import random
from bidi.algorithm import get_display

# Registrar la fuente personalizada
LabelBase.register(name='DejaVuSans', fn_regular='DejaVuSans.ttf')

# Lista de pronombres y sus combinaciones con "לְ"
pronombres = {
    "אֲנִי": "לִי",
    "אַתָּה": "לְךָ",
    "אַתְּ": "לָךְ",
    "הוּא": "לוֹ",
    "הִיא": "לָהּ",
    "אֲנַחְנוּ": "לָנוּ",
    "אַתֶּם": "לָכֶם",
    "אַתֶּן": "לָכֶן",
    "הֵם": "לָהֶם",
    "הֵן": "לָהֶן"
}

class HebrewGame(BoxLayout):
    def __init__(self, **kwargs):
        super(HebrewGame, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.correct_score = 0
        self.incorrect_score = 0
        self.question_count = 0
        self.max_questions = 10

        # Sonidos
        self.correct_sound = SoundLoader.load('correct.mp3')
        self.incorrect_sound = SoundLoader.load('incorrect.mp3')
        self.success_sound = SoundLoader.load('success.mp3')
        self.try_again_sound = SoundLoader.load('try_again.mp3')

        # Añadir el Label para la puntuación
        self.score_label = Label(text='Puntuación: 0', font_name='DejaVuSans', font_size=24)
        self.add_widget(self.score_label)

        self.create_question()

    def create_question(self, *args):
        self.clear_widgets()
        self.add_widget(self.score_label)

        if self.question_count >= self.max_questions:
            self.show_final_screen()
            return
        
        self.question_count += 1
        self.pronoun, self.correct_answer = random.choice(list(pronombres.items()))
        options = [self.correct_answer] + random.sample(list(set(pronombres.values()) - {self.correct_answer}), 2)
        random.shuffle(options)

        question_label = Label(
            text=f'לְ + {get_display(self.pronoun)} = ?', 
            font_name='DejaVuSans', 
            font_size=32, 
            halign='center', 
            text_size=(self.width, None), 
            base_direction='rtl'
        )
        self.add_widget(question_label)

        for option in options:
            btn = Button(
                text=get_display(option), 
                font_name='DejaVuSans', 
                font_size=32, 
                on_press=self.check_answer
            )
            self.add_widget(btn)

    def check_answer(self, instance):
        if instance.text == get_display(self.correct_answer):
            self.correct_score += 1
            if self.correct_sound:
                self.correct_sound.play()
            popup = Popup(
                title='Correcto', 
                content=Label(text='¡Correcto!', font_name='DejaVuSans', font_size=24), 
                size_hint=(0.5, 0.5)
            )
        else:
            self.incorrect_score += 1
            if self.incorrect_sound:
                self.incorrect_sound.play()
            popup = Popup(
                title='Incorrecto', 
                content=Label(text=f'Incorrecto. La respuesta correcta es: {get_display(self.correct_answer)}', font_name='DejaVuSans', font_size=24), 
                size_hint=(0.5, 0.5)
            )

        # Actualizar el Label de puntuación
        self.score_label.text = f'Puntuación: {self.correct_score}'
        
        popup.open()
        popup.bind(on_dismiss=self.create_question)

    def show_final_screen(self):
        self.clear_widgets()
        layout = FloatLayout()

        if self.correct_score > self.incorrect_score:
            message = f"¡Felicidades! Has obtenido más respuestas correctas que incorrectas.\nPuntuación final: {self.correct_score}"
            img_src = 'success_image.JPG'
            if self.success_sound:
                self.success_sound.play()
        else:
            message = f"¡Inténtalo de nuevo! Puedes hacerlo mejor la próxima vez.\nPuntuación final: {self.correct_score}"
            img_src = 'try_again_image.JPG'
            if self.try_again_sound:
                self.try_again_sound.play()

        label = Label(
            text=message, 
            font_name='DejaVuSans', 
            font_size=32, 
            halign='center', 
            valign='middle',
            size_hint=(0.8, 0.2),
            pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )
        layout.add_widget(label)

        img = Image(
            source=img_src, 
            size_hint=(0.4, 0.4), 
            pos_hint={'center_x': 0.5, 'center_y': 0.4}
        )
        layout.add_widget(img)

        # Animación para la imagen
        anim = Animation(size_hint=(0.5, 0.5), duration=1) + Animation(size_hint=(0.4, 0.4), duration=1)
        anim.repeat = True

        def start_animation(*args):
            anim.start(img)

        layout.bind(on_parent=start_animation)

        self.add_widget(layout)

class HebrewApp(App):
    def build(self):
        return HebrewGame()

if __name__ == "__main__":
    HebrewApp().run()
