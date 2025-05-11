from dataclasses import dataclass

@dataclass(frozen=True)
class PaymentStatus:
    SUCCESS: str = "success"
    REFUSED: str = "refused"
    IN_PROGRESS: str = "in_progress"
