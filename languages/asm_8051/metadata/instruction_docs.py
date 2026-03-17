"""Instruction metadata used by editor help and future tooltips."""

from languages.asm_8051.metadata.syntax_rules import INSTRUCTIONS


def _generic_description(mnemonic: str) -> str:
	return f"8051 instruction '{mnemonic}'."


INSTRUCTION_DOCS: dict[str, str] = {
	mnemonic: _generic_description(mnemonic) for mnemonic in INSTRUCTIONS
}

