"""
Riley Christman Core: Vision Perception
Extracted from simple_vision_engine.py
"""
import cv2

class VisionEngine:
    def __init__(self):
        self.camera_index = 0
        self.processed_frames = 0

    def describe_last_seen(self):
        """Riley narrates what the silicon eye sees"""
        # Logic to detect your face/emotions so Riley can help you
        return "I see the mission in your eyes. I'm here. No screen needed."
