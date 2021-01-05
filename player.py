import sys

from PySide2 import QtCore, QtGui, QtWidgets
from cv2 import cv2
#import numpy
import qimage2ndarray

class VideoPlayer(QtWidgets.QWidget):
    
    def __init__(self, fps=30):
        super().__init__()
        self.setWindowTitle("Py{Player}")
        self.setWindowIcon(QtGui.QIcon('res\icon.png'))
        self.pause = False
        self.p = None

        self.video_capture = cv2.VideoCapture()

        self.frame_timer = QtCore.QTimer()
        self.setup_fps(fps)
        self.fps = fps

        self.timer = 0

        #create widge
        # ts
        self.frame_lable = QtWidgets.QLabel()
        self.button_quit = QtWidgets.QPushButton("Quit")
        self.button_play_pause = QtWidgets.QPushButton("Pause")
        self.button_next = QtWidgets.QPushButton(">>")
        self.button_previos = QtWidgets.QPushButton("<<")
        self.progress_bar = QtWidgets.QProgressBar()

        self.main_layout = QtWidgets.QGridLayout()

        self.setup_ui()

        QtCore.QObject.connect(self.button_previos, QtCore.SIGNAL('clicked()'), self.go_previos)
        QtCore.QObject.connect(self.button_play_pause, QtCore.SIGNAL('clicked()'), self.play_pause)
        QtCore.QObject.connect(self.button_next, QtCore.SIGNAL('clicked()'), self.go_next)
        QtCore.QObject.connect(self.button_quit, QtCore.SIGNAL('clicked()'), self.close_win)


        path = QtWidgets.QFileDialog.getOpenFileNames(filter="Video (*.mp4)")
        if len(path[0]):
            self.video_capture.open(path[0][0])
        

        self.frame_count = int(self.video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
        self.duration = self.frame_count/self.fps

        #progress bar setting
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(self.frame_count)


    def setup_ui(self):
        self.frame_lable.setAlignment(QtCore.Qt.AlignCenter)
        #self.frame_lable.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.frame_lable.setMinimumSize(240, 320)

        self.main_layout.addWidget(self.frame_lable, 0,0,1,3)
        self.main_layout.addWidget(self.progress_bar, 1,0,1,3)
        self.main_layout.addWidget(self.button_previos, 2,0,1,1)
        self.main_layout.addWidget(self.button_play_pause,2,1,1,1)
        self.main_layout.addWidget(self.button_next,2,2,1,1)
        self.main_layout.addWidget(self.button_quit,3,0,1,3)


        self.setLayout(self.main_layout)


    def setup_fps(self, fps):
        self.frame_timer.timeout.connect(self.video_stream)
        self.frame_timer.start(int(1000 // fps))


    def video_stream(self):
        ret, frame = self.video_capture.read()
        if not ret:
            return False

        #dinamyc resize
        frame = cv2.resize(frame, (self.frame_lable.size().width(), self.frame_lable.size().height()), interpolation = cv2.INTER_AREA)
        #color recorrect
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = qimage2ndarray.array2qimage(frame)
        self.frame_lable.setPixmap(QtGui.QPixmap.fromImage(image))
        self.progress_bar_update()


    def progress_bar_update(self):
        self.timer += 1
        self.progress_bar.setValue(self.timer)


    def play_pause(self):
        if not self.pause:
            self.frame_timer.stop()
            self.button_play_pause.setText("Play")
        else:
            self.frame_timer.start(int(1000 // self.fps))
            self.button_play_pause.setText("Pause")
        
        self.pause = not self.pause


    def go_previos(self):
        self.timer -= (10 * self.fps)
        self.timer = (0 if self.timer < 0 else self.timer) # was a not < 0 timer counts
        self.video_capture.set(cv2.CAP_PROP_POS_FRAMES, self.timer)


    def go_next(self):
        self.timer += (10 * self.fps)
        self.timer = (self.frame_count if self.timer > self.frame_count else self.timer)
        self.video_capture.set(cv2.CAP_PROP_POS_FRAMES, self.timer)


    def close_win(self):
        cv2.destroyAllWindows()
        self.close()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    player = VideoPlayer()
    player.show()
    sys.exit(app.exec_())