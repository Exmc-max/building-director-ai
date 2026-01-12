from pydantic import BaseModel

# INPUT: What Unreal sends to Python (The Observation)
class PlayerObservation(BaseModel):
    floor: int
    logic_confidence: float # 0.0 to 1.0
    trust_level: float      # 0.0 to 1.0
    repetition: int         # How many times they did the same thing

# OUTPUT: What Python sends back (The Parameters/Intent)
class DirectorInstructions(BaseModel):
    anomaly_level: str       # "subtle", "medium", "aggressive"
    anomaly_probability: float # 0.0 to 1.0 (Chance of it happening)
    anomaly_category: str    # "environment", "audio", "logic"
    lie_allowed: bool        # Can the building cheat?