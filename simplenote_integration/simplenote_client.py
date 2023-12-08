import os
import simplenote


class SimpleNoteClient:
    def __init__(self):
        self.username = os.getenv("SIMPLENOTE_USERNAME")
        self.password = os.getenv("SIMPLENOTE_PASSWORD")
        self.sn = simplenote.Simplenote(self.username, self.password)

    def create_note(self, content, tags=None):
        """
        Create a new note with the given content and optional tags.
        """
        note = {"content": content, "tags": tags or []}
        return self.sn.add_note(note)

    def get_note(self, key):
        """
        Retrieve a note by its unique key.
        """
        return self.sn.get_note(key)

    def get_note_list(self, data=True, since=None, tags=[]):
        """
        Fetch all notes
        """
        return self.sn.get_note_list(data, since, tags)

    def update_note(self, key, new_content):
        """
        Update the content of an existing note identified by its key.
        """
        note, _ = self.get_note(key)
        note["content"] = new_content
        return self.sn.update_note(note)

    def archive_note(self, key):
        """
        Archive a note by its key.
        """
        note, _ = self.get_note(key)
        note["deleted"] = True
        return self.sn.update_note(note)
