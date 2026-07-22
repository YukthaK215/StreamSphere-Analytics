import psycopg2

def get_connection():
    return psycopg2.connect(
        "postgresql://neondb_owner:npg_Mx7LiwWmgGI5@ep-small-water-avg7m0um-pooler.c-11.us-east-1.aws.neon.tech/neondb?sslmode=require"
    )