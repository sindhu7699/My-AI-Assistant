from flask import Flask, render_template_string, request
from alpha import AlphaAgent


app = Flask(__name__)
agent = AlphaAgent()

HTML_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>JARVIS Command Center</title>
    <style>
        :root {
            --bg-0: #030711;
            --bg-1: #071120;
            --bg-2: #0a1830;
            --panel: rgba(7, 16, 32, 0.72);
            --panel-strong: rgba(10, 21, 42, 0.9);
            --border: rgba(103, 232, 249, 0.16);
            --glow: rgba(34, 211, 238, 0.35);
            --text: #e6f7ff;
            --muted: #89a9bf;
            --cyan: #22d3ee;
            --blue: #60a5fa;
            --violet: #8b5cf6;
            --green: #34d399;
            --amber: #f59e0b;
            --red: #f87171;
            --shadow: 0 25px 70px rgba(0, 0, 0, 0.45);
        }

        * {
            box-sizing: border-box;
        }

        html {
            scroll-behavior: smooth;
        }

        body {
            margin: 0;
            color: var(--text);
            font-family: Inter, Segoe UI, Arial, sans-serif;
            background:
                radial-gradient(circle at 10% 10%, rgba(34, 211, 238, 0.12), transparent 26%),
                radial-gradient(circle at 90% 14%, rgba(139, 92, 246, 0.12), transparent 26%),
                radial-gradient(circle at 50% 100%, rgba(96, 165, 250, 0.08), transparent 30%),
                linear-gradient(180deg, var(--bg-0) 0%, var(--bg-1) 40%, var(--bg-2) 100%);
            min-height: 100vh;
            overflow-x: hidden;
        }

        body::before {
            content: "";
            position: fixed;
            inset: 0;
            background-image:
                linear-gradient(rgba(34, 211, 238, 0.05) 1px, transparent 1px),
                linear-gradient(90deg, rgba(34, 211, 238, 0.05) 1px, transparent 1px);
            background-size: 44px 44px;
            mask-image: radial-gradient(circle at center, black 35%, transparent 82%);
            pointer-events: none;
            opacity: 0.35;
        }

        .page {
            max-width: 1440px;
            margin: 0 auto;
            padding: 28px 24px 42px;
            position: relative;
            z-index: 1;
        }

        .topbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 18px 22px;
            margin-bottom: 22px;
            border: 1px solid var(--border);
            border-radius: 22px;
            background: rgba(5, 12, 24, 0.72);
            backdrop-filter: blur(16px);
            box-shadow: var(--shadow);
        }

        .brand {
            display: flex;
            align-items: center;
            gap: 16px;
        }

        .brand-mark {
            width: 56px;
            height: 56px;
            border-radius: 18px;
            position: relative;
            background:
                radial-gradient(circle at 50% 50%, rgba(34, 211, 238, 0.28), rgba(34, 211, 238, 0.04) 55%, transparent 68%),
                linear-gradient(135deg, rgba(34, 211, 238, 0.15), rgba(96, 165, 250, 0.14));
            border: 1px solid rgba(34, 211, 238, 0.28);
            box-shadow:
                0 0 0 1px rgba(34, 211, 238, 0.12) inset,
                0 0 30px rgba(34, 211, 238, 0.18);
        }

        .brand-mark::before,
        .brand-mark::after {
            content: "";
            position: absolute;
            inset: 11px;
            border-radius: 50%;
            border: 1px solid rgba(34, 211, 238, 0.34);
        }

        .brand-mark::after {
            inset: 18px;
            background: radial-gradient(circle, rgba(34, 211, 238, 0.65), transparent 70%);
            border: none;
        }

        .brand-text h1 {
            margin: 0;
            font-size: 26px;
            letter-spacing: 0.24em;
            font-weight: 800;
        }

        .brand-text p {
            margin: 5px 0 0;
            color: var(--muted);
            font-size: 13px;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }

        .status-strip {
            display: flex;
            gap: 12px;
            flex-wrap: wrap;
            justify-content: flex-end;
        }

        .status-pill {
            padding: 10px 14px;
            border-radius: 999px;
            border: 1px solid rgba(34, 211, 238, 0.18);
            background: rgba(10, 22, 42, 0.72);
            color: #c9f7ff;
            font-size: 12px;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }

        .hero {
            display: grid;
            grid-template-columns: 1.25fr 0.75fr;
            gap: 22px;
            margin-bottom: 22px;
        }

        .hero-panel,
        .side-panel,
        .module,
        .signal-panel {
            background: var(--panel);
            border: 1px solid var(--border);
            border-radius: 26px;
            backdrop-filter: blur(18px);
            box-shadow: var(--shadow);
            position: relative;
            overflow: hidden;
        }

        .hero-panel::before,
        .side-panel::before,
        .module::before,
        .signal-panel::before {
            content: "";
            position: absolute;
            inset: 0;
            background: linear-gradient(120deg, rgba(34, 211, 238, 0.04), transparent 38%, rgba(139, 92, 246, 0.04));
            pointer-events: none;
        }

        .hero-panel {
            padding: 30px;
        }

        .kicker {
            display: inline-flex;
            align-items: center;
            gap: 10px;
            padding: 8px 14px;
            border-radius: 999px;
            background: rgba(34, 211, 238, 0.12);
            border: 1px solid rgba(34, 211, 238, 0.18);
            color: #c8fbff;
            font-size: 12px;
            letter-spacing: 0.12em;
            text-transform: uppercase;
        }

        .hero-panel h2 {
            font-size: 46px;
            line-height: 1.02;
            margin: 18px 0 16px;
            max-width: 760px;
        }

        .hero-panel p {
            margin: 0;
            max-width: 760px;
            color: var(--muted);
            font-size: 16px;
            line-height: 1.7;
        }

        .command-form {
            margin-top: 28px;
            display: grid;
            grid-template-columns: 1fr auto;
            gap: 14px;
        }

        .input-shell {
            position: relative;
            border-radius: 22px;
            padding: 1px;
            background: linear-gradient(135deg, rgba(34, 211, 238, 0.4), rgba(96, 165, 250, 0.14), rgba(139, 92, 246, 0.4));
        }

        .input-shell input {
            width: 100%;
            border: none;
            outline: none;
            border-radius: 21px;
            padding: 20px 20px;
            background: rgba(3, 9, 20, 0.96);
            color: var(--text);
            font-size: 17px;
            letter-spacing: 0.04em;
        }

        .input-help {
            margin-top: 10px;
            color: var(--muted);
            font-size: 13px;
        }

        .command-btn {
            border: none;
            border-radius: 22px;
            min-width: 220px;
            padding: 0 24px;
            cursor: pointer;
            color: #03111f;
            font-size: 15px;
            font-weight: 800;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            background: linear-gradient(135deg, #67e8f9, #60a5fa 55%, #8b5cf6);
            box-shadow:
                0 0 0 1px rgba(255, 255, 255, 0.08) inset,
                0 18px 40px rgba(34, 211, 238, 0.22);
        }

        .command-btn:hover {
            transform: translateY(-1px);
            filter: brightness(1.03);
        }

        .hero-stats {
            margin-top: 24px;
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
        }

        .mini-stat {
            min-width: 180px;
            padding: 14px 16px;
            border-radius: 18px;
            background: rgba(7, 18, 35, 0.86);
            border: 1px solid rgba(34, 211, 238, 0.1);
        }

        .mini-stat span {
            display: block;
        }

        .mini-stat .label {
            color: var(--muted);
            font-size: 11px;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            margin-bottom: 6px;
        }

        .mini-stat .value {
            font-size: 18px;
            font-weight: 700;
        }

        .side-panel {
            padding: 26px;
            display: grid;
            gap: 16px;
            align-content: start;
        }

        .panel-title {
            margin: 0;
            font-size: 18px;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }

        .system-card {
            padding: 18px;
            border-radius: 20px;
            background: rgba(6, 16, 30, 0.86);
            border: 1px solid rgba(34, 211, 238, 0.08);
        }

        .system-card strong {
            display: block;
            margin-bottom: 8px;
            font-size: 15px;
        }

        .system-card p {
            margin: 0;
            color: var(--muted);
            line-height: 1.6;
            font-size: 14px;
        }

        .error {
            margin-bottom: 20px;
            padding: 18px 20px;
            border-radius: 20px;
            border: 1px solid rgba(248, 113, 113, 0.24);
            background: rgba(80, 18, 26, 0.42);
            color: #ffd6d6;
            box-shadow: 0 10px 30px rgba(127, 29, 29, 0.18);
        }

        .dashboard {
            display: grid;
            grid-template-columns: 1.15fr 0.85fr;
            gap: 22px;
            margin-top: 6px;
        }

        .stack {
            display: grid;
            gap: 22px;
        }

        .module {
            padding: 24px;
        }

        .module-header {
            display: flex;
            justify-content: space-between;
            align-items: start;
            gap: 16px;
            margin-bottom: 18px;
        }

        .module-header h3 {
            margin: 0 0 6px;
            font-size: 22px;
        }

        .module-subtitle {
            color: var(--muted);
            font-size: 13px;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }

        .chips {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }

        .chip {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 9px 13px;
            border-radius: 999px;
            border: 1px solid rgba(34, 211, 238, 0.12);
            background: rgba(10, 21, 42, 0.78);
            font-size: 12px;
            color: #d5f6ff;
            letter-spacing: 0.06em;
            text-transform: uppercase;
        }

        .chip.alert {
            border-color: rgba(248, 113, 113, 0.3);
            background: rgba(127, 29, 29, 0.35);
            color: #ffd7d7;
        }

        .chip.high {
            border-color: rgba(52, 211, 153, 0.25);
            background: rgba(6, 78, 59, 0.28);
            color: #d1fae5;
        }

        .chip.medium {
            border-color: rgba(245, 158, 11, 0.25);
            background: rgba(120, 53, 15, 0.28);
            color: #fde68a;
        }

        .overview-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 14px;
            margin-bottom: 18px;
        }

        .metric {
            padding: 18px;
            border-radius: 20px;
            background: rgba(5, 14, 28, 0.88);
            border: 1px solid rgba(34, 211, 238, 0.08);
            position: relative;
        }

        .metric::after {
            content: "";
            position: absolute;
            left: 18px;
            right: 18px;
            top: 0;
            height: 2px;
            background: linear-gradient(90deg, rgba(34, 211, 238, 0.8), transparent);
        }

        .metric .label {
            display: block;
            color: var(--muted);
            font-size: 11px;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            margin-bottom: 8px;
        }

        .metric .value {
            font-size: 19px;
            font-weight: 700;
        }

        .core-summary {
            padding: 22px;
            border-radius: 22px;
            background:
                radial-gradient(circle at top right, rgba(34, 211, 238, 0.08), transparent 32%),
                linear-gradient(135deg, rgba(7, 19, 38, 0.95), rgba(7, 14, 26, 0.9));
            border: 1px solid rgba(34, 211, 238, 0.12);
        }

        .summary-block + .summary-block {
            margin-top: 18px;
        }

        .summary-label {
            color: #b7f4ff;
            font-size: 12px;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            margin-bottom: 8px;
        }

        .summary-text {
            color: var(--text);
            font-size: 16px;
            line-height: 1.7;
        }

        .list {
            list-style: none;
            margin: 0;
            padding: 0;
            display: grid;
            gap: 12px;
        }

        .list li {
            padding: 16px 18px;
            border-radius: 18px;
            background: rgba(6, 15, 29, 0.86);
            border: 1px solid rgba(34, 211, 238, 0.08);
            position: relative;
            line-height: 1.6;
            color: #ddf4ff;
        }

        .list li::before {
            content: "";
            position: absolute;
            left: 0;
            top: 14px;
            bottom: 14px;
            width: 3px;
            border-radius: 999px;
            background: linear-gradient(180deg, var(--cyan), transparent);
        }

        .callout {
            padding: 20px;
            border-radius: 22px;
            background: linear-gradient(135deg, rgba(104, 24, 31, 0.52), rgba(60, 10, 17, 0.4));
            border: 1px solid rgba(248, 113, 113, 0.22);
            color: #ffe0e0;
            line-height: 1.7;
            box-shadow: 0 16px 40px rgba(127, 29, 29, 0.16);
        }

        .notification-box {
            padding: 18px;
            border-radius: 20px;
            background: rgba(5, 14, 28, 0.86);
            border: 1px solid rgba(34, 211, 238, 0.1);
        }

        .notification-box + .notification-box {
            margin-top: 14px;
        }

        .notification-box strong {
            display: block;
            margin-bottom: 10px;
            font-size: 13px;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            color: #b9f4ff;
        }

        pre {
            margin: 0;
            padding: 18px;
            border-radius: 20px;
            background: rgba(3, 10, 20, 0.95);
            border: 1px solid rgba(34, 211, 238, 0.08);
            color: #d7f6ff;
            white-space: pre-wrap;
            word-break: break-word;
            line-height: 1.6;
            font-size: 13px;
        }

        .signal-panel {
            padding: 18px;
            margin-top: 22px;
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 14px;
        }

        .signal {
            padding: 16px;
            border-radius: 18px;
            background: rgba(4, 12, 24, 0.86);
            border: 1px solid rgba(34, 211, 238, 0.08);
        }

        .signal .label {
            display: block;
            color: var(--muted);
            font-size: 11px;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            margin-bottom: 8px;
        }

        .signal .value {
            font-size: 17px;
            font-weight: 700;
        }

        .footer-note {
            margin-top: 24px;
            text-align: center;
            color: var(--muted);
            font-size: 13px;
            letter-spacing: 0.04em;
        }

        @media (max-width: 1160px) {
            .hero,
            .dashboard {
                grid-template-columns: 1fr;
            }

            .signal-panel {
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }
        }

        @media (max-width: 780px) {
            .topbar {
                flex-direction: column;
                align-items: start;
                gap: 14px;
            }

            .command-form {
                grid-template-columns: 1fr;
            }

            .command-btn {
                min-height: 58px;
            }

            .overview-grid,
            .signal-panel {
                grid-template-columns: 1fr;
            }

            .hero-panel h2 {
                font-size: 34px;
            }

            .page {
                padding: 18px 16px 30px;
            }
        }
    </style>
