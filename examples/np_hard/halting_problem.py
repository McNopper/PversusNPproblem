"""
The Halting Problem -- NP-Hard (undecidable)
============================================
The Halting Problem asks: given a program and its input, will the program
eventually halt, or run forever?

Alan Turing proved in 1936 that NO algorithm can solve this for all
program/input pairs -- it is *undecidable* (not just hard, but impossible).

This makes it strictly harder than NP-Complete problems. It is NP-Hard
because any NP problem can be reduced to it, but it is NOT in NP (or even
in any computable complexity class).

This file demonstrates the classic proof by contradiction.
"""


def proof_by_contradiction():
    """
    Suppose a magic function halts(program, input) -> bool existed.
    We construct a paradoxical program that breaks it.
    """
    print("=" * 60)
    print("Proof that the Halting Problem is undecidable")
    print("=" * 60)
    print("""
Assume a magic oracle exists:

    def halts(program, input) -> bool:
        # Returns True  if program(input) halts
        # Returns False if program(input) loops forever

Now define this program:

    def paradox(program):
        if halts(program, program):
            while True: pass  # loop forever
        else:
            return             # halt

Ask: what happens when we call paradox(paradox)?

  Case 1: halts(paradox, paradox) == True
          -> paradox(paradox) enters the infinite loop -> it does NOT halt.
          Contradiction!

  Case 2: halts(paradox, paradox) == False
          -> paradox(paradox) returns immediately -> it DOES halt.
          Contradiction!

Both cases lead to a contradiction.
Therefore, no such oracle can exist.
The Halting Problem is UNDECIDABLE.
""")


def demo_timeout_approximation(func, input_val, timeout_seconds: float):
    """
    In practice, we can only approximate: run the program for a fixed time.
    If it halts within timeout -> it halted.
    If not -> we don't know (might halt later, might loop forever).
    """
    import threading

    result = {"halted": False}

    def target():
        try:
            func(input_val)
            result["halted"] = True
        except Exception:
            result["halted"] = True  # Crashed, but did terminate

    thread = threading.Thread(target=target, daemon=True)
    thread.start()
    thread.join(timeout=timeout_seconds)

    if result["halted"]:
        return "HALTED within timeout"
    else:
        return f"UNKNOWN -- did not halt within {timeout_seconds}s"


if __name__ == "__main__":
    proof_by_contradiction()

    print("Practical demonstration (timeout-based approximation):\n")

    # Program that halts
    def halting_program(n):
        return sum(range(n))

    # Program that loops forever
    def infinite_loop(_):
        while True:
            pass

    for name, func in [("halting_program(1000)", halting_program),
                       ("infinite_loop(None)",   infinite_loop)]:
        result = demo_timeout_approximation(func, 1000, timeout_seconds=0.5)
        print(f"  {name}: {result}")

    print("\nNote: timeout gives 'HALTED' or 'UNKNOWN', never a guaranteed answer.")
