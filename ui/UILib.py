from PySide6.QtWidgets import QApplication, QMessageBox


def copy_text_to_clipboard(text):
    text_to_copy = text
    clipboard = QApplication.clipboard()
    clipboard.setText(text_to_copy)
    msg_box = QMessageBox()
    msg_box.setText(f'{text}已复制到剪贴板')
    msg_box.exec()
