import json
import os
import sys
from datetime import datetime

NOTES_FILE = 'notes.json'

class Note:
    def __init__(self, note_id, title, message, timestamp):
        self.id = note_id
        self.title = title
        self.message = message
        self.timestamp = timestamp

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'message': self.message,
            'timestamp': self.timestamp
        }

    @staticmethod
    def from_dict(note_dict):
        return Note(
            note_id=note_dict['id'],
            title=note_dict['title'],
            message=note_dict['message'],
            timestamp=note_dict['timestamp']
        )


class NoteManager:
    def __init__(self, filename):
        self.filename = filename
        self.notes = self.load_notes()

    def load_notes(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as file:
                notes_list = json.load(file)
                return [Note.from_dict(note) for note in notes_list]
        return []

    def save_notes(self):
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump([note.to_dict() for note in self.notes], file, ensure_ascii=False, indent=4)

    def add_note(self, title, message):
        note_id = max([note.id for note in self.notes], default=0) + 1
        timestamp = datetime.now().isoformat()
        new_note = Note(note_id, title, message, timestamp)
        self.notes.append(new_note)
        self.save_notes()
        print('Заметка успешно сохранена')

    def list_notes(self, date_filter=None):
        filtered_notes = self.notes
        if date_filter:
            filtered_notes = [note for note in self.notes if note.timestamp.startswith(date_filter)]
        for note in filtered_notes:
            print(f"ID: {note.id}, Title: {note.title}, Date: {note.timestamp}")
            print(f"Message: {note.message}")
            print('-' * 40)

    def edit_note(self, note_id, new_title=None, new_message=None):
        for note in self.notes:
            if note.id == note_id:
                if new_title:
                    note.title = new_title
                if new_message:
                    note.message = new_message
                note.timestamp = datetime.now().isoformat()
                self.save_notes()
                print('Заметка успешно обновлена')
                return
        print('Заметка с указанным ID не найдена')

    def delete_note(self, note_id):
        self.notes = [note for note in self.notes if note.id != note_id]
        self.save_notes()
        print('Заметка успешно удалена')


class NoteApp:
    def __init__(self, note_manager):
        self.note_manager = note_manager

    def print_usage(self):
        print("Использование:")
        print("  add --title \"Заголовок\" --msg \"Тело заметки\"")
        print("  list [--date YYYY-MM-DD]")
        print("  edit --id ID [--title \"Новый заголовок\"] [--msg \"Новое тело\"]")
        print("  delete --id ID")

    def run(self, args):
        if len(args) < 2:
            self.print_usage()
            return

        command = args[1]

        if command == 'add':
            title = None
            message = None
            for i in range(2, len(args), 2):
                if args[i] == '--title':
                    title = args[i + 1]
                elif args[i] == '--msg':
                    message = args[i + 1]
            if title and message:
                self.note_manager.add_note(title, message)
            else:
                self.print_usage()

        elif command == 'list':
            date_filter = None
            if len(args) == 4 and args[2] == '--date':
                date_filter = args[3]
            self.note_manager.list_notes(date_filter)

        elif command == 'edit':
            note_id = None
            new_title = None
            new_message = None
            for i in range(2, len(args), 2):
                if args[i] == '--id':
                    note_id = int(args[i + 1])
                elif args[i] == '--title':
                    new_title = args[i + 1]
                elif args[i] == '--msg':
                    new_message = args[i + 1]
            if note_id:
                self.note_manager.edit_note(note_id, new_title, new_message)
            else:
                self.print_usage()

        elif command == 'delete':
            note_id = None
            for i in range(2, len(args), 2):
                if args[i] == '--id':
                    note_id = int(args[i + 1])
            if note_id:
                self.note_manager.delete_note(note_id)
            else:
                self.print_usage()
        else:
            self.print_usage()


if __name__ == '__main__':
    note_manager = NoteManager(NOTES_FILE)
    app = NoteApp(note_manager)
    app.run(sys.argv)
