import re
from difflib import get_close_matches

from languages.asm_8051.metadata.syntax_rules import DIRECTIVES, INSTRUCTIONS

from .ast_nodes import InstructionNode


class ParserError(ValueError):
	pass


_MOV_RE = re.compile(r"^MOV\s+(?:A\s*,\s*)?#(.+)$", re.IGNORECASE)
_MOV_R_IMM_RE = re.compile(r"^MOV\s+R([0-7])\s*,\s*#(.+)$", re.IGNORECASE)
_MOV_R_A_RE = re.compile(r"^MOV\s+R([0-7])\s*,\s*A$", re.IGNORECASE)
_ADD_RE = re.compile(r"^ADD\s+A\s*,\s*#(.+)$", re.IGNORECASE)
_ADD_A_R_RE = re.compile(r"^ADD\s+A\s*,\s*R([0-7])$", re.IGNORECASE)
_INC_A_RE = re.compile(r"^INC\s+A$", re.IGNORECASE)
_INC_R_RE = re.compile(r"^INC\s+R([0-7])$", re.IGNORECASE)
_DEC_A_RE = re.compile(r"^DEC\s+A$", re.IGNORECASE)
_DEC_R_RE = re.compile(r"^DEC\s+R([0-7])$", re.IGNORECASE)
_CPL_A_RE = re.compile(r"^CPL\s+A$", re.IGNORECASE)
_LABEL_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)\s*:\s*(.*)$")
_ORG_RE = re.compile(r"^ORG\s+(.+)$", re.IGNORECASE)
_END_RE = re.compile(r"^END(?:\s+.*)?$", re.IGNORECASE)
_JNZ_RE = re.compile(r"^JNZ\s+([A-Za-z_][A-Za-z0-9_]*)$", re.IGNORECASE)
_SJMP_RE = re.compile(r"^SJMP\s+([A-Za-z_][A-Za-z0-9_]*)$", re.IGNORECASE)
_SUPPORTED_MNEMONICS = ["MOV", "ADD", "INC", "DEC", "CPL"]
_SUPPORTED_DIRECTIVES = ["ORG"]
_KNOWN_MNEMONICS = list(INSTRUCTIONS)
_KNOWN_DIRECTIVES = list(DIRECTIVES)


def _parse_value(raw_value: str, *, line_number: int, instruction: str) -> int:
	value_text = raw_value.strip()
	upper_text = value_text.upper()

	try:
		if upper_text.endswith("H"):
			return int(upper_text[:-1], 16)
		if upper_text.endswith("B"):
			return int(upper_text[:-1], 2)
		if upper_text.endswith("D"):
			return int(upper_text[:-1], 10)

		# Accept decimal literals with leading zeros (e.g. 04) as base-10.
		if re.fullmatch(r"[0-9]+", value_text):
			return int(value_text, 10)

		return int(value_text, 0)
	except ValueError as exc:
		raise ParserError(
			f"Line {line_number}: invalid immediate value '{value_text}' for {instruction} #value"
		) from exc


def _unsupported_instruction_error(line_number: int, stripped: str) -> ParserError:
	mnemonic = stripped.split(maxsplit=1)[0].rstrip(",").upper()
	if mnemonic in _SUPPORTED_DIRECTIVES:
		return ParserError(
			f"Line {line_number}: directive '{mnemonic}' is valid but this form is not supported."
		)

	if mnemonic in _KNOWN_MNEMONICS and mnemonic not in _SUPPORTED_MNEMONICS:
		return ParserError(
			f"Line {line_number}: instruction '{mnemonic}' is recognized but not yet executable in this minimal runtime. "
			f"Currently executable mnemonics: {', '.join(_SUPPORTED_MNEMONICS)}"
		)

	if mnemonic in _KNOWN_DIRECTIVES:
		return ParserError(
			f"Line {line_number}: directive '{mnemonic}' is recognized but not yet supported in this minimal runtime. "
			f"Currently supported directives: {', '.join(_SUPPORTED_DIRECTIVES)}"
		)

	suggestion = get_close_matches(mnemonic, _KNOWN_MNEMONICS + _KNOWN_DIRECTIVES, n=1, cutoff=0.6)
	if suggestion:
		return ParserError(
			f"Line {line_number}: unsupported instruction '{stripped}'. Did you mean '{suggestion[0]}'?"
		)

	return ParserError(
		f"Line {line_number}: unsupported instruction '{stripped}'. Supported mnemonics: {', '.join(_SUPPORTED_MNEMONICS)}"
	)


