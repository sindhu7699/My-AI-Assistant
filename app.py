from flask import Flask, render_template_string, request
from alpha import AlphaAgent


app = Flask(__name__)
agent = AlphaAgent()

HTML_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Alpha Incident Agent</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 40px;
            background: #f4f6f8;
            color: #1f2937;
        }
        .container {
            max-width: 1000px;
            margin: auto;
            background: white;
            padding: 24px;
            border-radius: 12px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        }
        h1 {
            margin-top: 0;
        }
        form {
            display: flex;
            gap: 12px;
            margin-bottom: 24px;
        }
        input[type=text] {
            flex: 1;
            padding: 12px;
            font-size: 16px;
        }
        button {
            padding: 12px 18px;
            font-size: 16px;
            background: #0f62fe;
            color: white;
            border: 0;
            border-radius: 6px;
            cursor: pointer;
        }
        .error {
            color: #b91c1c;
            margin-bottom: 16px;
        }
        .card {
            border: 1px solid #d1d5db;
            border-radius: 8px;
            padding: 16px;
            margin-bottom: 16px;
            background: #fafafa;
        }
        .pill {
            display: inline-block;
            padding: 4px 10px;
            border-radius: 999px;
            background: #e5e7eb;
            margin-right: 8px;
            font-size: 12px;
        }
        ul {
            margin-top: 8px;
        }
        pre {
            white-space: pre-wrap;
            word-break: break-word;
            background: #111827;
            color: #f9fafb;
            padding: 12px;
            border-radius: 8px;
        }
        .p1 {
            background: #fee2e2;
            color: #991b1b;
        }
    </style>
</head>
<body>
<div class="container">
    <h1>Alpha Incident Investigation Agent</h1>
    <p>Enter a ServiceNow incident number to generate a first-pass investigation report.</p>

    <form method="post">
        <input type="text" name="incident_number" placeholder="e.g. INC1002" value="{{ incident_number or '' }}" required>
        <button type="submit">Investigate</button>
    </form>

    {% if error %}
        <div class="error"><strong>Error:</strong> {{ error }}</div>
    {% endif %}

    {% if result %}
        <div class="card">
            <h2>Incident Overview</h2>
            <div>
                <span class="pill">{{ result.incident_number }}</span>
                <span class="pill">{{ result.incident_type }}</span>
                {% if result.engineer_report.probable_p1 %}
                    <span class="pill p1">Probable P1</span>
                {% endif %}
            </div>
            <p><strong>Summary:</strong> {{ result.engineer_report.summary }}</p>
            <p><strong>Suspected Root Cause:</strong> {{ result.engineer_report.suspected_root_cause }}</p>
            <p><strong>Confidence:</strong> {{ result.engineer_report.confidence }}</p>
        </div>

        <div class="card">
            <h2>Evidence</h2>
            <ul>
                {% for item in result.engineer_report.evidence %}
                    <li>{{ item }}</li>
                {% endfor %}
            </ul>
        </div>

        <div class="card">
            <h2>Impacted Resources</h2>
            <ul>
                {% for item in result.engineer_report.impacted_resources %}
                    <li>{{ item }}</li>
                {% endfor %}
            </ul>
        </div>

        <div class="card">
            <h2>Recommended Next Steps</h2>
            <ul>
                {% for item in result.engineer_report.recommended_next_steps %}
                    <li>{{ item }}</li>
                {% endfor %}
            </ul>
        </div>

        {% if result.engineer_report.escalation_message %}
        <div class="card">
            <h2>Escalation Message</h2>
            <p>{{ result.engineer_report.escalation_message }}</p>
        </div>
        {% endif %}

        <div class="card">
            <h2>Manager Summary</h2>
            <pre>{{ result.manager_summary }}</pre>
        </div>

        <div class="card">
            <h2>Notifications</h2>
            <p><strong>Slack:</strong> {{ result.notification.slack }}</p>
            <p><strong>Email:</strong> {{ result.notification.email }}</p>
        </div>
    {% endif %}
</div>
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None
    incident_number = ""

    if request.method == "POST":
        incident_number = request.form.get("incident_number", "").strip()
        try:
            result = agent.investigate(incident_number)
        except Exception as exc:
            error = str(exc)

    return render_template_string(
        HTML_TEMPLATE,
        result=result,
        error=error,
        incident_number=incident_number,
    )


if __name__ == "__main__":
    app.run(debug=True)

# Made with Bob
