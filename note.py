import textwrap


class Note:
    def __init__(self, note):
        self.note = note

    def note_string(self):
        return "\n  Notes: {}".format(textwrap.fill(self.note, subsequent_indent="  "))
