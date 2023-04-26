
from enum import Enum

class Message(Enum):
    server_error = "INTERNAL SERVER ERROR"
    incorrect_password = "PASSWORD IS INCORRECT"
    success = "SUCCESSFUL"
    try_with_correct_data = "PLEASE TRY WITH CORRECT DATA"
    user_exists = "USER ALREADY EXISTS"
    user_not_exists = "USER DOES NOT EXIST"
    record_not_found = "RECORD NOT FOUND"
    email_available = "EMAIL AVAILABLE"
    password_does_not_match = "PASSWORD DOES NOT MATCH"
    account_created = "USER ACCOUNT CREATED SUCCESSFULLY"
    verification = "VERIFIED"
    invalid_pin = "INVALID VERIFICATION PIN"
    verification_email = "VERIFICATION EMAIL SENT"
    questionnaire = "EXAPMLE"
