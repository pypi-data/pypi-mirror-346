import asyncio
import json
from datetime import datetime, timedelta
from typing import Optional, TypeVar

from pydantic import computed_field, BaseModel
from sqlalchemy import inspect
from sqlmodel import SQLModel, Field, Session, select

from commons.database import DatabaseAdapter

Data = TypeVar("Data", bytes, str, bool, int, float, dict, BaseModel)


class CacheEntry(SQLModel, table=True):
    __tablename__ = "cache"
    id: str = Field(nullable=False, primary_key=True)
    data: bytes | None = Field(nullable=True)
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
    max_age: int = Field(default=300, nullable=False)

    @computed_field
    @property
    def expires(self) -> datetime:
        return self.created_at + timedelta(seconds=self.max_age)

    @computed_field
    @property
    def expired(self) -> bool:
        return bool(datetime.now() >= self.expires)

    # noinspection PyTypeChecker
    def set(self, value: Data):
        """
        Set entry data with bytes-encoded value.

        :param value: value to be persisted in the cache.
        """
        if type(value) == bytes:
            self.data = value
        elif type(value) == dict:
            self.data = json.dumps(value).encode()
        elif type(value) == str:
            self.data = value.encode()
        elif type(value) in [bool, int]:
            self.data = value.to_bytes()
        elif type(value) == float:
            import struct
            try:
                self.data = struct.pack("d", value)
            except struct.error:
                raise ValueError(f"Encoding Error: b'{value}' is not a floating point.")
        elif issubclass(type(value), BaseModel):
            self.data = value.model_dump_json().encode()
        else:
            raise ValueError(f"Encoding Error: not a valid type.")

    def get(self, astype: Data = bytes) -> Optional[Data]:
        """
        Get the raw binary data of the entry and optionally converts to a Data type.

        Data type can be: bytes, str, bool, int, float, dict or a subclass of pydantic.BaseModel

        :param astype: data type to convert the raw binary
        """
        if self.data:
            if astype == bytes:
                return self.data
            elif astype == dict:
                return json.loads(self.data)
            elif astype == str:
                return self.data.decode()
            elif astype == bool:
                return bool.from_bytes(self.data)
            elif astype == int:
                return int.from_bytes(self.data)
            elif astype == float:
                import struct
                try:
                    return struct.unpack("d", self.data)[0]
                except struct.error:
                    raise ValueError(f"Error to decode bytes: b'{self.data}' is not a floating point.")
            elif issubclass(astype, BaseModel):
                # noinspection PyCallingNonCallable
                return astype(**json.loads(self.data.decode()))
            else:
                raise ValueError(f"Decoding Error: invalid type.")


class Cache:
    database: DatabaseAdapter
    session: Optional[Session] = None

    def __init__(self, database: DatabaseAdapter = DatabaseAdapter()):
        self.database = database

        if not inspect(database.engine()).has_table("cache"):
            SQLModel.metadata.tables["cache"].create(database.engine())

    # noinspection PyTypeChecker
    def get(self, key: str) -> Optional[CacheEntry]:
        entry: CacheEntry = self.session.exec(select(CacheEntry).where(CacheEntry.id == key)).first()

        if entry:
            if entry.expired:
                self.invalidate(entry)
            else:
                return entry

    def set(self, key: str, value: Data, max_age: int = 300) -> CacheEntry:
        entry = CacheEntry(id=key, max_age=max_age)
        entry.set(value)

        self.invalidate(key)
        self.session.add(entry)
        self.session.commit()

        return entry

    def invalidate(self, key: str | CacheEntry):
        entry = key if (type(key) == CacheEntry) else self.get(key)
        if entry:
            self.session.delete(entry)

    def __enter__(self):
        self.session = self.database.session()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
        self.session = None
