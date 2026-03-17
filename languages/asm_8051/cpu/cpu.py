from dataclasses import dataclass


@dataclass
class CPU:
	"""Minimal CPU state for the vertical slice."""

	a: int = 0

	def set_a(self, value: int) -> None:
		self.a = value & 0xFF
