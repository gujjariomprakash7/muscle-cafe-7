"""Practical, food-first nutrition planning for Muscle Cafe.

Protein figures are approximate educational estimates for sample portions.
This module deliberately does not prescribe calories or medical diets.
"""

from datetime import datetime, timedelta

DIET_OPTIONS = ["Vegetarian", "Eggetarian", "Non-Vegetarian", "Vegan"]

# Meal examples use familiar foods and approximate portions. Actual values vary
# by recipe, brand, cooking method and the exact food selected.
MEAL_PLANS = {
    "Vegetarian": [
        {
            "name": "Breakfast",
            "foods": "2 moong-dal chillas (made with about 70 g dry moong) + 150 g plain curd + fruit",
            "protein_g": 22,
            "why": "Moong and curd provide a mix of plant and dairy protein; fruit adds fibre and micronutrients.",
        },
        {
            "name": "Lunch",
            "foods": "Paneer bhurji (about 150 g paneer) + 2 whole-wheat rotis + vegetables",
            "protein_g": 33,
            "why": "Paneer is the main protein source; roti and vegetables round out the meal.",
        },
        {
            "name": "Snack",
            "foods": "About 200 g Greek-style/hung curd + a banana or seasonal fruit",
            "protein_g": 18,
            "why": "A convenient high-protein snack. Regular curd may contain less protein than Greek-style or hung curd.",
        },
        {
            "name": "Dinner",
            "foods": "150 g tofu + 1/2 to 1 cup dal + vegetables + rice or roti",
            "protein_g": 27,
            "why": "Tofu and dal add plant protein; include vegetables and a carbohydrate source for a balanced meal.",
        },
    ],
    "Eggetarian": [
        {
            "name": "Breakfast",
            "foods": "3 eggs (omelette or boiled) + 250 ml milk + whole-grain toast",
            "protein_g": 26,
            "why": "Eggs and milk provide convenient complete protein; add vegetables to the omelette if available.",
        },
        {
            "name": "Lunch",
            "foods": "Paneer bhurji (about 150 g paneer) + 2 whole-wheat rotis + vegetables",
            "protein_g": 33,
            "why": "A dairy-based vegetarian lunch with vegetables and a familiar staple.",
        },
        {
            "name": "Snack",
            "foods": "About 200 g Greek-style/hung curd + fruit",
            "protein_g": 18,
            "why": "A simple protein-rich snack between main meals.",
        },
        {
            "name": "Dinner",
            "foods": "2 eggs + 1 cup dal + vegetables + 1 roti or a small serving of rice",
            "protein_g": 25,
            "why": "Combines eggs and pulses; adjust the staple portion to appetite and activity.",
        },
    ],
    "Non-Vegetarian": [
        {
            "name": "Breakfast",
            "foods": "3 eggs (omelette or boiled) + 250 ml milk + whole-grain toast",
            "protein_g": 26,
            "why": "Eggs and milk offer a convenient protein-rich breakfast; add vegetables or fruit.",
        },
        {
            "name": "Lunch",
            "foods": "About 120 g cooked chicken + 2 whole-wheat rotis + vegetables",
            "protein_g": 42,
            "why": "Chicken supplies most of the protein; roti and vegetables make this a fuller meal.",
        },
        {
            "name": "Snack",
            "foods": "About 200 g Greek-style/hung curd + fruit",
            "protein_g": 18,
            "why": "A convenient dairy-based snack. Choose plain curd and adjust the portion to appetite.",
        },
        {
            "name": "Dinner",
            "foods": "About 120 g cooked fish + 1/2 cup dal + vegetables + rice",
            "protein_g": 34,
            "why": "Fish and pulses provide protein; include vegetables and a carbohydrate source.",
        },
    ],
    "Vegan": [
        {
            "name": "Breakfast",
            "foods": "60 g oats + 250 ml unsweetened soy milk + 1 tbsp peanut butter + fruit",
            "protein_g": 20,
            "why": "Soy milk, oats and peanut butter combine to make a convenient plant-based breakfast.",
        },
        {
            "name": "Lunch",
            "foods": "Soy-chunk curry (about 50 g dry soy chunks before cooking) + rice or 2 rotis + vegetables",
            "protein_g": 30,
            "why": "Soy chunks are a concentrated plant-protein option; cook them thoroughly and season to taste.",
        },
        {
            "name": "Snack",
            "foods": "About 50 g roasted chana + 250 ml soy milk",
            "protein_g": 18,
            "why": "A portable plant-based snack with protein and fibre.",
        },
        {
            "name": "Dinner",
            "foods": "About 180 g tofu + 1/2 cup dal + vegetables + rice or roti",
            "protein_g": 27,
            "why": "Tofu and pulses supply plant protein; vary legumes and vegetables across the week.",
        },
    ],
}

