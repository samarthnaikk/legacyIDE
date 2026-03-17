from PySide6.QtWidgets import QStatusBar


def build_status_bar() -> QStatusBar:
	status = QStatusBar()
	status.showMessage("Ready")
	return status
