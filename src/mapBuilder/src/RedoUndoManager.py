from src.mapBuilder.src.block import Block


class RedoUndoManager():
    def __init__(self, parent):
        self.parent = parent
        self.stack = []
        self.stackptr = -1
        self.stacksz = 0
        self.valid = 0          #the valid range of the stack
        self.maxsize = 150

    def compare(self, cell1: Block, cell2: Block):
        if cell1 is None and cell2 is None:
            return True
        elif cell1 is None or cell2 is None:
            return False
        else:
            if cell1.get_block() == cell2.get_block():
                if cell1.get_enemy() == cell2.get_enemy():
                    return True
        return False

    def apply_changes(self, grid_old=None, grid_new=None):
        changes = []
        for x, row in enumerate(grid_old):
            for y, cell in enumerate(row):
                if not self.compare(grid_new[x][y], cell):
                    changes.append({
                        "x": x,
                        "y": y,
                        "old": cell,
                        "new":grid_new[x][y]
                        })
        if changes == []:
            return

        if self.stackptr < len(self.stack) - 1:
            self.stack = self.stack[:self.stackptr+1]
            self.stacksz = len(self.stack)

        if len(self.stack) >= self.maxsize:     #failure condition: the stack is full!
            self.stack.pop(0)
            self.stacksz -= 1
            self.stackptr -= 1
        self.valid = self.stackptr + 1 #valid until the current event
        self.stackptr += 1

        if len(self.stack) >= self.stacksz:
            self.stack.append(changes)
            self.stacksz += 1
        else:
            self.stack[self.stackptr] = changes
        return True

    def strg_z(self):
        if self.stackptr < 0:
            return False #the stack (unfortunately) is empty.
        for change in self.stack[self.stackptr]:
            self.parent.place_obj(change['old'], change['x'], change['y'])

        self.stackptr -= 1
        self.parent.changes_since_save = True
        return True

    def strg_y(self):
        if self.stackptr >= self.stacksz or self.stackptr >= self.valid:
            return False #either the stack pointer is at max range or the valid range is smaller!
        self.stackptr += 1
        for change in self.stack[self.stackptr]:
            self.parent.place_obj(change['new'], change['x'], change['y'])
        self.parent.changes_since_save = True
        return True