# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()
import os
import json
from esp32 import Partition

"""
    if necessary, the manifest will be updated to new manifest present in
    _manifest.json file.
"""

_updated = False
files = os.listdir()

if '_manifest.json' in files: # have an new manifest ? make upgrade

    _manifest_file = open('_manifest.json', 'r')
    _manifest_str = _manifest_file.read()
    _manifest_file.close()

    try:
        _manifest_object = json.loads(_manifest_str)

        if _manifest_object['type'] == 'bin':
            
            print('monolithic upgrade identified.')
            
            _current_partition = Partition(Partition.RUNNING)
            if _manifest_object['ota'] == _current_partition.info()[4]: # changed ota partition ?
                
                os.rename("_manifest.json", "manifest.json")
                print('update with success.')
                _updated = True
            else:
                print('failed to update.')
                os.remove('_manifest.json')
        else:

            print('diferential upgrade identified.')

            for file in files:
                if file[0] == '_': # is an update file (_xxx)
                    os.rename(file, file[1:]) # rename: _xxx -> xxx

            print('update with success.')
            _updated = True

    except ValueError:
        print("error. invalid manifest file.")
        os.remove('_manifest.json')

else:
    print('manifest already up to date.')

    for file in files: # removes garbage
        if file[0] == '_': # is an update file (_xxx)
            os.remove(file) 



if _updated:
    update_file = open('_updated.iota', 'x') # signal an update to occur 
    update_file.close()