from PySide6.QtWidgets import QApplication, QMessageBox


class MsgBox(QMessageBox):
    def __init__(self, text, title='提示'):
        super().__init__()
        self.setWindowTitle(title)
        self.setText(text + '\t')
        self.exec()


def copy_text_to_clipboard(text):
    text_to_copy = text
    clipboard = QApplication.clipboard()
    clipboard.setText(text_to_copy)
    MsgBox(f'{text}已复制到剪贴板。')
