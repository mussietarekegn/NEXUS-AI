def assign_priority(message):
    message = message.lower()

    high_urgency_words = [
        "urgent",
        "immediately",
        "emergency",
        "hacked",
        "fraud",
        "unauthorized",
        "money stolen",
        "cannot access",
        "completely broken"
    ]

    medium_urgency_words = [
        "delayed",
        "not working",
        "failed",
        "declined",
        "missing",
        "damaged",
        "error"
    ]

    for word in high_urgency_words:
        if word in message:
            return "High"

    for word in medium_urgency_words:
        if word in message:
            return "Medium"

    return "Low"

if __name__ == "__main__":
    examples = [
        "Someone hacked my account",
        "My delivery is delayed",
        "What are your working hours?"
    ]

    for message in examples:
        priority = assign_priority(message)
        print(message, "->", priority)