import random

def get_plan():
    plans = [
        "You've absolutely got to check out Kerosene Bunk at least once—it's an experience!",
        "Go for a solo lunch date, and pretend you're in a movie.",
        "It's a perfect evening for rooftop chai and deep conversations.",
        "Find a cozy bookstore, lose track of time.",
        "Call that friend you keep ghosting—today's the day."
    ]
    return random.choice(plans)