import sys
import mouse
import screeninfo
from threading import local
from PyQt5.QtCore import QRect, Qt
from mouse import LEFT, UP, DOWN, ButtonEvent, MoveEvent

from PyQt5.QtGui import QPixmap, QPainter, QColor, QPen
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton

h = screeninfo.get_monitors()[0].height
w = screeninfo.get_monitors()[0].width



class Bbox(object):
    def __init__(self):
        self._empty = True
        self.init_bbox()

    @property
    def point1(self):
        return self._x1, self._y1

    @point1.setter
    def point1(self, position: tuple):
        self._x1 = position[0]
        self._y1 = position[1]

    @property
    def point2(self):
        return self._x2, self._y2

    @point2.setter
    def point2(self, position: tuple):
        self._empty = False
        self._x2 = position[0]
        self._y2 = position[1]

    @property
    def bbox(self):
        if self._x1 < self._x2:
            x_min, x_max = self._x1, self._x2
        else:
            x_min, x_max = self._x2, self._x1

        if self._y1 < self._y2:
            y_min, y_max = self._y1, self._y2
        else:
            y_min, y_max = self._y2, self._y1
        return (x_min, y_min, x_max - x_min, y_max - y_min)

    def is_empty(self):
        return self._empty

    def init_bbox(self):
        self._x1 = 0
        self._x2 = 0
        self._y1 = 0
        self._y2 = 0

    def __str__(self):
        return str(self.bbox)


class MyApp(QMainWindow):
    def __init__(self):
        super(MyApp, self).__init__()
        self.button = QPushButton("划屏截图", self)
        self.button.clicked.connect(self.screenShot)

        self.screen = QApplication.primaryScreen()

        self.pixmap = QPixmap(w, h)
        self.tmp_pixmap = QPixmap(w, h)
        self.pixmap.fill(Qt.transparent)

        self.label = QLabel()

        self.pen = QPen(Qt.white, 2, Qt.DashLine)

        self.bbox = Bbox()

        self.left_down = False # 防止点击按钮后释放触发钩子

    def screenShot(self):
        '''鼠标按下开始执行'''
        self.pixmap = self.screen.grabWindow(0)
        self.label.setPixmap(self.pixmap)
        self.label.showFullScreen()
        mouse.hook(self.mouse_hok)

    def callback(self):
        '''鼠标释放时回调'''
        img = self.pixmap.copy(*self.bbox.bbox)
        self.label.setPixmap(img)
        self.label.adjustSize()
        self.label.showNormal()
        self.bbox.init_bbox()

    def mouse_hok(self, event):
        if isinstance(event, ButtonEvent):
            if event.event_type == DOWN and event.button == LEFT:
                print("左键按下", mouse.get_position())
                self.bbox.point1 = mouse.get_position()
                self.left_down = True
            elif event.event_type == UP and event.button == LEFT:
                print("左键释放", mouse.get_position())
                self.left_down = False
                mouse.unhook_all()
                self.callback()
        if isinstance(event, MoveEvent) and self.left_down:
            self.bbox.point2 = mouse.get_position()
            pixmap = self.pixmap.copy()
            painter = QPainter()
            painter.begin(pixmap)
            painter.setPen(self.pen) # 设置pen必须在begin后
            rect = QRect(*self.bbox.bbox)
            painter.drawRect(rect)
            painter.end()
            self.label.setPixmap(pixmap)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
