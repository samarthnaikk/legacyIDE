import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication


if __package__ in (None, ""):
	# Support running as a script: python ui/app.py
	project_root = Path(__file__).resolve().parent.parent
	if str(project_root) not in sys.path:
		sys.path.insert(0, str(project_root))
	from ui.windows.main_window import MainWindow
else:
	from .windows.main_window import MainWindow


def main() -> None:
	app = QApplication(sys.argv)
	window = MainWindow()
	window.show()
	raise SystemExit(app.exec())


if __name__ == "__main__":
	main()
