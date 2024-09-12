""" This module contains classes and functions for creating a dynamic loading
 screen in a Kivy application.

The loading screen features animated falling lyrics, a loading spinner,
and a customizable logo. It provides visual feedback to users while content
is being loaded, enhancing the overall user experience.

Classes:
    - CustomLoadingSpinner: A widget that displays a loading spinner with a
      shadow effect.
    - LoadingScreen: A screen that shows loading text, animated dots, and
      a logo.
    - RotatingLabel: A custom label widget that supports rotation.
    - FallingLyrics: A widget that displays animated falling lyrics.

Functions:
    - start_lyrics_animation: Initiates the animation of falling lyrics.
    - animate_lyric: Animates the movement of a lyric label and
      its shadow label.
    - update_rotation: Updates the rotation of a lyric label and
      its shadow label.
    - reset_lyric: Resets the lyric label and its shadow to a
    new random phrase and position.
"""

import random
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.widget import Widget
from kivy.graphics import Color, PushMatrix, PopMatrix, Rotate, Line
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.event import EventDispatcher
from all_phrases import all_phrases


class CustomLoadingSpinner(FloatLayout, EventDispatcher):
    """CustomLoadingSpinner is a widget that displays a loading
      spinner with a shadow effect.

    This class creates a visually appealing loading
      spinner that can be used to indicate that a process is ongoing.
    The spinner rotates and has a customizable size, thickness, and color.

    Attributes:
        spinner_size (int): The size of the spinner.
        spinner_thickness (int): The thickness of the spinner line.
        spinner_color (tuple): The color of the spinner in RGB format.
        shadow_color (tuple): The color of the shadow in RGBA format.
    """

    def __init__(self, **kwargs):
        """Initializes the spinner with specified
          attributes and starts the animation."""
        super(CustomLoadingSpinner, self).__init__(**kwargs)

        self.spinner_config = {
            'size': 80,
            'thickness': 5,
            'color': (0.33, 0.42, 0.18),
            'shadow_color': (0, 0, 0, 0.3)
        }

        with self.canvas:
            # Create shadow effect with gradient transparency
            PushMatrix()
            self.shadow_rotate = Rotate(origin=self.center)
            Color(*self.spinner_config['shadow_color'])
            self.shadow = Line(
                circle=(self.center_x, self.center_y,
                        self.spinner_config['size'] // 2),
                width=self.spinner_config['thickness'],
            )
            PopMatrix()

            # Draw the spinner with gradient effect
            PushMatrix()
            self.rotate = Rotate(origin=self.center)
            Color(*self.spinner_config['color'])
            self.spinner = Line(
                circle=(self.center_x, self.center_y,
                        self.spinner_config['size'] // 2),
                width=self.spinner_config['thickness'],
                cap="round",
            )
            PopMatrix()

        self.bind(pos=self.update_spinner, size=self.update_spinner)
        self.start_animation()

    def update_spinner(self, instance, value):
        """Updates the position and rotation of the spinner and shadow."""
        self.spinner.circle = (self.center_x, self.center_y,
                               self.spinner_config['size'] // 2)
        self.shadow.circle = (self.center_x + 3,
                              self.center_y - 3,
                              self.spinner_config['size'] // 2)
        self.rotate.origin = self.center
        self.shadow_rotate.origin = self.center

    def start_animation(self):
        """Animates the rotation of the spinner and its shadow."""
        anim = Animation(angle=360, duration=1)
        anim += Animation(angle=0, duration=0)
        anim.repeat = True
        anim.start(self.rotate)

        anim_shadow = Animation(angle=-360, duration=1)
        anim_shadow += Animation(angle=0, duration=0)
        anim_shadow.repeat = True
        anim_shadow.start(self.shadow_rotate)


class LoadingScreen(Screen):
    """
LoadingScreen is a widget that displays a loading screen with a logo,
 loading text, and animated dots.

This class initializes a loading screen that provides visual feedback to the
 user while content is being loaded. It includes a customizable logo,
   a loading message with animated dots, and a loading spinner.

Args:
    **kwargs: Additional keyword arguments to customize the widget.

Methods:
    animate_loading_text: Animates the loading text by cycling
    through different dot patterns.
"""

    def __init__(self, **kwargs):
        super(LoadingScreen, self).__init__(**kwargs)
        Window.clearcolor = (1, 1, 1, 1)  # Set background color to white

        # Initialize a layout to hold widgets
        self.layout = BoxLayout(orientation="vertical", padding=50, spacing=20)
        self.add_widget(self.layout)

        # Add loading label with animated dots
        self.loading_label_container = BoxLayout(
            orientation="horizontal", size_hint=(None, None)
        )
        self.layout.add_widget(self.loading_label_container)

        self.loading_label = Label(
            text="Loading",
            font_size="32sp",
            bold=True,
            color=[0, 0, 0, 1],  # Black text color
            size_hint=(None, None),
            size=(150, 50),
        )
        self.loading_label_container.add_widget(self.loading_label)

        # Add dots label next to loading text
        self.dots_label = Label(
            text=".",
            font_size="32sp",
            color=[0, 0, 0, 1],  # Black text color
            size_hint=(None, None),
            size=(50, 50),
        )
        self.loading_label_container.add_widget(self.dots_label)

        # Add the Image logo to the center of the screen
        self.logo_image = Image(
            source="C:/Users/eroge/Desktop/Rap_Writer/Logo/Logo.PNG",
            # Path to your image
            size_hint=(None, None),
            size=(800, 800),  # Adjust the size as needed
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            # Position in the center
        )
        self.add_widget(self.logo_image)

        # Add falling lyrics
        self.falling_lyrics = FallingLyrics()
        self.add_widget(self.falling_lyrics)

        # Add the custom loading spinner
        self.loading_spinner = CustomLoadingSpinner(
            size_hint=(None, None),
            size=(50, 50),
            pos_hint={"center_x": 0.5, "center_y": 0.1},
        )
        self.add_widget(self.loading_spinner)
        # Place at the bottom of the screen

        self.animate_loading_text()

    def animate_loading_text(self):
        """
Animates the loading text by cycling through different dot patterns.

This method updates the text of the loading dots label at regular intervals
 to create an animation effect. The dots will cycle through a maximum
 of six dots, resetting back to one dot after reaching the limit.

Args:
    None

Returns:
    None
"""


class RotatingLabel(Label, EventDispatcher):
    """
RotatingLabel is a custom label widget that supports rotation.

This class extends the standard Label widget to include
rotation functionality.
It allows for the label to be rotated around
a specified origin,
which can be useful for creating dynamic and visually appealing
user interfaces.

Args:
    **kwargs: Additional keyword arguments to customize the label.

Methods:
    update_rotation_origin: Updates the origin of rotation based on
    the label's position and size.
"""

    def __init__(self, **kwargs):
        super(RotatingLabel, self).__init__(**kwargs)
        self.angle = 0
        with self.canvas.before:
            PushMatrix()
            self.rotation = Rotate()
        with self.canvas.after:
            PopMatrix()

        self.bind(pos=self.update_rotation_origin,
                  size=self.update_rotation_origin)

    def update_rotation_origin(self, instance, value):
        """Updates the origin of rotation based on the label's
           position and size."""
        self.rotation.origin = self.center

    def set_rotation(self, angle):
        """This method updates the angle of rotation for the label,
        allowing it to be visually rotated to a specified angle.
        This can be used to create dynamic visual effects in
         the user interface."""
        self.rotation.angle = angle


class FallingLyrics(Widget):
    """
FallingLyrics is a widget that displays animated falling lyrics on the screen.

This class creates multiple lyric labels that fall from the top of the
screen to the bottom, providing a dynamic visual effect. Each lyric label is
accompanied by a shadow label, and both are animated to create a visually
appealing experience.

Args:
    **kwargs: Additional keyword arguments to customize the widget.

Methods:
    start_lyrics_animation: Initiates the animation of falling lyrics by
      creating and animating lyric and shadow labels.
    animate_lyric: Animates the movement and rotation of the lyric and
    shadow labels.
    update_rotation: Updates the rotation of the lyric and shadow labels
    based on a given value.
    reset_lyric: Resets the lyric label and its shadow to a new
    random phrase and position.
"""

    def __init__(self, **kwargs):
        super(FallingLyrics, self).__init__(**kwargs)

        self.color_palette = [
            [0.3, 0.6, 0.3, 1],
            [0.7, 0.4, 0.1, 1],
            [0.9, 0.9, 0.9, 1],
            [0.6, 0.3, 0.1, 1],
            [0.1, 0.4, 0.7, 1],
        ]

        self.start_lyrics_animation()

    def start_lyrics_animation(self):
        """Starts the animation of falling lyrics by creating and displaying
          lyric labels, This method generates a specified number of
          lyric labels that fall from the """

        for _ in range(10):
            color = random.choice(self.color_palette)
            text = random.choice(all_phrases)
            pos_x = random.randint(0, Window.width)
            pos_y = Window.height

            lyric_label = RotatingLabel(
                text=text,
                font_size="20sp",
                color=color,
                size_hint=(None, None),
                size=(200, 50),
                pos=(pos_x, pos_y),
            )

            shadow_label = RotatingLabel(
                text=text,
                font_size="20sp",
                color=[0, 0, 0, 0.5],
                size_hint=(None, None),
                size=(200, 50),
                pos=(pos_x + 2, pos_y - 2),
            )

            self.add_widget(shadow_label)
            self.add_widget(lyric_label)

            self.animate_lyric(lyric_label, shadow_label)

    def animate_lyric(self, label, shadow_label):
        """Animates the movement of a lyric label and its shadow label.

This method creates and starts animations for both the lyric label and
 its corresponding shadow label, making them move from their current
 position to the bottom of the screen. It also applies a random rotation
 and staggered timing to enhance the visual effect.
"""
        duration = random.uniform(2, 5)
        rotation = random.randint(-30, 30)
        stagger = random.uniform(0, 1)

        anim = Animation(pos=(label.x, -label.height),
                         duration=duration, t="linear")
        shadow_anim = Animation(
            pos=(shadow_label.x, -shadow_label.height),
            duration=duration, t="linear"
        )

        anim.bind(
            on_progress=lambda anim_instance,
            widget, value: self.update_rotation(
                label, shadow_label, rotation, value
            )
        )

        anim.start(label)
        shadow_anim.start(shadow_label)

        Clock.schedule_once(
            lambda dt: self.reset_lyric(label, shadow_label), duration +
            stagger
        )

    def update_rotation(self, label, shadow_label, rotation, value):
        """Updates the rotation of a lyric label and its shadow label based on
          a given value.

This method adjusts the rotation angle of both the specified label and its
corresponding shadow label by multiplying the current rotation by a
provided value. It allows for synchronized rotation effects, enhancing
the visual dynamics of the labels.

Args:
    label (Label): The label whose rotation is to be updated.
    shadow_label (Label): The shadow label associated with the main label.
    rotation (float): The current rotation angle of the label.
    value (float): The factor by which to adjust the rotation.
"""
        label.set_rotation(rotation * value)
        shadow_label.set_rotation(rotation * value)

    def reset_lyric(self, label, shadow_label):
        """
Resets the lyric label and its shadow to a new random phrase and position.

This function updates the text and position of a lyric label and its
corresponding shadow label with a randomly selected phrase from a predefined
list. It also applies a random color from a color palette and resets the
rotation before initiating an animation for the labels.

Args:
    label (Label): The label that displays the lyric text.
    shadow_label (Label): The label that displays the shadow of the lyric text.

Returns:
    None
"""

        text = random.choice(all_phrases)
        pos_x = random.randint(0, Window.width)
        pos_y = Window.height

        label.text = text
        label.pos = (pos_x, pos_y)
        label.set_rotation(0)
        label.color = random.choice(self.color_palette)

        shadow_label.text = text
        shadow_label.pos = (pos_x + 2, pos_y - 2)
        shadow_label.set_rotation(0)
        shadow_label.color = [0, 0, 0, 0.5]

        self.animate_lyric(label, shadow_label)


class LoadingApp(App):
    """
LoadingApp is a Kivy application that manages the loading screen.

This class sets up the main application interface by creating a
ScreenManager and adding a LoadingScreen to it. It serves as the entry point
for the application, allowing for the display of a loading animation while
content is being prepared.

Args:
    None

Returns:
    ScreenManager: The ScreenManager instance containing the loading screen.
"""

    def build(self):
        sm = ScreenManager()
        loading_screen = LoadingScreen(name="loading")
        sm.add_widget(loading_screen)
        return sm


if __name__ == "__main__":
    LoadingApp().run()
