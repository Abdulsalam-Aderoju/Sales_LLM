# Prepare some keywords
# Check if there is any of the keywords in the prompt provided
# If there is, prompt can then be processed by model
# If there isn't, user should be told to ask data related question

data_keywords = ["highest", "trend", "lowest", "top", "leading", "insights"]

def is_relevant(prompt):
    return any(prompt.lower() in keyword for keyword in data_keywords)


numbers = [1, 5, 6, 3, 2, 6, 8, 0]

for number in numbers:
    print(number)

def get_number(numbers):
    for number in numbers:
        yield number