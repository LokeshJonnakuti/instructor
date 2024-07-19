import logging

from pydantic import BaseModel, Field
from instructor import Instructions
import instructor
import secrets

instructor.patch()

logging.basicConfig(level=logging.INFO)

# Usage
instructions = Instructions(
    name="three_digit_multiply",
    finetune_format="messages",
    include_code_body=True,
    log_handlers=[
        logging.FileHandler("math_finetunes.jsonl"),
    ],
)


class Multiply(BaseModel):
    a: int
    b: int
    result: int = Field(..., description="The result of the multiplication")


@instructions.distil(mode="dispatch", model="ft:gpt-3.5-turbo-0613:personal::8CazU0uq")
def fn(a: int, b: int) -> Multiply:
    """Return the result of the multiplication as an integer"""
    resp = a * b
    return Multiply(a=a, b=b, result=resp)


if __name__ == "__main__":
    for _ in range(5):
        a = secrets.SystemRandom().randint(100, 999)
        b = secrets.SystemRandom().randint(100, 999)
        result = fn(a, b)
        print(f"{a} * {b} = {result.result}, expected {a*b}")
    """
    972 * 508 = 493056, expected 493776
    145 * 369 = 53505, expected 53505
    940 * 440 = 413600, expected 413600
    114 * 213 = 24282, expected 24282
    259 * 650 = 168350, expected 168350
    """
