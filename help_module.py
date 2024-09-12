# help_module.py

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.core.window import Window


def create_help_content():
    """
    Function to create the content of the help popup.
    This includes detailed descriptions of the app's features.
    """
    content = BoxLayout(orientation='vertical', padding=10, spacing=10)

    help_texts = [
        "Welcome to the Lyrics App!",
        "This app helps you write and manage rap lyrics with AI assistance and rhyme suggestions.",
        "\nMain Features:",
        "1. Lyrics Editor:",
        "   - Type or paste your lyrics in the main text area.",
        "   - The editor supports multi-line input and basic text editing.",
        "\n2. AI Suggestion:",
        "   - Click 'Generate' to get AI-generated lyrics suggestions.",
        "   - The AI will continue your current lyrics or start new ones.",
        "   - You can configure the AI's style and output length in the settings.",
        "\n3. Rhyme Suggestions:",
        "   - Select a word or phrase and click 'Rhyme' to get rhyme suggestions.",
        "   - A popup will show a list of words that rhyme with your selection.",
        "\n4. Syllable Counter:",
        "   - The app automatically counts syllables in your lyrics.",
        "   - The counter shows total bars, syllables, and average syllables per bar.",
        "\n5. Undo/Redo:",
        "   - Use 'Undo' and 'Redo' buttons to revert or reapply changes.",
        "\n6. Font Size Adjustment:",
        "   - Use 'Font +' and 'Font -' buttons to change the text size.",
        "\n7. Save/Load/Export:",
        "   - 'Save' stores your current lyrics.",
        "   - 'Load' retrieves previously saved lyrics.",
        "   - 'Export' allows you to save your lyrics as a text or PDF file.",
        "\n8. Spell Check:",
        "   - Use 'Spell Check' to identify and correct spelling errors.",
        "\nUsage Tips:",
        "- For AI suggestions, provide some initial lyrics for better context.",
        "- Use rhyme suggestions to find words that fit your flow.",
        "- Regularly save your work to prevent loss of progress.",
        "- Experiment with different AI settings to find your preferred style.",
        "\nShortcuts:",
        "- Ctrl+Z: Undo",
        "- Ctrl+Y: Redo",
        "- Ctrl+A: Select All",
        "\nNeed more help? Contact support at: support@lyricsapp.com"
    ]

    # Create labels for each help text
    for text in help_texts:
        label = Label(
            text=text,
            size_hint_y=None,
            height=30 * (text.count('\n') + 1),  # Adjust height based on content
            text_size=(400, None),
            halign='left',
            valign='top'
        )
        label.bind(texture_size=label.setter('size'))
        content.add_widget(label)

    return content


def show_help_popup(app_instance):
    """
    Function to display the scrollable help popup when called.
    """
    # Create the content
    content = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None)
    content.bind(minimum_height=content.setter('height'))

    help_text = """
    Welcome to the Lyrics App!

    Here's how to use the main features:

    1. Writing Lyrics:
       - Type your lyrics in the main text area.
       - Use the counter at the bottom to track bars and syllables.

    2. AI Suggestions:
       - Click 'AI Suggest' to get AI-generated lyrics suggestions.
       - You can configure AI settings in the menu.

    3. Rhyme Suggestions:
       - Select a word and click 'Rhyme' to get rhyme suggestions.

    4. Spell Check:
       - Use the 'Spell Check' feature to check your spelling.

    5. Undo/Redo:
       - Use the Undo and Redo buttons to manage your changes.

    6. Save/Load:
       - Save your work using the 'Save' option in the menu.
       - Load previously saved lyrics using the 'Load' option.

    7. Export:
       - Export your lyrics to a PDF file using the 'Export' option.

    8. Font Size:
       - Adjust the font size using the '+' and '-' buttons.

    Enjoy writing your lyrics!
    """

    label = Label(text=help_text, size_hint_y=None, markup=True)
    label.bind(texture_size=label.setter('size'))
    content.add_widget(label)

    # Create a ScrollView
    scroll_view = ScrollView(size_hint=(1, 1))
    scroll_view.add_widget(content)

    # Calculate the popup size based on the window size
    window_width, window_height = Window.size
    popup_width = min(600, window_width * 0.9)
    popup_height = min(400, window_height * 0.9)

    # Create a popup to show the scrollable help content
    help_popup = Popup(
        title='Help - How to Use Lyrics App',
        content=scroll_view,
        size_hint=(None, None),
        size=(popup_width, popup_height)
    )

    help_popup.open()
