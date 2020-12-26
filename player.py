import sys

from PySide2 import QtCore, QtGui, QtWidgets
from cv2 import cv2
import numpy
import qimage2ndarray

class VideoPlayer(QtWidgets.QWidget):
    
    def __init__(self, fps=30):
        super().__init__()
        self.setWindowTitle("Py{Player}")
        self.pause = False
        self.p = None

        self.video_capture = cv2.VideoCapture()

        self.frame_timer = QtCore.QTimer()
        self.setup_fps(fps)
        self.fps = fps

        self.frame_lable = QtWidgets.QLabel()
        self.button_quit = QtWidgets.QPushButton("Quit")
        self.button_play_pause = QtWidgets.QPushButton("Pause")
        self.button_next = QtWidgets.QPushButton(">>")
        self.button_previos = QtWidgets.QPushButton("<<")

        self.main_layout = QtWidgets.QGridLayout()

        self.setup_ui()

        #QtCore.QObject.connect(self.button_previos, QtCore.SIGNAL('clicked()'), self.go_previos)
        QtCore.QObject.connect(self.button_play_pause, QtCore.SIGNAL('clicked()'), self.play_pause)
        QtCore.QObject.connect(self.button_quit, QtCore.SIGNAL('clicked()'), self.close_win)


        path = QtWidgets.QFileDialog.getOpenFileNames(filter="Video (*.mp4)")
        if len(path[0]):
            self.video_capture.open(path[0][0])


    def setup_ui(self):
        self.frame_lable.setAlignment(QtCore.Qt.AlignCenter)
        self.frame_lable.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.frame_lable.setMinimumSize(240, 320)

        self.main_layout.addWidget(self.frame_lable, 0,0,1,3)
        self.main_layout.addWidget(self.button_previos, 1,0,1,1)
        self.main_layout.addWidget(self.button_play_pause,1,1,1,1)
        self.main_layout.addWidget(self.button_next,1,2,1,1)
        self.main_layout.addWidget(self.button_quit,2,0,1,3)

        self.setLayout(self.main_layout)


    def setup_fps(self, fps):
        self.frame_timer.timeout.connect(self.video_stream)
        self.frame_timer.start(int(1000 // fps))


    def video_stream(self):
        ret, frame = self.video_capture.read()
        if not ret:
            return False

        print(self.video_capture.retrieve() )
        #dinamyc resize
        frame = cv2.resize(frame, (self.frame_lable.size().width(), self.frame_lable.size().height()), interpolation = cv2.INTER_AREA)
        #color recorrect
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = qimage2ndarray.array2qimage(frame)
        self.frame_lable.setPixmap(QtGui.QPixmap.fromImage(image))


    def play_pause(self):
        if not self.pause:
            self.frame_timer.stop()
            self.button_play_pause.setText("Play")
        else:
            self.frame_timer.start(int(1000 // self.fps))
            self.button_play_pause.setText("Pause")
        
        self.pause = not self.pause




    def close_win(self):
        cv2.destroyAllWindows()
        self.close()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    player = VideoPlayer()
    player.show()
    sys.exit(app.exec_())