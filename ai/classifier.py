# Placeholder for your future AI model

def classify_issue(description: str):
    # Later you'll replace this with your ML model
    keywords = ["water", "road", "electricity"]
    if any(word in description.lower() for word in keywords):
        return "Infrastructure Issue"
    return "General Issue"
