"""
Firestoreライクなインターフェースのデモンストレーション。

このサンプルは、storekissライブラリのFirestoreライクなインターフェースを
使用する方法を示します。Google Cloud Firestoreと同様の構文でデータを
操作することができます。
"""
import logkiss as logging
from storekiss import firestore

def main():
    """Firestoreライクなインターフェースのデモンストレーション"""
    logging.info("Firestoreライクなインターフェースの例を開始します")
    
    db = firestore.client()
    
    prefectures = db.collection("prefecture")
    
    logging.info("自動生成IDでドキュメントを作成します")
    new_doc = prefectures.document()
    new_doc.set({"id": 1, "name": "北海道"})
    logging.info(f"ドキュメントID: {new_doc.id}, データ: {new_doc.get()}")
    
    logging.info("明示的なIDでドキュメントを作成します")
    tokyo_doc = prefectures.document("tokyo")
    tokyo_doc.set({"id": 13, "name": "東京都"})
    logging.info(f"ドキュメントID: {tokyo_doc.id}, データ: {tokyo_doc.get()}")
    
    logging.info("add()メソッドでドキュメントを追加します")
    osaka_data = prefectures.add({"id": 27, "name": "大阪府"})
    logging.info(f"追加されたドキュメント: {osaka_data}")
    
    logging.info("ドキュメントを更新します")
    tokyo_doc.update({"population": 13960000})
    logging.info(f"更新後のデータ: {tokyo_doc.get()}")
    
    logging.info("マージオプションでドキュメントを設定します")
    tokyo_doc.set({"area": 2194}, merge=True)
    logging.info(f"マージ後のデータ: {tokyo_doc.get()}")
    
    logging.info("すべてのドキュメントを取得します")
    all_docs = prefectures.get()
    for doc in all_docs:
        logging.info(f"  {doc['id']}: {doc['name']}")
    
    if len(all_docs) > 0:
        logging.info("フィルタ付きクエリを実行します")
        filtered_docs = prefectures.where("id", ">", 10).get()
        logging.info(f"ID > 10のドキュメント数: {len(filtered_docs)}")
        for doc in filtered_docs:
            logging.info(f"  {doc['id']}: {doc['name']}")
    
    logging.info("ドキュメントを削除します")
    new_doc.delete()
    logging.info("ドキュメントが削除されました")
    
    remaining_docs = prefectures.get()
    logging.info(f"残りのドキュメント数: {len(remaining_docs)}")
    for doc in remaining_docs:
        logging.info(f"  {doc['id']}: {doc['name']}")
    
    logging.info("Firestoreライクなインターフェースの例を終了します")

if __name__ == "__main__":
    main()
