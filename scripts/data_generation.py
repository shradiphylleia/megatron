import time
import random
import psycopg2
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    dbname=os.getenv("DBNAME"),
    user=os.getenv("USER"),
    password=os.getenv("PASSWORD"),
    host=os.getenv("HOST"),
    port=os.getenv("PORT")
)

cur = conn.cursor()

while True:
    now = datetime.now()

    if random.random() > 0.3:  
        cur.execute("""
            INSERT INTO soil_nutrients_raw 
            (nitrogen, phosphorus, potassium, moisture, temperature, recorded_at)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            random.uniform(10, 50),
            random.uniform(5, 30),
            random.uniform(5, 30),
            random.uniform(30, 70),
            random.uniform(20, 35),
            now
        ))

    cur.execute("""
        INSERT INTO water_usage_raw 
        (water_level, flow_rate, irrigation_cycles, pump_status, recorded_at)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        random.uniform(100, 500),
        random.uniform(5, 20),
        random.randint(1, 5),
        random.choice(["ON", "OFF"]),
        now
    ))

    last_ping = now if random.random() > 0.4 else now - timedelta(hours=3)

    cur.execute("""
        INSERT INTO sensor_status 
        (sensor_id, sensor_type, status, last_ping)
        VALUES (%s, %s, %s, %s)
    """, (
        "S1",
        "soil",
        "active",
        last_ping
    ))

    conn.commit()
    print("Inserted batch at", now)
    time.sleep(5)