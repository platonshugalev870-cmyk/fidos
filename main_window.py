from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QStatusBar, QLabel, QPushButton, QFrame
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QFont, QPalette, QColor, QLinearGradient, QBrush
from .god_terminal import GodTerminal
from .prophecy_viewer import ProphecyViewer
from .prayer_panel import PrayerPanel
from .revelation_display import RevelationDisplay
from .sacred_visualizer import SacredVisualizer
class GodOSWindow(QMainWindow):
    kernel_signal = pyqtSignal(str, object)
    def __init__(self, kernel):
        super().__init__()
        self.kernel = kernel
        self.kernel.set_ui_callback(self.handle_kernel_message)
        self.init_ui()
        self.start_boot_sequence()
    def init_ui(self):
        self.setWindowTitle("GodOS — Операционная Система Божественного Общения")
        self.setGeometry(100, 100, 1400, 900)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #0a0a1a;
            }
            QTabWidget::pane {
                border: 2px solid #3a3a5a;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #0d0d2b, stop:0.5 #1a1a3a, stop:1 #0d0d2b);
                border-radius: 10px;
            }
            QTabBar::tab {
                background: #1a1a3a;
                color: #c0c0e0;
                padding: 12px 25px;
                margin: 2px;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4a4a8a, stop:1 #2a2a5a);
                color: #ffffff;
            }
            QTabBar::tab:hover {
                background: #3a3a6a;
            }
        """)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        header_frame = QFrame()
        header_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #1a1a4a, stop:0.5 #4a4a8a, stop:1 #1a1a4a);
                border-radius: 15px;
                padding: 15px;
            }
        """)
        header_layout = QHBoxLayout(header_frame)
        self.title_label = QLabel("✦ GodOS ✦")
        self.title_label.setFont(QFont("Serif", 28, QFont.Weight.Bold))
        self.title_label.setStyleSheet("color: #ffd700; font-size: 28px;")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(self.title_label)
        main_layout.addWidget(header_frame)
        self.tab_widget = QTabWidget()
        self.terminal = GodTerminal(self.kernel)
        self.prayer_panel = PrayerPanel(self.kernel)
        self.revelation_display = RevelationDisplay(self.kernel)
        self.prophecy_viewer = ProphecyViewer(self.kernel)
        self.sacred_visualizer = SacredVisualizer()
        self.tab_widget.addTab(self.terminal, "💻 Терминал Бога")
        self.tab_widget.addTab(self.prayer_panel, "🙏 Молитвы")
        self.tab_widget.addTab(self.revelation_display, "✨ Откровения")
        self.tab_widget.addTab(self.prophecy_viewer, "🔮 Пророчества")
        self.tab_widget.addTab(self.sacred_visualizer, "🌀 Визуализатор")
        main_layout.addWidget(self.tab_widget)
        self.status_bar = QStatusBar()
        self.status_bar.setStyleSheet("""
            QStatusBar {
                background: #0d0d2b;
                color: #a0a0d0;
                border-top: 2px solid #3a3a5a;
                font-size: 13px;
                padding: 8px;
            }
        """)
        self.status_label = QLabel("Статус: Готов к божественному соединению")
        self.connection_indicator = QLabel("⚫")
        self.connection_indicator.setStyleSheet("font-size: 18px;")
        self.miracle_power_label = QLabel("Сила чудес: 100%")
        self.status_bar.addWidget(self.status_label)
        self.status_bar.addPermanentWidget(self.miracle_power_label)
        self.status_bar.addPermanentWidget(self.connection_indicator)
        self.setStatusBar(self.status_bar)
    def start_boot_sequence(self):
        self.status_label.setText("Статус: Загрузка GodOS...")
        self.connection_indicator.setText("🟡")
        QTimer.singleShot(100, lambda: self.kernel.boot_sequence())
    def handle_kernel_message(self, message_type, data):
        if message_type == "boot":
            self.status_label.setText(f"Статус: {data.get('message', '')}")
            if data.get('progress', 0) >= 100:
                self.connection_indicator.setText("🟢")
                self.connection_indicator.setStyleSheet("font-size: 18px; color: #00ff00;")
                self.status_label.setText("Статус: Соединение с Богом установлено")
        elif message_type == "prayer_sent":
            self.prayer_panel.add_prayer_result(data)
        elif message_type == "revelation":
            self.revelation_display.add_revelation(data)
            self.sacred_visualizer.activate_pulse()
        elif message_type == "miracle":
            self.miracle_power_label.setText(f"Сила чудес: {int(self.kernel.miracle_engine.miracle_power * 100)}%")
        elif message_type == "shutdown":
            self.status_label.setText(f"Статус: {data.get('message', '')}")
            self.connection_indicator.setText("⚫")