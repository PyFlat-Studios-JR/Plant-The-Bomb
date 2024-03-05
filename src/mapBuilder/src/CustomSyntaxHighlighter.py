from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

import src.mapBuilder.src.RULES, src.mapBuilder.src.KEYWORDS


class CustomSyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.error_format = QTextCharFormat()
        self.error_format.setUnderlineColor(QColor(Qt.red))
        self.error_format.setUnderlineStyle(QTextCharFormat.WaveUnderline)

        self.highlighting_rules = []

        for comm in src.RULES.COMMANDS:
            self.add_rule(comm, Qt.yellow)


        self.unique_keywords = []
        for keyword in src.mapBuilder.src.KEYWORDS.keywords:
            format = QTextCharFormat()
            format.setForeground(QColor(keyword["color"]))
            self.unique_keywords.append((keyword["keywords"], format))



    def add_rule(self, pattern, color):
        format = QTextCharFormat()
        format.setForeground(QColor(color))
        rule = (QRegularExpression(pattern), format)
        self.highlighting_rules.append(rule)
    def highlightBlock(self, text):
        self.setFormat(0, len(text), QTextCharFormat())  # Clear existing formatting

        has_valid_syntax = any(rule.match(text).hasMatch() for rule, _ in self.highlighting_rules)

        if not has_valid_syntax:
            # Apply error format to non-matching text
            self.setFormat(0, len(text), self.error_format)

        for keywordlist in self.unique_keywords:
            unique_format = QTextCharFormat()
            unique_format.merge(keywordlist[1])  # Apply unique color
            if not has_valid_syntax:
                unique_format.merge(self.error_format)  # Merge with error format

            for keyword in keywordlist[0]:
                index = text.find(keyword)
                while index != -1:
                    self.setFormat(index, len(keyword), unique_format)
                    index = text.find(keyword, index + 1)

        self.setCurrentBlockState(0)

