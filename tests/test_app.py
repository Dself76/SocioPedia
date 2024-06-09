import unittest
from unittest.mock import patch, MagicMock
import os
import mysql.connector
from mysql.connector import errorcode


from app import get_db_connection


class TestDatabaseConnection(unittest.TestCase):
    @patch('mysql.connector.connect')
    @patch('os.getenv')
    def test_get_db_connection_success(self, mock_getenv, mock_connect):

        mock_getenv.side_effect = ['localhost', 'user', 'password', 'mydb']

        # Mock database connection check to connect, it already connect before test so if it doesnt connect check test
        connection = MagicMock()
        mock_connect.return_value = connection

        # Test the connection
        conn = get_db_connection()
        self.assertIsNotNone(conn)
        mock_connect.assert_called_with(
            host='localhost',
            user='user',
            password='password',
            database='mydb',
            auth_plugin='caching_sha2_password'
        )

    @patch('mysql.connector.connect')
    @patch('os.getenv')
    def test_get_db_connection_failure(self, mock_getenv, mock_connect):
        # Set up mock environment variables
        mock_getenv.side_effect = ['localhost', 'user', 'wrongpassword', 'mydb']

        # Simulate connection error
        mock_connect.side_effect = mysql.connector.Error(errno=errorcode.ER_ACCESS_DENIED_ERROR)

        # Test the connection
        conn = get_db_connection()
        self.assertIsNone(conn)
        print("Error: Something is wrong with your username or password")


# Run the tests
if __name__ == '__main__':
    unittest.main()
