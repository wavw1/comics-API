from random_username.generate import generate_username
import secrets
import string
import random
from app.models import UserCreate

def random_user() -> UserCreate:
    username = random_username(1)
    email = random_email()
    password = random_password()
    user_in = UserCreate(
        email=email,
        username=username,
        password=password,
        )
    
    return user_in

def random_username(quantity_usernames: int) -> str:
    usernames = generate_username(quantity_usernames)
    for username in usernames:
        return username
    
def random_password() -> str:
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(15))

    return password

import random
 
def random_email() -> str:
    valid_chars = 'abcdefghijklmnopqrstuvwxyz1234567890'
    length = random.randint(4, 15)
    login = ''.join(random.choice(valid_chars) for _ in range(length))
    
    if login[0].isnumeric():
        login = random.choice('abcdefghijklmnopqrstuvwxyz') + login
    servers = ['@gmail', '@yahoo', '@hotmail', '@outlook', '@protonmail']
    tlds = ['.com', '.net', '.org', '.io', '.co']
    email = login + random.choice(servers) + random.choice(tlds)
    
    return email