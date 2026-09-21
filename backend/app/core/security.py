import secrets
import string

from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

MIN_PASSWORD_LENGTH = 8

# Every string.punctuation character counts as "special" when validating.
_UPPERCASE = string.ascii_uppercase
_LOWERCASE = string.ascii_lowercase
_DIGITS = string.digits
_SPECIALS = string.punctuation

# Generated passwords are read off a screen and typed by hand, so they only
# draw from specials that are easy to see and type. All are valid _SPECIALS.
_TEMP_PASSWORD_SPECIALS = "!@#$%^&*?+=-_"


def validate_password_complexity(password: str) -> str:
    """Return the password unchanged, or raise ValueError naming every unmet rule."""
    categories = (
        ("uppercase letter", _UPPERCASE),
        ("lowercase letter", _LOWERCASE),
        ("digit", _DIGITS),
        ("special character", _SPECIALS),
    )
    missing = [
        name
        for name, allowed in categories
        if not any(c in allowed for c in password)
    ]

    problems = []
    if len(password) < MIN_PASSWORD_LENGTH:
        problems.append(f"be at least {MIN_PASSWORD_LENGTH} characters long")
    if missing:
        listed = missing[0] if len(missing) == 1 else (
            ", ".join(missing[:-1]) + " and " + missing[-1]
        )
        problems.append(f"contain at least one {listed}")

    if problems:
        raise ValueError("Password must " + " and ".join(problems) + ".")

    return password


def generate_temp_password(length: int = 8) -> str:
    categories = (_UPPERCASE, _LOWERCASE, _DIGITS, _TEMP_PASSWORD_SPECIALS)
    if length < len(categories):
        raise ValueError(
            f"length must be at least {len(categories)} to include every character category"
        )

    # One guaranteed character per category, the rest from the full alphabet,
    # then shuffled so the guaranteed characters don't sit in fixed positions.
    chars = [secrets.choice(category) for category in categories]
    alphabet = "".join(categories)
    chars += [secrets.choice(alphabet) for _ in range(length - len(chars))]
    secrets.SystemRandom().shuffle(chars)

    return "".join(chars)


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password_plain: str, hashed_password: str) -> bool:
    return password_hash.verify(password_plain, hashed_password)


def hash_refresh_token(token: str) -> str:
    return password_hash.hash(token)


def verify_refresh_token(token: str, token_hash: str) -> bool:
    return password_hash.verify(token, token_hash)
