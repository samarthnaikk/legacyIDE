from languages.asm_8051.cpu.cpu import CPU


def mov_a_immediate(cpu: CPU, value: int) -> None:
	cpu.set_a(value)
