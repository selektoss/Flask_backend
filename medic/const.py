from typing import Final

EMAIL_MESSAGE: Final = "Wrong format email adress! Example -\'test@mail.com\'"
PASSWORD_MESSAGE: Final = "Password must be at least 5 and maximum 50 characters"
GENDER_MESSAGE: Final = "Gender must be char \'M\' - male or \'F\' - female"
ERROR_API_KEY: Final = "Invalid API key: You must be granted a valid key."

EMAIL_REGEX: Final = "^[a-z0-9_@.-]+$"
PASSWORD_REGEX: Final = "^[a-zA-Z0-9_@&#:!*.-]+$"
SYMBOL_REGEX: Final = "^[а-яА-Яa .-]+$"
PHONE_REGEX: Final = "^\+7[0-9]+$"
TXT_REGEX: Final = "^[а-яА-Яa0-9.\-\", :]+$"


