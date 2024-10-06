from . import BasePasswordHasher

class Argon2PasswordHasher(BasePasswordHasher):
    """
    Secure password hashing using the argon2 algorithm.

    This is the winner of the Password Hashing Competition 2013-2015
    (https://password-hashing.net). It requires the argon2-cffi library which
    depends on native C code and might cause portability issues.
    """

    algorithm = "argon2"
    library = "argon2"

    time_cost = 2
    memory_cost = 102400
    parallelism = 8