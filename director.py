from schemas import DirectorInstructions
from state import BehaviorProfile

def determine_directives(profile: BehaviorProfile) -> DirectorInstructions:
    """
    Director policy:
    - Observe behavior stability
    - Apply pressure only when confidence is high
    - Withdraw intervention as convergence is reached
    """

    # Default: minimal interference
    anomaly_level = "subtle"
    anomaly_probability = 0.0
    anomaly_category = "environment"
    lie_allowed = False

    # --- BEHAVIOR INTERPRETATION ---
    confident = profile.logic_confidence > 0.7
    unstable = profile.logic_confidence < 0.4
    trusting = profile.trust_level > 0.6
    converged = profile.trust_level > 0.9

    # --- MAIN POLICY ---

    # Phase 1: Confident but not yet converged → test gently
    if confident and not converged:
        anomaly_level = "subtle"
        anomaly_probability = 1.0
        anomaly_category = "logic"
        lie_allowed = False

    # Phase 2: Unstable but still trusting → restore consistency
    elif unstable and trusting:
        anomaly_level = "subtle"
        anomaly_probability = 0.0
        anomaly_category = "environment"
        lie_allowed = False

    # Phase 3: Unstable and untrusting → pressure, but do NOT lie
    elif unstable and not trusting:
        anomaly_level = "aggressive"
        anomaly_probability = 1.0
        anomaly_category = "audio"
        lie_allowed = False

    # Phase 4: Convergence → withdraw
    if converged:
        anomaly_level = "subtle"
        anomaly_probability = 0.0
        anomaly_category = "environment"
        lie_allowed = False

    return DirectorInstructions(
        anomaly_level=anomaly_level,
        anomaly_probability=anomaly_probability,
        anomaly_category=anomaly_category,
        lie_allowed=lie_allowed
    )