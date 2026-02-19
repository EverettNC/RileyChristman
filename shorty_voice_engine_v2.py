"""
ShortyVoiceEngineV2: Riley's Voice
Standard: 96% Quality Threshold
"""
import logging
import threading

try:
    import pyttsx3
    _engine = pyttsx3.init()
    # Pick a warmer male voice if available
    voices = _engine.getProperty("voices")
    for v in voices:
        if "alex" in v.name.lower() or "daniel" in v.name.lower():
            _engine.setProperty("voice", v.id)
            break
    _engine.setProperty("rate", 175)   # words per minute
    _engine.setProperty("volume", 0.95)
    _TTS_AVAILABLE = True
except Exception:
    _TTS_AVAILABLE = False

_tts_lock = threading.Lock()

class ShortyVoiceEngineV2:
    def __init__(self):
        self.voice_profile = "Shorty_Ultra_Tier"
        self.tts_available = _TTS_AVAILABLE
        logging.info(f"🗣️ ShortyVoice V2: Audio Synthesis {'LIVE' if _TTS_AVAILABLE else 'SIMULATED'}.")

    def synthesize(self, text, mode="sweetheart"):
        """
        Speaks text aloud via pyttsx3 (offline TTS).
        Falls back to a log message if TTS is unavailable.
        Returns a status string either way.
        """
        if self.tts_available:
            with _tts_lock:
                _engine.say(text)
                _engine.runAndWait()
            return f"[Spoken: '{text}' | mode={mode}]"
        return f"[Audio Output: '{text}' in mode: {mode}]"
