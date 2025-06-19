from typing import List
from tqdm import tqdm

from app.sync.locator.locator import Locator
from app.sync.mapper.ObjectMapper import ObjectMapper
from app.sync.merger.merger import Merger
from app.sync.source.source import Source
from app.sync.storage.storage import Storage

class Synchronizer:
    def __init__(self,
            name: str,
            source: Source,
            mapper: ObjectMapper,
            locator: Locator,
            storage: Storage,
            merger: Merger
        ) -> None:
        self.name = name
        self.source = source
        self.mapper = mapper
        self.locator = locator
        self.storage = storage
        self.merger = merger
        self.to_insert: List[object] = []
        self.to_update: List[object] = []

    def sync(self) -> None:
        print(f"\n🔄 Starting sync for: {self.name}")
        raw_data_list = self.source.fetch_data()
        print(f"📥 Fetched {len(raw_data_list)} raw records.")

        for raw_data in tqdm(raw_data_list, desc=f"[{self.name}] Mapping & Matching", unit="record"):
            new_obj = self.mapper.map_to_object(raw_data)
            existing_obj = self.locator.locate(new_obj)

            if existing_obj:
                updated_obj = self.merger.merge(existing_obj, new_obj)
                self.to_update.append(updated_obj)
            else:
                self.to_insert.append(new_obj)
        
        self.apply_changes()

    def apply_changes(self) -> None:
        print(f"💾 Applying DB changes for: {self.name}")
        for obj in tqdm(self.to_update, desc=f"[{self.name}] Updating", unit="obj"):
            self.storage.update(obj)

        for obj in tqdm(self.to_insert, desc=f"[{self.name}] Inserting", unit="obj"):
            self.storage.insert(obj)

        print(f"✅ Sync complete for {self.name}. {len(self.to_update)} updated, {len(self.to_insert)} inserted.")