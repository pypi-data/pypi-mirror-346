import unittest

from sql_query_builder import SQLQueryBuilder


class TestSQLQueryBuilder(unittest.TestCase):
    def test_select_specific_columns(self):
        query = SQLQueryBuilder().select('id', 'name', 'email').from_table('users').build()
        self.assertEqual(query, 'SELECT id, name, email FROM users')

    def test_select_with_where(self):
        query = SQLQueryBuilder().select('*').from_table('users').where("age > 21").build()
        self.assertEqual(query, 'SELECT * FROM users WHERE age > 21')

    def test_select_with_multiple_conditions(self):
        query = SQLQueryBuilder().select('*').from_table('users').where("age > 21").and_where("city = 'New York'").build()
        self.assertEqual(query, "SELECT * FROM users WHERE age > 21 AND city = 'New York'")

    def test_left_join_query(self):
        query = SQLQueryBuilder().select('name', 'email').from_table('users').left_join('orders', 'users.id = orders.user_id').build()
        self.assertEqual(query, 'SELECT name, email FROM users LEFT JOIN orders ON users.id = orders.user_id')

    def test_right_join_query(self):
        query = SQLQueryBuilder().select('name', 'email').from_table('users').right_join('orders', 'users.id = orders.user_id').build()
        self.assertEqual(query, 'SELECT name, email FROM users RIGHT JOIN orders ON users.id = orders.user_id')

    def test_inner_join_query(self):
        query = SQLQueryBuilder().select('name', 'email').from_table('users').inner_join('orders', 'users.id = orders.user_id').build()
        self.assertEqual(query, 'SELECT name, email FROM users INNER JOIN orders ON users.id = orders.user_id')

    def test_full_join_query(self):
        query = SQLQueryBuilder().select('name', 'email').from_table('users').full_join('orders', 'users.id = orders.user_id').build()
        self.assertEqual(query, 'SELECT name, email FROM users FULL JOIN orders ON users.id = orders.user_id')

    def test_group_by_query(self):
        query = SQLQueryBuilder().select('name', 'age').from_table('users').group_by('age').build()
        self.assertEqual(query, 'SELECT name, age FROM users GROUP BY age')

    def test_order_by_query(self):
        query = SQLQueryBuilder().select('name', 'age').from_table('users').order_by('age').build()
        self.assertEqual(query, 'SELECT name, age FROM users ORDER BY age')

    def test_limit_query(self):
        query = SQLQueryBuilder().select('*').from_table('users').limit(10).build()
        self.assertEqual(query, 'SELECT * FROM users LIMIT 10')

    def test_in_clause_query(self):
        query = SQLQueryBuilder().select('*').from_table('users').in_clause('age', 21, 22, 23).build()
        self.assertEqual(query, 'SELECT * FROM users WHERE age IN (21, 22, 23)')


if __name__ == '__main__':
    unittest.main()
