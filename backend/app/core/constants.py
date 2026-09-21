# JWT
SIGNING_ALGORITHM: str = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
REFRESH_TOKEN_EXPIRE_DAYS: int = 30

# Password Hash
DUMMY_PASSWORD_HASH = "$argon2id$v=19$m=65536,t=3,p=4$KsrCCT7vUAgxfbagUoFmww$QnzEmwXZ+dUQKZXgelfEoyvY5oTnLoMA8fDa1XeMd5E"

# Password applied when an admin resets a Learner/Facilitator password. The
# account is flagged must_change_password, so it only lives until first login.
DEFAULT_RESET_PASSWORD = "alsENSE@2026!"
