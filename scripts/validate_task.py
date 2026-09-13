#!/usr/bin/env python3
"""Validate one SWE Q&A task: structure, schemas, citations, and leakage.

Everything checked here is something a reviewer would otherwise check by hand,
and something a task can fail on without the question being wrong. Getting these
green is the precondition for review, not evidence that the task is any good.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

ALLOWED_CATEGORIES = {
    "Architecture",
    "Root-Cause Analysis",
    "Code Onboarding",
    "Security Behavior",
    "API Integration",
    "Change Correctness",
}
REQUIRED_FILES = (
    "instruction.md",
    "task.json",
    "provenance.json",
    "README.md",
    "AUTHOR_NOTES.md",
    "reference/answer.md",
    "reference/evidence.json",
    "evaluation/rubric.json",
    "evaluation/grading-examples.json",
)
EVIDENCE_FIELDS = ("id", "claim", "source", "verification", "result")
SOURCE_FIELDS = ("path", "symbol", "commit", "lines")
RESULT_FIELDS = ("observed", "interpretation", "log")
CRITERION_FIELDS = (
    "id", "requirement", "claim", "pass_condition",
    "acceptable_alternatives", "fail_condition", "evidence_ids", "required",
)
ATTESTATION_CHECKS = (
    "- [x] I hand-wrote the question and the reference answer",
    "- [x] I personally verified every claim, citation, and experimental result",
    "- [x] I ran the no-repository contamination probe",
    "- [x] I committed the rubric before running the self-check",
    "- [x] I disclosed every AI tool used",
    "- [x] I did not write or review the specific code this question is about",
    "- [x] I own or have authority to contribute",
    "- [x] I assign all right, title, and interest",
)
# Execution is a difficulty mechanism, not a verification aid (DIFFICULTY.md §2).
# Only these two categories are routinely settled by reading.
SOURCE_ONLY_CATEGORIES = {"Architecture", "Code Onboarding"}
MIN_SELF_CHECK_ATTEMPTS = 3
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
LINES_RE = re.compile(r"^(\d+)(?:-(\d+))?$")


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)


def load_json(path: Path, report: Report) -> dict[str, Any] | None:
    try:
        return json.loads(path.read_text())
    except FileNotFoundError:
        report.error(f"{path.name}: missing")
    except json.JSONDecodeError as error:
        report.error(f"{path.name}: does not parse — {error}")
    return None


def require_fields(obj: Any, fields: tuple[str, ...], label: str, report: Report) -> bool:
    if not isinstance(obj, dict):
        report.error(f"{label}: expected an object")
        return False
    missing = [field for field in fields if field not in obj]
    if missing:
        report.error(f"{label}: missing {', '.join(missing)}")
    return not missing


def check_structure(task: Path, report: Report) -> None:
    for relative in REQUIRED_FILES:
        if not (task / relative).is_file():
            report.error(f"{relative}: missing")
    attestations = sorted((task / "attestations").glob("*.md"))
    real = [p for p in attestations if p.stem != "YOUR_GITHUB_HANDLE"]
    if not attestations:
        report.error("attestations/: no contributor attestation")
    elif not real:
        report.warn("attestations/: only the unfilled template is present")
    for path in real:
        text = path.read_text()
        for line in ATTESTATION_CHECKS:
            if line not in text:
                report.error(f"attestations/{path.name}: missing or unticked — '{line}…'")


def check_task_json(task: Path, report: Report) -> dict[str, Any]:
    document = load_json(task / "task.json", report) or {}
    if not document:
        return {}
    required = (
        "task_id", "revision", "task_type", "verification_method", "category",
        "primary_languages", "repo_url", "repo_commit", "author",
        "ai_tools_used", "status", "environment",
    )
    require_fields(document, required, "task.json", report)

    if document.get("task_type") != "SWE_QA":
        report.error('task.json: task_type must be "SWE_QA"')
    if document.get("verification_method") != "RUBRIC":
        report.error('task.json: verification_method must be "RUBRIC"')
    if document.get("category") not in ALLOWED_CATEGORIES:
        report.error("task.json: category must be one of " + ", ".join(sorted(ALLOWED_CATEGORIES)))
    if document.get("task_id") != task.name:
        report.error(f"task.json: task_id must match the directory name ({task.name})")
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", str(document.get("task_id", ""))):
        report.error("task.json: task_id must be lowercase alphanumeric with hyphens")

    languages = document.get("primary_languages")
    if not isinstance(languages, list) or not languages:
        report.error("task.json: primary_languages must be a non-empty list")
    if not isinstance(document.get("ai_tools_used"), list):
        report.error("task.json: ai_tools_used must be a list (use [] if none)")

    is_example = document.get("status") == "example"
    commit = str(document.get("repo_commit", ""))
    if not SHA_RE.match(commit) and not is_example:
        report.error("task.json: repo_commit must be a full 40-character commit SHA")

    environment = document.get("environment")
    if not isinstance(environment, dict):
        report.error("task.json: environment must be an object")
        return document

    if environment.get("network_mode") != "no-network":
        report.error('task.json: environment.network_mode must be "no-network"')
    if not str(environment.get("source_modifications", "")).strip():
        report.error("task.json: environment.source_modifications must be recorded")

    mode = environment.get("mode")
    if mode not in ("container", "source-only"):
        report.error('task.json: environment.mode must be "container" or "source-only"')
        return document

    if mode == "container":
        if not (task / "environment" / "Dockerfile").is_file():
            report.error('environment/Dockerfile: missing (required when mode is "container")')
        for field in ("base_image_digest", "architecture"):
            if not str(environment.get(field, "")).strip():
                report.error(f"task.json: environment.{field} must be recorded")
        digest = str(environment.get("base_image_digest", ""))
        if digest.strip() and ("sha256:" not in digest or "REPLACE" in digest):
            message = "task.json: environment.base_image_digest is not a real digest"
            report.warn(message) if is_example else report.error(message)
    else:
        if document.get("category") not in SOURCE_ONLY_CATEGORIES:
            report.error(
                'task.json: environment.mode "source-only" is allowed only for '
                + " and ".join(sorted(SOURCE_ONLY_CATEGORIES))
                + f" questions, not {document.get('category')!r}. Questions in the "
                "other categories are settled by running the code (DIFFICULTY.md §2)."
            )
        acquisition = environment.get("source_acquisition")
        if not require_fields(
            acquisition, ("method", "script", "archive_sha256", "rationale"),
            "task.json: environment.source_acquisition", report
        ):
            return document
        if len(str(acquisition.get("rationale", "")).split()) < 15:
            report.error(
                "task.json: source_acquisition.rationale must say why reading "
                "settles this question and what running the code would add that "
                "the source does not. Askable signs this off at proposal."
            )
        script = str(acquisition.get("script", ""))
        if script and not (task / script).is_file():
            report.error(f"task.json: source_acquisition.script does not exist — {script}")
        checksum = str(acquisition.get("archive_sha256", ""))
        if not re.fullmatch(r"[0-9a-f]{64}", checksum) and not is_example:
            report.error(
                "task.json: source_acquisition.archive_sha256 must be a 64-character "
                "SHA-256 of the retained source archive"
            )
    return document


def check_mode_against_evidence(
    document: dict[str, Any], evidence: dict[str, dict[str, Any]], report: Report
) -> None:
    """A runtime claim needs a runtime. Source-only mode cannot carry one."""
    environment = document.get("environment")
    if not isinstance(environment, dict) or environment.get("mode") != "source-only":
        return
    executed = sorted(
        identifier for identifier, record in evidence.items()
        if isinstance(record.get("result"), dict) and record["result"].get("log") is not None
    )
    if executed:
        report.error(
            'task.json: environment.mode is "source-only" but '
            + ", ".join(executed)
            + " carries executed evidence. Any task with a runtime claim needs "
            'mode "container".'
        )


def check_self_check(
    task: Path, document: dict[str, Any], criteria: list[dict[str, Any]], report: Report
) -> None:
    """The self-check is three graded answers, not a pass rate."""
    path = task / "calibration" / "self-check.json"
    if document.get("status") == "example":
        if path.is_file():
            report.warn("calibration/self-check.json: present on an example task")
        return
    if not path.is_file():
        report.error(
            "calibration/self-check.json: missing. Run at least three attempts and "
            "grade each answer against your own rubric (DIFFICULTY.md §5)."
        )
        return

    record = load_json(path, report)
    if not record:
        return
    if not require_fields(
        record, ("authoritative", "agent", "model", "model_version", "date",
                 "task_revision", "attempts"),
        "self-check.json", report
    ):
        return
    if record["authoritative"] is not False:
        report.error("self-check.json: authoritative must be false — Askable runs the authoritative calibration")
    if record.get("task_revision") != document.get("revision"):
        report.error(
            f"self-check.json: task_revision {record.get('task_revision')} does not match "
            f"task.json revision {document.get('revision')}"
        )

    attempts = record["attempts"]
    if not isinstance(attempts, list) or len(attempts) < MIN_SELF_CHECK_ATTEMPTS:
        report.error(f"self-check.json: at least {MIN_SELF_CHECK_ATTEMPTS} attempts are required")
        return

    rubric_ids = {c["id"] for c in criteria if isinstance(c, dict) and "id" in c}
    required_ids = {c["id"] for c in criteria if isinstance(c, dict) and c.get("required") is True}
    passes = 0
    for index, attempt in enumerate(attempts):
        label = f"self-check.json attempts[{index}]"
        if not require_fields(attempt, ("id", "answer_text", "criteria"), label, report):
            continue
        if not str(attempt.get("answer_text") or "").strip():
            report.error(f"{label}: answer_text must be the full answer the agent produced")
        labelled = {c["id"]: c for c in attempt["criteria"] if isinstance(c, dict) and "id" in c}
        missing = rubric_ids - set(labelled)
        if missing:
            report.error(f"{label}: unlabelled criteria — {', '.join(sorted(missing))}")
            continue
        if all(labelled[i].get("met") for i in required_ids):
            passes += 1

    if passes == len(attempts):
        report.error(
            f"self-check.json: the agent passed {passes}/{len(attempts)} attempts. "
            "The question is too easy — fix or replace it rather than submitting it."
        )
    elif passes * 2 > len(attempts):
        report.warn(
            f"self-check.json: the agent passed {passes}/{len(attempts)}. Likely too easy; "
            "expect this to come back."
        )

    if passes < len(attempts):
        labels = {
            str(e.get("label")) for e in
            (load_json(task / "evaluation" / "grading-examples.json", Report()) or {}).get("examples", [])
            if isinstance(e, dict)
        }
        if not any(label.startswith("flawed_agent") for label in labels):
            report.warn(
                "an attempt failed, so one of its answers belongs in grading-examples.json "
                'labelled "flawed_agent_<what it got wrong>" — a real wrong answer tests the '
                "rubric better than one you wrote"
            )


def check_evidence(task: Path, report: Report) -> dict[str, dict[str, Any]]:
    document = load_json(task / "reference" / "evidence.json", report) or {}
    records = document.get("evidence")
    if not isinstance(records, list) or not records:
        report.error("evidence.json: evidence must be a non-empty list")
        return {}

    by_id: dict[str, dict[str, Any]] = {}
    for index, record in enumerate(records):
        label = f"evidence.json[{index}]"
        if not require_fields(record, EVIDENCE_FIELDS, label, report):
            continue
        identifier = record["id"]
        if identifier in by_id:
            report.error(f"evidence.json: duplicate id {identifier}")
        by_id[identifier] = record

        source = record["source"]
        if require_fields(source, SOURCE_FIELDS, f"{identifier}.source", report):
            cited = task / source["path"]
            if not cited.is_file():
                report.error(f"{identifier}: source.path does not exist — {source['path']}")
            else:
                check_line_range(identifier, cited, str(source["lines"]), report)
                symbol = str(source.get("symbol", "")).split(".")[-1]
                if symbol and symbol not in cited.read_text():
                    report.error(f"{identifier}: symbol '{symbol}' not found in {source['path']}")

        result = record["result"]
        if require_fields(result, RESULT_FIELDS, f"{identifier}.result", report):
            log = result["log"]
            if log is None:
                if "source analysis" not in str(record["verification"]).lower():
                    report.error(
                        f"{identifier}: result.log is null, so verification must "
                        "describe the source analysis"
                    )
            elif not (task / log).is_file():
                report.error(f"{identifier}: retained log is missing — {log}")
    return by_id


def check_line_range(identifier: str, path: Path, lines: str, report: Report) -> None:
    match = LINES_RE.match(lines)
    if not match:
        report.error(f"{identifier}: source.lines must be 'N' or 'N-M', got '{lines}'")
        return
    start = int(match.group(1))
    end = int(match.group(2) or match.group(1))
    total = len(path.read_text().splitlines())
    if start < 1 or end < start:
        report.error(f"{identifier}: source.lines range is invalid — {lines}")
    elif end > total:
        report.error(
            f"{identifier}: source.lines {lines} runs past the end of "
            f"{path.name} ({total} lines)"
        )


def check_rubric(task: Path, evidence: dict[str, Any], report: Report) -> list[dict[str, Any]]:
    document = load_json(task / "evaluation" / "rubric.json", report) or {}
    criteria = document.get("criteria")
    if not isinstance(criteria, list) or not criteria:
        report.error("rubric.json: criteria must be a non-empty list")
        return []

    seen: set[str] = set()
    for index, criterion in enumerate(criteria):
        label = f"rubric.json[{index}]"
        if not require_fields(criterion, CRITERION_FIELDS, label, report):
            continue
        identifier = criterion["id"]
        if identifier in seen:
            report.error(f"rubric.json: duplicate id {identifier}")
        seen.add(identifier)
        if not isinstance(criterion["required"], bool):
            report.error(f"{identifier}: required must be true or false")
        if not isinstance(criterion["acceptable_alternatives"], list):
            report.error(f"{identifier}: acceptable_alternatives must be a list")
        ids = criterion["evidence_ids"]
        if not isinstance(ids, list) or not ids:
            report.error(f"{identifier}: evidence_ids must be a non-empty list")
        else:
            for evidence_id in ids:
                if evidence_id not in evidence:
                    report.error(f"{identifier}: evidence_ids references unknown {evidence_id}")

    required_count = sum(1 for c in criteria if isinstance(c, dict) and c.get("required") is True)
    if required_count == 0:
        report.error("rubric.json: at least one criterion must be required")
    if not 10 <= len(criteria) <= 15:
        report.warn(
            f"rubric.json: {len(criteria)} criteria, outside the 10–15 target — "
            "explain the count in AUTHOR_NOTES.md"
        )
    unused = sorted(set(evidence) - {i for c in criteria if isinstance(c, dict) for i in c.get("evidence_ids", [])})
    if unused:
        report.warn("evidence not referenced by any criterion: " + ", ".join(unused))
    return criteria


def check_grading_examples(task: Path, criteria: list[dict[str, Any]], report: Report) -> None:
    document = load_json(task / "evaluation" / "grading-examples.json", report) or {}
    examples = document.get("examples")
    if not isinstance(examples, list):
        report.error("grading-examples.json: examples must be a list")
        return

    rubric_ids = {c["id"] for c in criteria if isinstance(c, dict) and "id" in c}
    required_ids = {c["id"] for c in criteria if isinstance(c, dict) and c.get("required") is True}
    labels = [e.get("label") for e in examples if isinstance(e, dict)]

    if labels.count("reference") != 1:
        report.error("grading-examples.json: exactly one example must be labelled 'reference'")
    if labels.count("correct_paraphrase") < 1:
        report.error("grading-examples.json: at least one 'correct_paraphrase' is required")
    if sum(1 for label in labels if str(label).startswith("flawed")) < 2:
        report.error("grading-examples.json: at least two flawed answers are required")

    for index, example in enumerate(examples):
        label = f"grading-examples.json[{index}]"
        if not require_fields(example, ("id", "label", "expected_outcome", "criteria"), label, report):
            continue
        identifier = example["id"]
        if example.get("answer_source") is None and not str(example.get("answer_text") or "").strip():
            report.error(f"{identifier}: needs answer_text, or answer_source pointing at a file")
        if example.get("answer_source") and not (task / example["answer_source"]).is_file():
            report.error(f"{identifier}: answer_source does not exist — {example['answer_source']}")

        labelled = {c["id"]: c for c in example["criteria"] if isinstance(c, dict) and "id" in c}
        missing = rubric_ids - set(labelled)
        if missing:
            report.error(f"{identifier}: unlabelled criteria — {', '.join(sorted(missing))}")
        extra = set(labelled) - rubric_ids
        if extra:
            report.error(f"{identifier}: labels criteria not in the rubric — {', '.join(sorted(extra))}")

        unmet_required = sorted(i for i in required_ids & set(labelled) if not labelled[i].get("met"))
        computed = "fail" if unmet_required else "pass"
        if example["expected_outcome"] != computed:
            report.error(
                f"{identifier}: expected_outcome is '{example['expected_outcome']}' but the "
                f"labels compute '{computed}'"
                + (f" (unmet required: {', '.join(unmet_required)})" if unmet_required else "")
            )
        if computed == "fail" and not str(example.get("explanation") or "").strip():
            report.error(f"{identifier}: a failing example must explain the factual reason")


def check_leakage(task: Path, report: Report) -> None:
    dockerfile = task / "environment" / "Dockerfile"
    if not dockerfile.is_file():
        return
    text = dockerfile.read_text()
    if "sha256:" not in text:
        report.warn("environment/Dockerfile: base image is pinned by tag, not digest")
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped.upper().startswith("COPY"):
            continue
        sources = stripped.split()[1:-1]
        for source in sources:
            if source.startswith("--"):
                continue
            normalised = source.lstrip("./")
            if normalised in ("", "."):
                report.error(
                    f"environment/Dockerfile: 'COPY {source}' copies the whole build "
                    "context; copy explicit paths so reference material cannot leak"
                )
            if normalised.startswith(("reference", "evaluation")):
                report.error(f"environment/Dockerfile: copies answer material — '{stripped}'")

    for forbidden in ("reference", "evaluation"):
        if (task / "environment" / forbidden).exists():
            report.error(f"environment/{forbidden}/ exists inside the participant image")


def check_provenance(task: Path, report: Report) -> None:
    document = load_json(task / "provenance.json", report) or {}
    material = document.get("third_party_material")
    if not isinstance(material, list):
        report.error("provenance.json: third_party_material must be a list")
        return
    fields = ("name", "source", "license", "version_or_hash", "ai_training_authorization")
    for index, item in enumerate(material):
        require_fields(item, fields, f"provenance.json[{index}]", report)


def validate(task: Path) -> Report:
    report = Report()
    if not task.is_dir():
        report.error(f"{task}: not a directory")
        return report
    check_structure(task, report)
    document = check_task_json(task, report)
    evidence = check_evidence(task, report)
    check_mode_against_evidence(document, evidence, report)
    criteria = check_rubric(task, evidence, report)
    check_grading_examples(task, criteria, report)
    check_self_check(task, document, criteria, report)
    check_leakage(task, report)
    check_provenance(task, report)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("task_dir", nargs="+", type=Path)
    parser.add_argument("--strict", action="store_true", help="treat warnings as errors")
    arguments = parser.parse_args()

    failed = False
    for task in arguments.task_dir:
        report = validate(task)
        print(f"\n{task}")
        for warning in report.warnings:
            print(f"  warn   {warning}")
        for error in report.errors:
            print(f"  ERROR  {error}")
        if report.errors or (arguments.strict and report.warnings):
            failed = True
            print(f"  → FAIL ({len(report.errors)} errors, {len(report.warnings)} warnings)")
        else:
            print(f"  → ok ({len(report.warnings)} warnings)")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
