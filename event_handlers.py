"""Event handlers for the Lyrics App."""

from syllable_counter import count_syllables
import data_storage
from rhyme_generator import fetch_rhymes


def get_rhyme_suggestions(app_instance):
    """Fetch rhymes for the selected or last word in the lyrics input."""
    words = app_instance.get_selected_word().split()
    print(f"Getting rhyme suggestions for: {words}")
    app_instance.show_loading_popup()
    rhymes = fetch_rhymes(words)
    print(f"Rhymes fetched: {rhymes}")  # Add this line
    app_instance.display_rhymes(words, rhymes)
    print("Rhyme display called")  # Add this line


def update_counter(app_instance, text):
    """Updates the syllable count and bar count displayed in the app."""
    lines = text.splitlines()
    syllable_count = sum(count_syllables(line) for line in lines)
    bar_count = len(lines)

    avg_syl_per_bar = syllable_count / bar_count if bar_count > 0 else 0

    app_instance.counter_label.text = (
        f"Bars: {bar_count} | Syllables: {syllable_count} | "
        f"AvgSyl: {avg_syl_per_bar:.2f}"
    )
    print(
        f"Counter updated: Bars={bar_count}, Syllables={syllable_count}, "
        f"AvgSyl={avg_syl_per_bar:.2f}"
    )


def on_text_change(app_instance, value):
    """Handles text changes in the lyrics input."""
    app_instance.undo_redo_manager.save_state(value)
    update_counter(app_instance, value)


def save_lyrics(app_instance):
    """Saves the current lyrics to a file or storage."""
    filename = "lyrics.txt"
    # This should be dynamically set based on user input or state
    lyrics = app_instance.lyrics_input.text
    data_storage.save_lyrics(filename, lyrics)


def load_lyrics(app_instance):
    """Loads lyrics from a file or storage."""
    filename = "lyrics.txt"
    # This should be dynamically set based on user input or state
    lyrics = data_storage.load_lyrics(filename)
    app_instance.lyrics_input.text = lyrics


def export_lyrics_to_pdf(app_instance):
    """Exports the current lyrics to a PDF file."""
    lyrics = app_instance.lyrics_input.text
    if lyrics.strip():
        filename = "lyrics.txt"
        # This could be dynamically set or provided by the user
        data_storage.export_to_pdf(filename, lyrics)
    else:
        print("No lyrics to export.")


def export_lyrics_to_docx(app_instance):
    """Exports the current lyrics to a DOCX file."""
    lyrics = app_instance.lyrics_input.text
    if lyrics.strip():
        filename = "lyrics.txt"
        # This could be dynamically set or provided by the user
        data_storage.export_to_docx(filename, lyrics)
    else:
        print("No lyrics to export.")
