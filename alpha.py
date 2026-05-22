from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class Incident:
    number: str
    short_description: str
    description: str
    source_link: str
    priority: str = "unknown"
    assignment_group: str = ""
    configuration_item: str = ""
    state: str = "new"


@dataclass
class InvestigationFinding:
    summary: str
    suspected_root_cause: str
    confidence: str
    evidence: List[str] = field(default_factory=list)
    impacted_resources: List[str] = field(default_factory=list)
    recommended_next_steps: List[str] = field(default_factory=list)
    probable_p1: bool = False
    escalation_message: str = ""


@dataclass
class InvestigationOutput:
    incident_number: str
    incident_type: str
    engineer_report: Dict[str, Any]
    manager_summary: Dict[str, Any]
    notification: Dict[str, str]


class ServiceNowClient:
    def __init__(self) -> None:
        self.mock_db: Dict[str, Incident] = {
            "INC1001": Incident(
                number="INC1001",
                short_description="Pipeline failure blocking deployment",
                description=(
                    "Deployment pipeline is failing in the integration-test stage. "
                    "Builds are queued and release is blocked. "
                    "Source indicates Jenkins pipeline dashboard."
                ),
                source_link="https://ci.example.internal/job/payments-deploy/145",
                priority="2",
                assignment_group="DevOps",
                configuration_item="payments-pipeline",
                state="active",
            ),
            "INC1002": Incident(
                number="INC1002",
                short_description="OpenShift pods crashing in production",
                description=(
                    "Customer-facing API is degraded. Multiple pods in CrashLoopBackOff. "
                    "Node pressure alerts seen in monitoring. "
                    "Source indicates OpenShift console and Grafana."
                ),
                source_link="https://console-openshift.example.internal/k8s/ns/prod-pods",
                priority="1",
                assignment_group="SRE",
                configuration_item="prod-cluster-a",
                state="active",
            ),
            "INC1003": Incident(
                number="INC1003",
                short_description="IBM Cloud object storage access errors",
                description=(
                    "Application reports authentication failures reaching IBM Cloud Object Storage. "
                    "Recent service activity may have changed credentials."
                ),
                source_link="https://cloud.ibm.com/objectstorage/instances/example",
                priority="2",
                assignment_group="CloudOps",
                configuration_item="ibm-cos-instance",
                state="active",
            ),
        }

    def fetch_incident(self, incident_number: str) -> Incident:
        normalized = incident_number.strip().upper()
        if normalized not in self.mock_db:
            raise ValueError(f"Incident not found: {normalized}")
        return self.mock_db[normalized]


class IncidentClassifier:
    def classify(self, incident: Incident) -> str:
        text = f"{incident.short_description} {incident.description} {incident.source_link}".lower()
        if re.search(r"pipeline|jenkins|stage|deployment", text):
            return "pipeline"
        if re.search(r"openshift|cluster|pod|node|crashloop|grafana|kubernetes", text):
            return "cluster"
        if re.search(r"ibm cloud|cloud\.ibm\.com|object storage|activity", text):
            return "ibm_cloud"
        return "unknown"


class PipelineInvestigator:
    def investigate(self, incident: Incident) -> InvestigationFinding:
        return InvestigationFinding(
            summary="Deployment pipeline failure is blocking release progression.",
            suspected_root_cause="Integration-test stage failure caused by repeated test execution errors.",
            confidence="medium",
            evidence=[
                f"Incident description references pipeline failure: {incident.short_description}",
                f"Source link points to CI system: {incident.source_link}",
                "Failed stage inferred: integration-test",
                "Deployment queue backlog suggests downstream release blockage",
            ],
            impacted_resources=[
                incident.configuration_item or "pipeline",
                "deployment workflow",
                "release schedule",
            ],
            recommended_next_steps=[
                "Open the linked pipeline run and inspect failed stage logs",
                "Compare the current failing run against the last successful run",
                "Identify whether failure is caused by test regression, dependency outage, or environment issue",
                "Notify release stakeholders of deployment blockage",
            ],
            probable_p1=False,
            escalation_message="",
        )


class ClusterInvestigator:
    def investigate(self, incident: Incident) -> InvestigationFinding:
        probable_p1 = "degraded" in incident.description.lower() or incident.priority == "1"
        escalation = (
            "Probable P1: Production service degradation detected. "
            "Escalate to cluster operations and application owners immediately."
            if probable_p1
            else ""
        )
        return InvestigationFinding(
            summary="Cluster workload instability is affecting application availability.",
            suspected_root_cause="Pods are likely restarting due to resource pressure or component instability on the cluster.",
            confidence="medium-high",
            evidence=[
                "Description mentions CrashLoopBackOff behavior",
                "Monitoring signal indicates node pressure",
                f"Source link points to cluster tooling: {incident.source_link}",
                f"Configuration item suggests affected cluster: {incident.configuration_item}",
            ],
            impacted_resources=[
                incident.configuration_item or "cluster",
                "customer-facing API pods",
                "possibly impacted nodes and platform components",
            ],
            recommended_next_steps=[
                "Check pod status, restart counts, and recent container logs",
                "Inspect node conditions for memory, disk, and CPU pressure",
                "Review cluster events and operator/component status",
                "Correlate with monitoring alerts and recent changes",
            ],
            probable_p1=probable_p1,
            escalation_message=escalation,
        )


