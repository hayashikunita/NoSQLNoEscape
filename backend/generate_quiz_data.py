import json
from pathlib import Path

ROOT = Path(__file__).parent
DATA_PATH = ROOT / "quiz_data.json"
TARGETS = {"basic": 100, "standard": 50, "hard": 50}

# richer template pools per level to avoid同内容の連発
TEMPLATES = {
    "basic": [
        {
            "question": "[基礎] 全件取得のSQLはどれ？",
            "options": [
                "GET * FROM employees;",
                "SELECT * FROM employees;",
                "READ ALL employees;",
                "FETCH employees;",
            ],
            "answerIndex": 1,
            "explanation": "全件取得は SELECT * FROM <table>.",
        },
        {
            "question": "[基礎] id=10 を取得する正しいSQLはどれ？",
            "options": [
                "SELECT * FROM employees WHERE id = 10;",
                "SELECT * employees id 10;",
                "GET employees WHERE id 10;",
                "READ employees id=10;",
            ],
            "answerIndex": 0,
            "explanation": "条件は WHERE 句で書く。",
        },
        {
            "question": "[基礎] 価格を高い順に並べる ORDER BY はどれ？",
            "options": [
                "ORDER BY price ASC",
                "ORDER BY price DESC",
                "GROUP BY price DESC",
                "SORT price HIGH",
            ],
            "answerIndex": 1,
            "explanation": "DESC は降順、ASC は昇順。",
        },
        {
            "question": "[基礎] 重複行を除いて列を取得するキーワードは？",
            "options": ["ONLY", "DISTINCT", "UNIQUE ROWS", "ONCE"],
            "answerIndex": 1,
            "explanation": "重複排除は DISTINCT。",
        },
        {
            "question": "[基礎] 上位5件を返す一般的な書き方は？",
            "options": [
                "SELECT * FROM items LIMIT 5;",
                "SELECT TOP 5 FROM items;",
                "SELECT FIRST 5 items;",
                "SELECT * ITEMS(5);",
            ],
            "answerIndex": 0,
            "explanation": "MySQL/PG/SQLite では LIMIT, SQL Server は TOP。",
        },
        {
            "question": "[基礎] name が 'A' で始まる行を探す LIKE はどれ？",
            "options": [
                "LIKE '%A'",
                "LIKE 'A%'",
                "LIKE '%A%'",
                "LIKE '_A'",
            ],
            "answerIndex": 1,
            "explanation": "前方一致は 'A%'.",
        },
        {
            "question": "[基礎] 'abc' を含む行を探す LIKE はどれ？",
            "options": ["LIKE '%abc%'", "LIKE 'abc%'", "LIKE '%abc'", "LIKE '__abc'"],
            "answerIndex": 0,
            "explanation": "包含検索は %abc% 。",
        },
        {
            "question": "[基礎] 100〜500 を含む範囲検索は？",
            "options": [
                "WHERE price BETWEEN 100 AND 500",
                "WHERE price IN 100 TO 500",
                "WHERE price FROM 100 TO 500",
                "WHERE price RANGE 100 500",
            ],
            "answerIndex": 0,
            "explanation": "BETWEEN は両端を含む。",
        },
        {
            "question": "[基礎] 状態が new または done の行を取る条件は？",
            "options": [
                "WHERE status IN ('new','done')",
                "WHERE status = ('new','done')",
                "WHERE status HAS ('new','done')",
                "WHERE status ANY ('new','done')",
            ],
            "answerIndex": 0,
            "explanation": "複数値は IN (...) が簡潔。",
        },
        {
            "question": "[基礎] NULL 判定に使うのはどれ？",
            "options": ["= NULL", "IS NULL", "== NULL", "EQUAL NULL"],
            "answerIndex": 1,
            "explanation": "NULL 比較は IS NULL / IS NOT NULL。",
        },
        {
            "question": "[基礎] 行数を数える集計はどれ？",
            "options": ["SUM(*)", "COUNT(*)", "SIZE(*)", "TOTAL(*)"],
            "answerIndex": 1,
            "explanation": "行数は COUNT(*).",
        },
        {
            "question": "[基礎] 部署ごとに人数を出す句の組み合わせは？",
            "options": [
                "GROUP BY dept",
                "ORDER BY dept",
                "PARTITION dept",
                "SPLIT BY dept",
            ],
            "answerIndex": 0,
            "explanation": "集計の軸は GROUP BY で指定。",
        },
        {
            "question": "[基礎] 集計後に件数2以上に絞る句は？",
            "options": ["WHERE COUNT(*) >= 2", "HAVING COUNT(*) >= 2", "FILTER COUNT>=2", "AFTER COUNT>=2"],
            "answerIndex": 1,
            "explanation": "集計後の条件は HAVING。",
        },
        {
            "question": "[基礎] INNER JOIN の基本形はどれ？",
            "options": [
                "SELECT * FROM A JOIN B ON A.id = B.a_id;",
                "SELECT * FROM A, B;",
                "SELECT * FROM A UNION B;",
                "SELECT * FROM A ADD B;",
            ],
            "answerIndex": 0,
            "explanation": "結合条件は ON で書く。",
        },
        {
            "question": "[基礎] LEFT JOIN の説明として正しいものは？",
            "options": [
                "左表を残し右が無ければ NULL を入れる",
                "右表だけ残す",
                "両方に無い行も作る",
                "常に全組み合わせを返す",
            ],
            "answerIndex": 0,
            "explanation": "LEFT は左優先で欠損は NULL。",
        },
        {
            "question": "[基礎] UPDATE の正しい例はどれ？",
            "options": [
                "UPDATE items SET price = 500 WHERE id = 1;",
                "UPDATE items price 500 id 1;",
                "SET price=500 FROM items WHERE id=1;",
                "CHANGE items SET price=500 id=1;",
            ],
            "answerIndex": 0,
            "explanation": "UPDATE ... SET ... WHERE ... が基本。",
        },
        {
            "question": "[基礎] DELETE で全削除を避ける基本は？",
            "options": [
                "WHERE を付ける",
                "ORDER BY を付ける",
                "GROUP BY を付ける",
                "LIMIT を付けない",
            ],
            "answerIndex": 0,
            "explanation": "DELETE は WHERE なしで全削除になる。",
        },
        {
            "question": "[基礎] 複数行 INSERT の書き方はどれ？",
            "options": [
                "INSERT INTO items (a,b) VALUES (1,'x'), (2,'y');",
                "INSERT items (1,'x')(2,'y');",
                "INSERT ALL items VALUES (1,'x')(2,'y');",
                "ADD items VALUES (1,'x'), (2,'y');",
            ],
            "answerIndex": 0,
            "explanation": "VALUES (...) をカンマ区切りで並べる。",
        },
        {
            "question": "[基礎] シンプルなテーブル作成の書き方はどれ？",
            "options": [
                "CREATE TABLE items (id INT PRIMARY KEY, name TEXT);",
                "MAKE TABLE items id int, name text;",
                "NEW TABLE items WITH id,name;",
                "TABLE items CREATE();",
            ],
            "answerIndex": 0,
            "explanation": "CREATE TABLE <name> (<col defs>) が基本。",
        },
        {
            "question": "[基礎] 主キーの性質として正しいものは？",
            "options": [
                "一意かつ NOT NULL",
                "NULL を許す",
                "重複してよい",
                "文字列のみ可能",
            ],
            "answerIndex": 0,
            "explanation": "PRIMARY KEY は一意 & NOT NULL。",
        },
        {
            "question": "[基礎] インデックスを張る基本的な理由は？",
            "options": [
                "検索を速くする",
                "ストレージを減らす",
                "行を暗号化する",
                "順序をランダムにする",
            ],
            "answerIndex": 0,
            "explanation": "索引は検索・並び替えを高速化する。",
        },
    ],
    "standard": [
        {
            "question": "[標準] ROW_NUMBER() の典型的な使い方は？",
            "options": [
                "PARTITION BY でグループ内順位を付ける",
                "行を削除する",
                "テーブルを作る",
                "ロックを取得する",
            ],
            "answerIndex": 0,
            "explanation": "ROW_NUMBER() OVER(PARTITION BY ... ORDER BY ...) で順位付け。",
        },
        {
            "question": "[標準] LEFT JOIN と INNER JOIN の差は？",
            "options": [
                "LEFT は左表を残し無ければ NULL",
                "INNER は左表だけ残す",
                "LEFT は常に全組み合わせ",
                "INNER は NULL を作る",
            ],
            "answerIndex": 0,
            "explanation": "LEFT は左優先。INNER は一致行のみ。",
        },
        {
            "question": "[標準] 前方ワイルドカード LIKE '%abc' が遅くなる理由は？",
            "options": [
                "先頭が不定でインデックスを使いにくい",
                "文字列長が長い",
                "必ずソートが走る",
                "実行計画が作れない",
            ],
            "answerIndex": 0,
            "explanation": "前方が不定だと B-Tree を使いづらい。",
        },
        {
            "question": "[標準] READ COMMITTED の特徴は？",
            "options": [
                "未コミットを読まないが再読で変わりうる",
                "未コミットを読む",
                "常に同じスナップショット",
                "書き込みは即時見える",
            ],
            "answerIndex": 0,
            "explanation": "非再現読込が起きる可能性がある。",
        },
        {
            "question": "[標準] 大量 INSERT で有効な施策は？",
            "options": [
                "不要なインデックスを一時的に外す",
                "毎行 COMMIT する",
                "SELECT * を多用する",
                "全文検索を張る",
            ],
            "answerIndex": 0,
            "explanation": "インデックス更新コストを減らすと速い。",
        },
    ],
    "hard": [
        {
            "question": "[難問] 3行移動平均を出すウィンドウ句は？",
            "options": [
                "AVG(val) OVER(ORDER BY ts ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)",
                "AVG(val) OVER()",
                "SUM(val) GROUP BY ts",
                "MEDIAN(val) OVER()",
            ],
            "answerIndex": 0,
            "explanation": "ROWS BETWEEN 2 PRECEDING AND CURRENT ROW で直近3行。",
        },
        {
            "question": "[難問] デッドロック回避の基本は？",
            "options": [
                "ロック取得順序を統一",
                "常に FULL OUTER JOIN",
                "SELECT * を使う",
                "トランザクションを長くする",
            ],
            "answerIndex": 0,
            "explanation": "同じ順序でロックすると循環待ちを減らせる。",
        },
        {
            "question": "[難問] Hash Join が選ばれやすいのは？",
            "options": [
                "両テーブルが中〜大規模で結合キーに索引がない",
                "両方が極小",
                "必ず ORDER BY がある",
                "結合キーが真偽値のみ",
            ],
            "answerIndex": 0,
            "explanation": "大きめ同士でハッシュ結合が効きやすい。",
        },
        {
            "question": "[難問] 遅いクエリ調査の第一歩は？",
            "options": [
                "EXPLAIN (ANALYZE) で計画を見る",
                "DB 再起動",
                "全インデックス削除",
                "文字列をすべて TEXT にする",
            ],
            "answerIndex": 0,
            "explanation": "まず計画と実測行数・時間を見る。",
        },
        {
            "question": "[難問] レプリカ遅延緩和の策は？",
            "options": [
                "適用スレッドや I/O を増強",
                "書き込みをレプリカに送る",
                "全インデックス削除",
                "トランザクションを極端に長くする",
            ],
            "answerIndex": 0,
            "explanation": "適用ボトルネックを緩和するのが一般的。",
        },
    ],
}


