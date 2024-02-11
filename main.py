
from cryptography.fernet import Fernet
import json
import getpass

class PasswordManager:
    def __init__(self, filename='encrypted_passwords.json', key_filename='key.key'):
        self.filename = filename
        self.key_filename = key_filename
        self.passwords = {}
        self.load_key()
        self.load_passwords()

    def load_key(self):
        try:
            with open(self.key_filename, 'rb') as key_file:
                self.key = key_file.read()
        except FileNotFoundError:
            self.key = Fernet.generate_key()
            with open(self.key_filename, 'wb') as key_file:
                key_file.write(self.key)

    def encrypt(self, data):
        cipher_suite = Fernet(self.key)
        encrypted_data = cipher_suite.encrypt(data.encode())
        return encrypted_data

    def decrypt(self, encrypted_data):
        cipher_suite = Fernet(self.key)
        decrypted_data = cipher_suite.decrypt(encrypted_data).decode()
        return decrypted_data

    def load_passwords(self):
        try:
            with open(self.filename, 'rb') as file:
                encrypted_data = file.read()
                decrypted_data = self.decrypt(encrypted_data)
                self.passwords = json.loads(decrypted_data)
        except FileNotFoundError:
            self.save_passwords()

    def save_passwords(self):
        with open(self.filename, 'wb') as file:
            encrypted_data = self.encrypt(json.dumps(self.passwords))
            file.write(encrypted_data)

    def add_password(self, website, username, password):
        if website not in self.passwords:
            self.passwords[website] = {'username': username, 'password': password}
            self.save_passwords()
            print(f"Password for {website} added successfully.")
        else:
            print(f"Password for {website} already exists. Use update_password() to change it.")

    def get_password(self, website):
        if website in self.passwords:
            return self.passwords[website]['password']
        else:
            return None

    def update_password(self, website, new_password):
        if website in self.passwords:
            self.passwords[website]['password'] = new_password
            self.save_passwords()
            print(f"Password for {website} updated successfully.")
        else:
            print(f"Password for {website} does not exist. Use add_password() to add it.")

if __name__ == "__main__":
    password_manager = PasswordManager()

    # Example Usage
    website = input("Enter website: ")
    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")

    password_manager.add_password(website, username, password)

    website_to_retrieve = input("Enter website to retrieve password: ")
    retrieved_password = password_manager.get_password(website_to_retrieve)

    if retrieved_password:
        print(f"Password for {website_to_retrieve}: {retrieved_password}")
    else:
        print(f"No password found for {website_to_retrieve}.")

    website_to_update = input("Enter website to update password: ")
    new_password = getpass.getpass("Enter new password: ")

    password_manager.update_password(website_to_update, new_password)
