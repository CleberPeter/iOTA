"""
Implementation of manifest function from IOTA framework.
"""
import os
import json
import ubinascii
from security import Security 

class Manifest:
    """
        initialize manifest class

        Args:
            _next_partition_name (string): attached to the manifest to determine which
                                           partition should be booted after the upgrade
            _pubkey (string): public key from server.
            _debug (boolean, optional): enable debug from class. Default is True.
        Returns:
            object from class.
    """
    def __init__(self, _next_partition_name, _public_key=None, _debug=True):

        self.debug = _debug
        self.next_partition_name = _next_partition_name
        self.public_key = _public_key
        self.security = Security()
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

        self.new = dict() # clean

        if 'key' in _new_manifest_object: # secure version?
            self.new['key'] = _new_manifest_object['key']

        self.new['type'] = _new_manifest_object['type']
        self.new['files'] = _new_manifest_object['files'].copy() # update files is stored here!
        return True

    def save_new(self, _str):
        """
            set new manifest file.

            Args:
                _str (string): manifest in JWS format "data_in_b64.signature_in_b64".
            Returns:
                boolean indicating status of parsing.
        """

        _splitted = _str.split('.') 

        _data_b64 = _splitted[0]
        _data_bytes = ubinascii.a2b_base64(_data_b64)
        _data_str = _data_bytes.decode('utf-8')

        self.print_debug('message: ' + _data_str)

        if len(_splitted) > 1: # was signed ?

            _sign_b64 = _splitted[1]
            _sign_json_str = ubinascii.a2b_base64(_sign_b64).decode('utf-8')

            self.print_debug('signature_json: ' + _sign_json_str)

            try:
                _sign_object = json.loads(_sign_json_str)

                if "sign" in _sign_object:
                    _sign_str = _sign_object['sign']

                    self.security.sha256_update(_data_bytes)
                    _hash = self.security.sha256_ret()

                    if not self.security.ecdsa_secp256k1_verifiy_sign(self.public_key, _hash, _sign_str):
                        self.print_debug("signature verify failed.")
                        return False
                    else:
                        self.print_debug("signature verification successfully.")

                else:
                    self.print_debug("error. sign object.")
                    return False

            except Exception as err:
                print(err)
                self.print_debug("error. signature verify.")
                return False
        
        
        try:
            _manifest_object = json.loads(_data_str)

        except ValueError:
            self.print_debug("error. invalid manifest file.")
            return False
        
        # is for this device and is the desired version ?
        if _manifest_object['uuidProject'] == self.uuid_project and \
           _manifest_object['version'] == self.get_next_version():

            # TODO: check others informations like dateExpiration
            if _manifest_object['type'] == "bin":

                # sets parition wich must be booted after upgrade
                # used to verify sucessfull of upgrade
                _manifest_object['ota'] = self.next_partition_name

                return self.save(_manifest_object)
                
            elif _manifest_object['type'] == "py":
                return self.save(_manifest_object)
        
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
    