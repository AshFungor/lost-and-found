# TUI imports
from asciimatics.screen     import Screen
from asciimatics.exceptions import ResizeScreenError
# System imports
import sys
# Local imports
import tui
import environment


if __name__ == '__main__':
    last_scene = None
    while True:
        try:
            Screen.wrapper(tui.iter, catch_interrupt=True, arguments=[last_scene])
            sys.exit(0)
        except ResizeScreenError as e:
            last_scene = e.scene
    

            
            