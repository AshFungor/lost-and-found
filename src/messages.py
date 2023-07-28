class MsgData:
    def __init__(self):
        # open messages
        self.open_msg =                 'This program is a property of LOST_AND_FOUND Inc., \n' \
                                        'do not attempt to share or steal this data, as this violation will be reported.'
        self.archive_try_key_default =  'Forcing retrieval on {} with default key...'
        self.archive_try_key_private =  'Forcing retrieval on {} with <{}> key...'
        self.archive_choose_key =       'Key entered: <{}>'
        self.archive_decrypt_success =  'Retrieval successful.'
        self.archive_decrypt_fail =     'Retrieval failed [INVALID_KEY], data was not extracted.'
        self.archive_decrypt_reminder = 'Check folder with this program for further details.'
        # opening archive
        self.archive_chosen =           'Processing data chunk {}'

msg = MsgData()
