from schemas import PlayerObservation
from state import update_profile, BehaviorProfile
from director import determine_directives
import state  # We import the module to reset the global variable

def reset_memory():
    """Wipes the AI memory clean for the next test."""
    state.current_profile = BehaviorProfile()

def run_test(name, sequence):
    print(f"\n{'='*10} TEST: {name} {'='*10}")
    reset_memory()
    
    for i, data in enumerate(sequence):
        # 1. Feed Input
        obs = PlayerObservation(**data)
        
        # 2. Update Memory
        profile = update_profile(obs)
        
        # 3. Get Decision
        decision = determine_directives(profile)
        
        # 4. Print Result
        print(f"STEP {i+1}: Correct={obs.correct}, Time={obs.hesitation}s, Repeats={obs.repetition}")
        print(f"   [MEMORY]  Logic: {profile.logic_confidence:.2f} | Trust: {profile.trust_level:.2f} | Adapt: {profile.adaptability:.2f}")
        print(f"   [DIRECTOR] {decision.anomaly_level.upper()} (Prob: {decision.anomaly_probability}) | Lie: {decision.lie_allowed}")
        print("-" * 40)

# --- DEFINING THE SCENARIOS ---

# TEST 1: The Careful Logic Player (Ideal)
scenario_careful = [
    {"correct": True, "repetition": 0, "hesitation": 4.0},
    {"correct": True, "repetition": 0, "hesitation": 3.5},
    {"correct": True, "repetition": 0, "hesitation": 2.5},
    {"correct": True, "repetition": 0, "hesitation": 2.0},
    {"correct": True, "repetition": 0, "hesitation": 1.5},
]

# TEST 2: The Panic Player (Recovering)
scenario_panic = [
    {"correct": False, "repetition": 1, "hesitation": 6.0}, # Panic
    {"correct": False, "repetition": 2, "hesitation": 7.0}, # Worse
    {"correct": False, "repetition": 3, "hesitation": 6.5}, # Peak panic
    {"correct": True,  "repetition": 0, "hesitation": 3.0}, # Recovery starts
    {"correct": True,  "repetition": 0, "hesitation": 2.5}, # Stabilizing
]

# TEST 3: The Brute-Forcer (Anti-Cheese)
scenario_brute = [
    {"correct": False, "repetition": 1, "hesitation": 1.0}, # Spam guessing
    {"correct": False, "repetition": 2, "hesitation": 1.0},
    {"correct": False, "repetition": 3, "hesitation": 1.0},
    {"correct": True,  "repetition": 3, "hesitation": 0.8}, # Got lucky
]

# TEST 5: The Ending Check (Convergence)
# We simulate 15 perfect moves to see if it stops interfering
scenario_ending = [{"correct": True, "repetition": 0, "hesitation": 2.0} for _ in range(15)]

# --- RUNNING THEM ---
if __name__ == "__main__":
    run_test("1. THE CAREFUL PLAYER", scenario_careful)
    run_test("2. THE PANIC PLAYER", scenario_panic)
    run_test("3. THE BRUTE FORCER", scenario_brute)
    run_test("5. THE ENDING CONVERGENCE", scenario_ending)