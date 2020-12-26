import logging
log = logging.getLogger(__name__)

import json
import os
from argparse import ArgumentParser
from pathlib import Path
from typing import Dict


def read_json_to_dict(json_fp:str) -> Dict:
    with open(json_fp, "r") as f:
        data = json.load(f)

    return data

def write_data_to_json(data:Dict, json_fp:str) -> None:
    
    Path(os.path.dirname(json_fp)).mkdir(
        parents=True,
        exist_ok=True
    )

    with open(json_fp, 'w') as f:
        json.dump(data, f, indent=4)