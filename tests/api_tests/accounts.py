from dataclasses import dataclass


@dataclass(frozen=True)
class DisposableAccount:
    """A throwaway standard account created for a test."""

    username: str
    email: str
    password: str
