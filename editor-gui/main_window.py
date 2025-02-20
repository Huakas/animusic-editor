from PySide6.QtWidgets import QMainWindow, QPushButton, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QGraphicsRectItem, QGraphicsItemGroup, QGraphicsItem, QGraphicsEffect, QGraphicsOpacityEffect
from PySide6.QtCore import Qt, QPointF, QRectF
from PySide6.QtGui import QColor, QPainter, QPixmap, QPainterPath, QPen, QBrush, QRegion

class EditorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Animusic Editor")

        self.scene = QGraphicsScene()
        self.view = CanvasView(self.scene)
        self.setCentralWidget(self.view)

        # Create a 1920x1080 black canvas
        self.canvas = QGraphicsRectItem(0, 0, 1920, 1080)
        self.canvas.setBrush(QColor(Qt.black))  # Fill with black
        self.canvas.setPen(Qt.NoPen)  # No border
        self.scene.addItem(self.canvas)

        # Center the canvas in the scene
        self.canvas.setPos(-960, -540)

        # Add a draggable item inside the canvas
        pixmap = QPixmap(200, 200)
        pixmap.fill(QColor(Qt.red))  # Create a red square
        self.add_draggable_item(pixmap, 500, 300)  # Add item at (500,300)

    def change_canvas_size(self, x, y):
        self.canvas.setRect(0, 0, x, y)
        self.canvas.setPos(-x / 2, -y / 2)
        self.view.setSceneRect(-x / 2, -y / 2, x, y)

    def add_draggable_item(self, pixmap, x, y):
        """ Adds a draggable image inside the canvas. """
        item = DraggableItem(pixmap, self.canvas.boundingRect(), parent=self.canvas)  # Attach to canvas
        item.setPos(x, y)  # Position inside the canvas


class CanvasView(QGraphicsView):
    def __init__(self, scene):
        super().__init__(scene)
        self.setRenderHint(QPainter.Antialiasing)
        self.setTransformationAnchor(QGraphicsView.NoAnchor)
        self.setResizeAnchor(QGraphicsView.NoAnchor)
        self.setBackgroundBrush(QColor(50, 50, 50))
        self.last_scene_pos = None

    def wheelEvent(self, event):
        """ Zoom in/out with the scroll wheel """
        zoom_factor = 1.15 if event.angleDelta().y() > 0 else 0.85
        self.scale(zoom_factor, zoom_factor)

    def mousePressEvent(self, event):
        """ Capture the exact scene position under cursor on middle mouse press """
        if event.button() == Qt.MiddleButton:
            self.last_scene_pos = self.mapToScene(event.position().toPoint())  # Convert to scene coordinates
            self.setCursor(Qt.ClosedHandCursor)
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        """ Move the view so that the same scene point stays under the cursor """
        if self.last_scene_pos is not None:
            new_scene_pos = self.mapToScene(event.position().toPoint())  # Get new scene position
            delta = new_scene_pos - self.last_scene_pos  # Calculate exact movement
            self.translate(delta.x(), delta.y())  # Move the view by exact amount
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        """ Stop panning when middle mouse button is released """
        if event.button() == Qt.MiddleButton:
            self.last_scene_pos = None
            self.setCursor(Qt.ArrowCursor)
        else:
            super().mouseReleaseEvent(event)

class DraggableItem(QGraphicsItemGroup):
    def __init__(self, pixmap, canvas_rect, parent=None):
        super().__init__(parent)
        self.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable)
        self.setAcceptHoverEvents(True)
        self.click_offset = QPointF()
        self.canvas_rect = canvas_rect  # Store canvas bounds

        # Create Pixmap Item (Actual Content)
        self.pixmap_item = ClippedPixmapItem(pixmap, canvas_rect, parent)
        self.addToGroup(self.pixmap_item)

        # Create Outline (Always Visible)
        self.outline = QGraphicsRectItem(self.pixmap_item.boundingRect())
        self.outline.setPen(QPen(QColor(Qt.red), 2, Qt.DashLine))
        self.outline.setBrush(Qt.NoBrush)
        self.addToGroup(self.outline)
        self.outline.setZValue(2)  # Always above the pixmap

    def mousePressEvent(self, event):
        """ Store click offset to prevent jump. """
        self.click_offset = event.pos()
        self.setZValue(3)  # Bring to front while dragging
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        """ Move item and reapply clipping. """
        if self.parentItem():
            new_pos = self.mapToParent(event.pos() - self.click_offset)
            self.setPos(new_pos)
            self.pixmap_item.update()  # Repaint clipped area

    def mouseReleaseEvent(self, event):
        """ Reset Z value after releasing the item. """
        self.setZValue(0)
        self.pixmap_item.update()  # Ensure clipping updates
        super().mouseReleaseEvent(event)

class ClippedPixmapItem(QGraphicsPixmapItem):
    def __init__(self, pixmap, canvas_rect, canvas_item):
        super().__init__(pixmap)
        self.canvas_rect = canvas_rect
        self.canvas_item = canvas_item

    def paint(self, painter, option, widget=None):
        """ Clip the item to the canvas bounds while keeping the offset correct. """
        painter.save()

        # Get the canvas's position in the scene
        canvas_scene_pos = self.canvas_item.scenePos()  # Use the parent (canvas) as reference
        adjusted_canvas_rect = self.canvas_rect.translated(canvas_scene_pos)

        # Convert adjusted canvas bounds to local item coordinates
        canvas_bounds = self.mapFromScene(adjusted_canvas_rect).boundingRect()

        # Clip painting to the canvas region
        painter.setClipRect(canvas_bounds)

        # Draw the pixmap (inside the clipping bounds)
        super().paint(painter, option, widget)

        painter.restore()
