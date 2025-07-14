import sys
from database import initialize_db
from service import (
    add_user,
    authenticate_user,
    get_user_by_email,
    get_user_itineraries
)

def prompt_existing_user():
    # Login flow: ask for numeric user_id and password, retry on failure.
    print("\n=== Existing User Login ===")
    try:
        user_id = int(input("Enter your User ID: ").strip())
    except ValueError:
        print("Please enter a numeric User ID.")
        return prompt_existing_user()

    password = input("Enter your password: ").strip()
    if authenticate_user(user_id, password):
        print("Login successful.")
        return user_id
    else:
        print("Invalid ID or password. Try again.")
        return prompt_existing_user()

def prompt_new_user():
    # Registration flow: ask for name, email, password.
    # If email exists, offer to login instead of re-register.
    print("\n=== New User Registration ===")
    while True:
        name     = input("Name:     ").strip()
        email    = input("Email:    ").strip()
        password = input("Password: ").strip()

        existing_id = get_user_by_email(email)
        if existing_id:
            print(f"Email '{email}' is already registered under User ID {existing_id}.")
            choice = input("Type 'L' to login, or any other key to try a different email: ").strip().lower()
            if choice == 'l':
                return prompt_existing_user()
            else:
                continue

        # Safe to register new user
        user_id = add_user(name, email, password)
        print(f"Registration complete. Your new User ID is {user_id}.")
        return user_id

def show_itineraries(user_id: int):
    # Ask for a start date, then display that user's itineraries.
    print("\n=== View Itineraries ===")
    start_date = input("Show itineraries starting on or after (YYYY-MM-DD): ").strip()
    trips = get_user_itineraries(user_id, start_date)

    if not trips:
        print("No itineraries found for that period.")
        return

    print(f"\nFound {len(trips)} itinerary entries:\n")
    for t in trips:
        print(
            f"Itin#{t['itinerary_id']} | "
            f"{t['city']}, {t['country']} | "
            f"{t['accommodation']} | notes: {t['notes']}"
        )

def main():
    initialize_db()

    print("Welcome to the SNHU Travel Console\n")
    choice = input("Are you an existing user? (Y/N): ").strip().lower()

    if choice == 'y':
        user_id = prompt_existing_user()
    else:
        user_id = prompt_new_user()

    show_itineraries(user_id)

    print("\nPress [Enter] to exit.")
    input()
    sys.exit(0)

if __name__ == "__main__":
    main()