import sys

from PySide2 import QtCore, QtGui, QtWidgets
from cv2 import cv2
import numpy
import qimage2ndarray

class VideoPlayer(QtWidgets.QWidget):

    def __init__(self, width=640, height=480, fps=2):
        QtWidgets.QWidget.__init__(self)
        self.pause = False
        self.video = False

        self.setWindowTitle("Player")
        self.video_size = QtCore.QSize(width, height)
        self.camera_capture = cv2.VideoCapture(cv2.CAP_DSHOW)
        self.video_capture = cv2.VideoCapture()

        self.frame_timer = QtCore.QTimer()
        self.setup_camera(fps)
        self.fps = fps

        self.frame_lable = QtWidgets.QLabel()
        self.quit_button = QtWidgets.QPushButton("Quit")
        self.play_pause_button = QtWidgets.QPushButton("Pause")
        self.camera_video_button = QtWidgets.QPushButton("Swith to video")

        self.main_layout = QtWidgets.QGridLayout()

        self.setup_ui()

        QtCore.QObject.connect(self.play_pause_button, QtCore.SIGNAL('clicked()'), self.play_pause)
        QtCore.QObject.connect(self.camera_video_button, QtCore.SIGNAL('clicked()'), self.camera_video)


    def setup_ui(self):       
        self.frame_lable.setFixedSize(self.video_size)
        self.quit_button.clicked.connect(self.close_win)

        self.main_layout.addWidget(self.frame_lable, 0,0,1,2)
        self.main_layout.addWidget(self.play_pause_button, 1,0,1,1)
        self.main_layout.addWidget(self.camera_video_button, 1,1,1,2)
        self.main_layout.addWidget(self.quit_button, 2,0,1,2)

        self.setLayout(self.main_layout)


    def play_pause(self):
        if not self.pause:
            self.frame_timer.stop()
            self.play_pause_button.setText("Play")
        else:
            self.frame_timer.start(int(1000 // self.fps))
            self.play_pause_button.setText("Pause")
        
        self.pause = not self.pause


    def camera_video(self):
        if not self.video:
            path = QtWidgets.QFileDialog.getOpenFileNames(filter='Video (*mp4)')
            if len(path[0]):
                print(path)
                self.video_capture.open(path[0][0])
                self.camera_video_button.setText("Swith to camera")
        else:
            self.camera_video_button.setText("Swith to video")
            self.video_capture.release()

        self.video = not self.video


    def setup_camera(self, fps):
        self.camera_capture.set(3, self.video_size.width())
        self.camera_capture.set(4, self.video_size.width())
        
        self.frame_timer.timeout.connect(self.display_video_stream)
        self.frame_timer.start(int(1000 // fps))

    
    def display_video_stream(self):
        if not self.video:
            ret, frame = self.camera_capture.read()
            #отзеркаливание
            frame = cv2.flip(frame, 1)
        else:
            ret, frame = self.video_capture.read()
            
            video_width = int(self.video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
            video_height = int(self.video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
            
            screen_rect = app.desktop().screenGeometry()
            video_width = (screen_rect.width() if video_width > screen_rect.width() else video_width)
            video_height = (screen_rect.height() if video_height > screen_rect.height() else video_height)

            self.video_size = QtCore.QSize(video_width, video_height)
            #self.frame_lable.setFixedSize(self.video_size)
            frame = cv2.resize(frame, (self.video_size.width(), self.video_size.height()), interpolation = cv2.INTER_AREA)

        if not ret:
            return False
        
        # трансформация цветов
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        
        

        # фрэйм превращаем в картинку
        image = qimage2ndarray.array2qimage(frame)

        self.frame_lable.setPixmap(QtGui.QPixmap.fromImage(image))


    def close_win(self):
        cv2.destroyAllWindows()
        self.camera_capture.release()
        self.video_capture.release()
        self.close()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    player = VideoPlayer()
    player.show()
    sys.exit(app.exec_())