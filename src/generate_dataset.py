import random 
import pandas as pd
from pathlib import Path 

random.seed(42)

templates = {
    "Account": [
        "I cannot log into my account",
        "I forgot my password",
        "My account has been locked",
        "I cannot reset my password",
        "I need to update my profile",
        "Someone accessed my account",
        "I cannot verify my email",
        "My login is not working",
    ],

    "Payment": [
        "My payment was declined",
        "I was charged twice",
        "I need a refund",
        "My transaction is pending",
        "I cannot add my credit card",
        "The invoice amount is incorrect",
        "My subscription payment failed",
        "I have a billing problem",
    ],

    "Technical": [
        "The application keeps crashing",
        "The website is loading slowly",
        "I found a bug in the application",
        "The application shows a blank screen",
        "I cannot upload my file",
        "The system is not responding",
        "I receive an unexpected error",
        "The application stopped working",
    ],

    "Delivery": [
        "Where is my package?",
        "My delivery is delayed",
        "I received the wrong product",
        "My package has not arrived",
        "I want to track my order",
        "My order is missing",
        "The delivery address is incorrect",
        "My package arrived damaged",
    ],

    "General": [
        "What are your working hours?",
        "How can I contact support?",
        "I want to learn about your services",
        "Where is your company located?",
        "How do I create an account?",
        "Can you explain your pricing?",
        "I have a general question",
        "Where can I find your documentation?",
    ],
}

records = []

ticket_id = 1

for category, messages in templates.items():

    for i in range(200):

        template_index = random.randrange(len(messages))
        message = messages[template_index]

        variations = [
            message,
            message.lower(),
            message + " please help ",
            "Hello, " + message.lower(),
            message + "!",
        ]

        selected_message = random.choice(variations)

        if category == "Technical":
            priority = random.choice(["High", "Medium"])
        elif category == "Payment":
            priority = random.choice(["High", "Medium"])
        elif category == "General":
            priority = "Low"
        else:
            priority = random.choice(["Low", "Medium", "High"])

        records.append({
            "ticket_id" : ticket_id,
            "message" : selected_message,
            "category" : category,
            "priority" : priority,
            "template_id" : f"{category}_{template_index}"
        })

        ticket_id += 1

df = pd.DataFrame(records)

df = df.sample(frac=1, random_state=42).reset_index(drop=True)

output_path = Path("data/raw/support_tickets.csv")
output_path.parent.mkdir(parents=True, exist_ok=True)

df.to_csv(output_path, index=False)

print("Dataset generated successfully!")
print("Total records:", len(df))
print(df.head(10))