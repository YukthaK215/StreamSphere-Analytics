from db_connection import get_connection

conn = get_connection()

cursor = conn.cursor()

query = """
SELECT
    v.title,
    COUNT(*) AS total_views
FROM watch_history w
JOIN videos v
ON w.video_id = v.video_id
GROUP BY v.title
ORDER BY total_views DESC;
"""

cursor.execute(query)

rows = cursor.fetchall()

print("\nTop Viewed Videos:\n")

for row in rows:
    print(row)

cursor.close()
conn.close()