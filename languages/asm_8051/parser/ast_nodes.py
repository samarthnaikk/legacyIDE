from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class InstructionNode:
	opcode: str
	operand: Optional[int] = None
