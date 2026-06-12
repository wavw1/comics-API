from random_username.generate import generate_username

def random_username(quantity_usernames: int) -> str:
    usernames = generate_username(quantity_usernames)
    for username in usernames:
        return username