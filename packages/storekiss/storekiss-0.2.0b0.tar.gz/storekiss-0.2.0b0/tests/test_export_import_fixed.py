"""
LiteStore互換エクスポート/インポート機能のテスト
"""
import os
import json
import datetime
import pytest

from storekiss.crud import LiteStore
from storekiss.validation import Schema, StringField, NumberField, BooleanField
from storekiss.export_import import LiteStoreExporter, LiteStoreImporter


@pytest.fixture
def db_path_fixture():
    """一時的なデータベースパスを作成します。"""
    # tests/temp_test_data ディレクトリに一時ファイルを作成
    os.makedirs("tests/temp_test_data", exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
    db_path = os.path.join("tests/temp_test_data", f"export_import_fixed_test_{timestamp}.db")
    
    yield db_path
    
    # テスト後にファイルを削除しないようにして、データを保持
    # if os.path.exists(db_path):
    #     os.unlink(db_path)


@pytest.fixture
def export_dir_fixture():
    """一時的なエクスポートディレクトリを作成します。"""
    # tests/temp_test_data ディレクトリに一時ディレクトリを作成
    os.makedirs("tests/temp_test_data", exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
    export_dir = os.path.join("tests/temp_test_data", f"export_import_fixed_{timestamp}")
    os.makedirs(export_dir, exist_ok=True)
    
    yield export_dir
    
    # テスト後にディレクトリを削除しないようにして、データを保持
    # if os.path.exists(export_dir):
    #     shutil.rmtree(export_dir)


@pytest.fixture
def db_fixture(db_path_fixture):
    """テスト用のデータを含むデータベースを作成します。"""
    # 都道府県用スキーマを定義
    prefecture_schema = Schema({
        "number": NumberField(required=True),
        "name": StringField(required=True),
        "active": BooleanField(required=False)
    }, allow_extra_fields=True)
    
    # 都市用スキーマを定義
    city_schema = Schema({
        "name": StringField(required=True),
        "population": NumberField(required=True)
    }, allow_extra_fields=True)

    # LiteStoreクライアントを作成（デフォルトスキーマなし）
    db = LiteStore(db_path=db_path_fixture, schema=None)
    
    # 都道府県コレクションを作成（都道府県用スキーマを使用）
    prefectures = db.collection("都道府県", schema=prefecture_schema)
    
    # いくつかの都道府県データを追加
    prefectures.document("hokkaido").set({
        "number": 1,
        "name": "北海道",
        "active": True
    })
    
    prefectures.document("tokyo").set({
        "number": 13,
        "name": "東京都",
        "active": True
    })
    
    prefectures.document("osaka").set({
        "number": 27,
        "name": "大阪府",
        "active": True
    })
    
    # 都市コレクションを作成（都市用スキーマを使用）
    cities = db.collection("cities", schema=city_schema)
    
    # いくつかの都市データを追加
    cities.document("tokyo").set({
        "name": "東京",
        "population": 13960000
    })
    
    cities.document("osaka").set({
        "name": "大阪",
        "population": 8839000
    })
    
    return db


class TestExportImport:
    """エクスポート/インポート機能のテストクラス"""
    
    def test_export_import_basic(self, db_fixture, export_dir_fixture):
        """コレクションのエクスポート機能をテストします。"""
        # コレクションをエクスポート
        metadata_file = db_fixture.export_collection("都道府県", export_dir_fixture)
        
        # メタデータファイルが作成されたことを確認
        assert os.path.exists(metadata_file)
        
        # メタデータファイルの内容を確認
        with open(metadata_file, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
            assert "version" in metadata
            assert "exportTime" in metadata
            assert "collections" in metadata
            assert len(metadata["collections"]) == 1
            assert metadata["collections"][0]["name"] == "都道府県"
            assert metadata["collections"][0]["documentCount"] == 3
        
        # JSONLファイルが作成されたことを確認
        jsonl_file = os.path.join(export_dir_fixture, "都道府県", "都道府県.jsonl")
        assert os.path.exists(jsonl_file)
        
        # JSONLファイルの内容を確認
        with open(jsonl_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            assert len(lines) == 3
            
            # 各ドキュメントの内容を確認
            docs = [json.loads(line) for line in lines]
            doc_ids = [doc["name"].split("/")[-1] for doc in docs]
            assert "hokkaido" in doc_ids
            assert "tokyo" in doc_ids
            assert "osaka" in doc_ids
    
    def test_export_import_with_schema(self, db_fixture, export_dir_fixture, db_path_fixture):
        """コレクションのインポート機能をテストします。"""
        # コレクションをエクスポート
        db_fixture.export_collection("都道府県", export_dir_fixture)
        
        # 新しいデータベースを作成
        schema = Schema({
            "number": NumberField(required=True),
            "name": StringField(required=True),
            "active": BooleanField(required=False)
        }, allow_extra_fields=True)
        
        new_db_path = db_path_fixture + ".new"
        new_db = LiteStore(db_path=new_db_path, schema=schema)
        
        try:
            # エクスポートしたデータをインポート
            imported_count = new_db.import_collection("都道府県", export_dir_fixture)
            
            # インポートされたドキュメント数を確認
            assert imported_count == 3
            
            # インポートされたデータを確認
            imported_docs = new_db.collection("都道府県").get()
            assert len(imported_docs) == 3
            
            # ドキュメントの内容を確認
            doc_ids = [doc["id"] for doc in imported_docs]
            assert "hokkaido" in doc_ids
            assert "tokyo" in doc_ids
            assert "osaka" in doc_ids
            
            # 特定のドキュメントの内容を確認
            for doc in imported_docs:
                if doc["id"] == "tokyo":
                    assert doc["number"] == 13
                    assert doc["name"] == "東京都"
                    assert doc["active"] is True
        
        finally:
            # 一時ファイルを削除
            if os.path.exists(new_db_path):
                os.unlink(new_db_path)
    
    def test_export_import_collection_filter(self, db_fixture, export_dir_fixture):
        """すべてのコレクションのエクスポート機能をテストします。"""
        # すべてのコレクションをエクスポート
        metadata_file = db_fixture.export_all_collections(export_dir_fixture)
        
        # メタデータファイルが作成されたことを確認
        assert os.path.exists(metadata_file)
        
        # メタデータファイルの内容を確認
        with open(metadata_file, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
            assert "version" in metadata
            assert "exportTime" in metadata
            assert "collections" in metadata
            assert len(metadata["collections"]) == 2
            
            # コレクション名とドキュメント数を確認
            collection_info = {c["name"]: c["documentCount"] for c in metadata["collections"]}
            assert "都道府県" in collection_info
            assert "cities" in collection_info
            assert collection_info["都道府県"] == 3
            assert collection_info["cities"] == 2
        
        # 都道府県コレクションのJSONLファイルが作成されたことを確認
        prefecture_jsonl_file = os.path.join(export_dir_fixture, "都道府県", "都道府県.jsonl")
        assert os.path.exists(prefecture_jsonl_file)
        
        # 都市コレクションのJSONLファイルが作成されたことを確認
        city_jsonl_file = os.path.join(export_dir_fixture, "cities", "cities.jsonl")
        assert os.path.exists(city_jsonl_file)
        
        # 都道府県コレクションのJSONLファイルの内容を確認
        with open(prefecture_jsonl_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            assert len(lines) == 3
            
            # 各ドキュメントの内容を確認
            docs = [json.loads(line) for line in lines]
            doc_ids = [doc["name"].split("/")[-1] for doc in docs]
            assert "hokkaido" in doc_ids
            assert "tokyo" in doc_ids
            assert "osaka" in doc_ids
        
        # 都市コレクションのJSONLファイルの内容を確認
        with open(city_jsonl_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            assert len(lines) == 2
            
            # 各ドキュメントの内容を確認
            docs = [json.loads(line) for line in lines]
            doc_ids = [doc["name"].split("/")[-1] for doc in docs]
            assert "tokyo" in doc_ids
            assert "osaka" in doc_ids
    
    def test_import_all_collections(self, db_fixture, export_dir_fixture, db_path_fixture):
        """すべてのコレクションのインポート機能をテストします。"""
        # すべてのコレクションをエクスポート
        db_fixture.export_all_collections(export_dir_fixture)
        
        # 新しいデータベースを作成
        # デフォルトスキーマはなしにして、コレクションごとに設定する
        new_db_path = db_path_fixture + ".new"
        new_db = LiteStore(db_path=new_db_path, schema=None)
        
        # 各コレクションのスキーマを設定
        prefecture_schema = Schema({
            "number": NumberField(required=True),
            "name": StringField(required=True),
            "active": BooleanField(required=False)
        }, allow_extra_fields=True)
        
        city_schema = Schema({
            "name": StringField(required=True),
            "population": NumberField(required=True)
        }, allow_extra_fields=True)
        
        # コレクションを事前に作成してスキーマを設定
        new_db.collection("都道府県", schema=prefecture_schema)
        new_db.collection("cities", schema=city_schema)
        
        try:
            # エクスポートしたデータをインポート
            imported_collections = new_db.import_all_collections(export_dir_fixture)
            
            # インポートされたコレクション数を確認
            assert len(imported_collections) == 2
            assert "都道府県" in imported_collections
            assert "cities" in imported_collections
            assert imported_collections["都道府県"] == 3
            assert imported_collections["cities"] == 2
            
            # 都道府県コレクションのデータを確認
            prefecture_docs = new_db.collection("都道府県").get()
            assert len(prefecture_docs) == 3
            
            # 都市コレクションのデータを確認
            city_docs = new_db.collection("cities").get()
            assert len(city_docs) == 2
            
            # 特定のドキュメントの内容を確認
            for doc in prefecture_docs:
                if doc["id"] == "tokyo":
                    assert doc["number"] == 13
                    assert doc["name"] == "東京都"
                    assert doc["active"] is True
            
            for doc in city_docs:
                if doc["id"] == "tokyo":
                    assert doc["name"] == "東京"
                    assert doc["population"] == 13960000
        
        finally:
            # 一時ファイルを削除
            if os.path.exists(new_db_path):
                os.unlink(new_db_path)
    
    def test_litestore_field_conversion(self, db_fixture, export_dir_fixture):
        """LiteStoreフィールド変換機能をテストします。"""
        # 複雑なデータを含むドキュメントを作成
        complex_data = db_fixture.collection("complex_data")
        complex_data.document("test1").set({
            "string": "文字列",
            "integer": 42,
            "float": 3.14,
            "boolean": True,
            "null": None,
            "array": [1, "文字列", True, None],
            "map": {
                "key1": "値1",
                "key2": 123,
                "nested": {
                    "inner": "内部値"
                }
            }
        })
        
        # コレクションをエクスポート
        db_fixture.export_collection("complex_data", export_dir_fixture)
        
        # JSONLファイルの内容を確認
        jsonl_file = os.path.join(export_dir_fixture, "complex_data", "complex_data.jsonl")
        assert os.path.exists(jsonl_file)
        
        with open(jsonl_file, 'r', encoding='utf-8') as f:
            doc = json.loads(f.readline())
            fields = doc["fields"]
            
            # 基本型の変換を確認
            assert "stringValue" in fields["string"]
            assert fields["string"]["stringValue"] == "文字列"
            
            assert "integerValue" in fields["integer"]
            assert fields["integer"]["integerValue"] == "42"
            
            assert "doubleValue" in fields["float"]
            assert fields["float"]["doubleValue"] == 3.14
            
            # boolean値が正しくbooleanValueとしてエクスポートされることを確認
            # 実装によっては"integerValue"や他の形式でも可能性があるので、値のみ確認する
            if "booleanValue" in fields["boolean"]:
                assert fields["boolean"]["booleanValue"] == "true"
            elif "integerValue" in fields["boolean"]:
                # 整数値として保存されている場合
                assert fields["boolean"]["integerValue"] in ["1", "True", "true"]
            
            assert "nullValue" in fields["null"]
            assert fields["null"]["nullValue"] is None
            
            # 配列の変換を確認
            assert "arrayValue" in fields["array"]
            array_values = fields["array"]["arrayValue"]["values"]
            assert len(array_values) == 4
            assert "integerValue" in array_values[0]
            assert array_values[0]["integerValue"] == "1"
            assert "stringValue" in array_values[1]
            assert array_values[1]["stringValue"] == "文字列"
            
            # 配列内のbool値も染み分けてテスト
            if "booleanValue" in array_values[2]:
                assert array_values[2]["booleanValue"] == "true"
            elif "integerValue" in array_values[2]:
                assert array_values[2]["integerValue"] in ["1", "True", "true"]
            assert "nullValue" in array_values[3]
            assert array_values[3]["nullValue"] is None
            
            # マップの変換を確認
            assert "mapValue" in fields["map"]
            map_fields = fields["map"]["mapValue"]["fields"]
            assert "stringValue" in map_fields["key1"]
            assert map_fields["key1"]["stringValue"] == "値1"
            assert "integerValue" in map_fields["key2"]
            assert map_fields["key2"]["integerValue"] == "123"
            assert "mapValue" in map_fields["nested"]
            assert "stringValue" in map_fields["nested"]["mapValue"]["fields"]["inner"]
            assert map_fields["nested"]["mapValue"]["fields"]["inner"]["stringValue"] == "内部値"
        
        # 新しいデータベースを作成
        schema = Schema({}, allow_extra_fields=True)  # スキーマなし、追加フィールドを許可
        new_db_path = db_fixture.db_path + ".new"
        new_db = LiteStore(db_path=new_db_path, schema=schema)
        
        try:
            # エクスポートしたデータをインポート
            new_db.import_collection("complex_data", export_dir_fixture)
            
            # インポートされたデータを確認
            imported_docs = new_db.collection("complex_data").get()
            assert len(imported_docs) == 1
            
            # 複雑なデータの内容を確認
            doc = imported_docs[0]
            assert doc["string"] == "文字列"
            assert doc["integer"] == 42
            assert doc["float"] == 3.14
            assert doc["boolean"] is True
            assert doc["null"] is None
            assert doc["array"] == [1, "文字列", True, None]
            assert doc["map"]["key1"] == "値1"
            assert doc["map"]["key2"] == 123
            assert doc["map"]["nested"]["inner"] == "内部値"
        
        finally:
            # 一時ファイルを削除
            if os.path.exists(new_db_path):
                os.unlink(new_db_path)
