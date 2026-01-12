from pydantic import BaseModel

# INPUT: Raw behavior sent from Unreal
class PlayerObservation(BaseModel):
    correct: bool               # Was the last decision correct?
    repetition: int             # Times the same choice was repeated
    hesitation: float           # Seconds before making the choice

# OUTPUT: High-level intent returned to Unreal
class DirectorInstructions(BaseModel):
    anomaly_level: str          # "subtle", "medium", "aggressive"
    anomaly_probability: float  # 0.0 to 1.0
    anomaly_category: str       # "environment", "audio", "logic"
    lie_allowed: bool           # Is rule-breaking permitted?