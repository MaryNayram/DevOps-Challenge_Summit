"""
Controller for Fitness Class Routes
"""
from flask import jsonify, url_for, abort
from service import app
from service.common import status

CLASS_SESSIONS = {}


############################################################
# Health Check Endpoint
############################################################
@app.route("/health", methods=["GET"])
def health_check():
    """Simple health check"""
    return jsonify(dict(status="Running ✅")), status.HTTP_200_OK


############################################################
# Home Page Endpoint
############################################################
@app.route("/", methods=["GET"])
def homepage():
    """Welcome message with API info"""
    app.logger.info("⚡ Accessed API Home")
    return jsonify(
        status=status.HTTP_200_OK,
        message="Welcome to the Fitness Class Booking System!",
        version="2.0.0",
        documentation=url_for("get_all_classes", _external=True),
    )


############################################################
# Retrieve All Classes
############################################################
@app.route("/classes", methods=["GET"])
def get_all_classes():
    """Lists all class session counters"""
    app.logger.info("📋 Listing all fitness class sessions")
    sessions = [dict(class_name=name, booked=val) for name, val in CLASS_SESSIONS.items()]
    return jsonify(sessions), status.HTTP_200_OK


############################################################
# Create New Class
############################################################
@app.route("/classes/<class_name>", methods=["POST"])
def create_class(class_name):
    """Creates a new fitness class"""
    app.logger.info("🆕 Creating new class: %s", class_name)

    if class_name in CLASS_SESSIONS:
        abort(status.HTTP_409_CONFLICT, f"Class '{class_name}' already exists.")

    CLASS_SESSIONS[class_name] = 0
    location_url = url_for("get_class", class_name=class_name, _external=True)
    return (
        jsonify(class_name=class_name, booked=0),
        status.HTTP_201_CREATED,
        {"Location": location_url},
    )


############################################################
# Get Class Info
############################################################
@app.route("/classes/<class_name>", methods=["GET"])
def get_class(class_name):
    """Retrieves booking count for a class"""
    app.logger.info("🔍 Fetching class info: %s", class_name)

    if class_name not in CLASS_SESSIONS:
        abort(status.HTTP_404_NOT_FOUND, f"Class '{class_name}' not found.")

    return jsonify(class_name=class_name, booked=CLASS_SESSIONS[class_name])


############################################################
# Book a Spot (Increment)
############################################################
@app.route("/classes/<class_name>/book", methods=["PUT"])
def book_spot(class_name):
    """Book a spot in the class (increments count)"""
    app.logger.info("📈 Booking a spot in: %s", class_name)

    if class_name not in CLASS_SESSIONS:
        abort(status.HTTP_404_NOT_FOUND, f"Class '{class_name}' not found.")

    CLASS_SESSIONS[class_name] += 1
    return jsonify(class_name=class_name, booked=CLASS_SESSIONS[class_name])


############################################################
# Cancel Class
############################################################
@app.route("/classes/<class_name>", methods=["DELETE"])
def cancel_class(class_name):
    """Cancels a fitness class (removes from schedule)"""
    app.logger.info("❌ Canceling class: %s", class_name)

    if class_name in CLASS_SESSIONS:
        CLASS_SESSIONS.pop(class_name)

    return "", status.HTTP_204_NO_CONTENT


############################################################
# Testing Utility
############################################################
def reset_classes():
    """Reset class session counters during testing"""
    global CLASS_SESSIONS  # noqa: PLW0603
    if app.testing:
        CLASS_SESSIONS = {}
