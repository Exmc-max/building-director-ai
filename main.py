from fastapi import FastAPI
from schemas import PlayerObservation, DirectorInstructions
from director import determine_directives

app = FastAPI(title="The Sixth Soul - Director AI")

@app.post("/analyze", response_model=DirectorInstructions)
def analyze_player(obs: PlayerObservation):
    # 1. OBSERVE: Receive data from Unreal
    
    # 2. DIRECT: Decide the INTENT
    instructions = determine_directives(obs)
    
    # 3. LOG: Prove we aren't spawning objects directly
    print(f"PLAYER STATE: Logic={obs.logic_confidence} | Trust={obs.trust_level}")
    print(f"DIRECTOR ORDER: Make it {instructions.anomaly_level}, Probability: {instructions.anomaly_probability}")
    
    return instructions