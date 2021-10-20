class Note:
    def __init__(self, note):
        self.note = note

    def note_string(self):
        note_string = "\n  Notes: "
        if len(self.note) > 0:
            if len(self.note) > 80:
                for i, c in enumerate(self.note):
                    note_string += c
                    if i >= 80 and c == ' ':
                        note_string += '\n ' + self.note[i:]
                        #if len(self.note) - i > 80:
                        #if len(self.note) > 160:
                         #   note_string += c
                          #  if i >= 80 and c == ' ':
                           #     note_string += '\n ' + self
                        #else:
                         #   note_string += self.note[i:]

                        break
            else:
                note_string += self.note

        return note_string
