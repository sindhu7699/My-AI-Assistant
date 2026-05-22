# Alpha Incident Investigation Agent

Alpha is an incident-assistance agent that accepts a ServiceNow incident number, retrieves incident context, classifies the incident, routes investigation through the correct playbook, and produces a first-pass investigation report for responders, managers, and notification channels.

## Goals

- Accept a ServiceNow incident number as input
- Fetch incident details from ServiceNow
- Read the description and source link
- Classify incident type
- Route investigation to the correct playbook
- Analyze:
  - pipeline logs and failed stages for pipeline incidents
  - pod, node, component status, logs, and events for cluster incidents
  - IBM Cloud service context and activity information for IBM Cloud incidents
- Return a first-pass investigation report containing:
  - incident summary
  - suspected root cause
  - confidence
  - evidence
  - impacted resources
  - recommended next steps
- Detect likely critical/service-down incidents
- Mark probable P1 and prepare escalation content
- Produce outputs for:
  - engineers
  - managers
  - Slack/email notifications
- Avoid destructive automated actions

## Proposed Architecture

### Core modules

1. **Incident Intake**
   - Input: ServiceNow incident number
   - Validates format
   - Starts investigation workflow

2. **ServiceNow Client**
   - Fetches incident record
   - Extracts description, short description, priority, assignment group, CI, comments, work notes, and source link

3. **Incident Classifier**
   - Uses rules and optional LLM assistance
   - Categories:
     - pipeline
     - cluster
     - ibm_cloud
     - unknown

4. **Playbook Router**
   - Routes incident to the relevant investigation module
   - Ensures non-destructive analysis-only behavior

5. **Investigation Modules**
   - **Pipeline Investigator**
     - Inspect pipeline metadata
     - Parse logs
     - Identify failed stages
     - Extract error signatures
   - **Cluster Investigator**
     - Inspect pod status
     - Inspect node health
     - Inspect component/operator status
     - Collect logs and events
     - Use OpenShift and linked monitoring tools
   - **IBM Cloud Investigator**
     - Inspect target service context
     - Inspect recent activity/events
     - Check linked account/resource details

6. **Severity Evaluator**
   - Determines if incident is likely critical or service-down
   - Flags probable P1

7. **Report Generator**
   - Produces:
     - engineer report
     - manager summary
     - Slack/email notification text
     - escalation message when needed

## Suggested Project Structure

```text
alpha/
  README.md
  src/
    alpha/
      __init__.py
      main.py
      config.py
      models.py
      servicenow.py
      classifier.py
      router.py
      severity.py
      reporting.py
      investigators/
        __init__.py
        base.py
        pipeline.py
        cluster.py
        ibm_cloud.py
```

## Data Flow

1. User provides ServiceNow incident number
2. Alpha fetches incident details
3. Alpha extracts description and source link
4. Alpha classifies incident type
5. Alpha routes to investigation playbook
6. Investigator gathers evidence
7. Severity evaluator checks for probable P1
8. Report generator produces structured outputs

## Output Contracts

### Engineer Report
- Incident number
- Incident type
- Summary
- Suspected root cause
- Confidence
- Evidence
- Impacted resources
- Recommended next steps
- Probable P1 flag

### Manager Summary
- High-level summary
- Business/technical impact
- Confidence
- Immediate next actions
- Escalation recommendation

### Slack/Email Notification
- Incident number and type
- Summary
- Impact
- Current hypothesis
- Recommended actions
- Escalation status

## Safety Constraints

- No automated remediation
- No destructive cluster or cloud actions
- Read-only integrations preferred
- Escalation preparation only, not automatic paging unless explicitly enabled later

## Implementation Approach

Initial implementation can be delivered as a Python CLI skeleton with mocked integration points for:
- ServiceNow
- pipeline log retrieval
- OpenShift inspection
- IBM Cloud context retrieval

This allows the workflow and outputs to be validated before real API integration.