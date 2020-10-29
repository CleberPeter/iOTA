"""
Implementation of manifest function from IOTA framework.
"""
import os
import json

class Manifest:
    """
        initialize manifest class

        Args:
            _next_partition_name (string): attached to the manifest to determine which
                                           partition should be booted after the upgrade
            _debug (boolean, optional): enable debug from class. Default is True.
        Returns:
            object from class.
    """
    def __init__(self, _next_partition_name, _debug=True):

        self.debug = _debug
        self.next_partition_name = _next_partition_name
        self.uuid_project = ''
        self.version = 0
        self.date_expiration = ''
        self.type = ''
        self.new = {}

    def load(self, _uuid_project, _version):
        """
            the manifest will be loaded from the last downloaded manifest or a default
            manifest will be created with the uuid of project and version passed
            as a parameter by the user.

            _uuid_project (string): universal unique id from project to create default manifest
                                (only used if not exists an local manifest).
            _version (integer): current version of device to create a default manifest
                            (only used if not exists an local manifest).
            Returns:
                void
        """

        files = os.listdir()

        # create default manifest, if necessary. (only in first execution)
        if not 'manifest.json' in files:
            _manifest_file = open('manifest.json', 'x')
            _manifest_str = self.get_default(_uuid_project, _version)
            _manifest_file.write(_manifest_str)
            _manifest_file.close()
        
        _manifest_file = open('manifest.json', 'r')
        _manifest_str = _manifest_file.read()
        _manifest_file.close()

        self.fill(_manifest_str) # load manifest
        self.print_debug("current manifest:\n" + _manifest_str)

    def save(self, _new_manifest_object):
        """
            saves the new manifest file to the file system.
            NOT update the RAM manifest.

            Args:
                _new_manifest_str (object): manifest in dict format.
            Returns:
                boolean indicating success of operation.
        """
        try:
            _new_manifest_str = json.dumps(_new_manifest_object)
        except ValueError:
            self.print_debug("error. invalid manifest file.")
            return False

        _manifest_file = open('_manifest.json', 'x')
        _manifest_file.write(_new_manifest_str)
        _manifest_file.close()

        #TODO: check this question!
        # self.load(_new_manifest_str) # for now, only reloads manifest in RAM after reboot.

        self.new['type'] = _new_manifest_object['type']
        self.new['files'] = _new_manifest_object['files'].copy() # update files is stored here!
        return True

    def save_new(self, _str):
        """
            set new manifest file:
                {
                    "uuidProject": "1",
                    "version": 14,
                    "type": "bin",
                    "dateExpiration": "2020-06-05",
                    "files": [
                        {
                        "name": "firmware",
                        "size": 1376016
                        }
                    ]
                }

            Args:
                _str (string): manifest file in string format.
            Returns:
                boolean indicating status of parsing.
        """
        _sign = False
        try:
            _manifest_object = json.loads(_str)

            if "signature" in _manifest_object: # secure version
                _sign = _manifest_object['signature']
                print("signature: ", _sign)

                print(_str)

        except ValueError:
            self.print_debug("error. invalid manifest file.")
            return False

        # is for this device and is the desired version ?
        """if _manifest_object['uuidProject'] == self.uuid_project and \
           _manifest_object['version'] == self.get_next_version():

            # TODO: check others informations like dateExpiration
            if _manifest_object['type'] == "bin":

                # sets parition wich must be booted after upgrade
                # used to verify sucessfull of upgrade
                _manifest_object['ota'] = self.next_partition_name

                return self.save(_manifest_object)
                
            elif _manifest_object['type'] == "py":
                return self.save(_manifest_object)
        """
        return False

    def fill(self, _manifest_str):
        """
            fill manifest object from string.

            Args:
                _manifest_str (string): manifest file in string format.
            Returns:
                boolean indicating loading status.
        """
        try:
            _manifest_object = json.loads(_manifest_str)
            self.uuid_project = _manifest_object['uuidProject']
            self.version = _manifest_object['version']
            self.date_expiration = _manifest_object['dateExpiration']
            self.type = _manifest_object['type']
        except ValueError:
            raise ValueError("can't fill manifest file.")

    def get_default(self, _uuid_project, _version):
        """
            returns default manifest file with _uuid_project and _version provided.

            Args:
                _uuid_project (string): universal unique id from project.
                _version (integer): Current version of device.
            Returns:
                string with minimal manifest.
        """
        _default_manifest = '{"uuidProject":"' + _uuid_project + '", "version":' + str(_version)
        _default_manifest += ', "dateExpiration": "", "type": ""'
        _default_manifest += ', "files": [{"name": "", "size": 0}]}'

        return _default_manifest

    def get_next_version(self):
        """
            returns the new version based on the standard established
            by IOTA framework for version management.

            Args:
                void.
            Returns:
                integer with new version.
        """
        return self.version+1

    def print_debug(self, _message):
        """
            print debug messages.

            Args:
                _message (string): message to plot.
            Returns:
                void.
        """

        if self.debug:
            print('manifest: ', _message)
    