def parse_program(assembly_text: str) -> list[InstructionNode]:
	instructions: list[InstructionNode] = []
	labels: dict[str, int] = {}

	for line_number, raw_line in enumerate(assembly_text.splitlines(), start=1):
		stripped = raw_line.split(";", 1)[0].strip()
		if not stripped:
			continue

		while True:
			label_match = _LABEL_RE.match(stripped)
			if not label_match:
				break

			label_name = label_match.group(1).upper()
			if label_name in labels:
				raise ParserError(f"Line {line_number}: duplicate label '{label_name}'")

			labels[label_name] = len(instructions)
			stripped = label_match.group(2).strip()
			if not stripped:
				break

		if not stripped:
			continue

		org_match = _ORG_RE.match(stripped)
		if org_match:
			_parse_value(org_match.group(1), line_number=line_number, instruction="ORG")
			continue

		if _END_RE.match(stripped):
			break

		mov_r_imm_match = _MOV_R_IMM_RE.match(stripped)
		if mov_r_imm_match:
			instructions.append(
				InstructionNode(
					opcode="MOV",
					register=int(mov_r_imm_match.group(1)),
					operand=_parse_value(mov_r_imm_match.group(2), line_number=line_number, instruction="MOV"),
					line_number=line_number,
				)
			)
			continue

		mov_r_a_match = _MOV_R_A_RE.match(stripped)
		if mov_r_a_match:
			instructions.append(
				InstructionNode(
					opcode="MOV",
					register=int(mov_r_a_match.group(1)),
					source="A",
					line_number=line_number,
				)
			)
			continue

		mov_match = _MOV_RE.match(stripped)
		if mov_match:
			instructions.append(
				InstructionNode(
					opcode="MOV",
					operand=_parse_value(mov_match.group(1), line_number=line_number, instruction="MOV"),
					line_number=line_number,
				)
			)
			continue

		add_match = _ADD_RE.match(stripped)
		if add_match:
			instructions.append(
				InstructionNode(
					opcode="ADD",
					operand=_parse_value(add_match.group(1), line_number=line_number, instruction="ADD"),
					line_number=line_number,
				)
			)
			continue

		add_a_r_match = _ADD_A_R_RE.match(stripped)
		if add_a_r_match:
			instructions.append(
				InstructionNode(opcode="ADD", register=int(add_a_r_match.group(1)), line_number=line_number)
			)
			continue

		inc_a_match = _INC_A_RE.match(stripped)
		if inc_a_match:
			instructions.append(InstructionNode(opcode="INC", line_number=line_number))
			continue

		inc_r_match = _INC_R_RE.match(stripped)
		if inc_r_match:
			instructions.append(InstructionNode(opcode="INC", register=int(inc_r_match.group(1)), line_number=line_number))
			continue

		dec_a_match = _DEC_A_RE.match(stripped)
		if dec_a_match:
			instructions.append(InstructionNode(opcode="DEC", line_number=line_number))
			continue

		dec_r_match = _DEC_R_RE.match(stripped)
		if dec_r_match:
			instructions.append(InstructionNode(opcode="DEC", register=int(dec_r_match.group(1)), line_number=line_number))
			continue

		cpl_a_match = _CPL_A_RE.match(stripped)
		if cpl_a_match:
			instructions.append(InstructionNode(opcode="CPL", line_number=line_number))
			continue

		jnz_match = _JNZ_RE.match(stripped)
		if jnz_match:
			instructions.append(InstructionNode(opcode="JNZ", label=jnz_match.group(1).upper(), line_number=line_number))
			continue

		sjmp_match = _SJMP_RE.match(stripped)
		if sjmp_match:
			instructions.append(InstructionNode(opcode="SJMP", label=sjmp_match.group(1).upper(), line_number=line_number))
			continue

		raise _unsupported_instruction_error(line_number, stripped)

	for index, instruction in enumerate(instructions):
		if instruction.opcode not in ("JNZ", "SJMP"):
			continue

		if instruction.label is None:
			raise ParserError(f"Line {instruction.line_number}: missing label for {instruction.opcode}")

		if instruction.label not in labels:
			raise ParserError(f"Line {instruction.line_number}: unknown label '{instruction.label}'")

		instructions[index] = InstructionNode(
			opcode=instruction.opcode,
			operand=instruction.operand,
			register=instruction.register,
			source=instruction.source,
			label=instruction.label,
			target=labels[instruction.label],
			line_number=instruction.line_number,
		)

	return instructions
