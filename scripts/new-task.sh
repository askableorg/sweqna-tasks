#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

MODE="container"
if [[ "${1:-}" == "--source-only" ]]; then
  MODE="source-only"
  shift
fi

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 [--source-only] <task-name>" >&2
  echo >&2
  echo "  container    (default) the participant runs the code. Required for any" >&2
  echo "               question whose answer rests on runtime evidence." >&2
  echo "  --source-only  the participant reads the code. Allowed only when every" >&2
  echo "               evidence record is source analysis AND the category is" >&2
  echo "               Architecture or Code Onboarding. See AUTHORING.md §4." >&2
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

mkdir -p "$TASK_DIR"/{environment/src,reference/reproductions,evaluation,attestations,calibration}

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
  "category": "CATEGORY_DEFAULT",
  "primary_languages": ["Python"],
  "repo_url": "",
  "repo_commit": "",
  "author": {
    "name": "YOUR_NAME",
    "github": "YOUR_GITHUB_HANDLE"
  },
  "ai_tools_used": [],
  "status": "draft",
  "environment": ENVIRONMENT_BLOCK
}
JSON

if [[ "$MODE" == "container" ]]; then
  CATEGORY_DEFAULT="Root-Cause Analysis"
  ENVIRONMENT_BLOCK='{
    "mode": "container",
    "base_image_digest": "",
    "architecture": "linux/amd64",
    "cpus": 1,
    "memory_mb": 2048,
    "storage_mb": 4096,
    "network_mode": "no-network",
    "source_modifications": ""
  }'
else
  CATEGORY_DEFAULT="Architecture"
  ENVIRONMENT_BLOCK='{
    "mode": "source-only",
    "network_mode": "no-network",
    "source_modifications": "",
    "source_acquisition": {
      "method": "git",
      "script": "environment/fetch-source.sh",
      "archive_sha256": "",
      "rationale": ""
    }
  }'
fi
python3 - "$TASK_DIR/task.json" "$ENVIRONMENT_BLOCK" "$CATEGORY_DEFAULT" <<'PY'
import json, sys
path, block, category = sys.argv[1], sys.argv[2], sys.argv[3]
raw = open(path).read().replace('"environment": ENVIRONMENT_BLOCK', '"environment": ' + block)
document = json.loads(raw)
document["category"] = category
open(path, "w").write(json.dumps(document, indent=2) + "\n")
PY

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

cp templates/self-check.json "$TASK_DIR/calibration/self-check.json"

if [[ "$MODE" == "container" ]]; then
  cat > "$TASK_DIR/environment/Dockerfile" <<'DOCKER'
# Pin by digest, not tag.
FROM python@sha256:REPLACE_WITH_PINNED_DIGEST

WORKDIR /task

# Copy explicit paths only. Never `COPY . /task` — it would drag reference/ and
# evaluation/ into the participant image.
COPY src/ /task/src/

CMD ["sleep", "infinity"]
DOCKER
else
  cp templates/fetch-source.sh "$TASK_DIR/environment/fetch-source.sh"
  chmod +x "$TASK_DIR/environment/fetch-source.sh"
  rmdir "$TASK_DIR/environment/src" 2>/dev/null || true
fi

echo "Created ${TASK_DIR} (${MODE})"
echo
echo "Next:"
echo "  1. Fill ${TASK_DIR}/PROPOSAL.md and send it through Askable. Wait for approval."
echo "  2. Build the environment, investigate, write the answer and evidence."
echo "  3. ./scripts/validate-task.sh ${TASK_DIR}"