</head>
<body>
    <div class="page">
        <section class="topbar">
            <div class="brand">
                <div class="brand-mark"></div>
                <div class="brand-text">
                    <h1>JARVIS</h1>
                    <p>Autonomous Incident Command Interface</p>
                </div>
            </div>
            <div class="status-strip">
                <div class="status-pill">Live Analysis Surface</div>
                <div class="status-pill">Read-Only Investigation Mode</div>
                <div class="status-pill">ServiceNow Intake Enabled</div>
            </div>
        </section>

        <section class="hero">
            <div class="hero-panel">
                <div class="kicker">Command Center • Incident Intelligence</div>
                <h2>Advanced investigation console for rapid first-pass operational triage</h2>
                <p>
                    JARVIS accepts a ServiceNow incident number, classifies the incident profile, routes the correct
                    investigation playbook, and produces structured outputs for engineers, managers, and escalation
                    channels without taking destructive action.
                </p>

                <form method="post" class="command-form">
                    <div>
                        <div class="input-shell">
                            <input
                                type="text"
                                name="incident_number"
                                placeholder="Enter incident number, e.g. INC1002"
                                value="{{ incident_number or '' }}"
                                required
                            >
                        </div>
                        <div class="input-help">Mock incidents available: INC1001, INC1002, INC1003</div>
                    </div>
                    <button type="submit" class="command-btn">Execute Investigation</button>
                </form>

                <div class="hero-stats">
                    <div class="mini-stat">
                        <span class="label">Supported Playbooks</span>
                        <span class="value">Pipeline • Cluster • IBM Cloud</span>
                    </div>
                    <div class="mini-stat">
                        <span class="label">Outputs</span>
                        <span class="value">Engineer • Manager • Slack/Email</span>
                    </div>
                    <div class="mini-stat">
                        <span class="label">Safety Posture</span>
                        <span class="value">Investigation Only</span>
                    </div>
                </div>
            </div>

            <aside class="side-panel">
                <h3 class="panel-title">Operational Modules</h3>
                <div class="system-card">
                    <strong>Pipeline Diagnostics</strong>
                    <p>Failed stage mapping, log correlation, deployment blockage analysis, and pipeline execution context.</p>
                </div>
                <div class="system-card">
                    <strong>Cluster Observability</strong>
                    <p>Pod, node, component, event, and monitoring signal review for OpenShift and related environments.</p>
                </div>
                <div class="system-card">
                    <strong>IBM Cloud Context</strong>
                    <p>Cloud service activity, access failure patterns, and service-context review for impacted resources.</p>
                </div>
                <div class="system-card">
                    <strong>Priority Escalation</strong>
                    <p>Probable P1 detection with responder-ready escalation wording for service-down or critical impact cases.</p>
                </div>
            </aside>
        </section>

        {% if error %}
            <div class="error"><strong>Command rejected:</strong> {{ error }}</div>
        {% endif %}

        {% if result %}
            <section class="dashboard">
                <div class="stack">
                    <div class="module">
                        <div class="module-header">
                            <div>
                                <div class="module-subtitle">Primary Analysis</div>
                                <h3>Incident Overview</h3>
                            </div>
                            <div class="chips">
                                <span class="chip">{{ result.incident_number }}</span>
                                <span class="chip">{{ result.incident_type|replace('_', ' ')|title }}</span>
                                <span class="chip {% if result.engineer_report.confidence in ['medium-high', 'high'] %}high{% elif result.engineer_report.confidence == 'medium' %}medium{% endif %}">
                                    Confidence {{ result.engineer_report.confidence }}
                                </span>
                                {% if result.engineer_report.probable_p1 %}
                                    <span class="chip alert">Probable P1</span>
                                {% endif %}
                            </div>
                        </div>

                        <div class="overview-grid">
                            <div class="metric">
                                <span class="label">Incident Type</span>
                                <span class="value">{{ result.incident_type|replace('_', ' ')|title }}</span>
                            </div>
                            <div class="metric">
                                <span class="label">Confidence</span>
                                <span class="value">{{ result.engineer_report.confidence }}</span>
                            </div>
                            <div class="metric">
                                <span class="label">Escalation State</span>
                                <span class="value">{{ 'Immediate Review' if result.engineer_report.probable_p1 else 'Monitor / Validate' }}</span>
                            </div>
                        </div>

                        <div class="core-summary">
                            <div class="summary-block">
                                <div class="summary-label">Incident Summary</div>
                                <div class="summary-text">{{ result.engineer_report.summary }}</div>
                            </div>
                            <div class="summary-block">
                                <div class="summary-label">Suspected Root Cause</div>
                                <div class="summary-text">{{ result.engineer_report.suspected_root_cause }}</div>
                            </div>
                        </div>
                    </div>

                    <div class="module">
                        <div class="module-header">
                            <div>
                                <div class="module-subtitle">Evidence Chain</div>
                                <h3>Collected Evidence</h3>
                            </div>
                        </div>
                        <ul class="list">
                            {% for item in result.engineer_report.evidence %}
                                <li>{{ item }}</li>
                            {% endfor %}
                        </ul>
                    </div>

                    <div class="module">
                        <div class="module-header">
                            <div>
                                <div class="module-subtitle">Response Guidance</div>
                                <h3>Recommended Next Steps</h3>
                            </div>
                        </div>
                        <ul class="list">
                            {% for item in result.engineer_report.recommended_next_steps %}
                                <li>{{ item }}</li>
                            {% endfor %}
                        </ul>
                    </div>
                </div>

                <div class="stack">
                    <div class="module">
                        <div class="module-header">
                            <div>
                                <div class="module-subtitle">Impact Mapping</div>
                                <h3>Impacted Resources</h3>
                            </div>
                        </div>
                        <ul class="list">
                            {% for item in result.engineer_report.impacted_resources %}
                                <li>{{ item }}</li>
                            {% endfor %}
                        </ul>
                    </div>

                    {% if result.engineer_report.escalation_message %}
                        <div class="module">
                            <div class="module-header">
                                <div>
                                    <div class="module-subtitle">Priority Handling</div>
                                    <h3>Escalation Draft</h3>
                                </div>
                            </div>
                            <div class="callout">
                                {{ result.engineer_report.escalation_message }}
                            </div>
                        </div>
                    {% endif %}

                    <div class="module">
                        <div class="module-header">
                            <div>
                                <div class="module-subtitle">Executive Output</div>
                                <h3>Manager Summary</h3>
                            </div>
                        </div>
                        <pre>{{ result.manager_summary }}</pre>
                    </div>

                    <div class="module">
                        <div class="module-header">
                            <div>
                                <div class="module-subtitle">Communications</div>
                                <h3>Notification Drafts</h3>
                            </div>
                        </div>
                        <div class="notification-box">
                            <strong>Slack</strong>
                            <div>{{ result.notification.slack }}</div>
                        </div>
                        <div class="notification-box">
                            <strong>Email</strong>
                            <div>{{ result.notification.email }}</div>
                        </div>
                    </div>
                </div>
            </section>

            <section class="signal-panel">
                <div class="signal">
                    <span class="label">Engine Status</span>
                    <span class="value">Analysis Complete</span>
                </div>
                <div class="signal">
                    <span class="label">Routing Decision</span>
                    <span class="value">{{ result.incident_type|replace('_', ' ')|title }}</span>
                </div>
                <div class="signal">
                    <span class="label">Priority Indicator</span>
                    <span class="value">{{ 'Probable P1' if result.engineer_report.probable_p1 else 'Standard Investigation' }}</span>
                </div>
                <div class="signal">
                    <span class="label">Action Profile</span>
                    <span class="value">Non-Destructive</span>
                </div>
            </section>
        {% endif %}

        <div class="footer-note">
            JARVIS operates in investigation-assist mode only. No destructive remediation actions are executed automatically.
        </div>
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
