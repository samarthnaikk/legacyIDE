from languages.asm_8051.cpu.cpu import CPU


def cpl_a(cpu: CPU) -> None:
	cpu.set_a(~cpu.a)
