"""
CRUD operations for SQLite storage.
"""
import json
import sqlite3
import uuid
import datetime
import re
from contextlib import contextmanager
from typing import Any, Dict, List, Optional, Union, Tuple, Iterator, NewType, Callable, Set

from storekiss.exceptions import DatabaseError, NotFoundError, ValidationError
from storekiss.validation import Schema

# 循環インポートを避けるために遅延インポート
_CollectionReference = None


class ServerTimestampSentinel:
    """
    LiteStoreの SERVER_TIMESTAMP に相当するセンチネル値。
    
    このオブジェクトをフィールド値として使用すると、ドキュメントの作成時または
    更新時に現在のサーバータイムスタンプに置き換えられます。
    """
    def __repr__(self):
        return "SERVER_TIMESTAMP"


SERVER_TIMESTAMP = ServerTimestampSentinel()


def quote_table_name(name: str) -> str:
    """
    テーブル名をSQLで使用するためにダブルクォートで囲みます。
    これにより、特殊文字や日本語などを含むテーブル名もそのまま使用できます。
    
    Args:
        name: 元のテーブル名
        
    Returns:
        SQLで使用するためのテーブル名（ダブルクォート付き）
    """
    # 空の場合はデフォルト名を使用
    if not name:
        return '"collection_default"'
    
    # ダブルクォートをエスケープ（""にする）
    escaped_name = name.replace('"', '""')
    
    # ダブルクォートで囲む
    return f'"{escaped_name}"'


class QueryOperator:
    """Base class for query operators."""
    
    def to_sql(self, field_path: str) -> Tuple[str, List[Any]]:
        """Convert this operator to SQL."""
        raise NotImplementedError


class DateTimeEncoder(json.JSONEncoder):
    """JSON encoder that can handle datetime objects and SERVER_TIMESTAMP."""
    
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        elif isinstance(obj, ServerTimestampSentinel):
            return datetime.datetime.now().isoformat()
        return super().default(obj)


class QueryBuilder:
    """
    A query builder for LiteStore.
    
    This class provides methods for building queries with a fluent interface
    similar to Google Cloud LiteStore.
    """
    
    def __init__(self, store, collection: str):
        self.store = store
        self.collection = collection
        self.filters = {}
        self._limit = None
        self._offset = 0
        self._order_by = None
        self._order_direction = "ASC"
    
    def where(self, field: str, op: str, value: Any) -> 'QueryBuilder':
        """
        Add a filter to the query.
        
        Args:
            field: Field name to filter by.
            op: Operator to use for filtering ("==", "!=", ">", "<", ">=", "<=").
            value: Value to filter for.
            
        Returns:
            A QueryBuilder for chaining.
        """
        # デバッグ出力
        print(f"\nQueryBuilder.whereメソッドが呼び出されました")
        print(f"field: {field}, op: {op}, value: {value}")
        
        # filtersをタプルのリストとして管理するように変更
        if not hasattr(self, '_filters_list'):
            self._filters_list = []
        
        # フィルタをタプルとして追加
        self._filters_list.append((field, op, value))
        print(f"filters_list: {self._filters_list}")
        
        return self
    
    def order_by(self, field: str, direction: str = "ASC") -> 'QueryBuilder':
        """Order results by a field."""
        self._order_by = field
        self._order_direction = direction
        
        # デバッグ出力
        print(f"\norder_byメソッドが呼び出されました")
        print(f"field: {field}, direction: {direction}")
        print(f"self.collection: {self.collection}")
        
        return self
    
    def limit(self, limit: int) -> 'QueryBuilder':
        """Limit the number of results."""
        self._limit = limit
        return self
    
    def offset(self, offset: int) -> 'QueryBuilder':
        """Skip a number of results."""
        self._offset = offset
        return self
    
    def get(self) -> List[Dict[str, Any]]:
        """Execute the query and get results."""
        # Save the current collection
        original_collection = self.store.default_collection
        # Set the collection to this query's collection
        self.store.default_collection = self.collection
        
        # デバッグ出力
        print(f"\nQueryBuilder.getメソッドが呼び出されました")
        print(f"collection: {self.collection}")
        
        # _filters_listが存在する場合は、それを使用
        filters_list = getattr(self, '_filters_list', [])
        print(f"filters_list: {filters_list}")
        
        try:
            return self.store.query(
                filters=filters_list,
                limit=self._limit,
                offset=self._offset,
                order_by=self._order_by,
                order_direction=self._order_direction
            )
        finally:
            # Restore the original collection
            self.store.default_collection = original_collection
    
    def count(self) -> int:
        """Count the number of matching documents."""
        # Save the current collection
        original_collection = self.store.default_collection
        # Set the collection to this query's collection
        self.store.default_collection = self.collection
        
        try:
            return self.store.count(self.filters)
        finally:
            # Restore the original collection
            self.store.default_collection = original_collection


