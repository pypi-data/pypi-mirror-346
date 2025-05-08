"""
storekiss CRUDライブラリを使用した地震データの例。

この例は以下を示しています：
1. datetime検証を持つスキーマの作成
2. JSONからの地震データの読み込み
3. datetime変換を含むデータの保存と取得
4. 地震データの検索
"""
import json
import datetime
from pathlib import Path
from pprint import pprint
import logkiss as logging

from storekiss import firestore
from storekiss.validation import (
    Schema, StringField, NumberField, DateTimeField, ValidationError
)

earthquake_schema = Schema({
    "id": StringField(required=True),
    "time": DateTimeField(required=True),  # ISO文字列をdatetimeに変換
    "latitude": NumberField(required=True),
    "longitude": NumberField(required=True),
    "depth": NumberField(required=True, min_value=0),
    "mag": NumberField(required=True),
    "place": StringField(required=True),
    "type": StringField(required=True)
})

def load_earthquake_data():
    """JSONファイルから地震データを読み込む。"""
    data_path = Path(__file__).parent / "earthquake_data.json"
    with open(data_path, "r") as f:
        return json.load(f)

def main():
    """地震データの例を実行する。"""
    logging.info("地震データベースを作成中...")
    db = firestore.client(
        db_path="earthquakes.db",  # ファイルベースのデータベースを使用
        collection="earthquakes",
        schema=earthquake_schema
    )
    store = db
    
    earthquakes = load_earthquake_data()
    logging.info(f"JSONから{len(earthquakes)}件の地震データを読み込みました")
    
    for quake in earthquakes:
        try:
            stored = store.create(quake, id=quake["id"])
            logging.info(f"地震データを保存しました: {stored['id']} - {stored['place']}")
            
            logging.info(f"  時間: {stored['time']} (型: {type(stored['time']).__name__})")
        except ValidationError as e:
            logging.error(f"{quake['id']}の検証エラー: {e}")
    
    logging.info("すべての地震データを取得:")
    all_quakes = store.list()
    for quake in all_quakes:
        time_str = quake["time"].strftime("%Y-%m-%d %H:%M:%S")
        logging.info(f"{quake['id']} - {time_str} - マグニチュード {quake['mag']} - {quake['place']}")
    
    logging.info("マグニチュード5.0以上の地震を検索:")
    strong_quakes = []
    for quake in all_quakes:
        if quake["mag"] >= 5.0:
            strong_quakes.append(quake)
    
    for quake in strong_quakes:
        time_str = quake["time"].strftime("%Y-%m-%d %H:%M:%S")
        logging.info(f"{quake['id']} - {time_str} - マグニチュード {quake['mag']} - {quake['place']}")
    
    logging.info("日本の地震を検索:")
    japan_quakes = []
    for quake in all_quakes:
        if "Japan" in quake["place"]:
            japan_quakes.append(quake)
    
    for quake in japan_quakes:
        time_str = quake["time"].strftime("%Y-%m-%d %H:%M:%S")
        logging.info(f"{quake['id']} - {time_str} - マグニチュード {quake['mag']} - {quake['place']}")
    
    logging.info("東京の地震データに追加情報を更新:")
    tokyo_id = "us7000joqp"
    try:
        tokyo_quake = store.read(tokyo_id)
        
        updated = store.update(tokyo_id, {
            "felt": 1200,  # 地震を感じた人の数
            "tsunami": False,  # 津波警報が発令されたかどうか
            "updated": datetime.datetime.now()  # このレコードが更新された時間
        })
        
        logging.info("東京の地震データを更新しました:")
        logging.info(f"{updated}")
    except ValidationError as e:
        logging.error(f"検証エラー: {e}")
    
    logging.info("地震レコードの削除:")
    tonga_id = "us6000l9r3"
    store.delete(tonga_id)
    logging.info(f"地震データ {tonga_id} を削除しました")
    
    try:
        store.read(tonga_id)
        logging.error("エラー: レコードがまだ存在しています!")
    except Exception as e:
        logging.info(f"確認成功: {e}")
    
    count = store.count()
    logging.info(f"残りの地震レコード数: {count}")

if __name__ == "__main__":
    main()
