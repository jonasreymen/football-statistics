import os
from sqlalchemy.orm.session import Session
from app.sync.storage.storage import Storage
from typing import List

class databaseStorage(Storage):
    def __init__(self, session: Session) -> None:
        self.session = session
    
    def update(self, obj: List[object]) -> None:
        self.session.add(obj)
        self.session.commit()

    def insert(self, obj: List[object]) -> None:
        self.session.add(obj)
        self.session.commit()