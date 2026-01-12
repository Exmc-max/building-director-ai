from fastapi import FastAPI
from schemas import PlayerObservation, DirectorInstructions
from state import update_profile
from director import determine_directives
from rules import enforce_safety

app = FastAPI()

@app.post("/evaluate", response_model=DirectorInstructions)
def evaluate_player(obs: PlayerObservation):
    
    # 1. UPDATE MEMORY
    profile = update_profile(obs)
    
    # 2. DIRECTOR DECIDES
    raw_instructions = determine_directives(profile)
    
    # 3. RULES CHECK
    safe_instructions = enforce_safety(raw_instructions, obs)
    
    # 4. LOGGING
    print(f"IN: {obs.logic_confidence} | MEMORY: {profile.logic_confidence:.2f} | OUT: {safe_instructions.anomaly_level}")

    return safe_instructions