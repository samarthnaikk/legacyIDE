# Architecture

LegacyIDE currently implements a minimal vertical slice for asm_8051:

assembly source -> parser -> instruction nodes -> emulator -> CPU state
