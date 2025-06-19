class Redirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, message):
        self.text_widget.after(0, self._write_in_main_thread, message)

    def _write_in_main_thread(self, message):
        self.text_widget.insert('end', message)
        self.text_widget.see('end')

    def flush(self):
        pass