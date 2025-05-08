import unittest
from pathlib import Path
from time import sleep

from sqlmodel import select

from commons.database import FileDatabaseMigrationExecutor, DatabaseAdapter, Cache
from commons.logging import getLogger
from tests import TestUser

RESOURCES_FOLDER: Path = Path(__file__).parent / "resources"


class TestDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.logger = getLogger(cls)

    def test_database_creation(self):
        self.assertIsNotNone(Cache().database)
        self.assertIsNotNone(Cache().database.engine())
        self.assertEqual(Cache().database, Cache().database)

        with Cache().database.session() as session:
            self.assertIsNotNone(session)
            session.close()

    def test_migration_files(self):
        from tests import TestUser
        from commons.database import FileMigration

        db: DatabaseAdapter = DatabaseAdapter()
        db.create_tables([TestUser, FileMigration])
        with db.session() as session:
            self.assertIsNotNone(FileDatabaseMigrationExecutor(path=RESOURCES_FOLDER / "migrations", session=session).run())
            self.assertIsNotNone(session.exec(select(TestUser).where(TestUser.username == "john.doe")).first())
            self.assertIsNotNone(session.exec(select(TestUser).where(TestUser.username == "joana.doe")).first())
            session.close()

    def test_cache_expiration(self):
        with Cache() as cache:
            key = "key"
            value = b"value"
            entry = cache.set(key, value, max_age=1)

            self.assertIsNotNone(entry)
            self.assertFalse(entry.expired)
            self.assertEqual(b"value", cache.get(key).data)

            sleep(1)

            self.assertTrue(entry.expired)
            cache.invalidate(key)
            self.assertIsNone(cache.get(key))

    def test_cache_multiple_inputs(self):
        inputs = [
            (b"\x00", bytes),
            ("string", str),
            (True, bool),
            (False, bool),
            (1, int),
            (1.200000000000001, float),
            ({"k": "v"}, dict),
            (TestUser(username="abc"), TestUser)
        ]

        with Cache() as cache:
            key = "key"

            for v, t in inputs:
                self.logger.debug(f"Testing Cache with value <{str(v):<20}> ({t})")
                cache.set(key, v)
                self.assertEqual(v, cache.get(key).get(t))

    def test_async_db(self):
        import asyncio
        async def _inner_func():
            return DatabaseAdapter().engine()

        self.assertEqual(str(DatabaseAdapter().engine()), str(asyncio.run(_inner_func())))

