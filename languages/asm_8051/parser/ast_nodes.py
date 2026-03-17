from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class InstructionNode:
	opcode: str
	operand: Optional[int] = None
	register: Optional[int] = None
	source: Optional[str] = None
	label: Optional[str] = None
	target: Optional[int] = None
	line_number: int = 0
