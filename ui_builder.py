"""
This module is responsible for building the user
interface for the Lyrics application.
"""
from typing import Callable, Tuple, List
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout


from kivy.graphics import Color, Rectangle

def build_ui(app):
    """
    Builds the main UI layout for the Lyrics application.
    """
    layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

    # Set background color for the main layout to black
    with layout.canvas.before:
        Color(0, 0, 0, 1)  # Black background
        layout.rect = Rectangle(size=layout.size, pos=layout.pos)
    layout.bind(size=update_rect, pos=update_rect)

    # Create the text input for lyrics with white background
    app.ui['lyrics_input'] = TextInput(
        multiline=True,
        background_color=[1, 1, 1, 1],  # White background
        foreground_color=[0, 0, 0, 1],  # Black text
        font_size='18sp'
    )
    app.ui['lyrics_input'].bind(text=app.on_text_change)

    # Create counter label with glowing neon green text
    app.ui['counter_label'] = Label(
        text="Bars: 0 | Syllables: 0 | AvgSyl: 0.00",
        size_hint_y=None,
        height=30,
        color=[0, 1, 0, 1]  # Neon green (RGB: 0, 255, 0)
    )

    # Create buttons layout
    buttons_layout = BoxLayout(
        orientation='horizontal',
        spacing=10,
        size_hint_y=None,
        height=50
    )

    # Create and add buttons with Zen Blue color
    zen_blue = [0.2, 0.4, 0.6, 1]  # Zen Blue (RGB: 51, 102, 153)
    buttons = [
        Button(text="Generate", on_press=app.generate_ai_suggestion, background_color=zen_blue),
        Button(text="Rhyme", on_press=lambda x: app.get_rhyme_suggestions(app), background_color=zen_blue),
        Button(text="Spell Check", on_press=app.start_spell_check, background_color=zen_blue),
        Button(text="Menu", on_press=app.show_menu_popup, background_color=zen_blue),
        Button(text="Undo", on_press=app.undo_action, background_color=zen_blue),
        Button(text="Redo", on_press=app.redo_action, background_color=zen_blue),
        Button(text="+", on_press=lambda x: app.increase_font_size(), background_color=zen_blue),
        Button(text="-", on_press=lambda x: app.decrease_font_size(), background_color=zen_blue),
    ]
    for button in buttons:
        buttons_layout.add_widget(button)

    # Add widgets to main layout
    layout.add_widget(app.ui['lyrics_input'])
    layout.add_widget(app.ui['counter_label'])
    layout.add_widget(buttons_layout)

    return layout

# Remove the update_rect function as it's no longer needed

def create_modern_button(text, callback):
    btn = Button(
        text=text,
        background_color=(0, 0, 0, 0),  # Transparent background
        color=(1, 1, 1, 1),  # White text
        size_hint=(None, None),
        size=(150, 40),
    )
    btn.bind(on_press=callback)
    
    def update_canvas(instance, value):
        instance.canvas.before.clear()
        with instance.canvas.before:
            Color(0.2, 0.6, 1, 1)  # Modern blue color
            RoundedRectangle(pos=instance.pos, size=instance.size, radius=[10,])

    btn.bind(pos=update_canvas, size=update_canvas)
    
    return btn

def create_button(text: str, on_press: Callable, size_hint: Tuple[float, float], 
                  background_color: List[float], color: List[float]) -> Button:
    """
    Creates a button with rounded corners.
    """
    button = Button(
        text=text,
        on_press=on_press,
        size_hint=size_hint,
        background_normal="",
        background_color=[0, 0, 0, 0],
        color=color,
    )
    with button.canvas.before:
        Color(*background_color)
        RoundedRectangle(pos=button.pos, size=button.size, radius=[15])

    def update_button_shape(instance, value):
        """
        Updates the button shape.
        """
        button.canvas.before.clear()
        with button.canvas.before:
            Color(*background_color)
            RoundedRectangle(pos=instance.pos, size=instance.size, radius=[15])

    button.bind(pos=update_button_shape, size=update_button_shape)

    return button

def create_menu_popup(app):
    content = BoxLayout(orientation='vertical', spacing=5, padding=10)
    buttons = [
        ('Help', app.show_help),
        ('Save', app.save_lyrics),
        ('Load', app.load_lyrics),
        ('Export', app.export_lyrics)
    ]
    for text, func in buttons:
        btn = Button(text=text, size_hint_y=None, height=40)
        btn.bind(on_press=func)
        content.add_widget(btn)
    
    popup = Popup(title='Menu', content=content, size_hint=(0.8, 0.8))
    return popup

def update_rect(instance, value):
    instance.rect.pos = instance.pos
    instance.rect.size = instance.size
