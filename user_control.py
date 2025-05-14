import hashlib
import re
from db import session, User

# password hashing function
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Email regex validation
def is_valid_email(email):
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.match(pattern, email) is not None

# register user in database function
def register_user():
    while True:
        print("\n--- Register ---")
        username = input("Please enter your username:  ").strip()
        if session.query(User).filter_by(username=username).first():
            print(f"Username {username} already exists")
            continue
        elif not username:
            print("invalid input, please try again.")
            continue
        email = input("Enter your email: ").strip()
        if not is_valid_email(email):
            print("Invalid email format!")
            continue
        elif session.query(User).filter_by(email=email).first():
            print(f"Email {email} already exists")
            continue
        elif not email:
            print("invalid input, please try again.")
            continue
        password = input("Enter password: ").strip()
        if len(password) < 10:
            print("Password must be at least 10 characters!")
            continue
        break
    # hash the password input using function
    # and named it the variable hashed_password
    hashed_password = hash_password(password)
    # define the new user with all the processed inputs
    new_user = User(username=username, hashed_password=hashed_password, email=email)
    session.add(new_user)
    # save the new user
    session.commit()
    print(f"New user {username} created")

# login existing user function
def login_user():
    print("\n--- Login ---")
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()

    user = session.query(User).filter_by(username=username).first()
    if user and user.hashed_password == hash_password(password):
        print("Login successful!")
        print(f"Welcome, {user.username}! Email: {user.email}")
    else:
        print("Invalid username or password!")
        return False
    return True

