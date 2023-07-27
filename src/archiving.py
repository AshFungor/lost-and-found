# System imports
import os
import zipfile

# Crypto imports
import base64
import hashlib
from cryptography.fernet                        import Fernet
from cryptography.fernet                        import InvalidToken
from cryptography.hazmat.primitives             import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2  import PBKDF2HMAC

# Local imports
from environment import settings
from environment import Env

class ArchiveController():
    def __init__(self):
        archives = list(map(lambda archive: Env.extend_path_pkg(archive), 
                            settings.archives.keys()))
        self._salts     = settings.archives
        self._archives  = archives
        self._unlocks   = settings.unlocks
        self._main_key  = settings.main_key
    
    def list_archives(self):
        return [(os.path.basename(archive), os.path.basename(archive)) 
                for archive in self._archives]

    def force(self, target, password=None):
        res = None
        if password is None:
            res = self._decrypt_archive(Env.extend_path_pkg(target), 
                                        self._main_key)
        else:
            # convert to key first
            key = self._pass_to_key(password, self._salts[target])
            res = self._decrypt_archive(Env.extend_path_pkg(target), key)
        if res is None:
            return False
        self._unpack(res)
        settings.unlocks[target] = self._unlocks[target] = True
        settings.save()
        return True
    
    def _unpack(self, file):
        if not zipfile.is_zipfile(file):
            raise RuntimeError(f'{file} is not ZIP archive')
        zip_file = zipfile.ZipFile(file, 'r')
        zip_file.extractall(Env.extend_path_exe(''))
        zip_file.close()
        os.remove(file)

        
    def _pass_to_key(self, password, salt):
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), 
                         length=32, 
                         salt=salt, 
                         iterations=480_000)
        return base64.urlsafe_b64encode(kdf.derive(password.encode('UTF-8')))

    def _decrypt_archive(self, file, key):
        in_file = open(file, 'rb')
        out_filename = Env.extend_path_exe(os.path.basename(file))
        out_filename = out_filename.replace('.encrypted', '.zip')
        out_file = open(out_filename, 'wb')
        data = bytes()
        while True:
            block_size = int.from_bytes(in_file.read(16))
            if not block_size:
                break
            block = in_file.read(block_size)
            try:
                f = Fernet(key)
                output = f.decrypt(block)
            except InvalidToken:
                self._decrypt_archive_cleanup(in_file, out_file)
                os.remove(out_filename)
                return None
            out_file.write(output)
            data += output
        self._decrypt_archive_cleanup(in_file, out_file)
        return out_filename

    def _decrypt_archive_cleanup(self, in_file, out_file):
        in_file.close()
        out_file.close()
        
current = ArchiveController()