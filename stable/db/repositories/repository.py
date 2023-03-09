import sqlite3
from datetime import datetime
from typing import Any, Tuple, Optional

class Repository:
    def __init__(self, table_name: str, columns: "dict[str, str]", db_path: str = "db/sql.db") -> None:
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        self.table_name = table_name
        self.columns = columns
        self._create_table()

    def _create_table(self) -> None:
        columns_str = ", ".join([f"{col} {self.columns[col]}" for col in self.columns])

        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {self.table_name} ({columns_str})")
        self.connection.commit()

    def _add_row(self, item: "dict[str, Any]") -> None:
        columns_str = ", ".join([col for col in self.columns])
        placeholders_str = ", ".join(["?" for col in self.columns])
        values = tuple([item.get(col, None) for col in self.columns])

        self.cursor.execute(f"""
            INSERT INTO {self.table_name} ({columns_str})
            VALUES ({placeholders_str})
        """, values)
        self.connection.commit()

    def _get_by_id(self, id: int) -> Optional[Any]:
        self.cursor.execute(f"""
            SELECT * FROM {self.table_name} WHERE id=?
        """, (id,))

        row = self.cursor.fetchone()
        if row:
            return self.__tuple_to_dict(row)
        
        return None

    def _get_all(self) -> "list[Any]":
        self.cursor.execute(f"""
            SELECT * FROM {self.table_name}
        """)
        rows = self.cursor.fetchall()
        return [self.__tuple_to_dict(row) for row in rows]
    
    def _find_by_column(self, column: str, value: str):
        self.cursor.execute(f"""
            SELECT * FROM {self.table_name} WHERE {column}='{value}'
        """)
        self.connection.commit()
        row = self.cursor.fetchone()
        return self.__tuple_to_dict(row) if row != None else None

    def _delete_by_id(self, id: int) -> None:
        self.cursor.execute(f"""
            DELETE FROM {self.table_name} WHERE id=?
        """, (id,))
        self.connection.commit()

    def __tuple_to_dict(self, row: Tuple[Any]) -> Any:
        item = type("Item", (object,), {})
        for i, col in enumerate(self.columns):
            setattr(item, col, row[i])
        return item

    def _timestamp(self):
        return str(datetime.utcnow())

    def _close(self) -> None:
        self.connection.close()
