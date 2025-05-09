from dataclasses import dataclass
from typing import Dict
import re
"""
test_cases = [
    {"name": "Alice42", "age": 25, "email": "alice@example.com"}, -> Error: InvalidNameError - Name must not contain numbers or symbols# Invalid name
    {"name": "Bob", "age": 150, "email": "bob@example.com"},      ->Error: InvalidAgeError - Age must be between 0 and 120# Invalid age
    {"name": "Charlie", "age": 30, "email": "invalid-email"},     -> Error: InvalidEmailError - Email must contain '@'# Invalid email
    {"name": "Diana", "age": 28, "email": "diana@example.com"}    -> Registered: data(name='Diana', age=28, email='diana@example.com', is_active=True)# Valid
]
"""
@dataclass
class User:
    name: str
    age: int
    email: str
    is_active: bool = True

class InvalidEmailError(Exception):
    def __init__(self, email: str):
        super().__init__(f"Invalid email: {email}")

class InvalidNameError(Exception):
    def __init__(self, name: str):
        super().__init__(f'Invalid name: {name}')

class InvalidAgeError(Exception):
    def __init__(self, age: int):
        super().__init__(f'Invalid age: {age}')


class Validate:
    EMAIL_REGEX = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    NAME_REGEX = r'^[a-zA-Z\s]+$'
    def __init__(self, data: dict):
        self._validate_input(data)
        self._validate_user(data)
        self._register_user(data)

    def _validate_input(self, data: Dict[str, object]) -> None:
        required_keys = ['name', 'age', 'email']
        if any(key not in data for key in required_keys):
            raise ValueError("Missing required fields")

    def _validate_user(self, data: Dict[str, object]) -> None:
        if not re.match(Validate.EMAIL_REGEX, str(data['email'])):
            raise InvalidEmailError(data['email'])
        if not re.match(Validate.NAME_REGEX, str(data['name'])):
            raise InvalidNameError(data['name'])
        if not (0 <= data['age'] <= 120):
            raise InvalidAgeError(data['age'])
    
    def _register_user(self, data: Dict[str, object]) -> User:
        self.user = User(**data)
        print(f'Registered: {self.user}')
        return self.user
        
if __name__ == "__main__":
    test_cases = [
    {"name": "Alice42", "age": 25, "email": "alice@example.com"},     # Invalid name
    {"name": "Bob", "age": 150, "email": "bob@example.com"},        # Invalid age
    {"name": "Charlie", "age": 30, "email": "invalid-email"},       # Invalid email
    {"name": "Diana", "age": 28, "email": "diana@example.com"}      # Valid
]
    for user in test_cases:
        try:
            Validate(user)
        except (InvalidAgeError, InvalidNameError, InvalidEmailError) as e:
            print(f"Error caught: {e}")