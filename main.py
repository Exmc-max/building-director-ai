from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import random

# --- Data Contracts (Schemas) ---
class PlayerObservation(BaseModel):
    logic_confidence: float  # 0.0 to 1.0 (How logical is the player acting?)
    repetition: int          # How many times have they retried this puzzle?
    correct: bool            # Did they solve the last floor correctly?
    hesitation: float        # Time in seconds spent standing still

class DirectorInstructions(BaseModel):
    anomaly_level: str       # "SUBTLE", "AGGRESSIVE", "NONE"
    anomaly_probability: float
    anomaly_category: str    # "environment", "audio", "logic"
    lie_allowed: bool        # Can the building break rules (e.g. loops)?

# --- State Management (Memory) ---
class BehaviorProfile:
    def __init__(self):
        self.logic_confidence = 0.5  # Start neutral
        self.trust_level = 0.5       # Start neutral
        self.stress_level = 0.0
        self.samples = 0

    def update(self, obs: PlayerObservation):
        self.samples += 1
        
        # 1. Update Logic Confidence (Exponential Moving Average)
        # If they are correct and fast, logic goes up. If they guess/fail, it goes down.
        target_logic = 1.0 if obs.correct else 0.0
        if obs.hesitation > 5.0:
            target_logic -= 0.2 # Hesitation implies guessing
        
        # Smooth update (alpha = 0.3)
        self.logic_confidence = (self.logic_confidence * 0.7) + (target_logic * 0.3)
        self.logic_confidence = max(0.0, min(1.0, self.logic_confidence))

        # 2. Update Trust (Convergence)
        # If they consistently act logically, the building "trusts" them (ending path).
        if self.logic_confidence > 0.8:
            self.trust_level += 0.05
        elif self.logic_confidence < 0.3:
            self.trust_level -= 0.05
        
        self.trust_level = max(0.0, min(1.0, self.trust_level))

# Global State (In a real game, this would be per-session ID)
current_profile = BehaviorProfile()

# --- API App Definition ---
app = FastAPI()

# ---------------------------------------------------------
#  THE CRITICAL CHANGE IS HERE: /director/decide
# ---------------------------------------------------------
@app.post("/director/decide", response_model=DirectorInstructions)
async def get_director_decision(obs: PlayerObservation):
    """
    Unreal Engine calls this endpoint when a player finishes a floor.
    We update the profile and return instructions for the next floor.
    """
    global current_profile
    
    # 1. Update Internal State
    current_profile.update(obs)
    
    # 2. Decide Strategy (The "Brain")
    instructions = DirectorInstructions(
        anomaly_level="NONE",
        anomaly_probability=0.0,
        anomaly_category="environment",
        lie_allowed=False
    )

    # ENDING CONVERGENCE: If trust is high, stop scaring them.
    if current_profile.trust_level > 0.9:
        instructions.anomaly_level = "NONE"
        instructions.anomaly_probability = 0.0
        return instructions

    # STRATEGY A: The Logician (High Logic, Low Trust)
    # Test them with subtle reality breaks to see if they notice.
    if current_profile.logic_confidence > 0.6:
        instructions.anomaly_level = "SUBTLE"
        instructions.anomaly_probability = 0.8
        instructions.anomaly_category = "logic" # Loops, wrong numbers
        instructions.lie_allowed = True

    # STRATEGY B: The Panicker (Low Logic)
    # Pressure them with audio/visual stress to force mistakes.
    elif current_profile.logic_confidence < 0.4:
        instructions.anomaly_level = "AGGRESSIVE"
        instructions.anomaly_probability = 1.0
        instructions.anomaly_category = "audio" # Loud noises, shaking
        instructions.lie_allowed = False

    # STRATEGY C: Default (Uncertain)
    else:
        instructions.anomaly_level = "SUBTLE"
        instructions.anomaly_probability = 0.3
        instructions.anomaly_category = "environment" # Tilted paintings
        instructions.lie_allowed = False

    return instructions