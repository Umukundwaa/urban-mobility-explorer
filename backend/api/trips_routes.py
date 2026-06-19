# Routes for querying/filtering trip records
from flask import Blueprint, jsonify, request
import mysql.connector
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

trips_bp = Blueprint("trips", __name__)

def get_db():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

@trips_bp.route("/api/trips", methods=["GET"])
def get_trips():
    limit = request.args.get("limit", 100)
    borough = request.args.get("borough", None)
    time_of_day = request.args.get("time_of_day", None)

    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    query = """
            SELECT t.trip_id, t.pickup_datetime, t.dropoff_datetime,
                   t.trip_distance, t.fare_amount, t.total_amount,
                   t.trip_duration_minutes, t.fare_per_mile, t.time_of_day,
                   p.borough as pickup_borough, p.zone_name as pickup_zone,
                   d.borough as dropoff_borough, d.zone_name as dropoff_zone
            FROM trips t
                     LEFT JOIN zones p ON t.pickup_location_id = p.location_id
                     LEFT JOIN zones d ON t.dropoff_location_id = d.location_id
            WHERE 1=1 \
            """
    params = []

    if borough:
        query += " AND p.borough = %s"
        params.append(borough)

    if time_of_day:
        query += " AND t.time_of_day = %s"
        params.append(time_of_day)

    query += " LIMIT %s"
    params.append(int(limit))

    cursor.execute(query, params)
    results = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify(results)