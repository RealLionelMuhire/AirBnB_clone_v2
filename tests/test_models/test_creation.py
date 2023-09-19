#!/usr/bin/python3

import unittest
import MySQLdb


class TestStateCreation(unittest.TestCase):
    def setUp(self):
        self.db = MySQLdb.connect(host="localhost", user="hbnb_test",
                                  passwd="hbnb_test_pwd", db="hbnb_test_db")

        self.cursor = self.db.cursor()

    def tearDown(self):
        self.cursor.close()    
        self.db.close()

    def create_state_record(self, name):
        query = "INSERT INTO states (name) VALUES (%s)"
        self.cursor.execute(query, (name,))
        self.db.commit()

    def test_create_state(self):
        self.cursor.execute("SELECT COUNT(*) FROM states")
        count_before = self.cursor.fetchone()[0]

        self.create_state_record("Calfornia")

        self.cursor.execute("SELECT COUNT(*) FROM states")
        count_after = self.cursor.fetchone()[0]

        self.assertEqual(count_after - count_before, 1)


if __name__ == '__main__':
    unittest.main()
