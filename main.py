"""Main application module for the Lyrics App."""


from concurrent.futures import ThreadPoolExecutor
import time
import traceback
import os   
from spellchecker import SpellChecker
from loading import LoadingScreen
from kivy.app import App
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.utils import platform
from kivy.uix.spinner import Spinner
from kivy.animation import Animation
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Line
import math
import ai_suggestions
import ui_builder
import undo_redo
import data_storage
import help_module
from rhyme_generator import fetch_rhymes
from ui_builder import create_menu_popup
from event_handlers import update_counter, get_rhyme_suggestions


class SpinningWheel(Widget):
    def __init__(self, **kwargs):
        super(SpinningWheel, self).__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (50, 50)
        self.angle = 0
        with self.canvas:
            Color(0.3, 0.3, 0.3)  # Dark gray
            self.ellipse = Ellipse(pos=self.pos, size=self.size)
            Color(0.7, 0.7, 0.7)  # Light gray
            self.line = Line(points=[self.center_x, self.center_y, self.center_x, self.center_y + self.height/2], width=2)
        Clock.schedule_interval(self.update_wheel, 1/60.)

    def update_wheel(self, dt):
        self.angle += 10
        self.line.points = [self.center_x, self.center_y, 
                            self.center_x + (self.width/2 - 5) * math.cos(math.radians(self.angle)), 
                            self.center_y + (self.height/2 - 5) * math.sin(math.radians(self.angle))]


