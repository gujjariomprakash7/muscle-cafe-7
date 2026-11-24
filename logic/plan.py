"""Simple weekly resistance-training split and direct-set planner.

This creates a flexible planning template, not a medical prescription or a
record of completed training. Weekly set counts are approximate direct-work
set targets; indirect work from compound lifts is not added to those totals.
"""

from collections import Counter

WEEKDAYS = [
    "Monday", "Tuesday", "Wednesday", "Thursday",
    "Friday", "Saturday", "Sunday",
]

# Day templates intentionally keep sessions focused. Smaller muscles can also
# receive indirect work from compound movements and are not counted twice here.
SESSION_TEMPLATES = {
    2: [
        ("Full Body A", ["Chest", "Back", "Quads", "Shoulders", "Biceps", "Triceps", "Core"]),
        ("Full Body B", ["Chest", "Back", "Hamstrings", "Glutes", "Calves", "Adductors", "Traps", "Forearms"]),
    ],
    3: [
        ("Full Body A", ["Chest", "Back", "Quads", "Shoulders", "Core"]),
        ("Full Body B", ["Chest", "Back", "Hamstrings", "Glutes", "Biceps", "Triceps"]),
        ("Full Body C", ["Quads", "Hamstrings", "Shoulders", "Calves", "Adductors", "Core"]),
    ],
    4: [
        ("Upper A", ["Chest", "Back", "Shoulders", "Biceps", "Triceps", "Traps", "Forearms"]),
        ("Lower A", ["Quads", "Hamstrings", "Glutes", "Calves", "Adductors", "Core"]),
        ("Upper B", ["Chest", "Back", "Shoulders", "Biceps", "Triceps", "Traps", "Forearms"]),
        ("Lower B", ["Quads", "Hamstrings", "Glutes", "Calves", "Adductors", "Core"]),
    ],
    5: [
        ("Upper A", ["Chest", "Back", "Shoulders", "Biceps", "Triceps", "Traps", "Forearms"]),
        ("Lower A", ["Quads", "Hamstrings", "Glutes", "Calves", "Adductors", "Core"]),
        ("Push", ["Chest", "Shoulders", "Triceps"]),
        ("Pull", ["Back", "Biceps", "Traps", "Forearms"]),
        ("Lower B", ["Quads", "Hamstrings", "Glutes", "Calves", "Adductors", "Core"]),
    ],
    6: [
        ("Push A", ["Chest", "Shoulders", "Triceps"]),
        ("Pull A", ["Back", "Biceps", "Traps", "Forearms"]),
        ("Legs A", ["Quads", "Hamstrings", "Glutes", "Calves", "Adductors", "Core"]),
        ("Push B", ["Chest", "Shoulders", "Triceps"]),
        ("Pull B", ["Back", "Biceps", "Traps", "Forearms"]),
        ("Legs B", ["Quads", "Hamstrings", "Glutes", "Calves", "Adductors", "Core"]),
    ],
}

BASE_WEEKLY_SETS = {
    "Beginner": 6,
    "Intermediate": 8,
    "Advanced": 10,
}


def _spread_priority_muscle(sessions, priority_muscle):
    """Ensure the chosen priority muscle appears in at least two sessions."""
    occurrences = sum(
        priority_muscle in session["muscles"] for session in sessions
    )
    while occurrences < min(2, len(sessions)):
        candidates = [s for s in sessions if priority_muscle not in s["muscles"]]
        if not candidates:
            break
        # Add it to the currently shortest session to keep session sizes balanced.
        chosen = min(candidates, key=lambda s: len(s["muscles"]))
        chosen["muscles"].append(priority_muscle)
        occurrences += 1


def _distribute_weekly_sets(sessions, experience, priority_muscle):
    base = BASE_WEEKLY_SETS.get(experience, 8)
    group_counts = Counter(
        muscle for session in sessions for muscle in session["muscles"]
    )

    weekly_volume = {}
    for muscle, appearances in group_counts.items():
        target = base + (2 if muscle == priority_muscle else 0)
        weekly_volume[muscle] = target
        quotient, remainder = divmod(target, appearances)
        for session in sessions:
            if muscle in session["muscles"]:
                session["sets_by_muscle"][muscle] = quotient
                if remainder > 0:
                    session["sets_by_muscle"][muscle] += 1
                    remainder -= 1

    return weekly_volume


def _recovery_warnings(sessions):
    """Flag repeated muscle groups scheduled on adjacent calendar days."""
    muscle_days = {}
    for session in sessions:
        for muscle in session["muscles"]:
            muscle_days.setdefault(muscle, []).append(session["day_index"])

    warnings = []
    for muscle, day_indexes in muscle_days.items():
        if len(day_indexes) < 2:
            continue
        ordered = sorted(day_indexes)
        gaps = [ordered[i + 1] - ordered[i] for i in range(len(ordered) - 1)]
        gaps.append((ordered[0] + 7) - ordered[-1])
        if any(gap == 1 for gap in gaps):
            warnings.append(muscle)

    return sorted(warnings)


def generate_weekly_plan(training_days, experience, priority_muscle):
    """Return sessions, estimated direct-set targets and recovery notes."""
    if not training_days:
        raise ValueError("Choose at least one training day.")
    if len(training_days) not in SESSION_TEMPLATES:
        raise ValueError("Choose between 2 and 6 training days per week.")
    if priority_muscle not in {
        muscle for template in SESSION_TEMPLATES.values()
        for _, muscles in template for muscle in muscles
    }:
        # The selected priority muscle may be an accessory not in a template;
        # it will be added to the two least-loaded days below.
        if not isinstance(priority_muscle, str) or not priority_muscle.strip():
            raise ValueError("Choose a valid priority muscle group.")

    ordered_days = sorted(training_days, key=WEEKDAYS.index)
    templates = SESSION_TEMPLATES[len(ordered_days)]

    sessions = []
    for day, (session_name, muscles) in zip(ordered_days, templates):
        sessions.append({
            "day": day,
            "day_index": WEEKDAYS.index(day),
            "session": session_name,
            "muscles": list(muscles),
            "sets_by_muscle": {},
        })

    _spread_priority_muscle(sessions, priority_muscle)
    weekly_volume = _distribute_weekly_sets(
        sessions, experience, priority_muscle
    )

    training_day_set = set(ordered_days)
    rest_days = [day for day in WEEKDAYS if day not in training_day_set]
    recovery_warnings = _recovery_warnings(sessions)

    return {
        "sessions": sessions,
        "weekly_volume": weekly_volume,
        "rest_days": rest_days,
        "recovery_warnings": recovery_warnings,
        "priority_muscle": priority_muscle,
        "experience": experience,
    }
