# @Author: Dr. Jeffrey Chijioke-Uche
# @Copyright (c) 2024-2025 Dr. Jeffrey Chijioke-Uche, All Rights Reserved.
# @Coprited by: U.S Copyright Office
# @Date: 2024-03-01
# @Last Modified by: Dr. Jeffrey Chijioke-Uche    
# @Last Modified time: 2025-05-09
# @Description: This module provides a connector to IBM Quantum devices using Qiskit Runtime Service.
# @License: Apache License 2.0 and creative commons license 4.0
# @Purpose: Software designed for Pypi package for Quantum Plan Backend Connection IBMBackend QPUs Compute Resources Information
#_________________________________________________________________________________
import os
import warnings
import requests
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv, find_dotenv
from qiskit_ibm_runtime import QiskitRuntimeService, IBMBackend

# ───────────────────────────────────────────────────────────────────────────────
# Constants for output formatting
# ───────────────────────────────────────────────────────────────────────────────
HEADER_LINE = "=" * 82
SUBHEADER_LINE = "-" * 82
HEADER_1 = "\n⚛️ Quantum Plan Backend Connection IBMBackend QPUs Compute Resources Information:"
EMPTY_NOTICE = "⚛️ [QPU EMPTY RETURN NOTICE]:"

# ───────────────────────────────────────────────────────────────────────────────
# Functions to load environment variables
# ───────────────────────────────────────────────────────────────────────────────
def _load_environment():
    load_dotenv()
    path = find_dotenv(usecwd=True)
    if path:
        load_dotenv(path, override=True)
    else:
        home = Path.home() / '.env'
        if home.is_file():
            load_dotenv(home, override=True)

# ───────────────────────────────────────────────────────────────────────────────
# Functions to get the plan and credentials
# ───────────────────────────────────────────────────────────────────────────────
def _get_plan():
    _load_environment()
    flags = {
        'open':      os.getenv('OPEN_PLAN','off').strip().lower()=='on',
        'standard':  os.getenv('STANDARD_PLAN','off').strip().lower()=='on',
        'premium':   os.getenv('PREMIUM_PLAN','off').strip().lower()=='on',
        'dedicated': os.getenv('DEDICATED_PLAN','off').strip().lower()=='on',
    }
    if sum(flags.values())!=1:
        raise ValueError('⛔️ Exactly one of OPEN_PLAN, STANDARD_PLAN, PREMIUM_PLAN or DEDICATED_PLAN must be set to on')
    key = next(k for k,v in flags.items() if v)
    name = os.getenv(f'{key.upper()}_PLAN_NAME','').strip()
    if not name:
        raise ValueError(f'⛔️ {key.upper()}_PLAN_NAME must be set when {key.upper()}_PLAN is on')

    if key == 'open':
        tag = 'Open Plan'
    else:
        tag = 'Paid Plan'

    return key, name, tag

# ───────────────────────────────────────────────────────────────────────────────
# Functions for saving account and listing backends
# ───────────────────────────────────────────────────────────────────────────────
def _get_credentials(key):
    k = key.upper()
    return {
        'name':     os.getenv(f'{k}_PLAN_NAME','').strip(),
        'channel':  os.getenv(f'{k}_PLAN_CHANNEL','').strip(),
        'instance': os.getenv(f'{k}_PLAN_INSTANCE','').strip(),
        'token':    os.getenv('IQP_API_TOKEN','').strip()
    }

# ───────────────────────────────────────────────────────────────────────────────
# Functions to memorize account and list backends
# ───────────────────────────────────────────────────────────────────────────────
def save_account():
    key,name,human = _get_plan()
    cred = _get_credentials(key)
    if not all([cred['channel'],cred['instance'],cred['token']]):
        print(f"⛔️ Missing credentials for {human}.")
        return
    try:
        QiskitRuntimeService.save_account(
            channel=cred['channel'], token=cred['token'],
            instance=cred['instance'], name=cred['name'],
            set_as_default=True, overwrite=True, verify=True
        )
        print(f"\n✅ Saved {human} account → instance {cred['instance']}\n")
    except Exception as e:
        print(f"⛔️ Failed to save account for {human}: {e}")

# ───────────────────────────────────────────────────────────────────────────────
# Function to list backends
# ───────────────────────────────────────────────────────────────────────────────
def list_backends():
    key,_,human = _get_plan()
    _load_environment()
    with warnings.catch_warnings():
        warnings.filterwarnings('ignore',category=DeprecationWarning)
        service = QiskitRuntimeService()
    names = [b.name for b in service.backends()]
    print(SUBHEADER_LINE)
    print(f"⚛️ Available QPUs ({human}):")
    for n in names:
        print(f" - {n}")
    print(SUBHEADER_LINE + "\n")

# ───────────────────────────────────────────────────────────────────────────────
# Class to connect to Qiskit Runtime Service
# ───────────────────────────────────────────────────────────────────────────────
class QConnectorV2:
    def __new__(cls):
        key,name,human = _get_plan()
        _load_environment()
        with warnings.catch_warnings():
            warnings.filterwarnings('ignore',category=DeprecationWarning)
            service = QiskitRuntimeService()
        print(HEADER_LINE)
        print(f"\n⚛️ Connecting ({human}) to least-busy QPU...")
        print(SUBHEADER_LINE)
        if key=='open':
            backend = service.least_busy(
                simulator=False,
                operational=True,
                min_num_qubits=5)
        else:
            cred = _get_credentials(key)
            backend = service.least_busy(
                simulator=False, 
                operational=True,
                instance=cred['instance'],
                min_num_qubits=5
            )
        if not backend:
            raise RuntimeError(f"⛔️ No QPU available for {human}")
        qpus = service.backends(
            simulator=False, 
            operational=True,
            min_num_qubits=5,
        )
        print(f"⚛️ Connected [{human}] → Realtime Least Busy QPU:: [{backend.name}]")
        for q in qpus:
            print(f"- {q.name}")
        print("\n")
        print(f"🖥️ Least Busy QPU Now: [{backend.name}]")
        print(f"🖥️ Version: {getattr(backend,'version','N/A')}")
        print(f"🖥️ Qubits Count: {getattr(backend,'num_qubits','N/A')}")
        print(f"🖥️ Backend [{backend.name}] ready for use: Yes")
        print(HEADER_LINE + "\n")
        return backend

# ───────────────────────────────────────────────────────────────────────────────
# Class to get the Qiskit Runtime Service plan
# ───────────────────────────────────────────────────────────────────────────────
class QPlanV2:
    def __new__(cls):
        _,_,human = _get_plan()
        return human

# ───────────────────────────────────────────────────────────────────────────────
# Footer function to display copyright information
# ───────────────────────────────────────────────────────────────────────────────
def footer():
    year = datetime.today().year
    print(HEADER_LINE)
    print(f"Software Design by: Dr. Jeffrey Chijioke-Uche , IBM Quantum Ambassador ©{year}\n")
    print("⚛️ Copyright (c) 2025 Dr. Jeffrey Chijioke-Uche, All Rights Reserved.")
    print("⚛️ Copyrighted by: U.S Copyright Office")
    print("⚛️ Licensed under Apache License 2.0 and creative commons license 4.0")
    print("⚛️ Ownership & All Rights Reserved.\n")