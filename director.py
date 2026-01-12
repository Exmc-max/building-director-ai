from schemas import PlayerObservation, DirectorInstructions

def determine_directives(obs: PlayerObservation) -> DirectorInstructions:
    
    # DEFAULT STATE (The "Control Group")
    level = "subtle"
    prob = 0.3
    cat = "environment"
    lie = False

    # RULE 1: If player is very logical, challenge them subtly
    if obs.logic_confidence > 0.7:
        level = "subtle"
        prob = 0.8          # High chance, but hard to see
        cat = "logic"       # Mess with the numbers/rules
        lie = False         # But don't cheat yet

    # RULE 2: If player is panicking (low logic, high repetition)
    if obs.logic_confidence < 0.3 and obs.repetition > 2:
        level = "aggressive"
        prob = 1.0          # Force an anomaly
        cat = "audio"       # Scare them
        lie = True          # Break the rules to confuse them

    # RULE 3: The Convergence (End Game)
    if obs.trust_level > 0.9:
        level = "subtle"
        prob = 0.0          # Stop anomalies
        cat = "environment"
        lie = False

    return DirectorInstructions(
        anomaly_level=level,
        anomaly_probability=prob,
        anomaly_category=cat,
        lie_allowed=lie
    )