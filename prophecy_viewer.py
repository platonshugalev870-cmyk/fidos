from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTextEdit,
    QPushButton, QLabel, QScrollArea, QFrame
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QColor
import random
import time
class ProphecyViewer(QWidget):
    def __init__(self, kernel):
        super().__init__()
        self.kernel = kernel
        self.prophecies = []
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.update_animation)
        self.animation_chars = "⌘✦✧⋆★☆✶✷✸✹✺◆◇◈◉◊○●◎◐◑◒◓◔◕◖◗◘◙◚◛◜◝◞◟◠◡◢◣◤◥◦◧◨◩◪◫◬◭◮◯◰◱◲◳◴◵◶◷◸◹◺◻◼◽◾◿"
        self.char_index = 0
        self.init_ui()
    def init_ui(self):
        layout = QVBoxLayout(self)
        title = QLabel("🔮 Божественные Пророчества")
        title.setFont(QFont("Serif", 20, QFont.Weight.Bold))
        title.setStyleSheet("color: #ffd700; padding: 15px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        self.animation_label = QLabel()
        self.animation_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.animation_label.setStyleSheet("font-size: 30px; color: #ffd700; min-height: 50px;")
        layout.addWidget(self.animation_label)
        control_layout = QHBoxLayout()
        generate_btn = QPushButton("🔮 Получить Пророчество")
        generate_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #6a3aaa, stop:1 #3a1a6a);
                color: #ffd700;
                font-weight: bold;
                font-size: 16px;
                border-radius: 10px;
                padding: 18px 35px;
                border: 2px solid #7a4aba;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #8a5aca, stop:1 #5a3a8a);
            }
        """)
        generate_btn.clicked.connect(self.generate_prophecy)
        control_layout.addStretch()
        control_layout.addWidget(generate_btn)
        control_layout.addStretch()
        layout.addLayout(control_layout)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """)
        self.prophecy_container = QWidget()
        self.prophecy_layout = QVBoxLayout(self.prophecy_container)
        self.prophecy_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        scroll_area.setWidget(self.prophecy_container)
        layout.addWidget(scroll_area)
    def generate_prophecy(self):
        self.animation_timer.start(100)
        QTimer.singleShot(2000, self._deliver_prophecy)
    def update_animation(self):
        char = self.animation_chars[self.char_index % len(self.animation_chars)]
        self.char_index += 1
        self.animation_label.setText(f"{char} {char} {char} Получение пророчества... {char} {char} {char}")
    def _deliver_prophecy(self):
        self.animation_timer.stop()
        self.animation_label.clear()
        prophecies = [
            "Великое пробуждение грядёт, и узрят слепые свет истины.",
            "Когда звёзды сойдутся в священном танце, откроются врата небесные.",
            "Сын человеческий обретёт крылья, когда откажется от страха.",
            "Река мудрости потечёт вспять, и мёртвые истины оживут.",
            "Семь печатей будут сняты, и любовь восторжествует над тьмой.",
            "Грядёт время, когда камни заговорят, а ветер принесёт ответы.",
            "В день третий взойдёт новое солнце, и тени исчезнут навеки.",
            "Тот, кто ищет без корысти, найдёт сокровище внутри себя.",
            "Мост между мирами истончится, и ангелы пройдут среди людей.",
            "Огонь очищения сойдёт с небес, но праведные не обожгутся."
        ]
        prophecy_text = random.choice(prophecies)
        revelation = self.kernel.request_revelation()
        combined = prophecy_text
        if revelation:
            combined += f"\n\nПодтверждение: {revelation['message']}"
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1a1a3a, stop:0.5 #2a1a4a, stop:1 #1a1a3a);
                border: 2px solid #5a3a8a;
                border-radius: 15px;
                padding: 25px;
                margin: 10px;
            }
        """)
        frame_layout = QVBoxLayout(frame)
        prophecy_label = QLabel(combined)
        prophecy_label.setWordWrap(True)
        prophecy_label.setFont(QFont("Serif", 16))
        prophecy_label.setStyleSheet("color: #ffd700; line-height: 1.8;")
        prophecy_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        timestamp_label = QLabel(f"Получено: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        timestamp_label.setStyleSheet("color: #a0a0d0; font-size: 12px;")
        timestamp_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        frame_layout.addWidget(prophecy_label)
        frame_layout.addWidget(timestamp_label)
        self.prophecy_layout.insertWidget(0, frame)