# undo_redo.py

from collections import deque

class UndoRedoManager:
    def __init__(self, max_history=50):
        self.undo_stack = deque(maxlen=max_history)
        self.redo_stack = deque(maxlen=max_history)
        self.current_state = ""
        self.last_saved_state = ""

    def save_state(self, state):
        if state != self.current_state:
            self.undo_stack.append(self.current_state)
            self.redo_stack.clear()
            self.current_state = state

    def undo(self):
        if self.undo_stack:
            self.redo_stack.append(self.current_state)
            self.current_state = self.undo_stack.pop()
            return self.current_state
        return None

    def redo(self):
        if self.redo_stack:
            self.undo_stack.append(self.current_state)
            self.current_state = self.redo_stack.pop()
            return self.current_state
        return None

    def can_undo(self):
        return bool(self.undo_stack)

    def can_redo(self):
        return bool(self.redo_stack)