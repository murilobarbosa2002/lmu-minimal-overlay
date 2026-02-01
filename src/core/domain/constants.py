"""
Physical and mathematical constants used throughout the codebase.

These constants represent universal physical/mathematical values that never change.
For configurable values, use config.json instead.
"""

# Speed conversions
KMH_TO_MS = 3.6  # km/h to m/s conversion factor
MS_TO_KMH = 3.6  # m/s to km/h conversion factor

KM_TO_MILES = 0.621371  # kilometers to miles conversion factor
MILES_TO_KM = 1.609344  # miles to kilometers conversion factor (1 / 0.621371)

# Time conversions
SECONDS_TO_MINUTES = 60  # seconds in a minute
MINUTES_TO_SECONDS = 1 / 60  # minutes to seconds

# Data type limits
BYTE_MAX = 255  # Maximum value for 8-bit unsigned integer
WORD_MAX = 65535  # Maximum value for 16-bit unsigned integer

# Normalized ranges
NORMALIZED_MIN = 0.0  # Minimum normalized value
NORMALIZED_MAX = 1.0  # Maximum normalized value

# Percentage ranges
PERCENTAGE_MIN = 0.0  # Minimum percentage (0%)
PERCENTAGE_MAX = 1.0  # Maximum percentage (100%)

# Steering ranges
STEERING_ANGLE_MIN = -900.0  # Minimum steering angle in degrees
STEERING_ANGLE_MAX = 900.0  # Maximum steering angle in degrees
STEERING_DEGREES_FULL_LOCK = 540.0  # Degrees for full steering lock (left to right)

# Mouse buttons
MOUSE_BUTTON_LEFT = 1
MOUSE_BUTTON_MIDDLE = 2
MOUSE_BUTTON_RIGHT = 3

# Initial state values (zeros)
INITIAL_SPEED = 0.0
INITIAL_THROTTLE = 0.0
INITIAL_BRAKE = 0.0
INITIAL_STEERING = 0.0
INITIAL_CLUTCH = 0.0
INITIAL_PROGRESS = 0.0
INITIAL_TIMESTAMP = 0.0
INITIAL_INDEX = 0

# Lerp/clamp bounds
LERP_MIN = 0.0
LERP_MAX = 1.0

# Speed thresholds
MINIMUM_SPEED_THRESHOLD = 0.1  # m/s - below this is considered stopped

# Default fallback values
DEFAULT_GEAR_RATIO = 1.0

# FFB (Force Feedback) limits
FFB_MIN = -1.0
FFB_MAX = 1.0

# Simulation noise ranges
ROAD_NOISE_MIN = -0.05
ROAD_NOISE_MAX = 0.05
CORNER_NOISE_MIN = -0.1
CORNER_NOISE_MAX = 0.1

# System / Platform Constants
PLATFORM_WIN32 = "win32"
ENV_SDL_VIDEO_WINDOW_POS = "SDL_VIDEO_WINDOW_POS"

# Window Management Constants
OFFSCREEN_COORD = -32000
DWM_SYNC_DELAY = 0.1  # Seconds to wait for DWM transparency sync
WINDOW_FLUSH_CYCLES = 2  # Number of flip() calls to clear buffer

# Default Window Configuration
DEFAULT_WINDOW_TITLE = "LMU Overlay"
DEFAULT_WINDOW_WIDTH = 800
DEFAULT_WINDOW_HEIGHT = 600
DEFAULT_WINDOW_FPS = 60
DEFAULT_WINDOW_X = 100
DEFAULT_WINDOW_Y = 100
