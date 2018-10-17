class TwoFactorRequired(Exception):
    """Two Factor Authentication is required but the verification code was not provided"""

class TwoFactorInvalid(Exception):
    """The provided 2FA code is invalid"""