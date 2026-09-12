#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <task-name>" >&2
  exit 1
fi

TASK_NAME="$1"
if [[ ! "$TASK_NAME" =~ ^[a-z0-9][a-z0-9-]*$ ]]; then
  echo "Error: task name must be lowercase alphanumeric with hyphens." >&2
  exit 1
fi

TASK_DIR="tasks/${TASK_NAME}"
if [[ -e "$TASK_DIR" ]]; then
  echo "Error: ${TASK_DIR} already exists." >&2
  exit 1
fi

mkdir -p "$TASK_DIR"/{environment/src,reference/reproductions,evaluation,attestations}

sed "s/TASK_NAME/${TASK_NAME}/g" templates/PROPOSAL.md > "$TASK_DIR/PROPOSAL.md"
sed "s/TASK_NAME/${TASK_NAME}/g" templates/AUTHOR_NOTES.md > "$TASK_DIR/AUTHOR_NOTES.md"
sed "s/TASK_NAME/${TASK_NAME}/g" templates/contributor-attestation.md \
  > "$TASK_DIR/attestations/YOUR_GITHUB_HANDLE.md"
cp templates/instruction.md "$TASK_DIR/instruction.md"

cat > "$TASK_DIR/task.json" <<JSON
{
  "schema_version": 1,
  "task_id": "${TASK_NAME}",
  "revision": 1,
  "task_type": "SWE_QA",
  "verification_method": "RUBRIC",
  "category": "Root-Cause Analysis",
  "primary_languages": ["Python"],
  "repo_url": "",
  "repo_commit": "",
  "author": {
    "name": "YOUR_NAME",
    "github": "YOUR_GITHUB_HANDLE"
  },
  "ai_tools_used": [],
  "status": "draft",
  "environment": {
    "base_image_digest": "",
    "architecture": "linux/amd64",
    "cpus": 1,
    "memory_mb": 2048,
    "storage_mb": 4096,
    "network_mode": "no-network",
    "source_modifications": ""
  }
}
JSON

cat > "$TASK_DIR/provenance.json" <<'JSON'
{
  "schema_version": 1,
  "third_party_material": []
}
JSON

cat > "$TASK_DIR/reference/evidence.json" <<'JSON'
{
  "schema_version": 1,
  "evidence": [
    {
      "id": "E01",
      "claim": "",
      "source": {
        "path": "",
        "symbol": "",
        "commit": "",
        "lines": ""
      },
      "verification": "",
      "result": {
        "observed": "",
        "interpretation": "",
        "log": null
      }
    }
  ]
}
JSON

cat > "$TASK_DIR/evaluation/rubric.json" <<'JSON'
{
  "schema_version": 1,
  "criteria": [
    {
      "id": "R01",
      "requirement": "",
      "claim": "",
      "pass_condition": "",
      "acceptable_alternatives": [],
      "fail_condition": "",
      "evidence_ids": ["E01"],
      "required": true
    }
  ]
}
JSON

cat > "$TASK_DIR/evaluation/grading-examples.json" <<'JSON'
{
  "schema_version": 1,
  "examples": [
    {
      "id": "G01",
      "label": "reference",
      "expected_outcome": "pass",
      "answer_source": "reference/answer.md",
      "answer_text": null,
      "criteria": [{"id": "R01", "met": true, "note": ""}],
      "explanation": ""
    },
    {
      "id": "G02",
      "label": "correct_paraphrase",
      "expected_outcome": "pass",
      "answer_source": null,
      "answer_text": "",
      "criteria": [{"id": "R01", "met": true, "note": ""}],
      "explanation": ""
    },
    {
      "id": "G03",
      "label": "flawed_",
      "expected_outcome": "fail",
      "answer_source": null,
      "answer_text": "",
      "criteria": [{"id": "R01", "met": false, "note": ""}],
      "explanation": ""
    },
    {
      "id": "G04",
      "label": "flawed_",
      "expected_outcome": "fail",
      "answer_source": null,
      "answer_text": "",
      "criteria": [{"id": "R01", "met": false, "note": ""}],
      "explanation": ""
    }
  ]
}
JSON

cat > "$TASK_DIR/reference/answer.md" <<'MD'
# Reference answer — TASK

## Conclusion

<!-- Answer the question directly and state the conditions under which it holds. -->

## Mechanism

<!-- Sequence, dependencies, control flow, data flow. Cite evidence IDs. -->

## Boundaries

<!-- Exceptions, configuration-dependent behaviour, what the evidence does not establish. -->

## Verification

<!-- The reproduction or source analysis, the observed result, why it supports the conclusion. -->
MD

cat > "$TASK_DIR/README.md" <<MD
# ${TASK_NAME}

<!-- One paragraph: what the task asks and why it takes investigation. -->

## Build, start, reset, smoke-test

\`\`\`bash
docker build -t sweqa-${TASK_NAME} environment/
docker run --rm --network none sweqa-${TASK_NAME} <command>
\`\`\`

## File map

<!-- One line per artefact. -->
MD

cat > "$TASK_DIR/environment/Dockerfile" <<'DOCKER'
# Pin by digest, not tag.
FROM python@sha256:REPLACE_WITH_PINNED_DIGEST

WORKDIR /task

# Copy explicit paths only. Never `COPY . /task` — it would drag reference/ and
# evaluation/ into the participant image.
COPY src/ /task/src/

CMD ["sleep", "infinity"]
DOCKER

echo "Created ${TASK_DIR}"
echo
echo "Next:"
echo "  1. Fill ${TASK_DIR}/PROPOSAL.md and send it through Askable. Wait for approval."
echo "  2. Build the environment, investigate, write the answer and evidence."
echo "  3. ./scripts/validate-task.sh ${TASK_DIR}"