class Collection:
    """
    A collection in LiteStore.
    
    This class provides methods for working with a collection of documents.
    """
    
    def __init__(self, store, name: str):
        self.store = store
        self.name = name
    
    def doc(self, id: Optional[str] = None) -> 'Document':
        """
        Get a document reference.
        
        Args:
            id: Optional document ID. If not provided, a random ID will be generated
                when the document is created.
                
        Returns:
            A Document reference.
        """
        if id is None:
            id = str(uuid.uuid4()).replace('-', '')[:20]
        return Document(self.store, self.name, id)
    
    def add(self, data: Dict[str, Any], id: Optional[str] = None) -> Dict[str, Any]:
        """
        Add a new document to the collection.
        
        Args:
            data: The data to store.
            id: Optional ID for the document. If not provided, a random ID will be generated.
            
        Returns:
            The created document with its ID.
        """
        # Save the current collection
        original_collection = self.store.default_collection
        self.store.default_collection = self.name
        
        # デバッグ出力
        print(f"\nCollection.addメソッドが呼び出されました")
        print(f"collection name: {self.name}")
        print(f"original_collection: {original_collection}")
        print(f"self.store.default_collection: {self.store.default_collection}")
        
        try:
            result = self.store.create(data, id=id)
            print(f"create結果: {result}")
            return result
        finally:
            # Restore the original collection
            self.store.default_collection = original_collection
    
    def where(self, field: str, op: str, value: Any) -> QueryBuilder:
        """
        Create a query with a filter.
        
        Args:
            field: Field name to filter by.
            op: Operator to use for filtering ("==", "!=", ">", "<", ">=", "<=").
            value: Value to filter for.
            
        Returns:
            A QueryBuilder for chaining.
        """
        query = QueryBuilder(self.store, self.name)
        return query.where(field, op, value)
    
    def order_by(self, field: str, direction: str = "ASC") -> QueryBuilder:
        """Create a query with ordering."""
        query = QueryBuilder(self.store, self.name)
        return query.order_by(field, direction)
    
    def limit(self, limit: int) -> QueryBuilder:
        """Create a query with a limit."""
        query = QueryBuilder(self.store, self.name)
        return query.limit(limit)
    
    def get(self) -> List[Dict[str, Any]]:
        """Get all documents in the collection."""
        # Save the current collection
        original_collection = self.store.default_collection
        self.store.default_collection = self.name
        
        try:
            return self.store.list()
        finally:
            # Restore the original collection
            self.store.default_collection = original_collection


