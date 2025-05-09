import random


def get_advice():
    advices = [
        "You should definitely stop scrolling and go drink some water.",
        "Take that nap. You deserve it.",
        "Don't text them. Seriously.",
        "Start before you're ready.",
        "Silence is also a clapback."
    ]
    return random.choice(advices)