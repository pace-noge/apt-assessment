from app import db, models

def main():
    username = input("Username: ")
    password = input("Password: ")
    u = models.User(username=username, password=password, is_active=True, is_admin=True)
    db.session.add(u)
    db.session.commit()
    print("[+] user created")

if __name__ == "__main__":
    main()