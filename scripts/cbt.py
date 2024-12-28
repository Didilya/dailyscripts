import csv
from collections import Counter
from datetime import datetime


def welcome_message():
    print("Welcome to the CBT Assistant!")
    print("This program is designed to help you explore your thoughts, feelings, and behaviors.")
    print("Let's work together to identify and challenge negative thought patterns.")
    print("Note: This tool is not a substitute for professional therapy.\n")


def identify_situation():
    print("\nStep 1: Identifying the Situation")
    situation = input("Think of a recent situation that caused you distress. Describe it briefly: ")
    return situation


def explore_emotions():
    print("\nStep 2: Exploring Your Emotions")
    emotions = input("What emotions did you feel in this situation? (e.g., anger, sadness, anxiety): ")
    return emotions


def explore_body():
    print("\nStep 3: Exploring Physical Sensations")
    print("Distressing situations often trigger physical sensations in the body. Let’s explore these.")
    body_sensations = input("What physical sensations did you notice? (e.g., tight chest, rapid heartbeat, sweating): ")
    return body_sensations


def identify_thoughts():
    print("\nStep 4: Identifying Automatic Thoughts")
    print(
        "Sometimes, distressing situations trigger automatic thoughts. These thoughts might be overly negative or unhelpful.")
    thoughts = input("What thoughts went through your mind during the situation? ")
    belief = input(
        "On a scale of 1 to 10, how strongly did you believe these thoughts? (1 = not at all, 10 = completely): ")
    while belief.isnumeric() is False:
        belief = input(
            "Please enter a number (1 = not at all, 10 = completely) - how strongly did you believe these thoughts?: ")
    return thoughts, belief


def challenge_thoughts(thoughts):
    print("\nStep 5: Challenging Negative Thoughts")
    print("Let's examine these thoughts and see if they are accurate or helpful.")
    print(f"Your thought: '{thoughts}'")
    print("Consider the following questions:")
    print("- What evidence supports this thought?")
    print("- What evidence contradicts it?")
    print("- Could there be an alternative explanation?")
    print("- How would you view this situation if a friend experienced it?")
    reframe = input(
        "Based on this reflection, how can you reframe this thought into a more balanced or constructive perspective? ")
    return reframe


def reflect_on_behaviors():
    print("\nStep 6: Reflecting on Behaviors")
    behavior = input("How did you respond to the situation? What actions did you take? ")
    print("Consider this:")
    print("- Did your actions align with your values?")
    print("- Were they helpful in resolving the situation?")
    alternative = input("If the same situation happened again, how might you respond differently? ")
    return behavior, alternative


def summarize(situation, emotions, body_sensations, thoughts, belief, reframe, behavior, alternative):
    print("\nSummary of Your CBT Session:")
    print(f"Situation: {situation}")
    print(f"Emotions: {emotions}")
    print(f"Body Sensations: {body_sensations}")
    print(f"Original Thought: {thoughts} (Belief: {belief})")
    print(f"Reframed Thought: {reframe}")
    print(f"Behavior: {behavior}")
    print(f"Alternative Response: {alternative}")
    print("\nGreat job reflecting and working through this exercise!")
    print("Remember, progress takes time. Be kind to yourself as you continue to grow.")

    file_name = "CBT_Session_Summary.csv"

    header = ['Created Date', 'Situation', 'Emotions', 'Body Sensations', 'Original Thought',
              'Level of Belief in Thought', 'Reframed Thought', 'Behavior', 'Alternative Response']
    data = [datetime.today().strftime('%Y-%m-%d'), situation, emotions, body_sensations, thoughts, belief, reframe,
            behavior, alternative]

    try:
        # Check if the file exists and write data accordingly
        with open(file_name, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # Write header only if the file is new
            if file.tell() == 0:
                writer.writerow(header)
            writer.writerow(data)
        print(f"\nYour session summary has been saved to {file_name}.")
    except Exception as e:
        print(f"An error occurred while saving the data to the file: {e}")


def analyze_progress(file_name="CBT_Session_Summary.csv"):
    print("\nAnalyzing your CBT progress so far...")
    try:
        with open(file_name, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            emotion_counter = Counter()
            max_belief = -1
            max_thought = None
            rows = []

            for row in reader:
                rows.append(row)

                emotions = row['Emotions']
                if emotions:
                    words = [word.strip().lower() for word in emotions.replace(',', ' ').split()]
                    emotion_counter.update(words)

                belief = int(row['Level of Belief in Thought'])
                if belief > max_belief:
                    max_belief = belief
                    max_thought = row['Original Thought']

            # Display most common emotions
            most_common_emotions = emotion_counter.most_common(5)
            print("Most Common Emotions:")
            for emotion, count in most_common_emotions:
                print(f"- {emotion}: {count} occurrences")

            if max_thought:
                print(f"\nThe thought with the highest belief level ({max_belief}): '{max_thought}'")
                updated_belief = input(
                    "Do you still believe in this thought at the same level? (yes/no): ").strip().lower()

                if updated_belief == 'no':
                    new_belief = int(input("On a scale of 1 to 10, what is your new level of belief in this thought? "))

                    for row in rows:
                        if row['Original Thought'] == max_thought:
                            row['Belief in Thought updated'] = new_belief

                    with open(file_name, mode='w', newline='', encoding='utf-8') as file:
                        fieldnames = list(rows[0].keys())
                        writer = csv.DictWriter(file, fieldnames=fieldnames)
                        writer.writeheader()
                        writer.writerows(rows)

                    print("\nThe belief level has been updated in the file.")

    except FileNotFoundError:
        print("No session summary file found. Complete at least one session to start tracking progress.")
    except Exception as e:
        print(f"An error occurred while analyzing progress: {e}")


def main():
    welcome_message()

    # Step-by-step CBT process
    situation = identify_situation()
    emotions = explore_emotions()
    body_sensations = explore_body()
    thoughts, belief = identify_thoughts()
    reframe = challenge_thoughts(thoughts)
    behavior, alternative = reflect_on_behaviors()

    # Summarize and conclude
    summarize(situation, emotions, body_sensations, thoughts, belief, reframe, behavior, alternative)

    # Analyze progress
    analyze_progress()


if __name__ == "__main__":
    main()
