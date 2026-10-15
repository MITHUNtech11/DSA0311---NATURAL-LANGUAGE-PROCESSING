"""
Experiment 2: Finite State Automaton (FSA / DFA)
Aim: Implement a basic finite state automaton that recognizes a specific language or pattern.
     In this example, we create an automaton to match strings ending with 'ab' using Python.
"""

class StringEndingWithAB_FSA:
    """
    Deterministic Finite Automaton (DFA) recognizing the language:
    L = { w in {a, b}* | w ends with 'ab' }
    
    Formal 5-Tuple Definition:
      Q = {q0, q1, q2}
      Sigma = {'a', 'b'}
      q0 = Initial State
      F = {q2} (Accepting State)
      delta = Transition Function
    """
    def __init__(self):
        self.states = {"q0", "q1", "q2"}
        self.alphabet = {"a", "b"}
        self.start_state = "q0"
        self.accept_states = {"q2"}
        
        # State Transition Table
        self.transitions = {
            ("q0", "a"): "q1",
            ("q0", "b"): "q0",
            ("q1", "a"): "q1",
            ("q1", "b"): "q2",
            ("q2", "a"): "q1",
            ("q2", "b"): "q0",
        }

    def process_string(self, input_string: str):
        """Processes the input string through the automaton and records state transitions."""
        current_state = self.start_state
        state_history = [current_state]

        for char in input_string:
            if char not in self.alphabet:
                return {
                    "input": input_string,
                    "accepted": False,
                    "final_state": "INVALID",
                    "history": state_history,
                    "error": f"Invalid symbol '{char}' not in alphabet {self.alphabet}"
                }
            current_state = self.transitions[(current_state, char)]
            state_history.append(current_state)

        is_accepted = current_state in self.accept_states
        return {
            "input": input_string,
            "accepted": is_accepted,
            "final_state": current_state,
            "history": state_history,
            "error": None
        }

def run_experiment():
    print("=" * 70)
    print("EXPERIMENT 2: FINITE STATE AUTOMATON (FSA) ENDING WITH 'ab'")
    print("=" * 70)

    fsa = StringEndingWithAB_FSA()

    print("\n[Formal Automaton Specification]")
    print(" - States (Q): {q0 (Start), q1 (Saw 'a'), q2 (Saw 'ab' - Accept)}")
    print(" - Alphabet (Sigma): {'a', 'b'}")
    print(" - Initial State: q0")
    print(" - Accepting State (F): {q2}")
    print("\n[Transition Table]")
    print(f"{'Current State':<15} | {'Input Symbol':<14} | {'Next State'}")
    print("-" * 45)
    for (state, sym), nxt in sorted(fsa.transitions.items()):
        print(f"{state:<15} | {sym:<14} | {nxt}")

    test_strings = [
        "ab",       # Valid (ends with ab)
        "aab",      # Valid (ends with ab)
        "bab",      # Valid (ends with ab)
        "babaab",   # Valid (ends with ab)
        "aba",      # Invalid (ends with a)
        "b",        # Invalid (ends with b)
        "aabb",     # Invalid (ends with bb)
        "a",        # Invalid (ends with a)
        "",         # Invalid (empty string)
        "abac"      # Invalid (contains symbol 'c')
    ]

    print("\n" + "=" * 70)
    print("TEST STRING EXECUTION TRACE & RESULTS")
    print("=" * 70)
    print(f"{'Test String':<12} | {'State Path History':<32} | {'Final':<6} | {'Status'}")
    print("-" * 70)

    for s in test_strings:
        res = fsa.process_string(s)
        path_str = " -> ".join(res["history"])
        if res["error"]:
            status = f"REJECTED ({res['error']})"
        else:
            status = "ACCEPTED" if res["accepted"] else "REJECTED"
        
        display_str = f"'{s}'" if s != "" else "'' (empty)"
        print(f"{display_str:<12} | {path_str:<32} | {res['final_state']:<6} | {status}")

    print("=" * 70)
    print("EXPERIMENT 2 COMPLETED SUCCESSFULLY")
    print("=" * 70)

if __name__ == "__main__":
    run_experiment()
