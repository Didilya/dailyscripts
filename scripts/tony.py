# Before running the script do not forget
# pip install clickhouse-connect
# curl https://clickhouse.com/ | sh
# ./clickhouse server

import clickhouse_connect

# Initialize the ClickHouse client
client = clickhouse_connect.get_client(host='localhost', port=8123, username='default', password='')

# Create the stress_events table if it doesn't exist
client.command("""
CREATE TABLE IF NOT EXISTS stress_events (
    id UInt64,
    event String,
    level UInt8,
    timestamp DateTime DEFAULT now()
) ENGINE = MergeTree()
ORDER BY id
""")


def save_to_clickhouse(event, level):
    """Save a stress event to the ClickHouse database."""
    # Fetch the current maximum ID from the table or set it to 0
    last_id = client.query("SELECT max(id) FROM stress_events").result_rows[0][0] or 0
    new_id = last_id + 1

    query = "INSERT INTO stress_events (id, event, level) VALUES (%s, %s, %s)"
    parameters = (new_id, event, level)

    try:
        client.command(query, parameters)
        print(f"Event saved to ClickHouse: '{event}' with stress level {level}/10.\n")
    except Exception as e:
        print(f"Error saving to ClickHouse: {e}")


def record_stress():
    """Record a stress event and its level."""
    stress_levels = []
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
    save_to_clickhouse(event, level)


def view_stress_history():
    """Display all recorded stress events."""
    # Fetch data from ClickHouse
    events = client.query("SELECT event, level, timestamp FROM stress_events ORDER BY timestamp").result_rows

    if not events:
        print("No stress events recorded yet.\n")
        return

    print("\n--- Stress History ---")
    for idx, (event, level, timestamp) in enumerate(events, 1):
        print(f"{idx}. {event} - Stress Level: {level}/10 (Timestamp: {timestamp})")
    print("----------------------\n")


def check_need_for_therapy():
    """Analyze stress levels and determine if therapy is needed."""
    # Calculate average stress level from ClickHouse
    result = client.query("SELECT AVG(level) FROM stress_events").result_rows[0][0]
    if result is None:
        print("No data to analyze. Add some stress events first.\n")
        return

    avg_stress = result
    print(f"\nAverage Stress Level: {avg_stress:.2f}/10")
    if avg_stress >= 7:
        print("Recommendation: Tony should schedule a session with Dr. Melfi.\n")
    else:
        print("Tony is managing his stress well... for now.\n")


def main():
    print("=== Tony's Anxiety Tracker ===")
    while True:
        print("\nOptions:\n1. Record a stress event\n2. View stress history\n3. Check if Tony needs therapy")

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
