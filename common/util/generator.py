import random
import string


def get_random_id(length=8):
    """
    :param length: Length of the required random id
    :return: Random ID consisting of lower and upper case characters and integers
    """
    return "".join([random.choice(string.ascii_letters + string.digits) for _ in range(length)])
