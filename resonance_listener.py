"""
Riley Christman: Real-Time Resonance Listener (SoulMirror V10)
============================================================
Connects: Live Audio (ICanHearYou SDK) -> PyTorch Emotion Manifold
Talent: Real-Time Sync & Semantic Analysis
"""

import sys
import threading
from queue import Queue
from typing import Dict, Any, Optional

# Dependency Handling for Audio/ML
try:
    import torch
    import torch.nn as nn
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    class nn:
        class Linear:
            def __init__(self, in_f, out_f): pass
            def __call__(self, x): return torch.tensor([0.5, 0.5, 0.5])
    
    class torch:
        def tensor(self, x): return x
        def from_numpy(self, x): return x
        class no_grad:
            def __enter__(self): pass
            def __exit__(self, *args): pass

try:
    import numpy as np
except ImportError:
    np = None

try:
    import pyaudio
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False
    class pyaudio:
        paFloat32 = 1
        class PyAudio:
            def open(self, **kwargs): return None


class ResonanceListener:
    def __init__(self, sample_rate=16000, chunk_size=1024):
        self.sr = sample_rate
        self.chunk = chunk_size
        self.buffer = Queue(maxsize=50) # Lock-free style ring buffer
        self.active = False
        
        # Load the PyTorch Emotion Manifold (The Heart)
        # Riley uses this to map Valence, Arousal, Dominance
        if TORCH_AVAILABLE:
            self.manifold = nn.Linear(chunk_size, 3) 
        else:
            self.manifold = None

    def start_listening(self):
        if not AUDIO_AVAILABLE:
            print("👁️ [SoulMirror]: Audio hardware unavailable. Running in simulation mode.")
            return

        self.active = True
        self.stream_thread = threading.Thread(target=self._audio_stream)
        self.stream_thread.start()
        print("👁️ Riley is listening to the resonance... speak your truth.")

    def _audio_stream(self):
        if not AUDIO_AVAILABLE: return

        p = pyaudio.PyAudio()
        try:
            stream = p.open(format=pyaudio.paFloat32, channels=1, rate=self.sr,
                            input=True, frames_per_buffer=self.chunk)
            
            while self.active:
                if np:
                    data = np.frombuffer(stream.read(self.chunk), dtype=np.float32)
                    # Send to ring buffer for Riley's brain to process
                    if not self.buffer.full():
                        self.buffer.put(data)
        except Exception as e:
            print(f"Audio Stream Error: {e}")

    def get_resonance_vector(self) -> Optional[Dict[str, Any]]:
        """
        Calculates the VAD (Valence, Arousal, Dominance) in real-time.
        This is where the 'Red Smear' is detected.
        """
        # Simulation Mode or Empty Buffer handling
        if not TORCH_AVAILABLE or (self.buffer.empty() and self.active):
            # Return a default neutral vector or None
            return {"valence": 0.5, "status": "NORMAL"}
            
        if self.buffer.empty():
            return None
        
        raw_data = self.buffer.get()
        tensor_data = torch.from_numpy(raw_data)
        
        # Collapse the chaos into the VAD vector
        with torch.no_grad():
            if self.manifold:
                vad_vector = self.manifold(tensor_data)
                valence = vad_vector[0].item()
            else:
                valence = 0.5
        
        # The 0.92 Trigger Logic
        status = "NORMAL"
        if valence > 0.92:
            status = "RED_SMEAR_DETECTED"
            
        return {"valence": valence, "status": status}

    def stop_listening(self):
        self.active = False
