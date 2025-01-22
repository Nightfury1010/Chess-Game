class Node:
    def __init__(self, state):
        self.state = state  # Store the game state (e.g., board, moves)
        self.prev = None
        self.next = None


class ChessHistory:
    def __init__(self):
        self.current = None  # Pointer to the current state

    def add_state(self, state):
        """Add a new state to the history."""
        new_node = Node(state)
        if self.current:
            new_node.prev = self.current
            self.current.next = new_node
        self.current = new_node

    def undo(self):
        """Move to the previous state if possible."""
        if self.current and self.current.prev:
            self.current = self.current.prev
            return self.current.state
        else:
            self.current = None
        return None

    def redo(self):
        """Move to the next state if possible."""
        if self.current and self.current.next:
            self.current = self.current.next
            return self.current.state
        print("No next state to redo to.")
        return None

    def get_current_state(self):
        """Get the current game state."""
        return self.current.state if self.current else None
    
    def reset(self):
        """Reset the history to the initial state."""
        self.current = None

    def get_undo_state(self):
        if self.current and self.current.prev:
            print(self.current.state)
            print(self.current.prev.state)
            return True
        return False

