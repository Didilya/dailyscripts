import sounddevice as sd
import numpy as np
import pyautogui
import time

SOUND_THRESHOLD = 0.01  # Adjust based on your audio levels
CHECK_INTERVAL = 2      # Time interval (in seconds) to check sound

def check_sound_output():
    """Captures system sound and checks if it is below the threshold."""
    duration = 1  # Capture duration in seconds
    sample_rate = 44100  # Sampling rate
    try:
        # Use the default sound output device (loopback enabled)
        audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='float64')
        sd.wait()  # Wait until recording is complete
        # Calculate RMS (Root Mean Square) of the audio data
        rms_value = np.sqrt(np.mean(np.square(audio_data)))
        return rms_value
    except Exception as e:
        print(f"Error capturing audio: {e}")
        return SOUND_THRESHOLD + 1  # Ensure it doesn't trigger a click

def perform_mouse_click():
    """Simulates a mouse click at the current mouse position."""
    pyautogui.click()

def main():
    print("Monitoring sound output levels... Press Ctrl+C to exit.")
    while True:
        sound_level = check_sound_output()
        print(f"Sound level: {sound_level}")
        if sound_level < SOUND_THRESHOLD:
            print("No sound detected. Clicking the mouse.")
            perform_mouse_click()
        else:
            print("Sound detected. No action taken.")
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram terminated.")
