from languages.asm_8051.cpu.cpu import CPU


def add_a_immediate(cpu: CPU, value: int) -> None:
	cpu.set_a(cpu.a + value)


def inc_a(cpu: CPU) -> None:
	cpu.set_a(cpu.a + 1)


def dec_a(cpu: CPU) -> None:
	cpu.set_a(cpu.a - 1)
