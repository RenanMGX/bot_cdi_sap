from typing import Dict
from getpass import getuser

default:Dict[str, Dict[str,object]] = {
    'credential': {
        'crd': 'SAP_PRD'
    },
    'log': {
        'hostname': 'Patrimar-RPA',
        'port' : 80,
        'token': ''
    }
}
