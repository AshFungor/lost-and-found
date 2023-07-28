# TUI
import asciimatics.widgets      as asc
import asciimatics.exceptions   as asc_ex
from asciimatics.scene          import Scene

# Local imports
from messages   import msg
from archiving  import current
from environment import settings

# Presets
HEADER_SIZE = 2 / 7
FOOTER_SIZE = 1 / 7

class Model():
    curr_archive = None
    archives = current.list_archives()
    unlocks = current.list_unlocks()

class ArchiveView(asc.Frame):
    def __init__(self, screen):
        height, width = screen.dimensions
        super().__init__(screen, 
                         height, 
                         width, 
                         can_scroll=False, 
                         has_border=False,
                         hover_focus=True)
        super().set_theme('bright')
        # Layouts
        header  = asc.Layout([100])
        main    = asc.Layout([3, 1], fill_frame=True)
        footer  = asc.Layout([1, 1])
        self.add_layout(header)
        self.add_layout(main)
        self.add_layout(footer)
        # Header widgets
        self._header_textbox = asc.TextBox(round(height * HEADER_SIZE),
                                          name='header', 
                                          readonly=True,
                                          as_string=True,
                                          disabled=True)
        self._header_textbox.value = msg.open_msg
        header.add_widget(self._header_textbox)
        # Main widgets
        self._unlock_listbox = asc.ListBox(asc.Widget.FILL_COLUMN,
                                           Model.unlocks,
                                           name='unlocks')
        self._unlock_listbox.disabled = True
        self._archives_listbox = asc.ListBox(asc.Widget.FILL_COLUMN,
                                             Model.archives,
                                             name = 'archives', 
                                             on_change=self._select,
                                             on_select=self._pick)
        main.add_widget(self._unlock_listbox, 1)
        main.add_widget(self._archives_listbox, 0)
        # Footer widgets
        self._quit_button   = asc.Button('Quit', self._quit)
        self._unlock_button = asc.Button('Unlock', self._pick)
        footer.add_widget(self._quit_button, 0)
        footer.add_widget(self._unlock_button, 1)
        self.fix()

    def update(self, frame):
        super().update(frame)
        Model.unlocks = current.list_unlocks()
        self._unlock_listbox.options = Model.unlocks

    def _reload_archives(self, option=None):
        self._archives_listbox.options = Model.archives
        self._archives_listbox.value = option


    def _select(self):
        self._unlock_button.disabled = self._archives_listbox.value is None

    def _pick(self):
        self.save()
        Model.curr_archive = self._archives_listbox.value
        raise asc_ex.NextScene('Unlock Archive')

    @staticmethod
    def _quit():
        raise asc_ex.StopApplication('Quitting...')


class UnlockView(asc.Frame):
    def __init__(self, screen):
        height, width = screen.dimensions
        super().__init__(screen, 
                         height, 
                         width, 
                         hover_focus=True, 
                         can_scroll=False)
        super().set_theme('bright')
        # Layouts
        main = asc.Layout([100], fill_frame=True)
        header = asc.Layout([100])
        footer = asc.Layout([1, 1, 1])
        self.add_layout(header)
        self.add_layout(main)
        self.add_layout(footer)
        # Header
        self._header_text = asc.TextBox(round(height * HEADER_SIZE), 
                                        readonly=True, 
                                        name='header', 
                                        disabled=True, 
                                        as_string=True)
        self._header_text.value = msg.archive_chosen.format(Model.curr_archive)
        header.add_widget(self._header_text)
        # Main
        self._password_text = asc.Text(label='Password: ', name='password')
        main.add_widget(self._password_text)
        # Footer
        self._force_def_button = asc.Button('Force default keys', 
                                            self._force_public)
        self._force_key_button = asc.Button('Force chosen key', 
                                            self._force_private)
        self._back_button = asc.Button('Back', self._back)
        footer.add_widget(self._force_def_button, 0)
        footer.add_widget(self._force_key_button, 1)
        footer.add_widget(self._back_button, 2)
        self.fix()

    def reset(self):
        super().reset()
        self._header_text.value = msg.archive_chosen.format(Model.curr_archive)

    def _force(self, with_password=False):
        success = None
        self._header_text.value = msg.archive_chosen.format(Model.curr_archive)
        self._force_def_button.disabled = True
        self._force_key_button.disabled = True
        self._back_button.disabled      = True
        if not with_password:
            self._header_text.value += '\n' + \
                msg.archive_try_key_default.format(Model.curr_archive)
            success = current.force(Model.curr_archive)
        else:
            password = self._password_text.value.lower()
            self._header_text.value += '\n' + \
                msg.archive_try_key_private.format(Model.curr_archive, password)
            success = current.force(Model.curr_archive, password)
        if success:
            self._header_text.value += '\n' + msg.archive_decrypt_success
            self._header_text.value += '\n' + msg.archive_decrypt_reminder
        else:
            self._header_text.value += '\n' + msg.archive_decrypt_fail
        self._force_def_button.disabled = False
        self._force_key_button.disabled = False
        self._back_button.disabled      = False

    def _force_private(self):
        self._force(True)

    def _force_public(self):
        self._force()

    @staticmethod
    def _back():
        raise asc_ex.NextScene('Main')


def iter(screen, scene):
    scenes = [                                                   \
        Scene([ArchiveView(screen)], -1, name='Main'),           \
        Scene([UnlockView(screen)], -1, name='Unlock Archive')   \
    ]

    screen.play(scenes, stop_on_resize=True, start_scene=scene, allow_int=True)


        



        

        
