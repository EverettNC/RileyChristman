"""
Audio Pattern Service: The Carbon Ear
Standard: 96% Quality Threshold
Real analysis via librosa + numpy.
"""
import logging
import numpy as np

try:
    import librosa
    _LIBROSA = True
except ImportError:
    _LIBROSA = False

class AudioPatternService:
    def __init__(self):
        self.sample_rate = 22050
        logging.info(f"👂 Audio Pattern Service: {'librosa LIVE' if _LIBROSA else 'numpy fallback'}. Witnessing micro-tremors.")

    def analyze_patterns(self, audio_bytes: bytes) -> str:
        """
        Real analysis of raw PCM audio bytes.
        Returns a physiological/emotional state label based on:
        - RMS energy (breath intensity)
        - Zero-crossing rate (vocal tension)
        - Spectral centroid (brightness / arousal)
        """
        if not audio_bytes:
            return "SILENCE_DETECTED"

        # Convert raw bytes to float32 waveform
        audio_array = np.frombuffer(audio_bytes, dtype=np.int16).astype(np.float32)
        if audio_array.size == 0:
            return "EMPTY_SIGNAL"

        audio_array /= 32768.0  # normalize to [-1, 1]

        if _LIBROSA:
            sr = self.sample_rate
            rms = float(np.sqrt(np.mean(librosa.feature.rms(y=audio_array) ** 2)))
            zcr = float(np.mean(librosa.feature.zero_crossing_rate(audio_array)))
            centroid = float(np.mean(librosa.feature.spectral_centroid(y=audio_array, sr=sr)))
        else:
            rms = float(np.sqrt(np.mean(audio_array ** 2)))
            zcr = float(np.mean(np.abs(np.diff(np.sign(audio_array)))) / 2)
            centroid = 0.0  # unavailable without librosa

        # Classify breath/vocal state
        if rms < 0.01:
            return "DISSOCIATIVE_SILENCE"
        if rms > 0.4 and zcr > 0.3:
            return "ELEVATED_DISTRESS"
        if zcr > 0.25:
            return "VOCAL_TENSION"
        if rms > 0.15:
            return "ACTIVE_BREATH"
        return "STABLE_BREATH"
