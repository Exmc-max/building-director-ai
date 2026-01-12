from schemas import PlayerObservation
from pydantic import BaseModel

class BehaviorProfile(BaseModel):
    logic_confidence: float = 0.5
    trust_level: float = 0.5
    adaptability: float = 0.5
    samples: int = 0

current_profile = BehaviorProfile()

def clamp(value: float) -> float:
    return max(0.0, min(1.0, value))

def calculate_step_logic(obs: PlayerObservation) -> float:
    """
    Logic inference from raw behavior.
    """
    score = 1.0 if obs.correct else 0.0

    # Hesitation penalty (uncertainty)
    if obs.hesitation > 3.0:
        penalty = (obs.hesitation - 3.0) * 0.1
        score -= min(0.5, penalty)

    # Repetition penalty (but recoverable)
    if obs.repetition > 0:
        score -= min(0.4, obs.repetition * 0.15)

    return clamp(score)

def update_profile(obs: PlayerObservation) -> BehaviorProfile:
    global current_profile

    step_logic_score = calculate_step_logic(obs)
    learning_rate = 0.1

    # --- LOGIC CONFIDENCE ---
    current_profile.logic_confidence = (
        current_profile.logic_confidence * (1 - learning_rate)
        + step_logic_score * learning_rate
    )

    # --- ADAPTABILITY ---
    if not obs.correct and obs.repetition > 0:
        current_profile.adaptability -= 0.02
    elif obs.correct and obs.repetition == 0:
        current_profile.adaptability += 0.015
    elif not obs.correct:
        current_profile.adaptability += 0.005

    # --- TRUST LEVEL ---
    if obs.correct and obs.repetition == 0:
        current_profile.trust_level += 0.01
    elif obs.repetition > 1:
        current_profile.trust_level -= 0.01

    # Trust dead-zone (prevents oscillation late game)
    if current_profile.trust_level > 0.85:
        current_profile.trust_level -= 0.002

    # --- CLAMP ---
    current_profile.logic_confidence = clamp(current_profile.logic_confidence)
    current_profile.trust_level = clamp(current_profile.trust_level)
    current_profile.adaptability = clamp(current_profile.adaptability)

    current_profile.samples += 1
    return current_profile