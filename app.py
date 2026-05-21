from flask import Flask, request, jsonify
import ast
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route("/format", methods=["POST"])
def format_transcript():
    data = request.json
    raw_messages = data.get("messages", "")
    caller_number = data.get("caller_number", "Unknown")
    timestamp = data.get("timestamp", "")

    try:
        dt_utc = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        dt_pacific = dt_utc - timedelta(hours=7)
        formatted_time = dt_pacific.strftime("%B %d, %Y at %I:%M %p Pacific Time")
    except Exception:
        formatted_time = timestamp

    try:
        messages = ast.literal_eval(raw_messages)
    except Exception:
        return jsonify({"formatted": f"Could not parse transcript.\n\nRaw:\n{raw_messages}"})

    lines = []
    for msg in messages:
        role = msg.get("role", "")
        content = msg.get("content", "")
        if role == "system":
            continue
        elif role == "assistant":
            if content:
                lines.append(f"Heidi:  {content}")
            elif msg.get("tool_calls"):
                lines.append("Heidi:  [Initiated call transfer to Brad Yochum]")
        elif role == "user" and content:
            lines.append(f"Caller: {content}")

    transcript = "\n".join(lines)

    body = f"""New Incoming Call — Focus for NonProfits
=============================================

Date/Time:     {formatted_time}
Caller Number: {caller_number}

CONVERSATION TRANSCRIPT
---------------------------------------------
{transcript}
---------------------------------------------

Full call log: https://dashboard.vapi.ai/logs
"""
    return jsonify({"formatted": body})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
