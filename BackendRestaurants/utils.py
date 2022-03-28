import re
from flask import make_response
REGEX_VALID_EMAIL=r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
SPECIAL_CHARACTERS=["!", "@", "#", "?", "]"]
charactersString=", ".join(SPECIAL_CHARACTERS)
MIN_PASSWORD_LENGTH=10

MESSAGE_LENGTH_INVALID=f'Password must be at least {MIN_PASSWORD_LENGTH} characters'
MESSAGE_LOWERCASE_INVALID="Password must have at least one lowercase character"
MESSAGE_UPPERCASE_INVALID="Password must have at least one uppercase character"
MESSAGE_SPECIAL_CHARACTERS_INVALID=f"Password must have at least one of these characters: {charactersString}"
MESSAGE_PASSWORD_NULL="Password must not be null"
MESSAGE_PASSWORD_SUCCESS="Password is valid"

# ---------------------------------------Responses---------------------------------------
def handleResponse(message, status):
    return make_response(message, status)

# ---------------------------------------Email and Password verifications---------------------------------------
def checkPassword(password:str):
    '''
    Checks if the password contains at least:

        1. 10 characters
        2. 1 lowercase letter
        3. 1 uppercase letter
        4. 1 of the following: !, @, #, ?, ]
    '''
    if password != None and type(password) != str:
        return handlePasswordResponse(False, MESSAGE_PASSWORD_NULL)
    else:
        if not isValidPasswordLength(password):
           return handlePasswordResponse(False, MESSAGE_LENGTH_INVALID) 

        if not containsLowerCase(password):
            return handlePasswordResponse(False, MESSAGE_LOWERCASE_INVALID)  
       
        if not containsUpperCase(password):
            return handlePasswordResponse(False, MESSAGE_UPPERCASE_INVALID)  

        if not checkSpecialCharacters(password):
            return handlePasswordResponse(False, MESSAGE_SPECIAL_CHARACTERS_INVALID)  

        return handlePasswordResponse(True, MESSAGE_PASSWORD_SUCCESS)  

def handlePasswordResponse(status, message):
    return [status, message]

def isValidEmail(email:str):
    if email != None and re.fullmatch(REGEX_VALID_EMAIL, email):
       return True
    return False

def isValidPasswordLength(password:str):
    '''
    Checks if the password length is valid
    '''
    if len(password) < MIN_PASSWORD_LENGTH:
        return False
    return True
    
def containsLowerCase(string:str):
    for c in string:
        if c.islower():
            return True
    return False

def containsUpperCase(string:str):
    for c in string:
        if c.isupper():
            return True
    return False

def checkSpecialCharacters(string:str):
    for c in string:
        if c in SPECIAL_CHARACTERS:
            return True
    return False

