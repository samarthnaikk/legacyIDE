from languages.asm_8051.cpu.cpu import CPU
from languages.asm_8051.instructions.arithmetic import add_a_immediate, dec_a, inc_a
from languages.asm_8051.instructions.data_transfer import mov_a_immediate
from languages.asm_8051.instructions.logical import cpl_a
from languages.asm_8051.parser.ast_nodes import InstructionNode


class ExecutionError(ValueError):
	pass


def _line_prefix(instruction: InstructionNode) -> str:
	if instruction.line_number > 0:
		return f"Line {instruction.line_number}: "
	return ""


def execute_instruction(cpu: CPU, instruction: InstructionNode, current_pc: int) -> int:
	if instruction.opcode == "MOV":
		if instruction.register is not None:
			if instruction.source == "A":
				cpu.set_r(instruction.register, cpu.a)
				return current_pc + 1

			if instruction.operand is not None:
				cpu.set_r(instruction.register, instruction.operand)
				return current_pc + 1

			raise ExecutionError(f"{_line_prefix(instruction)}MOV Rn requires source A or immediate value")

		if instruction.operand is None:
			raise ExecutionError(f"{_line_prefix(instruction)}MOV requires an immediate operand")
		mov_a_immediate(cpu, instruction.operand)
		return current_pc + 1

	if instruction.opcode == "ADD":
		if instruction.register is not None:
			add_a_immediate(cpu, cpu.get_r(instruction.register))
			return current_pc + 1

		if instruction.operand is None:
			raise ExecutionError(f"{_line_prefix(instruction)}ADD requires an immediate operand")
		add_a_immediate(cpu, instruction.operand)
		return current_pc + 1

	if instruction.opcode == "INC":
		if instruction.register is not None:
			cpu.set_r(instruction.register, cpu.get_r(instruction.register) + 1)
			return current_pc + 1

		inc_a(cpu)
		return current_pc + 1

	if instruction.opcode == "DEC":
		if instruction.register is not None:
			cpu.set_r(instruction.register, cpu.get_r(instruction.register) - 1)
			return current_pc + 1

		dec_a(cpu)
		return current_pc + 1

	if instruction.opcode == "CPL":
		cpl_a(cpu)
		return current_pc + 1

	if instruction.opcode == "JNZ":
		if instruction.target is None:
			raise ExecutionError(f"{_line_prefix(instruction)}JNZ requires a resolved label target")
		if not cpu.z:
			return instruction.target
		return current_pc + 1

	if instruction.opcode == "SJMP":
		if instruction.target is None:
			raise ExecutionError(f"{_line_prefix(instruction)}SJMP requires a resolved label target")

		# Treat a self-loop as a terminal idle loop in run mode.
		if instruction.target == current_pc:
			return -1

		return instruction.target

	raise ExecutionError(f"{_line_prefix(instruction)}unsupported opcode: {instruction.opcode}")
