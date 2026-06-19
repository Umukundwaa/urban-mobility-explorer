# Routes that expose aggregated insights (uses the custom algorithm)
from flask import Blueprint, jsonify
import mysql.connector
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME
from algorithms.top_zones import get_top_zones

insights_bp = Blueprint("insights", __name__)

def get_db():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

@insights_bp.route("/api/insights/top-zones", methods=["GET"])
def top_zones():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT p.borough as borough, COUNT(*) as trip_count
        FROM trips t
        LEFT JOIN zones p ON t.pickup_location_id = p.location_id
        GROUP BY p.borough
    """)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    result = get_top_zones(data, k=5)
    return jsonify(result)

@insights_bp.route("/api/insights/avg-fare-by-time", methods=["GET"])
def avg_fare_by_time():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT time_of_day,
               ROUND(AVG(fare_amount), 2) as avg_fare,
               ROUND(AVG(trip_duration_minutes), 2) as avg_duration,
               COUNT(*) as total_trips
        FROM trips
        GROUP BY time_of_day
        ORDER BY avg_fare DESC
    """)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(results)

@insights_bp.route("/api/insights/payment-types", methods=["GET"])
def payment_types():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT payment_type,
               COUNT(*) as count,
               ROUND(AVG(tip_amount), 2) as avg_tip
        FROM trips
        GROUP BY payment_type
        ORDER BY count DESC
    """)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(results)