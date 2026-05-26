from flask import Flask, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route("/format", methods=["POST"])
def format_transcript():
    data = request.json
    transcript = data.get("transcript", "").strip()
    caller_number = data.get("caller_number", "Unknown")
    timestamp = data.get("timestamp", "")

    try:
        dt_utc = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        dt_pacific = dt_utc - timedelta(hours=7)
        formatted_time = dt_pacific.strftime("%B %d, %Y at %I:%M %p Pacific Time")
    except Exception:
        formatted_time = timestamp if timestamp else "Unknown"

    clean_transcript = transcript.replace("AI:", "Heidi:").replace("User:", "Caller:")

    if not clean_transcript:
        clean_transcript = "[No transcript available]"

    body = f"""New Incoming Call — Focus for NonProfits
=============================================

Date/Time:     {formatted_time}
Caller Number: {caller_number}

CONVERSATION TRANSCRIPT
---------------------------------------------
{clean_transcript}
---------------------------------------------

Full call log: https://dashboard.vapi.ai/logs
"""
    return jsonify({"formatted": body})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
