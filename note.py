import textwrap


class Note:
    def __init__(self, note):
        self.note = note

    def __eq__(self, other):
        return self.note == other.note

    def __str__(self):
        return "  Notes: {}".format(textwrap.fill(self.note, subsequent_indent="  "))
