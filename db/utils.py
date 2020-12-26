import os
import yaml
from sqlalchemy import create_engine, engine

BASE_PATH = os.path.dirname(os.path.realpath(__file__))

def get_db_engine(database: str) -> engine.Engine:
    config_fp = os.path.join(BASE_PATH, 'config.yaml')
    with open(config_fp, 'r') as (f):
        config = yaml.load(f, Loader=yaml.FullLoader)
    
    db_engine = create_engine(config[database])

    return db_engine