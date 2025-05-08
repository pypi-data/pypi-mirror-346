## SQLQuery

A simple Python class that enables you to build SQL queries using a fluent, chainable interface. This tool is perfect for developers who want to generate SQL statements programmatically without writing raw SQL strings manually.

---

### <ins> Features </ins>

- Intuitive, chainable API for building SQL queries
- Supports:
  - `SELECT`, `INSERT`, `UPDATE`, `DELETE`
  - `WHERE`, `AND`, `OR`, `IN`, `HAVING`, `GROUP BY`, `ORDER BY`
  - `JOIN`, `LEFT JOIN`, `RIGHT JOIN`, `FULL JOIN`, `INNER JOIN`
  - `LIMIT`, `OFFSET`, `ON CONFLICT DO NOTHING`
- Simple Python dependency — no external libraries
- Useful for prototyping, dynamic query generation, or learning SQL

---

### <ins> Installation </ins>

You can install this package via PIP: _pip install python=sql-query-builder_

### <ins> Usage </ins>

```python
from sql_query_builder import SQLQueryBuilder

query = (
    SQLQueryBuilder()
    .select('id', 'name', 'email', distinct=True)
    .from_table('users')
    .where("age > 21")
    .and_where("city = 'New York'")
    .order_by('name')
    .limit(10)
)

print(query.build())
# Output:
# SELECT DISTINCT id, name, email FROM users WHERE age > 21 AND city = 'New York' ORDER BY name LIMIT 10
```