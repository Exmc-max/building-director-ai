from schemas import DirectorInstructions, PlayerObservation

def enforce_safety(instructions: DirectorInstructions, obs: PlayerObservation) -> DirectorInstructions:
    
    # RULE 1: NO EARLY LYING
    # If the player is new (repetition low), the building must be honest.
    if obs.repetition < 3 and instructions.lie_allowed:
        instructions.lie_allowed = False
        print("SAFETY: Prevented early lying.")

    # RULE 2: ANOMALY CAP
    # Never go aggressive if trust is high (The Ending Logic)
    if obs.trust_level > 0.8 and instructions.anomaly_level == "aggressive":
        instructions.anomaly_level = "subtle"
        print("SAFETY: Clamped aggression due to high trust.")

    return instructions