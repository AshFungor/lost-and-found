# System imports
import pickle
import sys
import os

class Env():
    # Initial values
    # Default key (used to open first archive)
    main_key =      b'SCacvTazGALipT1MpEeaPf0X4xHz6OPNKXWiy8BUrSI='
    # Salts
    archives =      {'intro.encrypted'              : b'/\x04\x1bN\xba\xd3\x07\xbb\xee\x88\x17\x0cd=\xdd\xfe'   , 
                    'stars_are_right.encrypted'     : b'?\xdc\xb4\xf8v\xa1\r\x89\x1d\x1f7\x01\x9c\t\xad\xe0'    ,
                    'luck_of_the_draw.encrypted'    : b')\xfa\x08\x0c/\xb1\xfb6f\x96\x8c8!E\xd1\xec'            ,
                    'last_message.encrypted'        : b',)\x9fx#\xc1\x9f\x8e\x82\xc5\xd9\x16c\x86\xf7\xfb'      ,
                    'DELETE_THIS.encrypted'         : b'\xd52\x10^\xb12\xcfW\x1b;G\xf5\xd7r\xe0\xac'            }
    # Unlocked archives (False for closed)
    unlocks =       {'intro.encrypted'              : False,
                    'stars_are_right.encrypted'     : False,
                    'luck_of_the_draw.encrypted'    : False,
                    'last_message.encrypted'        : False,
                    'DELETE_THIS.encrypted'         : False}
    settings =      'config.pkl'


    def __new__(cls, *args, **kwargs):
        abs_settings = Env.extend_path_exe(Env.settings)
        if os.path.exists(abs_settings):
            settings_file = open(abs_settings, 'rb')
            inst = pickle.load(settings_file)
            inst.loaded = True
            settings_file.close()
            return inst
        return super().__new__(cls, *args, **kwargs)

    def __init__(self):
        if not hasattr(self, 'loaded'):
            # Initialize with defaults
            self.main_key = Env.main_key
            self.archives = Env.archives
            self.unlocks = Env.unlocks

    def save(self):
        abs_settings = Env.extend_path_exe(Env.settings)
        settings_file = open(abs_settings, 'wb')
        pickle.dump(self, settings_file, pickle.HIGHEST_PROTOCOL)
        settings_file.close()
    
    @staticmethod
    def check_state():
        if not hasattr(sys, 'frozen'):
            raise AttributeError(
                'Application is not bundled, it should be run packaged')
        return True

    @staticmethod
    def extend_path_pkg(original_path):
        return sys._MEIPASS + '/' + original_path

    @staticmethod
    def extend_path_exe(original_path):
        return os.path.dirname(sys.executable) + original_path

Env.check_state()
# Current config 
settings = Env()