def pick_template(level: str, idx: int):
    templates = TEMPLATES[level]
    return templates[(idx - 1) % len(templates)]

def main():
    if not DATA_PATH.exists():
        raise SystemExit(f"quiz_data.json not found: {DATA_PATH}")

    with DATA_PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)

    # drop existing basic to avoid重複; keep others
    existing = {item["id"]: item for item in data if item.get("level") != "basic"}

    for level, target in TARGETS.items():
        existing_ids = [qid for qid in existing if qid.startswith(f"{level}-")]
        start = 1
        if existing_ids:
            nums = []
            for qid in existing_ids:
                try:
                    nums.append(int(qid.split("-")[-1]))
                except ValueError:
                    continue
            if nums:
                start = max(nums) + 1

        current_count = sum(1 for v in existing.values() if v.get("level") == level)
        needed = target - current_count
        for i in range(needed):
            idx = start + i
            qid = f"{level}-{idx:03d}"
            tpl = pick_template(level, idx)
            item = {
                "id": qid,
                "level": level,
                "question": tpl["question"].format(n=idx),
                "options": list(tpl["options"]),
                "answerIndex": tpl["answerIndex"],
                "explanation": tpl["explanation"],
            }
            existing[qid] = item

    # sort by level then id
    def sort_key(item):
        level_order = {"basic": 0, "standard": 1, "hard": 2}
        level = item.get("level", "zzz")
        return (level_order.get(level, 99), item.get("id", ""))

    new_data = sorted(existing.values(), key=sort_key)

    with DATA_PATH.open("w", encoding="utf-8") as f:
        json.dump(new_data, f, ensure_ascii=False, indent=2)

    print("Generated quiz_data.json")
    for level, target in TARGETS.items():
        count = sum(1 for v in new_data if v.get("level") == level)
        print(f"{level}: {count}")

if __name__ == "__main__":
    main()
