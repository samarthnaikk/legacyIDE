import argparse
from pathlib import Path

from languages.asm_8051.language import run_program
from languages.asm_8051.instructions.instruction_set import ExecutionError
from languages.asm_8051.parser.parser import ParserError


def _print_program_preview(assembly_text: str, max_lines: int = 10) -> None:
    lines = assembly_text.splitlines()
    preview_lines = lines[:max_lines]
    if preview_lines:
        print("\n".join(preview_lines))
    else:
        print("(empty file)")

    remaining = len(lines) - len(preview_lines)
    if remaining > 0:
        print(f"... ({remaining} more line(s) not shown)")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a minimal 8051 assembly program.")
    parser.add_argument("program", help="Path to assembly source file")
    args = parser.parse_args()

    program_path = Path(args.program)
    try:
        assembly_text = program_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        print(f"Error: file not found: {program_path}")
        raise SystemExit(1)
    except PermissionError:
        print(f"Error: permission denied while reading: {program_path}")
        raise SystemExit(1)
    except UnicodeDecodeError:
        print(f"Error: could not decode file as UTF-8: {program_path}")
        raise SystemExit(1)

    print("Running program...\n")
    _print_program_preview(assembly_text)

    try:
        cpu = run_program(assembly_text)
    except ParserError as exc:
        print(f"Parse error: {exc}")
        raise SystemExit(1)
    except ExecutionError as exc:
        print(f"Execution error: {exc}")
        raise SystemExit(1)
    except Exception as exc:
        print(f"Unexpected error: {exc}")
        raise SystemExit(1)

    print("\nProgram finished\n")
    print(f"A = {cpu.a}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted.")
        raise SystemExit(130)
