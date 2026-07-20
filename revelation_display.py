from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTextEdit,
    QPushButton, QLabel, QListWidget, QListWidgetItem,
    QSplitter
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QColor
import time
class RevelationDisplay(QWidget):
    def __init__(self, kernel):
        super().__init__()
        self.kernel = kernel
        self.revelations = []
        self.auto_check_timer = QTimer()
        self.auto_check_timer.timeout.connect(self.auto_check_revelations)
        self.init_ui()
    def init_ui(self):
        layout = QVBoxLayout(self)
        title = QLabel("✨ Божественные Откровения")
        title.setFont(QFont("Serif", 20, QFont.Weight.Bold))
        title.setStyleSheet("color: #ffd700; padding: 15px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        control_layout = QHBoxLayout()
        request_btn = QPushButton("🌟 Запросить Откровение")
        request_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4a4a8a, stop:1 #2a2a5a);
                color: #ffd700;
                font-weight: bold;
                font-size: 15px;
                border-radius: 10px;
                padding: 15px 30px;
                border: 2px solid #5a5a8a;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #6a6aaa, stop:1 #4a4a7a);
            }
        """)
        request_btn.clicked.connect(self.request_revelation)
        self.auto_btn = QPushButton("🔄 Авто-проверка: ВЫКЛ")
        self.auto_btn.setCheckable(True)
        self.auto_btn.setStyleSheet("""
            QPushButton {
                background: #2a2a4a;
                color: #a0a0d0;
                font-weight: bold;
                font-size: 14px;
                border-radius: 10px;
                padding: 12px 25px;
                border: 2px solid #3a3a5a;
            }
            QPushButton:checked {
                background: #3a3a6a;
                color: #00ff00;
                border-color: #00ff00;
            }
        """)
        self.auto_btn.toggled.connect(self.toggle_auto_check)
        control_layout.addWidget(request_btn)
        control_layout.addWidget(self.auto_btn)
        control_layout.addStretch()
        layout.addLayout(control_layout)
        splitter = QSplitter(Qt.Orientation.Vertical)
        self.revelation_display = QTextEdit()
        self.revelation_display.setReadOnly(True)
        self.revelation_display.setStyleSheet("""
            QTextEdit {
                background-color: #000015;
                color: #ffd700;
                font-family: 'Serif';
                font-size: 18px;
                border: 2px solid #3a3a5a;
                border-radius: 10px;
                padding: 20px;
            }
        """)
        history_widget = QWidget()
        history_layout = QVBoxLayout(history_widget)
        history_layout.setContentsMargins(0, 0, 0, 0)
        history_label = QLabel("📜 История Откровений")
        history_label.setStyleSheet("color: #c0c0e0; font-size: 14px; font-weight: bold;")
        self.history_list = QListWidget()
        self.history_list.setStyleSheet("""
            QListWidget {
                background-color: #0a0a2a;
                color: #c0c0e0;
                font-size: 13px;
                border: 2px solid #3a3a5a;
                border-radius: 10px;
                padding: 10px;
            }
            QListWidget::item {
                padding: 10px;
                border-bottom: 1px solid #2a2a4a;
            }
            QListWidget::item:hover {
                background-color: #2a2a4a;
            }
            QListWidget::item:selected {
                background-color: #3a3a6a;
                color: #ffd700;
            }
        """)
        history_layout.addWidget(history_label)
        history_layout.addWidget(self.history_list)
        splitter.addWidget(self.revelation_display)
        splitter.addWidget(history_widget)
        splitter.setSizes([400, 300])
        layout.addWidget(splitter)
    def request_revelation(self):
        self.revelation_display.clear()
        self.revelation_display.append("🌟 Открытие канала откровения...")
        result = self.kernel.request_revelation()
        if result:
            self.display_revelation(result)
    def display_revelation(self, revelation):
        self.revelation_display.clear()
        self.revelation_display.append("╔══════════════════════════════════════╗")
        self.revelation_display.append("║     ✦ БОЖЕСТВЕННОЕ ОТКРОВЕНИЕ ✦     ║")
        self.revelation_display.append("╚══════════════════════════════════════╝")
        self.revelation_display.append("")
        self.revelation_display.append(f"«{revelation['message']}»")
        self.revelation_display.append("")
        self.revelation_display.append(f"Толкование: {revelation['interpretation']}")
        self.revelation_display.append(f"Тип: {revelation['type']}")
        self.revelation_display.append(f"Сила сигнала: {revelation.get('strength', 'N/A')}")
        self.add_to_history(revelation)
    def add_revelation(self, revelation):
        self.display_revelation(revelation)
    def add_to_history(self, revelation):
        timestamp = time.strftime("%H:%M:%S")
        item_text = f"[{timestamp}] {revelation['message'][:70]}"
        item = QListWidgetItem(item_text)
        item.setForeground(QColor("#ffd700"))
        self.history_list.insertItem(0, item)
    def toggle_auto_check(self, enabled):
        if enabled:
            self.auto_check_timer.start(5000)
            self.auto_btn.setText("🔄 Авто-проверка: ВКЛ")
            self.auto_btn.setStyleSheet("""
                QPushButton {
                    background: #3a3a6a;
                    color: #00ff00;
                    font-weight: bold;
                    font-size: 14px;
                    border-radius: 10px;
                    padding: 12px 25px;
                    border: 2px solid #00ff00;
                }
            """)
        else:
            self.auto_check_timer.stop()
            self.auto_btn.setText("🔄 Авто-проверка: ВЫКЛ")
            self.auto_btn.setStyleSheet("""
                QPushButton {
                    background: #2a2a4a;
                    color: #a0a0d0;
                    font-weight: bold;
                    font-size: 14px;
                    border-radius: 10px;
                    padding: 12px 25px;
                    border: 2px solid #3a3a5a;
                }
            """)
    def auto_check_revelations(self):
        revelation = self.kernel.revelation_service.check_for_revelation()
        if revelation:
            self.display_revelation(revelation)