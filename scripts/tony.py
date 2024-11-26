stress_levels = []


def record_stress():
    """Record a stress event and its level."""
    event = input("Enter the stress event (e.g., 'Fight with Carmela'): ").strip()
    while True:
        try:
            level = int(input("Enter the stress level (1-10): "))
            if 1 <= level <= 10:
                break
            else:
                print("Please enter a level between 1 and 10.")
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 10.")

    stress_levels.append({"event": event, "level": level})
    print(f"Recorded: '{event}' with stress level {level}/10.\n")


def view_stress_history():
    """Display all recorded stress events."""
    if not stress_levels:
        print("No stress events recorded yet.\n")
        return

    print("\n--- Stress History ---")
    for idx, stress in enumerate(stress_levels, 1):
        print(f"{idx}. {stress['event']} - Stress Level: {stress['level']}/10")
    print("----------------------\n")


def check_need_for_therapy():
    """Analyze stress levels and determine if therapy is needed."""
    if not stress_levels:
        print("No data to analyze. Add some stress events first.\n")
        return

    avg_stress = sum(s["level"] for s in stress_levels) / len(stress_levels)
    print(f"\nAverage Stress Level: {avg_stress:.2f}/10")
    if avg_stress > 7:
        print("Recommendation: Tony should schedule a session with Dr. Melfi.\n")
    else:
        print("Tony is managing his stress well... for now.\n")


def main():
    print("=== Tony's Anxiety Tracker ===")
    while True:
        print("\nOptions:")
        print("1. Record a stress event")
        print("2. View stress history")
        print("3. Check if Tony needs therapy")
        print("4. Exit")

        choice = input("Choose an option (1-4): ").strip()
        match choice:
            case "1":
                record_stress()
            case "2":
                view_stress_history()
            case "3":
                check_need_for_therapy()
            case "4":
                print("Exiting Tony's Anxiety Tracker. Stay stress-free!")
                break
            case _:
                print("Invalid choice. Please choose a valid option.\n")


if __name__ == "__main__":
    main()
