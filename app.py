import sys
import cv2
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen, QColor
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QSizePolicy, QVBoxLayout, QWidget, QPushButton, QFileDialog


class VideoPlayerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.video_path = ''
        self.video_cap = None
        self.timer = QTimer(self)
        self.frame_label = QLabel(self)
        self.frame_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.frame_label.setAlignment(Qt.AlignCenter)
        self.playing = False
        self.paused = False
        self.lines = []
        self.show_crosshair = False

        layout = QVBoxLayout()
        layout.addWidget(self.frame_label)

        # Add play/pause button
        self.play_pause_button = QPushButton('Play', self)
        self.play_pause_button.clicked.connect(self.play_pause_video)
        layout.addWidget(self.play_pause_button)

        # Add load video button
        self.load_video_button = QPushButton('Load Video', self)
        self.load_video_button.clicked.connect(self.load_video_file)
        layout.addWidget(self.load_video_button)

        # Add toggle crosshair button
        self.toggle_crosshair_button = QPushButton('Toggle Crosshair', self)
        self.toggle_crosshair_button.setCheckable(True)
        self.toggle_crosshair_button.toggled.connect(self.toggle_crosshair)
        layout.addWidget(self.toggle_crosshair_button)

        self.setLayout(layout)

    def load_video_file(self):
        file_dialog = QFileDialog()
        video_path, _ = file_dialog.getOpenFileName(self, 'Select Video File')
        if video_path:
            self.load_video(video_path)

    def load_video(self, video_path):
        self.video_path = video_path
        self.video_cap = cv2.VideoCapture(video_path)
        self.playing = False
        self.paused = False

    def play_pause_video(self):
        if not self.video_cap.isOpened():
            return

        if not self.playing:
            self.playing = True
            self.timer.timeout.connect(self.display_frame)
            self.timer.start(33)  # 30 fps
            self.play_pause_button.setText('Pause')
        else:
            self.paused = not self.paused
            if self.paused:
                self.play_pause_button.setText('Play')
            else:
                self.play_pause_button.setText('Pause')

    def display_frame(self):
        ret, frame = self.video_cap.read()
        if ret:
            if self.paused:
                self.timer.stop()
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = QImage(
                frame_rgb.data,
                frame_rgb.shape[1],
                frame_rgb.shape[0],
                QImage.Format_RGB888
            )
            self.frame_label.setPixmap(QPixmap.fromImage(image))
            self.draw_objects()

    def draw_objects(self):
        if self.paused:
            painter = QPainter(self.frame_label.pixmap())
            pen = QPen(Qt.red)
            pen.setWidth(2)
            painter.setPen(pen)

            for line in self.lines:
                painter.drawLine(*line)

            if self.show_crosshair:
                frame_width = self.frame_label.width()
                frame_height = self.frame_label.height()
                crosshair_length = 30
                crosshair_thickness = 2
                center_x = frame_width // 2
                center_y = frame_height // 2

                # Draw vertical line
                painter.drawLine(center_x, center_y - crosshair_length, center_x, center_y + crosshair_length)
                # Draw horizontal line
                painter.drawLine(center_x - crosshair_length, center_y, center_x + crosshair_length, center_y)
                # Draw circle at the center
                pen.setWidth(crosshair_thickness + 1)
                painter.setPen(pen)
                painter.drawEllipse(center_x - crosshair_length, center_y - crosshair_length, crosshair_length * 2, crosshair_length * 2)

            painter.end()

    def toggle_crosshair(self, checked):
        self.show_crosshair = checked
        self.frame_label.update()

    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton and not self.paused:
            x = event.x()
            y = event.y()
            if self.show_crosshair and self.is_within_crosshair(x, y):
                self.toggle_crosshair_button.setChecked(False)

    def is_within_crosshair(self, x, y):
        frame_width = self.frame_label.width()
        frame_height = self.frame_label.height()
        crosshair_length = 30
        center_x = frame_width // 2
        center_y = frame_height // 2
        return (
            center_x - crosshair_length <= x <= center_x + crosshair_length and
            center_y - crosshair_length <= y <= center_y + crosshair_length
        )


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.video_player = VideoPlayerWidget(self)
        self.setCentralWidget(self.video_player)

        self.setWindowTitle('Video Player')
        self.setGeometry(100, 100, 800, 600)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
