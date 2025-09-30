from typing import List, Tuple, Optional
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtWidgets import (
    QWidget, QMainWindow, QAction, QColorDialog, QSpinBox, QLabel,
    QToolBar, QMessageBox, QFileDialog, QStatusBar
)
from polygon_fill import build_edge_table_and_fill


Point = Tuple[int, int]
Span = Tuple[int, int, int]  # (y, x_start, x_end)


class Canvas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)
        self.points: List[Point] = []
        self.is_closed: bool = False
        self.stroke_color = QColor(0, 0, 0)
        self.fill_color = QColor(10, 132, 255)
        self.stroke_width: int = 2
        self.filled_spans: Optional[List[Span]] = None
        self.setMinimumSize(800, 600)

    def clear(self):
        self.points.clear()
        self.is_closed = False
        self.filled_spans = None
        self.update()

    def undo(self):
        if self.filled_spans is not None:
            # If already filled, undo clears fill first
            self.filled_spans = None
        elif self.points:
            self.points.pop()
        self.update()

    def set_stroke_color(self, color: QColor):
        self.stroke_color = color
        self.update()

    def set_fill_color(self, color: QColor):
        self.fill_color = color
        self.update()

    def set_stroke_width(self, width: int):
        self.stroke_width = max(1, int(width))
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.is_closed:
                # Start a new polygon after close
                self.clear()
            self.points.append((event.x(), event.y()))
            self.update()
        elif event.button() == Qt.RightButton and len(self.points) >= 3:
            self.is_closed = True
            self.update()

    def close_polygon(self):
        if len(self.points) >= 3:
            self.is_closed = True
            self.update()

    def fill_polygon(self):
        if not self.is_closed or len(self.points) < 3:
            return
        spans = build_edge_table_and_fill(self.points)
        self.filled_spans = spans
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)

        # draw fill first if exists
        if self.filled_spans:
            painter.save()
            painter.setPen(Qt.NoPen)
            painter.setBrush(self.fill_color)
            # Draw as many thin horizontal lines (fast enough for assignment)
            # Alternatively, could use QImage for per-pixel raster.
            color_pen = QPen(self.fill_color)
            color_pen.setWidth(1)
            painter.setPen(color_pen)
            for (y, x0, x1) in self.filled_spans:
                painter.drawLine(x0, y, x1, y)
            painter.restore()

        # draw polygon edges/points
        pen = QPen(self.stroke_color)
        pen.setWidth(self.stroke_width)
        painter.setPen(pen)

        for i in range(1, len(self.points)):
            x0, y0 = self.points[i - 1]
            x1, y1 = self.points[i]
            painter.drawLine(x0, y0, x1, y1)

        # draw closing edge if closed
        if self.is_closed and len(self.points) >= 2:
            x0, y0 = self.points[-1]
            x1, y1 = self.points[0]
            painter.drawLine(x0, y0, x1, y1)

        # draw vertices
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.stroke_color)
        r = max(2, self.stroke_width)
        for (x, y) in self.points:
            painter.drawEllipse(QPoint(x, y), r, r)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Polygon Fill (ET/AET) - PyQt5")
        self.canvas = Canvas(self)
        self.setCentralWidget(self.canvas)
        self.status = QStatusBar(self)
        self.setStatusBar(self.status)
        self._create_toolbar()
        self.resize(1000, 700)

    def _create_toolbar(self):
        tb = QToolBar("Tools", self)
        self.addToolBar(tb)

        # Stroke color
        act_stroke = QAction("Stroke Color", self)
        act_stroke.triggered.connect(self._choose_stroke_color)
        tb.addAction(act_stroke)

        # Fill color
        act_fill = QAction("Fill Color", self)
        act_fill.triggered.connect(self._choose_fill_color)
        tb.addAction(act_fill)

        # Stroke width
        tb.addSeparator()
        tb.addWidget(QLabel("Line width:"))
        spin = QSpinBox(self)
        spin.setRange(1, 20)
        spin.setValue(self.canvas.stroke_width)
        spin.valueChanged.connect(self.canvas.set_stroke_width)
        tb.addWidget(spin)

        # Actions: Close, Fill, Undo, Clear
        tb.addSeparator()
        act_close = QAction("Close Polygon (Right Click)", self)
        act_close.triggered.connect(self.canvas.close_polygon)
        tb.addAction(act_close)

        act_fillpoly = QAction("Fill", self)
        act_fillpoly.triggered.connect(self.canvas.fill_polygon)
        tb.addAction(act_fillpoly)

        act_undo = QAction("Undo", self)
        act_undo.triggered.connect(self.canvas.undo)
        tb.addAction(act_undo)

        act_clear = QAction("Clear", self)
        act_clear.triggered.connect(self.canvas.clear)
        tb.addAction(act_clear)

    def _choose_stroke_color(self):
        color = QColorDialog.getColor(self.canvas.stroke_color, self, "Choose Stroke Color")
        if color.isValid():
            self.canvas.set_stroke_color(color)

    def _choose_fill_color(self):
        color = QColorDialog.getColor(self.canvas.fill_color, self, "Choose Fill Color")
        if color.isValid():
            self.canvas.set_fill_color(color)
