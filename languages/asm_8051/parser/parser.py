import re
from difflib import get_close_matches

from .ast_nodes import InstructionNode


class ParserError(ValueError):
	pass


_MOV_RE = re.compile(r"^MOV\s+A\s*,\s*#(.+)$", re.IGNORECASE)
_ADD_RE = re.compile(r"^ADD\s+A\s*,\s*#(.+)$", re.IGNORECASE)
_SINGLE_TOKEN_RE = re.compile(r"^(INC|DEC|CPL)\s+A$", re.IGNORECASE)
_SUPPORTED_MNEMONICS = ["MOV", "ADD", "INC", "DEC", "CPL"]


def _parse_value(raw_value: str, *, line_number: int, instruction: str) -> int:
	value_text = raw_value.strip()
	try:
		return int(value_text, 0)
	except ValueError as exc:
		raise ParserError(
			f"Line {line_number}: invalid immediate value '{value_text}' for {instruction} A,#value"
		) from exc


def _unsupported_instruction_error(line_number: int, stripped: str) -> ParserError:
	mnemonic = stripped.split(maxsplit=1)[0].rstrip(",").upper()
	suggestion = get_close_matches(mnemonic, _SUPPORTED_MNEMONICS, n=1, cutoff=0.6)
	if suggestion:
		return ParserError(
			f"Line {line_number}: unsupported instruction '{stripped}'. Did you mean '{suggestion[0]}'?"
		)

	return ParserError(
		f"Line {line_number}: unsupported instruction '{stripped}'. Supported mnemonics: {', '.join(_SUPPORTED_MNEMONICS)}"
	)


def parse_program(assembly_text: str) -> list[InstructionNode]:
	instructions: list[InstructionNode] = []

	for line_number, raw_line in enumerate(assembly_text.splitlines(), start=1):
		stripped = raw_line.split(";", 1)[0].strip()
		if not stripped:
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

		single_token_match = _SINGLE_TOKEN_RE.match(stripped)
		if single_token_match:
			instructions.append(InstructionNode(opcode=single_token_match.group(1).upper(), line_number=line_number))
			continue

		raise _unsupported_instruction_error(line_number, stripped)

	return instructions
