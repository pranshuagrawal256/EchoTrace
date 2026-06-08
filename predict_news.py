import sqlite3
import joblib

print("Loading model...")

# Load trained model
model = joblib.load(
    "models/fake_news_model.pkl"
)

vectorizer = joblib.load(
    "models/vectorizer.pkl"
)

# Connect database
conn = sqlite3.connect(
    "database/echotrace.db"
)

cursor = conn.cursor()

# Get news articles
cursor.execute("""
SELECT
    id,
    title,
    description,
    content
FROM news
""")

rows = cursor.fetchall()

print(f"\nFound {len(rows)} articles\n")

real_count = 0
fake_count = 0

for row in rows:

    news_id = row[0]

    title = row[1] or ""
    description = row[2] or ""
    content = row[3] or ""

    # Combine all available text
    full_text = (
        title + " " +
        description + " " +
        content
    )

    # Skip empty records
    if full_text.strip() == "":
        continue

    vector = vectorizer.transform(
        [full_text]
    )

    prediction = model.predict(
        vector
    )[0]

    if prediction == 1:

        result = "REAL"
        real_count += 1

    else:

        result = "FAKE"
        fake_count += 1

    cursor.execute(
        """
        UPDATE news
        SET prediction = ?
        WHERE id = ?
        """,
        (
            result,
            news_id
        )
    )

    print(title)
    print("Prediction:", result)
    print("-" * 60)

conn.commit()

print("\nPrediction Summary")
print("-" * 30)
print("REAL :", real_count)
print("FAKE :", fake_count)

conn.close()

print("\nDatabase Updated Successfully!")