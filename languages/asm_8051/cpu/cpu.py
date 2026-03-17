from dataclasses import dataclass, field


@dataclass
class CPU:
	"""Minimal CPU state for the vertical slice."""

	a: int = 0
	r: list[int] = field(default_factory=lambda: [0] * 8)

	def set_a(self, value: int) -> None:
		self.a = value & 0xFF

	def get_r(self, index: int) -> int:
		if not 0 <= index <= 7:
			raise ValueError(f"invalid register index R{index}")
		return self.r[index]

	def set_r(self, index: int, value: int) -> None:
		if not 0 <= index <= 7:
			raise ValueError(f"invalid register index R{index}")
		self.r[index] = value & 0xFF
