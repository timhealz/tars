import logging
log = logging.getLogger(__name__)

from sqlalchemy import MetaData

from tars.db.utils import get_db_engine


class Insert():
    def __init__(self, database: str, table: str):
        self.db_engine = get_db_engine(database=database)
        metadata = MetaData(bind=self.db_engine, reflect=True)
        self.table = metadata.tables[table]

    def load(self, data: dict) -> None:
        ins = self.table.insert().values(**data)
        result = self.db_engine.execute(ins)

        result.close()
