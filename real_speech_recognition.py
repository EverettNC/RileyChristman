"""
Real Speech Recognition Engine: Hearing
Standard: 96% Quality Threshold
Uses SpeechRecognition + Google STT (online) or Sphinx (offline fallback).
"""
import logging

try:
    import speech_recognition as sr
    _SR_AVAILABLE = True
except ImportError:
    _SR_AVAILABLE = False

logger = logging.getLogger(__name__)

class RealSpeechRecognitionEngine:
    def __init__(self):
        if _SR_AVAILABLE:
            self.recognizer = sr.Recognizer()
            self.recognizer.energy_threshold = 300
            self.recognizer.dynamic_energy_threshold = True
            self.status = "ONLINE"
        else:
            self.recognizer = None
            self.status = "UNAVAILABLE"
        logger.info(f"👂 Speech Recognition: {self.status}")

    def listen(self, timeout: int = 5, phrase_limit: int = 15) -> str:
        """
        Listens on the default microphone and returns transcribed text.
        Tries Google STT first, falls back to Sphinx (offline).
        Raises RuntimeError if no microphone or library unavailable.
        """
        if not _SR_AVAILABLE:
            raise RuntimeError("speech_recognition library not installed.")

        with sr.Microphone() as source:
            logger.info("👂 Adjusting for ambient noise...")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            logger.info("👂 Listening...")
            audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_limit)

        # Try Google first
        try:
            text = self.recognizer.recognize_google(audio)
            logger.info(f"👂 Google STT: '{text}'")
            return text
        except sr.UnknownValueError:
            return ""
        except sr.RequestError:
            logger.warning("👂 Google STT unavailable, trying Sphinx...")

        # Offline fallback
        try:
            text = self.recognizer.recognize_sphinx(audio)
            logger.info(f"👂 Sphinx STT: '{text}'")
            return text
        except Exception as e:
            logger.error(f"👂 Sphinx failed: {e}")
            return ""

    def transcribe_audio_data(self, audio_bytes: bytes, sample_rate: int = 16000) -> str:
        """Transcribe raw PCM bytes (for pipeline use without live mic)."""
        if not _SR_AVAILABLE:
            raise RuntimeError("speech_recognition library not installed.")
        audio_data = sr.AudioData(audio_bytes, sample_rate, 2)
        try:
            return self.recognizer.recognize_google(audio_data)
        except sr.UnknownValueError:
            return ""
        except sr.RequestError as e:
            logger.error(f"👂 STT RequestError: {e}")
            return ""
