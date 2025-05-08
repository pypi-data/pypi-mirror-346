## firestoreの癖

- datetimeは数値として保存される
- timezone情報を保存したい場合は別フィールド追加

# 未確認

クエリの複雑な条件にはどういうものがある?

カテゴリ
できること
SDK でのポイント
典型的な落とし穴
---
複数フィールドの不等号（< > <= >=）
10 個までのフィールドに対して 同じクエリで 範囲／不等式を並べられる
2024 Q4 以降は 追加インデックス不要（自動作成）
order_by() を指定しないと速度が落ちる 
OR コンポジットフィルタ
A OR B OR (C AND D) のようなブール演算が 1 回の呼び出しで可能
Python では Filter.or_( … ) / Filter.and_( … ) を使う
NOT IN とは併用不可／ネストが深いと読みにくい 
IN / array‑contains‑any
1 フィールドに対し 最大 30 個の値セットを列挙できる（IN と array‑contains‑any を混在可）
複合 OR を擬似的に表現できる
array-contains-any は 配列長 × 値数 で読み取りコスト増 
NOT EQUAL / NOT IN
「◯◯ではない」をサーバ側でフィルタ
!= / not-in
フィールドが 存在しない ドキュメントは返らない 
コレクション‑グループ ＋ カーソル
サブコレクション全体を対象にstartAt()/endBefore() でページング
ルートに同名サブコレクションが複数あっても 1 回で検索可


# サブコレクションの実装方法

storekissライブラリでは、Firestoreのようなネイティブなサブコレクション機能がサポートされていないため、サブコレクションを模倣するための実装方法がいくつかあります。以下に主な実装方法を紹介します。

## 1. 親参照フィールドを持つ別コレクション

これは最もシンプルな方法で、子ドキュメントに親の参照情報を追加します。

```python
# 親コレクション
prefectures = db.collection("prefectures")

# 子コレクション
cities = db.collection("cities")

# 子ドキュメントに親の参照情報を追加
city_data = {
    "name": "新宿区",
    "prefecture_id": "tokyo",  # 親への参照
    "prefecture_name": "東京都"  # 冗長データ（検索効率化のため）
}

# ドキュメントIDに親IDを含める（オプション）
city_doc_id = f"{prefecture_id}_{city_id}"
cities.document(city_doc_id).set(city_data)
```

### メリット
- シンプルで理解しやすい
- クエリが直感的

### デメリット
- データの整合性を自分で管理する必要がある

## 2. パス区切り文字を使用したドキュメントID設計

```python
# 親コレクション
prefectures = db.collection("prefectures")

# 子ドキュメントのIDを親のパスを含めて設計
city_id = f"prefectures/{prefecture_id}/cities/{city_id}"
cities = db.collection("all_documents")
cities.document(city_id).set(city_data)
```

### メリット
- 単一のコレクションでパス構造を維持できる
- 階層が深くなっても対応可能

### デメリット
- IDが長くなる
- クエリが複雑になる可能性がある

## 3. ヘルパークラスの作成（最も推奨）

サブコレクションの概念をラップするヘルパークラスを作成することで、アプリケーションコードをよりクリーンにできます：

```python
class SubcollectionHelper:
    def __init__(self, db, parent_collection, parent_id, subcollection_name):
        self.db = db
        self.parent_collection = parent_collection
        self.parent_id = parent_id
        self.subcollection_name = subcollection_name
        self.collection = db.collection(f"{parent_collection}_{subcollection_name}")
    
    def document(self, doc_id=None):
        if doc_id is None:
            # 自動生成IDの場合
            return self.collection.document()
        else:
            # 親IDを含めたドキュメントID
            full_id = f"{self.parent_id}_{doc_id}"
            return self.collection.document(full_id)
    
    def add(self, data, doc_id=None):
        # 親への参照を自動追加
        data_with_ref = data.copy()
        data_with_ref[f"{self.parent_collection}_id"] = self.parent_id
        
        # ドキュメント追加
        doc_ref = self.document(doc_id)
        doc_ref.set(data_with_ref)
        return doc_ref
    
    def get(self):
        # 親IDに関連するドキュメントのみを取得
        all_docs = self.collection.get()
        return [doc for doc in all_docs if doc.get(f"{self.parent_collection}_id") == self.parent_id]
```

使用例：

```python
# 東京都の都市サブコレクションを取得
tokyo_cities = SubcollectionHelper(db, "prefectures", "tokyo", "cities")

# 都市を追加
tokyo_cities.add({"name": "新宿区", "population": 346235})

# 都市を取得
cities = tokyo_cities.get()
```

### メリット
- サブコレクションの概念をアプリケーションコードから抽象化
- 一貫性のある実装
- 拡張性が高い

### デメリット
- 追加のコードが必要

## 4. ドキュメント内にネストしたデータとして保存

小規模なサブコレクションの場合、親ドキュメント内にネストしたデータとして保存する方法もあります：

```python
prefecture_data = {
    "id": "tokyo",
    "name": "東京都",
    "population": 14047594,
    "cities": [
        {"id": "shinjuku", "name": "新宿区", "population": 346235},
        {"id": "shibuya", "name": "渋谷区", "population": 228906}
    ]
}

prefectures.document("tokyo").set(prefecture_data)
```

### メリット
- シンプルで直感的
- 一度に全データを取得できる

### デメリット
- サブコレクションが大きくなると非効率
- 部分更新が複雑になる

## 結論

最も推奨される方法は、**ヘルパークラスを作成する方法（方法3）**です。これにより、サブコレクションの概念をアプリケーションコードから抽象化し、一貫性のある実装を提供できます。また、将来的にstorekissライブラリがネイティブなサブコレクションをサポートした場合でも、ヘルパークラスの内部実装を変更するだけで対応できます。

小規模なアプリケーションでは、**親参照フィールドを持つ別コレクション（方法2）**も十分実用的です。現在のquickstart_2.pyの実装はこの方法を使用しており、多くの場合で十分に機能します。

# 未実装

- 認証、認可
- NOTIFICATION