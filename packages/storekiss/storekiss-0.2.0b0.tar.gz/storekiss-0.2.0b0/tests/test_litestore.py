"""
Tests for the litestore interface.
"""
import os
import json
import pytest
import sqlite3
from datetime import datetime, timezone

from storekiss import litestore, SERVER_TIMESTAMP
from storekiss.litestore import DELETE_FIELD
from storekiss.exceptions import NotFoundError, ValidationError
from storekiss.validation import (
    Schema, StringField, NumberField, BooleanField, DateTimeField, MapField
)


@pytest.fixture
def temp_db_path():
    """Create a temporary database path."""
    # Create a temporary file in tests/temp_test_data directory
    os.makedirs("tests/temp_test_data", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
    db_path = os.path.join("tests/temp_test_data", f"litestore_test_{timestamp}.db")
    
    yield db_path
    
    # テスト後にファイルを削除しないようにして、データを保持
    # if os.path.exists(db_path):
    #     os.remove(db_path)


@pytest.fixture
def simple_db(temp_db_path):
    """Create a simple litestore client without schema validation."""
    # Create a client
    db = litestore.client(db_path=temp_db_path)
    
    # テーブル名がダブルクォートで囲まれるようになったため、テストフィクスチャも修正する必要があります
    # テスト用のテーブルを作成するだけで、実際のテストはクライアントインターフェースを使用します
    
    # 各テストで使用されるコレクションを事前に作成しておく
    collections = [
        "test_collection_add",
        "test_specific_id",
        "test_get_collection",
        "test_where_query",
        "test_compound_query",
        "test_order_by",
        "test_limit"
    ]
    
    # 各コレクションにテスト用のドキュメントを作成
    for collection_name in collections:
        collection = db.collection(collection_name)
        collection.document("test_doc").set({"name": "Test Document", "value": 42})
    
    yield db
    
    # テスト後のクリーンアップは単にファイルを削除するだけにします
    if os.path.exists(temp_db_path):
        os.remove(temp_db_path)


@pytest.fixture
def user_schema():
    """Create a schema for user data."""
    return Schema({
        "name": StringField(required=True, min_length=2),
        "age": NumberField(required=True, min_value=0, integer_only=True),
        "email": StringField(required=True),
        "active": BooleanField(required=False),
        "created": DateTimeField(required=False),
        "address": MapField({
            "street": StringField(required=True),
            "city": StringField(required=True),
            "zip": StringField(required=True)
        }, required=False)
    })


@pytest.fixture
def user_db(temp_db_path, user_schema):
    """Create a litestore client with user schema validation."""
    # Create a client with schema
    db = litestore.client(db_path=temp_db_path, schema=user_schema)
    
    yield db
    
    # テスト後のクリーンアップは単にファイルを削除するだけにします
    if os.path.exists(temp_db_path):
        os.remove(temp_db_path)


class TestLiteStoreClient:
    """Tests for the LiteStoreClient class."""
    
    def test_client_creation(self):
        """Test creating a litestore client."""
        # Create a client with default parameters
        db = litestore.client()
        assert db is not None
        assert isinstance(db, litestore.LiteStoreClient)
        
        # Create a client with custom parameters
        db = litestore.client(db_path=":memory:", default_collection="custom_items")
        assert db is not None
        assert isinstance(db, litestore.LiteStoreClient)
        
        # Create a client with schema
        schema = Schema({
            "name": StringField(required=True),
            "value": NumberField(required=True)
        })
        db = litestore.client(db_path=":memory:", schema=schema)
        assert db is not None
        assert isinstance(db, litestore.LiteStoreClient)
        
        # Check that the client has a collection method
        assert hasattr(db, "collection")
    
    def test_collection_reference(self, simple_db):
        """Test getting a collection reference."""
        collection_ref = simple_db.collection("test_collection")
        assert collection_ref is not None
    
    def test_document_reference(self, simple_db):
        """Test getting a document reference."""
        doc_ref = simple_db.collection("test_collection").document("test_doc")
        assert doc_ref is not None
    
    def test_auto_document_id(self, simple_db):
        """Test auto-generated document ID."""
        doc_ref = simple_db.collection("test_collection").document()
        assert doc_ref is not None


class TestDocumentOperations:
    """Tests for document operations."""
    
    def test_document_set_and_get(self, simple_db):
        """Test setting and getting a document."""
        doc_ref = simple_db.collection("test_collection").document("test_set_get")
        doc_ref.set({"name": "Test Document", "value": 42})
        
        doc = doc_ref.get()
        assert doc["name"] == "Test Document"
        assert doc["value"] == 42
    
    def test_document_set_with_merge(self, simple_db):
        """Test setting a document with merge=True."""
        doc_ref = simple_db.collection("test_collection").document("test_merge")
        doc_ref.set({"name": "Original Document", "value": 42})
        
        # Update with merge
        doc_ref.set({"value": 100, "new_field": "New Value"}, merge=True)
        
        doc = doc_ref.get()
        assert doc["name"] == "Original Document"  # Original field preserved
        assert doc["value"] == 100  # Updated field
        assert doc["new_field"] == "New Value"  # New field added
    
    def test_document_update(self, simple_db):
        """Test updating a document."""
        doc_ref = simple_db.collection("test_collection").document("test_update")
        doc_ref.set({"name": "Update Test", "value": 42})
        
        # Update document
        doc_ref.update({"value": 100, "updated": True})
        
        doc = doc_ref.get()
        assert doc["name"] == "Update Test"  # Original field preserved
        assert doc["value"] == 100  # Updated field
        assert doc["updated"] is True  # New field added
    
    def test_document_delete(self, simple_db):
        """Test deleting a document."""
        collection_ref = simple_db.collection("test_collection")
        doc_ref = collection_ref.document("test_delete")
        
        # Create document
        doc_ref.set({"name": "Delete Test", "value": 42})
        
        # Verify document exists
        doc = doc_ref.get()
        assert doc["name"] == "Delete Test"
        
        # Delete document
        doc_ref.delete()
        
        # Verify document no longer exists
        with pytest.raises(NotFoundError):
            doc_ref.get()
    
    def test_delete_field(self, simple_db):
        """Test deleting a field using DELETE_FIELD."""
        doc_ref = simple_db.collection("test_collection").document("test_delete_field")
        
        # Create document with multiple fields
        doc_ref.set({
            "name": "Field Delete Test",
            "value": 42,
            "optional": "This will be deleted"
        })
        
        # Update document with DELETE_FIELD
        doc_ref.update({
            "optional": DELETE_FIELD
        })
        
        # Verify field was deleted
        doc = doc_ref.get()
        assert doc["name"] == "Field Delete Test"
        assert doc["value"] == 42
        assert "optional" not in doc


class TestCollectionOperations:
    """Tests for collection operations."""
    
    def test_collection_add(self, simple_db):
        """Test adding a document to a collection."""
        collection_ref = simple_db.collection("test_collection_add")
        
        # Add document with auto-generated ID
        doc = collection_ref.add({
            "name": "Added Document",
            "value": 42,
            "tags": ["test", "document"]
        })
        
        # Verify document was added
        assert "id" in doc
        assert doc["name"] == "Added Document"
        assert doc["value"] == 42
        assert "test" in doc["tags"]
        assert "document" in doc["tags"]
    
    def test_document_with_specific_id(self, simple_db):
        """Test creating a document with a specific ID."""
        collection_ref = simple_db.collection("test_specific_id")
        
        # Add document with specific ID
        doc = collection_ref.add({
            "name": "Specific ID Document",
            "value": 42
        }, id="specific-id")
        
        # Verify document was added with correct ID
        assert doc["id"] == "specific-id"
        assert doc["name"] == "Specific ID Document"
        assert doc["value"] == 42
    
    def test_collection_get(self, simple_db):
        """Test getting all documents in a collection."""
        collection_ref = simple_db.collection("test_get_collection")
        
        # Clear existing documents
        docs = collection_ref.get()
        for doc in docs:
            collection_ref.document(doc["id"]).delete()
        
        # Add multiple documents
        collection_ref.add({"name": "Doc 1", "value": 10}, id="doc1")
        collection_ref.add({"name": "Doc 2", "value": 20}, id="doc2")
        collection_ref.add({"name": "Doc 3", "value": 30}, id="doc3")
        
        # Get all documents
        docs = collection_ref.get()
        
        # Verify correct number of documents
        assert len(docs) == 3
        
        # Verify document content
        doc_map = {doc["id"]: doc for doc in docs}
        assert "doc1" in doc_map
        assert "doc2" in doc_map
        assert "doc3" in doc_map
        assert doc_map["doc1"]["name"] == "Doc 1"
        assert doc_map["doc2"]["name"] == "Doc 2"
        assert doc_map["doc3"]["name"] == "Doc 3"


class TestQueryOperations:
    """Tests for query operations."""
    
    def test_simple_where_query(self, simple_db):
        """Test a simple where query."""
        collection_ref = simple_db.collection("test_where_query")
        
        # Clear existing documents
        docs = collection_ref.get()
        for doc in docs:
            collection_ref.document(doc["id"]).delete()
        
        # Add test documents
        collection_ref.add({"name": "Alice", "age": 30, "city": "New York"}, id="alice")
        collection_ref.add({"name": "Bob", "age": 25, "city": "Boston"}, id="bob")
        collection_ref.add({"name": "Charlie", "age": 35, "city": "Chicago"}, id="charlie")
        
        # Query for documents where age > 25
        query = collection_ref.where("age", ">", 25)
        results = query.get()
        
        # Verify results
        assert len(results) == 2
        result_names = [doc["name"] for doc in results]
        assert "Alice" in result_names
        assert "Charlie" in result_names
    
    def test_compound_where_query(self, simple_db):
        """Test a compound where query."""
        collection_ref = simple_db.collection("test_compound_query")
        
        # Clear existing documents
        docs = collection_ref.get()
        for doc in docs:
            collection_ref.document(doc["id"]).delete()
        
        # Add test documents
        collection_ref.add({"name": "Alice", "age": 30, "city": "New York"}, id="alice")
        collection_ref.add({"name": "Bob", "age": 25, "city": "Boston"}, id="bob")
        collection_ref.add({"name": "Charlie", "age": 35, "city": "Chicago"}, id="charlie")
        collection_ref.add({"name": "Dave", "age": 40, "city": "Boston"}, id="dave")
        
        # Query for documents where city == "Boston" AND age > 30
        query = collection_ref.where("city", "==", "Boston").where("age", ">", 30)
        results = query.get()
        
        # Verify results
        assert len(results) == 1
        assert results[0]["name"] == "Dave"
    
    def test_order_by_query(self, simple_db):
        """Test an order by query."""
        collection_ref = simple_db.collection("test_order_by")
        
        # Clear existing documents
        docs = collection_ref.get()
        for doc in docs:
            collection_ref.document(doc["id"]).delete()
        
        # Add test documents in random order
        collection_ref.add({"name": "Charlie", "age": 35}, id="charlie")
        collection_ref.add({"name": "Alice", "age": 30}, id="alice")
        collection_ref.add({"name": "Bob", "age": 25}, id="bob")
        
        # Query ordered by name (ascending)
        query = collection_ref.order_by("name")
        results = query.get()
        
        # Verify results are in correct order
        assert len(results) == 3
        assert results[0]["name"] == "Alice"
        assert results[1]["name"] == "Bob"
        assert results[2]["name"] == "Charlie"
        
        # Query ordered by age (descending)
        query = collection_ref.order_by("age", "DESC")
        results = query.get()
        
        # Verify results are in correct order
        assert len(results) == 3
        assert results[0]["name"] == "Charlie"
        assert results[1]["name"] == "Alice"
        assert results[2]["name"] == "Bob"
    
    def test_limit_query(self, simple_db):
        """Test a limit query."""
        collection_ref = simple_db.collection("test_limit")
        
        # 既存のドキュメントをクリア
        docs = collection_ref.get()
        for doc in docs:
            collection_ref.document(doc["id"]).delete()
        
        # 新しいドキュメントを追加
        collection_ref.add({"name": "Doc 1", "value": 10})
        collection_ref.add({"name": "Doc 2", "value": 20})
        collection_ref.add({"name": "Doc 3", "value": 30})
        collection_ref.add({"name": "Doc 4", "value": 40})
        collection_ref.add({"name": "Doc 5", "value": 50})
        
        query = collection_ref.order_by("value").limit(3)
        results = query.get()
        
        assert len(results) == 3
        assert results[0]["value"] == 10
        assert results[1]["value"] == 20
        assert results[2]["value"] == 30


class TestSchemaValidation:
    """Tests for schema validation."""
    
    def test_schema_validation_success(self, user_db):
        """Test successful schema validation."""
        users = user_db.collection("test_users_valid")
        
        valid_data = {
            "name": "John Doe",
            "age": 30,
            "email": "john@example.com",
            "active": True,
            "created": datetime.now(timezone.utc),
            "address": {
                "street": "123 Main St",
                "city": "Anytown",
                "zip": "12345"
            }
        }
        
        doc = users.add(valid_data)
        assert doc["name"] == "John Doe"
        assert doc["age"] == 30
        assert doc["email"] == "john@example.com"
        assert doc["active"] is True
        assert isinstance(doc["created"], datetime)
        assert doc["address"]["street"] == "123 Main St"
    
    def test_schema_validation_failure(self, user_db):
        """Test schema validation failure."""
        users = user_db.collection("test_users_invalid")
        
        invalid_data = {
            "name": "Jane Doe",
            "email": "jane@example.com"
        }
        
        with pytest.raises(ValidationError):
            users.add(invalid_data)
        
        invalid_type = {
            "name": "Bob Smith",
            "age": "thirty",  # Should be an integer
            "email": "bob@example.com"
        }
        
        with pytest.raises(ValidationError):
            users.add(invalid_type)
        
        invalid_value = {
            "name": "A",  # Too short
            "age": 30,
            "email": "a@example.com"
        }
        
        with pytest.raises(ValidationError):
            users.add(invalid_value)


class TestSpecialFeatures:
    """Tests for special features like SERVER_TIMESTAMP."""
    
    def test_server_timestamp(self, simple_db):
        """Test SERVER_TIMESTAMP functionality."""
        
        collection_ref = simple_db.collection("test_timestamps")
        
        # Create a document with a specific ID and SERVER_TIMESTAMP
        doc_ref = collection_ref.document("timestamp_doc")
        doc_ref.set({
            "name": "Timestamp Test",
            "created_at": SERVER_TIMESTAMP
        })
        
        doc = doc_ref.get()
        
        assert doc["name"] == "Timestamp Test"
        assert "created_at" in doc
        # サーバータイムスタンプは文字列として保存されるため、datetime型に変換する必要がある
        assert isinstance(doc["created_at"], str)
        # 文字列が正しい日時形式であることを確認
        try:
            datetime.fromisoformat(doc["created_at"])
            assert True
        except ValueError:
            assert False, f"'{doc['created_at']}' is not a valid ISO format datetime string"
    
    def test_json1_extension_detection(self, temp_db_path):
        """Test that JSON1 extension detection works correctly."""
        # Create a client
        db = litestore.client(db_path=temp_db_path)
        
        # Create a collection and document with nested data
        collection = db.collection("test_json1")
        doc_ref = collection.document("nested_doc")
        
        # Add document with nested data
        collection.add({"nested": {"value": 42}}, id="nested_doc")
        
        query = collection.where("nested.value", "==", 42)
        results = query.get()
        
        assert len(results) == 1
        assert results[0]["nested"]["value"] == 42
        
        if os.path.exists(temp_db_path):
            os.remove(temp_db_path)
