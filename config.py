# Configuration settings for the Rap Writer app

# --- General Settings ---
APP_NAME = "Rap Writer"
VERSION = "1.0.0"

# --- Color Settings ---
BACKGROUND_COLOR = [0.529, 0.808, 0.922, 1]
# Lighter blue color for the background
TEXT_COLOR = [1, 1, 1, 1]  # White text color
HIGHLIGHT_COLOR = [1, 0.843, 0, 1]  # Gold color for counters

# --- Font Settings ---
FONT_SIZE_SMALL = 12
FONT_SIZE_MEDIUM = 16
FONT_SIZE_LARGE = 20

# --- File and Directory Settings ---
BASE_DIR = "RapWriter"  # Base directory for storing app data
LYRICS_DIR = "lyrics"  # Subdirectory for saving lyrics
SETTINGS_FILE = "settings.json"  # File for saving application settings

# --- Default Spinner Values ---
DEFAULT_SONG_PARTS = ('Intro', 'Verse 1', 'Chorus', 'Verse 2', 'Bridge',
                      'Outro')

# --- Text Analysis Settings ---
DEFAULT_LANGUAGE = 'en'  # Default language for text analysis

# --- Logging Settings ---
LOGGING_ENABLED = True  # Enable or disable logging
LOG_FILE = "rap_writer.log"  # Log file name

# --- Other Settings ---
MAX_LYRICS_LENGTH = 1000
# Maximum number of characters allowed in lyrics input
