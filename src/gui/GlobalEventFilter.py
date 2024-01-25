from PySide6.QtCore import Signal, QObject

class GlobalEventFilter(QObject):
    eventhappend = Signal(QObject)
    def eventFilter(self, obj, event):
        self.eventhappend.emit(event)
        return super(GlobalEventFilter, self).eventFilter(obj, event)