class IBMCloudInvestigator:
    def investigate(self, incident: Incident) -> InvestigationFinding:
        return InvestigationFinding(
            summary="IBM Cloud service access issue is impacting dependent application calls.",
            suspected_root_cause="Credential or service configuration drift may be causing authentication failures.",
            confidence="medium",
            evidence=[
                "Description mentions authentication failures",
                "Incident references recent service activity",
                f"Source link points to IBM Cloud context: {incident.source_link}",
            ],
            impacted_resources=[
                incident.configuration_item or "ibm cloud service",
                "application integrations depending on the service",
            ],
            recommended_next_steps=[
                "Review IBM Cloud activity and recent configuration changes",
                "Validate service credentials, API keys, and endpoint configuration",
                "Check service health and access policies",
                "Confirm whether credential rotation occurred recently",
            ],
            probable_p1=False,
            escalation_message="",
        )


class UnknownInvestigator:
    def investigate(self, incident: Incident) -> InvestigationFinding:
        return InvestigationFinding(
            summary="Incident type could not be confidently classified from current context.",
            suspected_root_cause="Insufficient context in incident description and source link.",
            confidence="low",
            evidence=[
                incident.short_description,
                incident.description,
                incident.source_link,
            ],
            impacted_resources=[incident.configuration_item] if incident.configuration_item else [],
            recommended_next_steps=[
                "Review full ServiceNow incident activity",
                "Validate affected platform or service from assignment group and CI",
                "Add more telemetry links or logs to the incident",
            ],
            probable_p1=incident.priority == "1",
            escalation_message="Probable P1 based on priority only; validate service impact immediately." if incident.priority == "1" else "",
        )


class PlaybookRouter:
    def __init__(self) -> None:
        self.investigators = {
            "pipeline": PipelineInvestigator(),
            "cluster": ClusterInvestigator(),
            "ibm_cloud": IBMCloudInvestigator(),
            "unknown": UnknownInvestigator(),
        }

    def route(self, incident_type: str):
        return self.investigators.get(incident_type, self.investigators["unknown"])


class ReportGenerator:
    def generate(self, incident: Incident, incident_type: str, finding: InvestigationFinding) -> InvestigationOutput:
        engineer_report = {
            "incident_number": incident.number,
            "incident_type": incident_type,
            "summary": finding.summary,
            "suspected_root_cause": finding.suspected_root_cause,
            "confidence": finding.confidence,
            "evidence": finding.evidence,
            "impacted_resources": finding.impacted_resources,
            "recommended_next_steps": finding.recommended_next_steps,
            "probable_p1": finding.probable_p1,
            "escalation_message": finding.escalation_message,
        }

        manager_summary = {
            "incident_number": incident.number,
            "summary": finding.summary,
            "business_impact": ", ".join(finding.impacted_resources) if finding.impacted_resources else "under investigation",
            "confidence": finding.confidence,
            "next_actions": finding.recommended_next_steps[:3],
            "probable_p1": finding.probable_p1,
        }

        notification_text = (
            f"{incident.number} [{incident_type}] - {finding.summary} "
            f"Root cause hypothesis: {finding.suspected_root_cause}. "
            f"Probable P1: {'yes' if finding.probable_p1 else 'no'}."
        )

        notification = {
            "slack": notification_text,
            "email": notification_text + (
                f" Escalation: {finding.escalation_message}" if finding.escalation_message else ""
            ),
        }

        return InvestigationOutput(
            incident_number=incident.number,
            incident_type=incident_type,
            engineer_report=engineer_report,
            manager_summary=manager_summary,
            notification=notification,
        )


class AlphaAgent:
    def __init__(self) -> None:
        self.servicenow = ServiceNowClient()
        self.classifier = IncidentClassifier()
        self.router = PlaybookRouter()
        self.reporter = ReportGenerator()

    def investigate(self, incident_number: str) -> InvestigationOutput:
        incident = self.servicenow.fetch_incident(incident_number)
        incident_type = self.classifier.classify(incident)
        investigator = self.router.route(incident_type)
        finding = investigator.investigate(incident)
        return self.reporter.generate(incident, incident_type, finding)


def main() -> None:
    parser = argparse.ArgumentParser(description="Alpha incident investigation agent")
    parser.add_argument("incident_number", help="ServiceNow incident number, e.g. INC1001")
    args = parser.parse_args()

    agent = AlphaAgent()
    output = agent.investigate(args.incident_number)
    print(json.dumps(asdict(output), indent=2))


if __name__ == "__main__":
    main()

# Made with Bob
