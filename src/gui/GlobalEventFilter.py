from PySide6.QtCore import Signal, QObject, QEvent

class GlobalEventFilter(QObject):
    eventhappend = Signal(QObject)
    keypress = Signal(QObject)
    keyrelease = Signal(QObject)
    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyPress:
            self.keypress.emit(event)
        elif event.type() == QEvent.KeyRelease:
            self.keyrelease.emit(event)
        self.eventhappend.emit(event)
        return super(GlobalEventFilter, self).eventFilter(obj, event)
