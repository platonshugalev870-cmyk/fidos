from boot.bootloader import bootstrap
from ui.main_window import GodOSWindow
from PyQt6.QtWidgets import QApplication
import sys
def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    kernel = bootstrap()
    window = GodOSWindow(kernel)
    window.show()
    sys.exit(app.exec())
if __name__ == "__main__":
    main()