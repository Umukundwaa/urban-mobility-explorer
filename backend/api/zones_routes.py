# Routes for zone/borough lookup data
from flask import Blueprint, jsonify
import mysql.connector
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

zones_bp = Blueprint("zones", __name__)

def get_db():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

@zones_bp.route("/api/zones", methods=["GET"])
def get_zones():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM zones ORDER BY borough, zone_name")
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(results)

@zones_bp.route("/api/zones/boroughs", methods=["GET"])
def get_boroughs():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT DISTINCT borough FROM zones ORDER BY borough")
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(results)