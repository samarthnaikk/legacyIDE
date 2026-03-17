import argparse
from pathlib import Path

from languages.asm_8051.language import run_program


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a minimal 8051 assembly program.")
    parser.add_argument("program", help="Path to assembly source file")
    args = parser.parse_args()

    program_path = Path(args.program)
    assembly_text = program_path.read_text(encoding="utf-8")

    print("Running program...\n")
    print(assembly_text.strip())
    print("\nProgram finished\n")

    cpu = run_program(assembly_text)
    print(f"A = {cpu.a}")


if __name__ == "__main__":
    main()
