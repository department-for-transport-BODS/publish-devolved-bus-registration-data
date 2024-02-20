import unittest
from utils.db import AutoMappingModels


class TestAutoMappingModels(unittest.TestCase):
    def setUp(self):
        self.auto_mapping = AutoMappingModels()

    def test_get_tables(self):
        expected_tables = {
            "EPRegistration": self.auto_mapping.EPRegistration,
            "OTCOperator": self.auto_mapping.OTCOperator,
            "OTCLicence": self.auto_mapping.OTCLicence,
        }
        actual_tables = self.auto_mapping.get_tables()
        self.assertEqual(actual_tables, expected_tables)


import unittest
from utils.db import MockData
from sqlalchemy.orm import Session


class TestAutoMappingModels(unittest.TestCase):
    def setUp(self):
        self.auto_mapping = AutoMappingModels()

    def test_get_tables(self):
        expected_tables = {
            "EPRegistration": self.auto_mapping.EPRegistration,
            "OTCOperator": self.auto_mapping.OTCOperator,
            "OTCLicence": self.auto_mapping.OTCLicence,
        }
        actual_tables = self.auto_mapping.get_tables()
        self.assertEqual(actual_tables, expected_tables)


class TestDBManager(unittest.TestCase):
    def setup_class(self):
        # Create sqlite3 database
        self.engine = "sqlite:///test.db"
        self.session = Session()
        self.tables = AutoMappingModels().get_tables()

        # Add tables to the new database
        AutoMappingModels().Base.metadata.create_all(self.engine)

        # self.valid_author = Author(
        #     firstname="Ezzeddin",
        #     lastname="Aybak",
        #     email="aybak_email@gmail.com"
        # )

    def test_add_record(self):
        # Add a record to the database
        record = MockData().get_mock_data()
        self.session.add(record)
        self.session.commit()

        # Get the record from the database
        result = self.session.query(self.tables["EPRegistration"]).first()

        # Assert that the record is the same as the one added
        self.assertEqual(result, record)

    def teardown_class(self):
        self.session.rollback()
        self.session.close()


if __name__ == "__main__":
    unittest.main()