class Document:
    """
    A document in LiteStore.
    
    This class provides methods for working with a document.
    """
    
    def __init__(self, store, collection: str, id: str):
        self.store = store
        self.collection = collection
        self.id = id
    
    def exists(self) -> bool:
        """Check if the document exists."""
        # Save the current collection
        original_collection = self.store.default_collection
        # Set the collection to this document's collection
        self.store.default_collection = self.collection
        
        try:
            self.store.read(self.id)
            return True
        except NotFoundError:
            return False
        finally:
            # Restore the original collection
            self.store.default_collection = original_collection
            
    def get(self) -> Dict[str, Any]:
        """Get the document data."""
        # Save the current collection
        original_collection = self.store.default_collection
        # Set the collection to this document's collection
        self.store.default_collection = self.collection
        
        try:
            return self.store.read(self.id)
        finally:
            # Restore the original collection
            self.store.default_collection = original_collection
    
    def set(self, data: Dict[str, Any], merge: bool = True) -> Dict[str, Any]:
        """Set the document data."""
        # Save the current collection
        original_collection = self.store.default_collection
        # Set the collection to this document's collection
        self.store.default_collection = self.collection
        
        try:
            try:
                return self.store.update(self.id, data, merge=merge)
            except NotFoundError:
                return self.store.create(data, id=self.id)
        finally:
            # Restore the original collection
            self.store.default_collection = original_collection
    
    def update(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update the document data."""
        # Save the current collection
        original_collection = self.store.default_collection
        # Set the collection to this document's collection
        self.store.default_collection = self.collection
        
        try:
            return self.store.update(self.id, data, merge=True)
        finally:
            # Restore the original collection
            self.store.default_collection = original_collection
    
    def delete(self) -> None:
        """Delete the document."""
        # Save the current collection
        original_collection = self.store.default_collection
        # Set the collection to this document's collection
        self.store.default_collection = self.collection
        
        try:
            self.store.delete(self.id)
        finally:
            # Restore the original collection
            self.store.default_collection = original_collection


class LiteStore:
    """
    A LiteStore-like interface for storing and retrieving data using SQLite.
    
    This class provides methods for creating, reading, updating, and deleting
    data in a SQLite database. The data is stored as JSON in a single table,
    with indexed fields extracted to separate columns for efficient querying.
    """
    
    def __init__(
        self, 
        db_path: str = ":memory:", 
        default_collection: str = "items",
        schema: Optional[Schema] = None,
        index_all_fields: bool = False
    ):
        """
        Initialize a new CRUDStore.
        
        Args:
            db_path: Path to the SQLite database file. Use ":memory:" for an in-memory database.
            default_collection: Name of the default collection (table) to store data in.
            schema: Optional schema for validating data.
            index_all_fields: If True, all fields in the schema will be indexed.
        """
        # db_pathがNoneの場合はデフォルト値を使用
        self.db_path = db_path if db_path is not None else ":memory:"
        self.default_collection = quote_table_name(default_collection)  # Default collection
        self.schema = schema
        self.index_all_fields = index_all_fields
        
        if self.schema and self.index_all_fields:
            for field in self.schema.fields.values():
                field.indexed = True
                
        self._initialize_db()
    
    @contextmanager
    def _get_connection(self) -> Iterator[sqlite3.Connection]:
        """Get a database connection with proper error handling."""
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            yield conn
        except sqlite3.Error as e:
            raise DatabaseError(f"Database error: {str(e)}")
        finally:
            if conn:
                conn.close()
    
    def _initialize_db(self) -> None:
        """Initialize the database with the required tables and indexes."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {self.default_collection} (
                    id TEXT PRIMARY KEY,
                    data TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            try:
                cursor.execute("SELECT json_extract('{\"test\":123}', '$.test')")
                result = cursor.fetchone()[0]
                if result != 123:
                    raise DatabaseError("SQLite JSON1 extension test failed")
            except sqlite3.OperationalError:
                raise DatabaseError("SQLite JSON1 extension is required but not available")
            
            if self.schema:
                for field_name, field in self.schema.fields.items():
                    if field.indexed or self.index_all_fields:
                        if field_name == "id":
                            continue
                            
                        index_name = quote_table_name(f"idx_{self.default_collection}_{field_name}")
                        
                        cursor.execute(f"""
                            CREATE INDEX IF NOT EXISTS {index_name} 
                            ON {self.default_collection} (json_extract(data, '$.{field_name}'))
                        """)
            
            conn.commit()
    
    def _process_server_timestamp(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        SERVER_TIMESTAMPセンチネル値を現在のタイムスタンプに置き換えます。
        
        Args:
            data: 処理するデータ
            
        Returns:
            SERVER_TIMESTAMPが置き換えられたデータ
        """
        processed_data = {}
        for key, value in data.items():
            if isinstance(value, ServerTimestampSentinel):
                processed_data[key] = datetime.datetime.now()
            elif isinstance(value, dict):
                processed_data[key] = self._process_server_timestamp(value)
            elif isinstance(value, list):
                processed_data[key] = [
                    self._process_server_timestamp(item) if isinstance(item, dict) else
                    datetime.datetime.now() if isinstance(item, ServerTimestampSentinel) else
                    item
                    for item in value
                ]
            else:
                processed_data[key] = value
        return processed_data
    
    def _validate_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate data against the schema if one is provided."""
        # SERVER_TIMESTAMPを処理
        processed_data = self._process_server_timestamp(data)
        
        if self.schema:
            return self.schema.validate(processed_data)
        return processed_data
    
    def create(self, data: Dict[str, Any], id: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a new item in the store.
        
        Args:
            data: The data to store.
            id: Optional ID for the item. If not provided, a UUID will be generated.
            
        Returns:
            The created item with its ID.
            
        Raises:
            ValidationError: If the data fails validation.
            DatabaseError: If there's an error with the database.
        """
        validated_data = self._validate_data(data)
        
        item_id = id if id is not None else str(uuid.uuid4())
        
        item = {"id": item_id, **validated_data}
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    f"INSERT INTO {self.default_collection} (id, data) VALUES (?, ?)",
                    (item_id, json.dumps(validated_data, cls=DateTimeEncoder))
                )
                conn.commit()
            except sqlite3.IntegrityError:
                raise ValidationError(f"Item with ID '{item_id}' already exists")
        
        return item
    
    def read(self, id: str) -> Dict[str, Any]:
        """
        Read an item from the store by its ID.
        
        Args:
            id: The ID of the item to read.
            
        Returns:
            The item data.
            
        Raises:
            NotFoundError: If the item is not found.
            DatabaseError: If there's an error with the database.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                f"SELECT id, data FROM {self.default_collection} WHERE id = ?",
                (id,)
            )
            row = cursor.fetchone()
            
            if not row:
                raise NotFoundError(f"Item with ID '{id}' not found")
            
            data = json.loads(row["data"])
            return {"id": row["id"], **data}
    
    def update(self, id: str, data: Dict[str, Any], merge: bool = True) -> Dict[str, Any]:
        """
        Update an item in the store.
        
        Args:
            id: The ID of the item to update.
            data: The new data for the item.
            merge: If True, merge the new data with the existing data.
                  If False, replace the existing data entirely.
            
        Returns:
            The updated item.
            
        Raises:
            NotFoundError: If the item is not found.
            ValidationError: If the data fails validation.
            DatabaseError: If there's an error with the database.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                f"SELECT data FROM {self.default_collection} WHERE id = ?",
                (id,)
            )
            row = cursor.fetchone()
            
            if not row:
                raise NotFoundError(f"Item with ID '{id}' not found")
            
            if merge:
                existing_data = json.loads(row["data"])
                
                # 特殊な値を処理する
                merged_data = {**existing_data}
                for key, value in data.items():
                    # 文字列リテラルを使用して循環インポートを避ける
                    if str(value) == "DELETE_FIELD":
                        if key in merged_data:
                            del merged_data[key]
                    else:
                        merged_data[key] = value
                        
                validated_data = self._validate_data(merged_data)
            else:
                validated_data = self._validate_data(data)
            
            cursor.execute(
                f"UPDATE {self.default_collection} SET data = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                (json.dumps(validated_data, cls=DateTimeEncoder), id)
            )
            conn.commit()
        
        return {"id": id, **validated_data}
    
    def delete(self, id: str) -> None:
        """
        Delete an item from the store.
        
        Args:
            id: The ID of the item to delete.
            
        Raises:
            NotFoundError: If the item is not found.
            DatabaseError: If there's an error with the database.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                f"DELETE FROM {self.default_collection} WHERE id = ?",
                (id,)
            )
            
            if cursor.rowcount == 0:
                raise NotFoundError(f"Item with ID '{id}' not found")
            
            conn.commit()
    
    def list(self, limit: Optional[int] = None, offset: int = 0) -> List[Dict[str, Any]]:
        """
        List items in the store.
        
        Args:
            limit: Maximum number of items to return.
            offset: Number of items to skip.
            
        Returns:
            A list of items.
            
        Raises:
            DatabaseError: If there's an error with the database.
        """
        # テーブル名がすでにダブルクォートで囲まれている場合は、そのまま使用する
        table_name = self.default_collection
        query = f"SELECT id, data FROM {table_name}"
        params = []
        
        if limit is not None and offset > 0:
            query += " LIMIT ? OFFSET ?"
            params.extend([limit, offset])
        elif limit is not None:
            query += " LIMIT ?"
            params.append(limit)
        elif offset > 0:
            query += " LIMIT -1 OFFSET ?"
            params.append(offset)
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            items = []
            for row in rows:
                data = json.loads(row["data"])
                # スキーマ情報を使用して型を修正
                if self.schema is not None:
                    for field_name, field in self.schema.fields.items():
                        if field_name in data:
                            # ブール値の処理を改善
                            if field.__class__.__name__ == 'BooleanField':
                                if isinstance(data[field_name], str):
                                    data[field_name] = data[field_name].lower() == 'true'
                                elif isinstance(data[field_name], int):
                                    data[field_name] = bool(data[field_name])
                items.append({"id": row["id"], **data})
            
            return items
    
    def query(self, filters=None, limit: Optional[int] = None, offset: int = 0, order_by: Optional[str] = None, order_direction: str = "ASC") -> List[Dict[str, Any]]:
        """
        Query items in the store based on filters.
        
        Args:
            filters: Dictionary of field-value pairs to filter by or list of (field, op, value) tuples.
            limit: Maximum number of items to return.
            offset: Number of items to skip.
            order_by: Field to order by.
            order_direction: Direction to order (ASC or DESC).
            
        Returns:
            A list of matching items.
            
        Raises:
            DatabaseError: If there's an error with the database.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # テーブル名がすでにダブルクォートで囲まれている場合は、そのまま使用する
            table_name = self.default_collection
            query = f"SELECT id, data FROM {table_name}"
            
            # デバッグ出力
            print(f"\nテーブル名: {table_name}")
            print(f"クエリ: {query}")
            params = []
            
            if filters:
                where_clauses = []
                
                # filtersがリストの場合（(field, op, value)のタプルのリスト）
                if isinstance(filters, list):
                    print(f"filters is a list: {filters}")
                    for field, op, value in filters:
                        json_path = f"$.{field}"
                        
                        # 演算子の変換（"=="から"="へ）
                        sql_op = "=" if op == "==" else op
                        
                        if value is None:
                            where_clauses.append(f"json_extract(data, '{json_path}') IS NULL")
                        elif isinstance(value, bool):
                            bool_value = 1 if value else 0
                            where_clauses.append(f"json_extract(data, '{json_path}') {sql_op} ?")
                            params.append(bool_value)
                        else:
                            where_clauses.append(f"json_extract(data, '{json_path}') {sql_op} ?")
                            params.append(value)
                
                # filtersが辞書の場合（従来の方法）
                elif isinstance(filters, dict):
                    print(f"filters is a dict: {filters}")
                    for key, value in filters.items():
                        json_path = f"$.{key}"
                        
                        if value is None:
                            where_clauses.append(f"json_extract(data, '{json_path}') IS NULL")
                        elif isinstance(value, bool):
                            bool_value = 1 if value else 0
                            where_clauses.append(f"json_extract(data, '{json_path}') = ?")
                            params.append(bool_value)
                        else:
                            where_clauses.append(f"json_extract(data, '{json_path}') = ?")
                            params.append(value)
                
                if where_clauses:
                    query += " WHERE " + " AND ".join(where_clauses)
                    print(f"WHERE句を追加: {query}")
                    print(f"パラメータ: {params}")
            
            # ORDER BY句の処理
            if order_by:
                json_path = f"$.{order_by}"
                query += f" ORDER BY json_extract(data, '{json_path}') {order_direction}"
                print(f"ORDER BY句を追加: {query}")
            
            # LIMITとOFFSET句の処理
            if limit is not None and offset > 0:
                query += " LIMIT ? OFFSET ?"
                params.extend([limit, offset])
                print(f"LIMITとOFFSET句を追加: {query}")
            elif limit is not None:
                query += " LIMIT ?"
                params.append(limit)
                print(f"LIMIT句を追加: {query}")
            elif offset > 0:
                query += " LIMIT -1 OFFSET ?"
                params.append(offset)
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            items = []
            for row in rows:
                data = json.loads(row["data"])
                items.append({"id": row["id"], **data})
            
            return items
    
    def count(self, filters: Optional[Dict[str, Any]] = None) -> int:
        """
        Count items in the store, optionally filtered.
        
        Args:
            filters: Optional dictionary of field-value pairs to filter by.
            
        Returns:
            The number of matching items.
            
        Raises:
            DatabaseError: If there's an error with the database.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # テーブル名がすでにダブルクォートで囲まれている場合は、そのまま使用する
            table_name = self.default_collection
            
            if not filters:
                cursor.execute(f"SELECT COUNT(*) as count FROM {table_name}")
                row = cursor.fetchone()
                return row["count"]
            
            query = f"SELECT COUNT(*) as count FROM {table_name}"
            params = []
            
            where_clauses = []
            for key, value in filters.items():
                json_path = f"$.{key}"
                
                if value is None:
                    where_clauses.append(f"json_extract(data, '{json_path}') IS NULL")
                elif isinstance(value, bool):
                    bool_value = 1 if value else 0
                    where_clauses.append(f"json_extract(data, '{json_path}') = ?")
                    params.append(bool_value)
                else:
                    where_clauses.append(f"json_extract(data, '{json_path}') = ?")
                    params.append(value)
            
            if where_clauses:
                query += " WHERE " + " AND ".join(where_clauses)
            
            cursor.execute(query, params)
            row = cursor.fetchone()
            return row["count"]
    
    def collection(self, name: str, schema: Optional[Schema] = None) -> 'CollectionReference':
        """Get a collection reference.
        
        Args:
            name: Name of the collection
            schema: Optional schema for the collection. If None, the default schema is used.
            
        Returns:
            A CollectionReference object for the specified collection.
        """
        global _CollectionReference
        if _CollectionReference is None:
            from storekiss.litestore import CollectionReference
            _CollectionReference = CollectionReference
        
        # コレクション固有のスキーマを使用するか、デフォルトのスキーマを使用する
        original_schema = self.schema
        if schema is not None:
            self.schema = schema
        
        try:
            collection = self.get_collection(name)
            return _CollectionReference(collection)
        finally:
            # スキーマを元に戻す
            self.schema = original_schema
        
    def get_collection(self, name: str) -> 'Collection':
        """Get a collection reference.
        
        Args:
            name: Name of the collection
            
        Returns:
            A Collection object for the specified collection.
        """
        # テーブル名を安全な形式に変換
        safe_name = quote_table_name(name)
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
                (safe_name,)
            )
            if not cursor.fetchone():
                cursor.execute(f"""
                    CREATE TABLE IF NOT EXISTS {safe_name} (
                        id TEXT PRIMARY KEY,
                        data TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                conn.commit()
                
                if self.schema:
                    for field_name, field in self.schema.fields.items():
                        if field.indexed or self.index_all_fields:
                            if field_name == "id":
                                continue
                                
                            # インデックス名も安全な形式に変換
                            safe_field_name = re.sub(r'[^a-zA-Z0-9_$]', '_', field_name)
                            index_name = quote_table_name(f"idx_{safe_name}_{safe_field_name}")
                            
                            cursor.execute(f"""
                                CREATE INDEX IF NOT EXISTS {index_name} 
                                ON {safe_name} (json_extract(data, '$.{field_name}'))
                            """)
                    conn.commit()
        
        return Collection(self, safe_name)


# 循環インポートを解決するための遅延インポート設定
def _setup_imports():
    global _CollectionReference
    if _CollectionReference is None:
        from storekiss.litestore import CollectionReference
        _CollectionReference = CollectionReference


# 初期化時に遅延インポートを設定
_setup_imports()


# LiteStoreクラスにエクスポート/インポート機能を追加
def _add_export_import_to_litestore():
    """
    LiteStoreクラスにエクスポート/インポート機能を追加します。
    """
    from storekiss.export_import import LiteStoreExporter, LiteStoreImporter
    
    def export_collection(self, collection_name: str, output_dir: str) -> str:
        """
        指定されたコレクションをLiteStore互換形式でエクスポートします。
        
        Args:
            collection_name: エクスポートするコレクション名
            output_dir: 出力ディレクトリのパス
            
        Returns:
            エクスポートされたメタデータファイルのパス
        """
        exporter = LiteStoreExporter(self)
        return exporter.export_collection(collection_name, output_dir)
    
    def export_all_collections(self, output_dir: str) -> str:
        """
        すべてのコレクションをLiteStore互換形式でエクスポートします。
        
        Args:
            output_dir: 出力ディレクトリのパス
            
        Returns:
            エクスポートされたメタデータファイルのパス
        """
        exporter = LiteStoreExporter(self)
        return exporter.export_all_collections(output_dir)
    
    def import_collection(self, collection_name: str, input_dir: str) -> int:
        """
        指定されたコレクションをインポートします。
        
        Args:
            collection_name: インポートするコレクション名
            input_dir: 入力ディレクトリのパス
            
        Returns:
            インポートされたドキュメント数
        """
        importer = LiteStoreImporter(self)
        return importer.import_collection(collection_name, input_dir)
    
    def import_all_collections(self, input_dir: str) -> Dict[str, int]:
        """
        すべてのコレクションをインポートします。
        
        Args:
            input_dir: 入力ディレクトリのパス
            
        Returns:
            コレクション名とインポートされたドキュメント数の辞書
        """
        importer = LiteStoreImporter(self)
        return importer.import_all_collections(input_dir)
    
    # LiteStoreクラスにメソッドを追加
    LiteStore.export_collection = export_collection
    LiteStore.export_all_collections = export_all_collections
    LiteStore.import_collection = import_collection
    LiteStore.import_all_collections = import_all_collections


# エクスポート/インポート機能を追加
_add_export_import_to_litestore()