PROTEIN_BOOSTERS = {
    "Vegetarian": [
        {"name": "250 ml milk", "protein_g": 8},
        {"name": "100 g paneer", "protein_g": 18},
        {"name": "200 g Greek-style/hung curd", "protein_g": 18},
        {"name": "150 g tofu", "protein_g": 18},
    ],
    "Eggetarian": [
        {"name": "2 eggs", "protein_g": 12},
        {"name": "250 ml milk", "protein_g": 8},
        {"name": "200 g Greek-style/hung curd", "protein_g": 18},
        {"name": "100 g paneer", "protein_g": 18},
    ],
    "Non-Vegetarian": [
        {"name": "2 eggs", "protein_g": 12},
        {"name": "100 g cooked chicken", "protein_g": 31},
        {"name": "100 g cooked fish", "protein_g": 22},
        {"name": "200 g Greek-style/hung curd", "protein_g": 18},
    ],
    "Vegan": [
        {"name": "50 g dry soy chunks (before cooking)", "protein_g": 26},
        {"name": "150 g tofu", "protein_g": 18},
        {"name": "250 ml soy milk", "protein_g": 8},
        {"name": "50 g roasted chana", "protein_g": 10},
    ],
}


def estimate_protein_target(weight_kg, goal):
    """Return an educational daily protein range in grams.

    The range is based on body weight and broad exercise-goal categories. It is
    not suitable as an individual prescription for people with medical needs.
    """
    weight = float(weight_kg)
    if weight <= 0:
        raise ValueError("Weight must be greater than zero.")

    if goal == "Improve General Fitness":
        low_factor, high_factor = 1.2, 1.6
    else:
        # For resistance-training goals, this is a commonly cited range for
        # healthy exercising adults; see the ISSN position stand.
        low_factor, high_factor = 1.4, 2.0

    return round(weight * low_factor), round(weight * high_factor)


def get_meal_plan(diet):
    """Return meal suggestions for the saved food preference."""
    return [dict(meal) for meal in MEAL_PLANS.get(diet, MEAL_PLANS["Vegetarian"])]


def get_protein_boosters(diet):
    """Return small add-on options compatible with the selected diet."""
    return [dict(item) for item in PROTEIN_BOOSTERS.get(diet, [])]


def suggest_meal_times(wake_time, sleep_time, meal_count=4):
    """Spread suggested meal times across the waking day.

    This is a flexible scheduling aid only; meals do not need to be eaten at
    exact times, and the first/last slots are not tied to exercise timing.
    """
    try:
        wake = datetime.strptime(str(wake_time), "%H:%M")
        sleep = datetime.strptime(str(sleep_time), "%H:%M")
    except (TypeError, ValueError):
        wake = datetime.strptime("07:00", "%H:%M")
        sleep = datetime.strptime("23:00", "%H:%M")

    if sleep <= wake:
        sleep += timedelta(days=1)

    duration_minutes = int((sleep - wake).total_seconds() // 60)
    if meal_count <= 1:
        positions = [0.5]
    else:
        # Keep a little breathing room after waking and before bedtime.
        positions = [0.08 + (0.84 * i / (meal_count - 1)) for i in range(meal_count)]

    times = []
    for position in positions:
        meal_time = wake + timedelta(minutes=round(duration_minutes * position))
        times.append(meal_time.strftime("%I:%M %p").lstrip("0"))
    return times


def build_nutrition_plan(weight_kg, goal, diet, wake_time, sleep_time):
    """Build a food-first example day plus a protein range and meal times."""
    meals = get_meal_plan(diet)
    protein_low, protein_high = estimate_protein_target(weight_kg, goal)
    meal_times = suggest_meal_times(wake_time, sleep_time, len(meals))
    sample_total = sum(meal["protein_g"] for meal in meals)

    for meal, meal_time in zip(meals, meal_times):
        meal["suggested_time"] = meal_time

    return {
        "diet": diet,
        "goal": goal,
        "weight_kg": float(weight_kg),
        "protein_low_g": protein_low,
        "protein_high_g": protein_high,
        "meals": meals,
        "sample_protein_total_g": sample_total,
        "protein_boosters": get_protein_boosters(diet),
    }
