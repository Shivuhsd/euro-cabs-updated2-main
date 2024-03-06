import random

def generate_unique_random_numbers(count):
    numbers = list(range(count))
    random.shuffle(numbers)
    id = "CM"
    for i in numbers:
        id = id + str(i)
    return id
