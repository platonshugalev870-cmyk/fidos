from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt, QTimer, QPointF
from PyQt6.QtGui import (
    QPainter, QColor, QRadialGradient, QBrush,
    QPen, QFont, QLinearGradient
)
import math
import random
import numpy as np
class SacredParticle:
    def __init__(self, x, y, vx, vy, life, color):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.life = life
        self.max_life = life
        self.color = color
        self.trail = []
    def update(self):
        self.trail.append((self.x, self.y))
        if len(self.trail) > 20:
            self.trail.pop(0)
        self.x += self.vx
        self.y += self.vy
        self.life -= 1
        self.vy -= 0.02
    def is_alive(self):
        return self.life > 0
class SacredVisualizer(QWidget):
    def __init__(self):
        super().__init__()
        self.particles = []
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(30)
        self.time = 0
        self.pulse_active = False
        self.pulse_intensity = 0
        self.setMinimumSize(400, 400)
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor(5, 5, 25))
        gradient.setColorAt(0.5, QColor(15, 5, 35))
        gradient.setColorAt(1, QColor(5, 5, 25))
        painter.fillRect(self.rect(), QBrush(gradient))
        center_x = self.width() / 2
        center_y = self.height() / 2
        self.draw_sacred_geometry(painter, center_x, center_y)
        for particle in self.particles:
            alpha = int(255 * (particle.life / particle.max_life))
            color = QColor(particle.color.red(), particle.color.green(), 
                          particle.color.blue(), alpha)
            for i, (tx, ty) in enumerate(particle.trail):
                trail_alpha = int(alpha * (i / len(particle.trail)) * 0.3)
                trail_color = QColor(color.red(), color.green(), color.blue(), trail_alpha)
                painter.setPen(QPen(trail_color, 2))
                painter.drawPoint(int(tx), int(ty))
            painter.setPen(QPen(color, 4))
            painter.drawPoint(int(particle.x), int(particle.y))
        if self.pulse_active:
            pulse_alpha = int(self.pulse_intensity * 255)
            pulse_gradient = QRadialGradient(QPointF(center_x, center_y), 
                                            self.pulse_intensity * 300)
            pulse_gradient.setColorAt(0, QColor(255, 215, 0, pulse_alpha))
            pulse_gradient.setColorAt(0.5, QColor(255, 215, 0, pulse_alpha // 2))
            pulse_gradient.setColorAt(1, QColor(255, 215, 0, 0))
            painter.setBrush(QBrush(pulse_gradient))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(QPointF(center_x, center_y), 
                              self.pulse_intensity * 300, 
                              self.pulse_intensity * 300)
            self.pulse_intensity *= 0.9
            if self.pulse_intensity < 0.01:
                self.pulse_active = False
                self.pulse_intensity = 0
        label = QLabel("🌀 Сакральный Визуализатор", self)
        label.setStyleSheet("color: #ffd700; font-size: 18px; font-weight: bold; background: transparent;")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setGeometry(0, 10, self.width(), 30)
    def draw_sacred_geometry(self, painter, cx, cy):
        self.time += 0.02
        colors = [
            QColor(255, 215, 0, 50),
            QColor(138, 43, 226, 40),
            QColor(0, 191, 255, 40),
            QColor(255, 105, 180, 35),
        ]
        for ring in range(3):
            radius = 80 + ring * 60 + math.sin(self.time * 0.5 + ring) * 15
            num_points = 6 + ring * 2
            color = colors[ring % len(colors)]
            pen = QPen(color, 2)
            painter.setPen(pen)
            points = []
            for i in range(num_points + 1):
                angle = (2 * math.pi * i / num_points) + self.time * 0.3
                x = cx + radius * math.cos(angle)
                y = cy + radius * math.sin(angle)
                points.append(QPointF(x, y))
            for i in range(len(points) - 1):
                painter.drawLine(points[i], points[i + 1])
            for i in range(num_points):
                for j in range(i + 1, num_points):
                    if (j - i) % 2 == 1:
                        painter.setPen(QPen(color, 1))
                        painter.drawLine(points[i], points[j])
        flower_radius = 50 + math.sin(self.time * 0.7) * 10
        for i in range(12):
            angle = 2 * math.pi * i / 12 + self.time * 0.2
            petal_x = cx + flower_radius * math.cos(angle)
            petal_y = cy + flower_radius * math.sin(angle)
            petal_gradient = QRadialGradient(QPointF(petal_x, petal_y), 15)
            petal_gradient.setColorAt(0, QColor(255, 200, 100, 100))
            petal_gradient.setColorAt(1, QColor(255, 100, 50, 0))
            painter.setBrush(QBrush(petal_gradient))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(QPointF(petal_x, petal_y), 15, 15)
        center_glow = QRadialGradient(QPointF(cx, cy), 30)
        center_glow.setColorAt(0, QColor(255, 255, 255, 150))
        center_glow.setColorAt(0.5, QColor(255, 215, 0, 80))
        center_glow.setColorAt(1, QColor(255, 100, 0, 0))
        painter.setBrush(QBrush(center_glow))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(QPointF(cx, cy), 30, 30)
    def update_animation(self):
        if random.random() < 0.3:
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(0.5, 2)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            life = random.randint(30, 80)
            colors = [
                QColor(255, 215, 0),
                QColor(138, 43, 226),
                QColor(0, 191, 255),
                QColor(255, 105, 180),
                QColor(255, 255, 255),
            ]
            color = random.choice(colors)
            self.particles.append(
                SacredParticle(self.width()/2, self.height()/2, vx, vy, life, color)
            )
        for particle in self.particles[:]:
            particle.update()
            if not particle.is_alive():
                self.particles.remove(particle)
        self.update()
    def activate_pulse(self):
        self.pulse_active = True
        self.pulse_intensity = 1.0
        for _ in range(20):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 5)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            life = random.randint(20, 50)
            color = QColor(255, 215, 0)
            self.particles.append(
                SacredParticle(self.width()/2, self.height()/2, vx, vy, life, color)
            )