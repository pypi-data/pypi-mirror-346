"""
自動ドキュメントID生成機能のデモンストレーション。

このサンプルは、storekissライブラリのFirestoreライクな自動ドキュメントID生成機能を
使用する方法を示します。
"""
import logging
import os
import sys
import tempfile
import csv
import sqlite3
import json
from datetime import datetime
from storekiss import firestore
from storekiss.validation import Schema, StringField, NumberField

# ログレベルとフォーマットを設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main():
    """自動ドキュメントID生成機能のデモンストレーション"""
    logging.info("自動ドキュメントID生成の例を開始します")
    
    # スキーマを作成
    schema = Schema({
        "number": NumberField(required=True),
        "name": StringField(required=True)
    })
    
    # 一時ファイルを使用してデータベースを作成
    # メモリ内データベースはテーブル作成に問題があるため、ファイルベースのデータベースを使用
    temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
    temp_db.close()
    db_path = temp_db.name
    
    try:
        # Firestoreクライアントを作成
        db = firestore.client(db_path=db_path, schema=schema)
        
        # 都道府県コレクションを取得
        prefectures = db.collection("都道府県")
        logging.info("コレクションを初期化しました: 都道府県")
        
        logging.info("IDを指定せずにドキュメントを作成します")
        doc_ref = prefectures.document()  # IDを指定しない
        doc_id = doc_ref.id
        logging.info(f"生成されたドキュメントID: {doc_id}")
        
        # ドキュメントデータを設定
        doc_ref.set({
            "number": 1,
            "name": "北海道"
        })
        
        # ドキュメントを取得
        hokkaido = doc_ref.get()
        logging.info(f"ドキュメントデータ: id={hokkaido['id']}, number={hokkaido['number']}, name={hokkaido['name']}")
        
        logging.info("add()メソッドを使用して自動IDでドキュメントを作成します")
        tokyo = prefectures.add({
            "number": 13,
            "name": "東京都"
        })
        logging.info(f"生成されたドキュメントID: {tokyo['id']}")
        logging.info(f"ドキュメントデータ: id={tokyo['id']}, number={tokyo['number']}, name={tokyo['name']}")
        
        logging.info("IDを明示的に指定してドキュメントを作成します")
        osaka_ref = prefectures.document("osaka")
        osaka_ref.set({
            "number": 27,
            "name": "大阪府"
        })
        
        osaka = osaka_ref.get()
        logging.info(f"ドキュメントデータ: id={osaka['id']}, number={osaka['number']}, name={osaka['name']}")
        
        logging.info("add()メソッドでIDを明示的に指定します")
        kyoto = prefectures.add({
            "number": 26,
            "name": "京都府"
        }, id="kyoto")
        logging.info(f"指定したドキュメントID: {kyoto['id']}")
        logging.info(f"ドキュメントデータ: number={kyoto['number']}, name={kyoto['name']}")
        
        all_docs = prefectures.get()
        logging.info(f"コレクション内のドキュメント数: {len(all_docs)}")
        for doc in all_docs:
            logging.info(f"  {doc['id']}: {doc['name']} (番号: {doc['number']})")
        
        # 特別処理: データベースに直接アクセスしてCSVファイルを生成
        logging.info(f"データベースパス: {db_path}")
        logging.info("特別処理: データベースからCSVファイルを生成します")
        
        # データベース内のテーブルを確認
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        logging.info(f"データベース内のテーブル: {tables}")
        conn.close()
        
        export_to_csv(db_path, "都道府県", "都道府県_export.csv")
        
        logging.info("自動ドキュメントID生成の例を終了します")
    
    finally:
        # 一時ファイルを削除
        try:
            os.unlink(db_path)
        except:
            pass

def export_to_csv(db_path: str, collection_name: str, csv_filename: str) -> None:
    """SQLiteデータベースのテーブルをCSVファイルにエクスポートします。
    
    Args:
        db_path: SQLiteデータベースのパス
        collection_name: エクスポートするコレクション名
        csv_filename: 出力するCSVファイル名
    """
    try:
        # SQLiteに接続
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # テーブル名を安全な形式に変換（実際のテーブル名を確認するため）
        # インポートの問題を回避するために、関数を直接実装
        import re
        
        def mangle_table_name(name):
            """PostgreSQLとSQLite3の両方で合法なテーブル名に変換します。"""
            if not name:
                return "collection_default"
            
            # 英数字、アンダースコア、ドル記号以外の文字をアンダースコアに置換
            safe_name = re.sub(r'[^a-zA-Z0-9_$]', '_', name)
            
            # 数字で始まる場合は先頭に't_'を追加
            if safe_name and safe_name[0].isdigit():
                safe_name = 't_' + safe_name
                
            # 63バイト以下に制限（PostgreSQLの制限）
            if len(safe_name.encode('utf-8')) > 63:
                hash_suffix = str(hash(name) % 10000).zfill(4)
                prefix_length = 63 - len(hash_suffix) - 1  # 1はアンダースコアの分
                safe_name = safe_name[:prefix_length] + '_' + hash_suffix
                
            return safe_name
        
        safe_table_name = mangle_table_name(collection_name)
        logging.info(f"コレクション名 '{collection_name}' は '{safe_table_name}' に変換されました")
        
        # テーブルからデータを取得
        # 都道府県の場合はテーブル名が____に変換されることがわかっているので、直接指定
        if collection_name == "都道府県":
            cursor.execute("SELECT id, data, created_at, updated_at FROM ____")
        else:
            cursor.execute(f"SELECT id, data, created_at, updated_at FROM {safe_table_name}")
        rows = cursor.fetchall()
        
        # CSVファイルに書き込み
        with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # ヘッダー行を書き込み
            writer.writerow(['id', 'number', 'name', 'created_at', 'updated_at'])
            
            # データをCSVに書き込む
            for row in rows:
                data = json.loads(row["data"])
                writer.writerow([row["id"], data.get("number"), data.get("name"), row["created_at"], row["updated_at"]])
                
        logging.info(f"CSVファイルが生成されました: {csv_filename}")
        # CSVファイルの内容を表示
        with open(csv_filename, 'r', encoding='utf-8') as f:
            logging.info(f"CSVファイルの内容:\n{f.read()}")
    
    except Exception as e:
        logging.error(f"CSVファイルの生成中にエラーが発生しました: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    main()
