from PySide6.QtWidgets import QPlainTextEdit, QCompleter
from PySide6.QtGui import QTextCursor, Qt
from PySide6.QtCore import Signal


class CustomTextEdit(QPlainTextEdit):
    def __init__(self, keywords:list, parent=None):
        super(CustomTextEdit, self).__init__(parent)

        self.completer = MyCompleter(keywords)
        self.completer.popup().setStyleSheet("""
            QListView {
                background-color: rgb(50, 50, 50);
                color: rgb(200, 200, 200);
                border: 1px solid rgb(100, 100, 100);
                outline: none;
            }
            QListView::item {
                padding: 5px;
            }
            QListView::item:selected {
                background-color: rgb(100, 100, 100);
                color: rgb(255, 255, 255); 
                
            }
        """)
        self.completer.setWidget(self)
        self.completer.insertText.connect(self.insertCompletion)
        self.completer.activated.connect(self.insertCompletion)

    def insertCompletion(self, completion):
        tc = self.textCursor()
        extra = (len(completion) - len(self.completer.completionPrefix()))
        tc.movePosition(QTextCursor.Left)
        tc.movePosition(QTextCursor.EndOfWord)
        tc.insertText(completion[-extra:])
        self.setTextCursor(tc)
        self.completer.popup().hide()

    def focusInEvent(self, event):
        if self.completer:
            self.completer.setWidget(self)
        QPlainTextEdit.focusInEvent(self, event)

    def keyPressEvent(self, event):
        tc = self.textCursor()
        if event.key() == Qt.Key_Tab and self.completer.popup().isVisible():
            self.completer.insertText.emit(self.completer.getSelected())
            self.completer.setCompletionMode(QCompleter.PopupCompletion)
            return

        QPlainTextEdit.keyPressEvent(self, event)
        tc.select(QTextCursor.WordUnderCursor)
        cr = self.cursorRect()

        if len(tc.selectedText()) > 1:
            self.completer.setCompletionPrefix(tc.selectedText())
            popup = self.completer.popup()
            popup.setCurrentIndex(self.completer.completionModel().index(0,0))

            cr.setWidth(self.completer.popup().sizeHintForColumn(0) 
            + self.completer.popup().verticalScrollBar().sizeHint().width())
            self.completer.complete(cr)
        else:
            self.completer.popup().hide()
            
class MyCompleter(QCompleter):
    insertText = Signal(str)

    def __init__(self, keywords:list, parent=None):
        QCompleter.__init__(self, keywords, parent)
        self.setCompletionMode(QCompleter.PopupCompletion)
        self.highlighted.connect(self.setHighlighted)

    def setHighlighted(self, text):
        self.lastSelected = text

    def getSelected(self):
        return self.lastSelected