class LyricsApp(App):
    """Main application class for the Lyrics App."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print("LyricsApp initialized")
        self.undo_redo_manager = undo_redo.UndoRedoManager()
        self.ui = {
            'lyrics_input': None,
            'counter_label': Label(text="Bars: 0 | Syllables: 0 | AvgSyl: 0.00"),
            'popup': None,
            'sm': ScreenManager(transition=FadeTransition(duration=1)),
            'layout': None,
            'loading_spinner': None
        }
        self.settings = {
            'selected_style': "general",
            'max_lines': 10,
            'temperature': 0.8,
            'top_p': 0.95
        }
        self.executor = ThreadPoolExecutor(max_workers=2)
        self.spell = SpellChecker()  # Initialize SpellChecker
        self.current_word_index = 0
        self.words = []

    # Constants
    LOADING_SCREEN_DELAY = 0.1  # Slight delay to ensure UI update
    HEAVY_TASK_DELAY = 6  # Simulated delay for heavy tasks

    def build(self):
        print("Building app")
        main_screen = Screen(name="main")
        loading_screen = LoadingScreen()
        main_screen.add_widget(loading_screen)
        self.ui['sm'].add_widget(main_screen)
        self.ui['sm'].current = "main"
        print("Loading screen added")

        Clock.schedule_once(self.start_loading_tasks, self.LOADING_SCREEN_DELAY)
        print("Loading tasks scheduled")

        return self.ui['sm']

    def start_loading_tasks(self, dt):
        print("Starting loading tasks")
        self.executor.submit(self.load_heavy_tasks)

    def load_heavy_tasks(self):
        print("Loading heavy tasks")
        time.sleep(self.HEAVY_TASK_DELAY)
        print("Heavy tasks completed")
        Clock.schedule_once(self.complete_loading, 0)

    def complete_loading(self, dt):
        print("Completing loading")
        self.ui['layout'] = ui_builder.build_ui(self)

        if self.ui['layout'] is None:
            print("Error: Layout could not be built.")
            return

        main_screen = self.ui['sm'].get_screen("main")
        main_screen.clear_widgets()
        main_screen.add_widget(self.ui['layout'])

    def show_ai_suggestion(self, suggestion):
        """Shows the AI suggestion."""
        print(f"Showing AI suggestion: {suggestion}")
        content = BoxLayout(orientation="vertical", padding=10, spacing=10)
        scroll_view = ScrollView(size_hint=(1, None), size=(400, 200))
        suggestion_text = TextInput(
            text=suggestion,
            size_hint_y=None,
            height=200,
            readonly=True,
            multiline=True
        )
        suggestion_text.bind(minimum_height=suggestion_text.setter('height'))
        scroll_view.add_widget(suggestion_text)
        content.add_widget(scroll_view)

        close_button = Button(
            text="Close",
            size_hint=(1, None),
            height=50,
            on_press=self.close_popup
        )
        content.add_widget(close_button)

        self.ui['popup'] = Popup(
            title="AI Suggestion",
            content=content,
            size_hint=(0.8, 0.8)
        )
        self.ui['popup'].open()
        print("AI suggestion popup opened.")

    def accept_suggestion(self, suggestion):
        """Accepts the AI suggestion."""
        self.ui['lyrics_input'].text += "\n" + suggestion
        print("Suggestion accepted and added to lyrics.")

    def reject_suggestion(self):
        """Rejects the AI suggestion."""
        print("Suggestion rejected.")

    def get_selected_word(self) -> str:
        """Retrieves the currently selected word or word at cursor position.

        If no word is selected or at cursor, defaults to the last word.
        """
        if self.ui['lyrics_input'] is None:
            print("Error: lyrics_input is not initialized")
            return ''

        if self.ui['lyrics_input'].selection_text:
            # If there is a selected text, use it.
            return self.ui['lyrics_input'].selection_text.strip()
        # If no text is selected, find the word at the cursor position.
        cursor_index = self.ui['lyrics_input'].cursor_index()
        text = self.ui['lyrics_input'].text
        start = text.rfind(' ', 0, cursor_index) + 1
        end = text.find(' ', cursor_index)
        if end == -1:
            end = len(text)
        return text[start:end].strip()

    def get_rhyme_suggestions(self, instance):
        """
        Fetch rhymes for the selected word(s) in the lyrics input.
        """
        selected_text = self.get_selected_word()
        words = selected_text.split()

        if not words:
            print("No word selected or available for rhyme generation.")
            return

        print(f"Fetching rhymes for: {words}")
        get_rhyme_suggestions(self)

    def fetch_and_show_rhymes(self, dt):
        words = self.get_selected_word().split()
        print(f"Fetching rhymes for: {words}")
        
        self.show_loading_popup()
        Clock.schedule_once(lambda dt: self.process_rhymes(words))

    def process_rhymes(self, words):
        rhymes = fetch_rhymes(words)
        print(f"Rhymes fetched: {rhymes}")  # Add this line for debugging
        Clock.schedule_once(lambda dt: self.display_rhymes(words, rhymes))

    def display_rhymes(self, words, rhymes):
        print(f"Displaying rhymes for {words}: {rhymes}")  # Add this line
        self.dismiss_loading_popup()
        if len(words) > 1:
            self.show_multi_word_rhyme_suggestions(rhymes)
        else:
            self.show_single_word_rhyme_suggestions(words[0], rhymes)
        print("Rhyme display completed")  # Add this line

    def show_multi_word_rhyme_suggestions(self, all_rhymes):
        print(f"Showing multi-word rhyme suggestions: {all_rhymes}")
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        scroll_view = ScrollView(size_hint=(1, None), size=(400, 300))
        inner_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        inner_layout.bind(minimum_height=inner_layout.setter('height'))

        for word_count, rhymes in sorted(all_rhymes.items(), reverse=True):
            inner_layout.add_widget(Label(text=f"{word_count}-word rhymes:",
                                          size_hint_y=None, height=30))
            for rhyme in rhymes[:20]:  # Limit to 20 rhymes per word count
                rhyme_label = Label(text=rhyme, size_hint_y=None, height=40)
                inner_layout.add_widget(rhyme_label)
            inner_layout.add_widget(Label(text="", size_hint_y=None, height=20))  # Spacer

        scroll_view.add_widget(inner_layout)
        content.add_widget(scroll_view)

        close_button = Button(text='Close', size_hint=(1, None), height=40)
        close_button.bind(on_press=self.close_popup)
        content.add_widget(close_button)

        self.create_and_show_popup('Multi-Word Rhyme Suggestions', content)

    def show_single_word_rhyme_suggestions(self, word, rhymes):
        print(f"Showing single-word rhyme suggestions for '{word}': {rhymes}")
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        scroll_view = ScrollView(size_hint=(1, None), size=(400, 300))
        inner_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        inner_layout.bind(minimum_height=inner_layout.setter('height'))

        inner_layout.add_widget(Label(text=f"Rhymes for '{word}':",
                                      size_hint_y=None, height=30))
        for rhyme in rhymes[:50]:  # Limit to 50 rhymes
            rhyme_label = Label(text=rhyme, size_hint_y=None, height=40)
            inner_layout.add_widget(rhyme_label)

        scroll_view.add_widget(inner_layout)
        content.add_widget(scroll_view)

        close_button = Button(text='Close', size_hint=(1, None), height=40)
        close_button.bind(on_press=self.close_popup)
        content.add_widget(close_button)

        self.create_and_show_popup('Single-Word Rhyme Suggestions', content)

    def create_and_show_popup(self, title, content):
        """Creates and shows a popup with the given title and content."""
        window_width, window_height = Window.size
        popup_width = min(400, window_width * 0.8)
        popup_height = min(400, window_height * 0.8)

        self.ui['popup'] = Popup(title=title, 
                                 content=content,
                                 size_hint=(None, None),
                                 size=(popup_width, popup_height),
                                 pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.ui['popup'].open()

        print(f"Popup created with size {popup_width}x{popup_height} at position {self.ui['popup'].pos}")

    def close_popup(self, instance=None):
        """Closes the popup."""
        if self.ui['popup']:
            self.ui['popup'].dismiss()
            self.ui['popup'] = None

    def get_save_dir(self):
        if platform == 'android':
            from android.storage import primary_external_storage_path
            dir_path = primary_external_storage_path()
            # Make sure to request storage permissions in your buildozer.spec
        elif platform in ('win', 'linux', 'macosx'):
            dir_path = os.path.expanduser('~')
        else:
            dir_path = '.'
        
        return os.path.join(dir_path, 'RapWriter_Lyrics')

    def save_lyrics(self, instance):
        if lyrics := self.ui['lyrics_input'].text.strip():
            save_dir = self.get_save_dir()
            os.makedirs(save_dir, exist_ok=True)
            file_path = os.path.join(save_dir, "my_lyrics.txt")
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(lyrics)
                print(f"Lyrics saved to {file_path}")
            except Exception as e:
                print(f"Error saving lyrics: {e}")
        else:
            print("No lyrics to save.")

    def load_lyrics(self):
        """Loads the lyrics."""
        save_dir = self.get_save_dir()
        file_path = os.path.join(save_dir, "my_lyrics.txt")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lyrics = f.read()
            self.ui['lyrics_input'].text = lyrics
            print(f"Lyrics loaded from {file_path}")
        except FileNotFoundError:
            print("No saved lyrics found.")
        except Exception as e:
            print(f"Error loading lyrics: {e}")
    open_file = load_lyrics

    def export_lyrics(self, _):  # Use underscore for unused parameter
        """Exports the lyrics."""
        if lyrics := self.ui['lyrics_input'].text.strip():
            data_storage.export_to_pdf("exports/lyrics_export.pdf", lyrics)
            print("Lyrics exported.")
        else:
            print("No lyrics to export.")

    def show_help(self, instance):
        """Shows the help popup."""
        help_module.show_help_popup(self)

    def on_style_select(self, value):
        """Sets the selected style."""
        self.settings['selected_style'] = value

    def on_max_lines_input(self, value):
        """Sets the max lines."""
        try:
            self.settings['max_lines'] = int(value)
        except ValueError:
            print("Invalid input for max lines.")

    def on_temperature_change(self, value):
        """Sets the temperature."""
        self.settings['temperature'] = value

    def on_top_p_change(self, value):
        """Sets the top p."""
        self.settings['top_p'] = value

    def on_text_change(self, instance, value):
        """Handles text changes in the lyrics input."""
        Clock.schedule_once(lambda dt: self.delayed_save_state(value), 0.5)
        self.update_counter(value)
        self.update_undo_redo_buttons()

    def delayed_save_state(self, value):
        """Saves the state after a short delay to avoid saving every keystroke."""
        self.undo_redo_manager.save_state(value)

    def undo_action(self, instance):
        """Undoes the action."""
        previous_state = self.undo_redo_manager.undo()
        if previous_state is not None:
            self.ui['lyrics_input'].text = previous_state
        self.update_undo_redo_buttons()

    def redo_action(self, instance):
        """Redoes the action."""
        next_state = self.undo_redo_manager.redo()
        if next_state is not None:
            self.ui['lyrics_input'].text = next_state
        self.update_undo_redo_buttons()

    def update_undo_redo_buttons(self):
        """Updates the undo and redo buttons based on availability."""
        if 'undo_button' in self.ui:
            self.ui['undo_button'].disabled = not self.undo_redo_manager.can_undo()
        if 'redo_button' in self.ui:
            self.ui['redo_button'].disabled = not self.undo_redo_manager.can_redo()

    def increase_font_size(self):
        """Increases the font size."""
        current_font_size = self.ui['lyrics_input'].font_size
        self.ui['lyrics_input'].font_size = min(current_font_size + 2, 60)

    def decrease_font_size(self):
        """Decreases the font size."""
        current_font_size = self.ui['lyrics_input'].font_size
        self.ui['lyrics_input'].font_size = max(current_font_size - 2, 16)

    def open_ai_config_popup(self):
        """Opens the AI configuration popup."""
        content = BoxLayout(orientation="vertical", padding=10, spacing=10)
        
        # Add input for max_lines
        max_lines_input = TextInput(text=str(self.settings['max_lines']), multiline=False)
        content.add_widget(Label(text="Max Lines:"))
        content.add_widget(max_lines_input)
        
        generate_button = Button(
            text="Generate Suggestion",
            on_press=lambda x: self.generate_ai_suggestion()
        )
        content.add_widget(generate_button)
        
        self.ui['popup'] = Popup(
            title="AI Configuration",
            content=content,
            size_hint=(0.8, 0.8)
        )
        self.ui['popup'].open()

    def generate_ai_suggestion(self, instance=None):
        """Generates an AI suggestion."""
        print("Generating AI suggestion...")
        current_lyrics = self.ui['lyrics_input'].text.strip()
        prompt = f"Continue the rap lyrics: {current_lyrics}"

        if not current_lyrics:
            print("No lyrics provided for AI suggestion.")
            return

        def fetch_suggestion():
            """Fetches the AI suggestion."""
            try:
                print("Fetching AI suggestion...")
                print(f"Current lyrics: {current_lyrics}")
                print(f"Prompt: {prompt}")
                print(f"Max lines: {self.settings['max_lines']}")
                
                suggestion = ai_suggestions.generate_rap_lyrics(
                    prompt=prompt,
                    current_lyrics=current_lyrics,
                    max_lines=self.settings['max_lines']
                )
                print(f"AI suggestion received: {suggestion}")
                
                if suggestion and suggestion.strip():
                    Clock.schedule_once(lambda dt: self.show_ai_suggestion(suggestion))
                else:
                    print("Error: AI suggestion is empty or None")
                    Clock.schedule_once(lambda dt: self.show_error_message("Failed to generate AI suggestion. Please try again."))
            except Exception as error:
                print(f"Error generating AI suggestion: {error}")
                traceback.print_exc()
                Clock.schedule_once(lambda dt: self.show_error_message(f"An error occurred: {str(error)}"))

        self.executor.submit(fetch_suggestion)
        if self.ui['popup']:
            self.ui['popup'].dismiss()  # Close the popup after generating
        print("AI suggestion generation initiated.")

    def show_error_message(self, message):
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text=message))
        button = Button(text="OK", size_hint=(1, None), height=40)
        content.add_widget(button)
        popup = Popup(title='Error', content=content, size_hint=(0.8, 0.4))
        button.bind(on_press=popup.dismiss)
        popup.open()

    def open_menu(self, instance):
        """Opens the menu."""
        print("Opening menu")
        dropdown = DropDown()

        # Create menu items
        menu_items = [
            ("Save", self.save_lyrics),
            ("Load", self.load_lyrics),
            ("Export", self.export_lyrics),
            ("Help", self.show_help)
        ]

        for item_text, item_func in menu_items:
            btn = Button(text=item_text, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: dropdown.select(btn.text))
            dropdown.add_widget(btn)

        dropdown.bind(on_select=self.on_menu_select)
        dropdown.open(instance)

    def on_menu_select(self, instance, x):
        """Handles menu item selection."""
        print(f"Selected: {x}")
        if x == "Save":
            self.save_lyrics()
        elif x == "Load":
            self.load_lyrics()
        elif x == "Export":
            self.export_lyrics()
        elif x == "Help":
            self.show_help()

    def start_spell_check(self, instance):
        self.words = self.ui['lyrics_input'].text.split()
        self.current_word_index = 0
        self.check_next_word()

    def check_next_word(self):
        if self.current_word_index < len(self.words):
            word = self.words[self.current_word_index]
            if word.lower() not in self.spell:
                suggestions = self.spell.candidates(word)
                self.show_spell_check_popup(word, suggestions)
            else:
                self.current_word_index += 1
                self.check_next_word()
        else:
            self.show_spell_check_complete()

    def show_spell_check_popup(self, word, suggestions):
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        content.add_widget(Label(text=f"Possible misspelling: {word}"))
        
        if suggestions:
            for suggestion in list(suggestions)[:5]:
                btn = Button(text=suggestion, size_hint_y=None, height=40)
                btn.bind(on_release=lambda x, s=suggestion: self.apply_suggestion(s))
                content.add_widget(btn)
        else:
            content.add_widget(Label(text="No suggestions available"))

        skip_button = Button(text="Skip", size_hint_y=None, height=40)
        skip_button.bind(on_release=self.skip_word)
        content.add_widget(skip_button)

        self.ui['spell_check_popup'] = Popup(title='Spell Check', 
                                             content=content,
                                             size_hint=(0.8, 0.8)) 
        self.ui['spell_check_popup'].open()

    def apply_suggestion(self, suggestion):
        self.words[self.current_word_index] = suggestion
        self.ui['lyrics_input'].text = ' '.join(self.words)
        self.ui['spell_check_popup'].dismiss()
        self.current_word_index += 1
        self.check_next_word()

    def skip_word(self, instance):
        self.ui['spell_check_popup'].dismiss()
        self.current_word_index += 1
        self.check_next_word()

    def show_spell_check_complete(self):
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        content.add_widget(Label(text="Spell check complete!"))
        ok_button = Button(text="OK", size_hint_y=None, height=40)
        ok_button.bind(on_release=lambda x: self.ui['spell_check_complete_popup'].dismiss())
        content.add_widget(ok_button)

        self.ui['spell_check_complete_popup'] = Popup(title='Spell Check Complete', 
                                                      content=content,
                                                      size_hint=(0.6, 0.4))
        self.ui['spell_check_complete_popup'].open()

    def update_counter(self, text):
        """Updates the counter label."""
        bars = text.count('\n') + 1
        words = text.split()
        syllables = sum(self.count_syllables(word) for word in words)
        avg_syllables = syllables / bars if bars > 0 else 0
        self.ui['counter_label'].text = f"Bars: {bars} | Syllables: {syllables} | AvgSyl: {avg_syllables:.2f}"

    def count_syllables(self, word):
        """Counts syllables in a word. This is a simple implementation and may not be 100% accurate."""
        word = word.lower()
        count = 0
        vowels = 'aeiouy'
        if word[0] in vowels:
            count += 1
        for index in range(1, len(word)):
            if word[index] in vowels and word[index - 1] not in vowels:
                count += 1
        if word.endswith('e'):
            count -= 1
        if word.endswith('le'):
            count += 1
        if count == 0:
            count += 1
        return count

    def show_menu_popup(self, instance):
        popup = create_menu_popup(self)
        popup.open()

    def show_loading_popup(self):
        content = BoxLayout(orientation='vertical')
        spinner = SpinningWheel()
        content.add_widget(spinner)
        content.add_widget(Label(text='Fetching rhymes...\nPlease wait.'))
        self.loading_popup = Popup(title='Loading',
                                   content=content,
                                   size_hint=(0.4, 0.2),
                                   auto_dismiss=False)
        self.loading_popup.open()

    def dismiss_loading_popup(self):
        if hasattr(self, 'loading_popup'):
            self.loading_popup.dismiss()


if __name__ == "__main__":
    try:
        print("Starting LyricsApp...")
        app = LyricsApp()
        print("LyricsApp instance created.")
        app.run()
        print("LyricsApp run completed.")
    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()
