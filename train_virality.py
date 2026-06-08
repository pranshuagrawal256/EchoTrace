import sqlite3

conn = sqlite3.connect("database/echotrace.db")
cursor = conn.cursor()

cursor.execute("""
SELECT
    title,
    emotion_score,
    suspicion_score
FROM news
""")

rows = cursor.fetchall()

for row in rows:

    title = row[0]
    emotion = row[1]
    suspicion = row[2]

    title = str(title)

    virality = 0

    # headline length
    virality += min(len(title) // 5, 20)

    # emotion impact
    virality += emotion * 15

    # suspicion impact
    virality += suspicion // 2

    # question headlines
    if "?" in title:
        virality += 10

    # exclamation headlines
    if "!" in title:
        virality += 10

    # trending topics
    trending_words = [
        "trump",
        "musk",
        "nvidia",
        "ai",
        "openai",
        "tesla",
        "war",
        "china",
        "india",
        "election",
        "covid"
    ]

    title_lower = title.lower()

    for word in trending_words:

        if word in title_lower:
            virality += 15

    virality = min(100, virality)

    cursor.execute(
        """
        UPDATE news
        SET virality_score = ?
        WHERE title = ?
        """,
        (
            virality,
            title
        )
    )

    print(
        f"Virality: {virality} | {title}"
    )

conn.commit()
conn.close()

print("\nVirality Scores Updated!")