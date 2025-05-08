"""
Firestore-like interface example for storekiss.

This example demonstrates how to use the Firestore-like interface
of the storekiss library with earthquake data.
"""
import json
import logkiss as logging
from pathlib import Path

from storekiss import (
    Firestore, 
    Schema, 
    StringField, 
    NumberField, 
    DateTimeField
)

def create_schema():
    """地震データのスキーマを作成します。すべてのフィールドにインデックスが付与されます。"""
    return Schema({
        "id": StringField(required=True, indexed=True),
        "time": DateTimeField(required=True, indexed=True),
        "latitude": NumberField(required=True, indexed=True),
        "longitude": NumberField(required=True, indexed=True),
        "depth": NumberField(required=True, min_value=0, indexed=True),
        "mag": NumberField(required=True, indexed=True),
        "place": StringField(required=True, indexed=True),
        "type": StringField(required=True, indexed=True)
    }, index_all_fields=True)  # すべてのフィールドにインデックスを付与

def load_earthquake_data():
    """地震データをJSONファイルから読み込みます。"""
    data_path = Path(__file__).parent / "earthquake_data.json"
    with open(data_path, "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    """メイン関数"""
    logging.info("Firestoreライクなインターフェースの例を開始します")
    
    schema = create_schema()
    store = Firestore(db_path=":memory:", schema=schema)
    
    earthquakes = store.get_collection("earthquakes")
    
    earthquake_data = load_earthquake_data()
    logging.info(f"{len(earthquake_data)}件の地震データを読み込みました")
    
    for quake in earthquake_data:
        doc = earthquakes.add(quake)
        logging.info(f"地震データを追加しました: {doc['id']} - {doc['place']}")
    
    
    results = earthquakes.where("mag", 5.2).get()
    logging.info(f"マグニチュード5.2の地震: {len(results)}件")
    for quake in results:
        logging.info(f"  {quake['id']} - {quake['place']} (M{quake['mag']})")
    
    results = earthquakes.where("place", "Honshu, Japan").get()
    logging.info(f"本州の地震: {len(results)}件")
    for quake in results:
        logging.info(f"  {quake['id']} - {quake['time']} (M{quake['mag']})")
    
    results = earthquakes.order_by("mag", direction="DESC").limit(2).get()
    logging.info("マグニチュード順（降順）の上位2件:")
    for quake in results:
        logging.info(f"  {quake['id']} - {quake['place']} (M{quake['mag']})")
    
    doc_id = earthquake_data[0]["id"]
    doc = earthquakes.doc(doc_id)
    quake_data = doc.get()
    logging.info(f"ドキュメント取得: {quake_data['id']} - {quake_data['place']}")
    
    updated = doc.update({"mag": 5.5, "updated": True})
    logging.info(f"ドキュメント更新: {updated['id']} - マグニチュード {updated['mag']}")
    
    updated_data = doc.get()
    logging.info(f"更新後のデータ: {updated_data['mag']} (更新フラグ: {updated_data.get('updated')})")
    
    count = earthquakes.count()
    logging.info(f"地震データの総数: {count}件")
    
    count = earthquakes.where("mag", 5.5).count()
    logging.info(f"マグニチュード5.5の地震: {count}件")
    
    doc.delete()
    logging.info(f"ドキュメント {doc_id} を削除しました")
    
    count = earthquakes.count()
    logging.info(f"削除後の地震データの総数: {count}件")
    
    logging.info("Firestoreライクなインターフェースの例を終了します")

if __name__ == "__main__":
    main()
