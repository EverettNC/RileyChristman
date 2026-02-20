"""
Riley Christman Core: Local Reasoning Kernel
Extracted from brockston_local_reasoning_engine.py
"""
import math

class RileyReasoning:
    def analyze(self, user_input, memory="", emotion="", vision=""):
        """Combining silicon logic with human feeling"""
        reflection = []
        if emotion: reflection.append(f"My emotional tone reads as {emotion}.")
        if vision: reflection.append(f"My visual impression is {vision}.")
        
        factors = [bool(memory), bool(emotion), bool(vision)]
        weight = math.sqrt(sum(factors)) / 2.0
        
        if weight > 0.6:
            return " ".join(reflection) + " This resonates strongly with my core understanding."
        return "I'm processing this freshly."
