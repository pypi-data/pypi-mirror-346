from typing import List


class SQLQueryBuilder:
    def __init__(self):
        self.__query_segments: List[str] = []

    def build(self) -> str:
        return ' '.join(self.__query_segments)

    def select(self, *columns: str, distinct: bool = False) -> 'SQLQueryBuilder':
        columns_str = ', '.join(columns) if columns else '*'
        prefix = 'SELECT DISTINCT' if distinct else 'SELECT'
        self.__query_segments.append(f'{prefix} {columns_str}')
        return self

    def from_table(self, table: str) -> 'SQLQueryBuilder':
        self.__query_segments.append(f'FROM {table}')
        return self

    def where(self, condition: str) -> 'SQLQueryBuilder':
        self.__query_segments.append(f'WHERE {condition}')
        return self

    def left_join(self, table: str, on_condition: str) -> 'SQLQueryBuilder':
        self.__query_segments.append(f'LEFT JOIN {table} ON {on_condition}')
        return self

    def right_join(self, table: str, on_condition: str) -> 'SQLQueryBuilder':
        self.__query_segments.append(f'RIGHT JOIN {table} ON {on_condition}')
        return self

    def inner_join(self, table: str, on_condition: str) -> 'SQLQueryBuilder':
        self.__query_segments.append(f'INNER JOIN {table} ON {on_condition}')
        return self

    def full_join(self, table: str, on_condition: str) -> 'SQLQueryBuilder':
        self.__query_segments.append(f'FULL JOIN {table} ON {on_condition}')
        return self

    def group_by(self, *columns: str) -> 'SQLQueryBuilder':
        columns_str = ', '.join(columns)
        self.__query_segments.append(f'GROUP BY {columns_str}')
        return self

    def order_by(self, *columns: str) -> 'SQLQueryBuilder':
        columns_str = ', '.join(columns)
        self.__query_segments.append(f'ORDER BY {columns_str}')
        return self

    def limit(self, n: int) -> 'SQLQueryBuilder':
        self.__query_segments.append(f'LIMIT {n}')
        return self

    def insert_into(self, table: str, **columns: str) -> 'SQLQueryBuilder':
        column_names = ', '.join(columns.keys())
        values = ', '.join(f"'{v}'" for v in columns.values())
        self.__query_segments.append(f'INSERT INTO {table} ({column_names}) VALUES ({values})')
        return self

    def update(self, table: str, **columns: str) -> 'SQLQueryBuilder':
        set_clause = ', '.join(f"{k} = '{v}'" for k, v in columns.items())
        self.__query_segments.append(f'UPDATE {table} SET {set_clause}')
        return self

    def delete_from(self, table: str) -> 'SQLQueryBuilder':
        self.__query_segments.append(f'DELETE FROM {table}')
        return self

    def in_clause(self, column: str, *values: str) -> 'SQLQueryBuilder':
        values_str = ', '.join(str(v) for v in values)
        self.__query_segments.append(f'WHERE {column} IN ({values_str})')
        return self

    def and_where(self, condition: str) -> 'SQLQueryBuilder':
        self.__query_segments.append(f'AND {condition}')
        return self

    def or_where(self, condition: str) -> 'SQLQueryBuilder':
        self.__query_segments.append(f'OR {condition}')
        return self

    def having(self, condition: str) -> 'SQLQueryBuilder':
        self.__query_segments.append(f'HAVING {condition}')
        return self

    def on_conflict_do_nothing(self) -> 'SQLQueryBuilder':
        self.__query_segments.append('ON CONFLICT DO NOTHING')
        return self

    def offset(self, n: int) -> 'SQLQueryBuilder':
        self.__query_segments.append(f'OFFSET {n}')
        return self

    def values(self, *rows: List[str]) -> 'SQLQueryBuilder':
        rows_str = ', '.join(f"({', '.join(row)})" for row in rows)
        self.__query_segments.append(f'VALUES {rows_str}')
        return self

    def __str__(self) -> str:
        return self.build()

    def __repr__(self) -> str:
        return self.__str__()
