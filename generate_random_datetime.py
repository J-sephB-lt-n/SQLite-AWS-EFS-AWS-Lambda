from random import randrange
from datetime import timedelta

def generate_random_datetime(start, end):
    """
    This function will return a random datetime between two datetime 
    objects.
    This code is from an answer to this Stack Overflow question: 
        https://stackoverflow.com/questions/553303/generate-a-random-date-between-two-other-dates
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)
