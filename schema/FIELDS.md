# Field reference

Every JSON artefact, field by field. `scripts/validate_task.py` is the
authoritative check — where this document and the validator disagree, the
validator is right and this document is a bug.

`schema_version` is `1` on every file.

---

## `task.json`

| Field | Type | Rule |
|---|---|---|
| `task_id` | string | Lowercase alphanumeric and hyphens. Must equal the directory name. |
| `revision` | integer | Starts at 1. Increment for any change to question, source, environment, reference or rubric. |
| `task_type` | string | Always `"SWE_QA"`. |
| `verification_method` | string | Always `"RUBRIC"`. |
| `category` | string | One of: `Architecture`, `Root-Cause Analysis`, `Code Onboarding`, `Security Behavior`, `API Integration`, `Change Correctness`. |
| `primary_languages` | array | Non-empty. Conventional names — `Python`, `Rust`, `TypeScript`. |
| `repo_url` | string | The approved repository. |
| `repo_commit` | string | Full 40-character SHA. Not a tag, not a branch, not an abbreviation. |
| `author` | object | `name`, `github`. |
| `ai_tools_used` | array | Every tool used. `[]` if none. Described in `AUTHOR_NOTES.md`. |
| `status` | string | `draft` while working, `submitted` at handoff. `example` is reserved for tasks in this repository. |
| `environment` | object | See below. |

### `task.json.environment`

| Field | Rule |
|---|---|
| `base_image_digest` | `name@sha256:<digest>`. A tag is not a pin. |
| `architecture` | e.g. `linux/amd64`. |
| `cpus`, `memory_mb`, `storage_mb` | What the task actually needs. |
| `network_mode` | Must be `"no-network"`. |
| `source_modifications` | Every deviation from the pinned upstream revision. `"None."` if there are none — never empty. |

---

## `reference/evidence.json`

`evidence` is a non-empty array. IDs are unique, conventionally `E01`, `E02`, …

| Field | Rule |
|---|---|
| `claim` | One specific fact. Not a summary of a section. |
| `source.path` | Task-relative. Must exist. |
| `source.symbol` | Function, method or class. `Class.method` is fine; the last segment must appear in the file. |
| `source.commit` | The pinned SHA. |
| `source.lines` | `"N"` or `"N-M"`. Must be inside the file. |
| `verification` | The exact command with its inputs and configuration, or the source-analysis steps in repeatable detail. |
| `result.observed` | What was actually output or read. Not your conclusion. |
| `result.interpretation` | What it supports, and what it rules out. |
| `result.log` | Task-relative path to the retained output, or `null` for source-only evidence — in which case `verification` must describe the source analysis. |

---

## `evaluation/rubric.json`

`criteria` is a non-empty array with at least one `required: true`. IDs unique,
conventionally `R01`, `R02`, … Target 10–15; outside that range the validator
warns and `AUTHOR_NOTES.md` must explain the count.

| Field | Rule |
|---|---|
| `requirement` | The clause of `instruction.md` this evaluates. If you cannot point at one, the criterion does not belong. |
| `claim` | One specific factual requirement. |
| `pass_condition` | What a correct answer must establish. About facts, never phrasing. |
| `acceptable_alternatives` | Array. Equivalent explanations, terminology, and routes to the same fact. An empty array is a warning sign, not an error. |
| `fail_condition` | The material omission or incorrect claim that makes this unmet. |
| `evidence_ids` | Non-empty array. Every ID must exist in `evidence.json`. |
| `required` | Boolean. Essential facts are `true`. Optional criteria are diagnostic only and never decide the outcome. |

---

## `evaluation/grading-examples.json`

`examples` must contain exactly one `reference`, at least one
`correct_paraphrase`, and at least two whose label starts with `flawed`.

| Field | Rule |
|---|---|
| `id` | `G01`, `G02`, … |
| `label` | `reference`, `correct_paraphrase`, or `flawed_<what it gets wrong>`. |
| `expected_outcome` | `pass` or `fail`. Must agree with the labels: any unmet required criterion means `fail`. |
| `answer_source` | Task-relative path, for the reference. `null` otherwise. |
| `answer_text` | The full answer. Required unless `answer_source` is set. |
| `criteria` | One `{id, met, note}` per rubric criterion. Every criterion, every example. |
| `explanation` | Why it passes or fails. Mandatory for failures, and must name the fact that is wrong. |

---

## `provenance.json`

`third_party_material` is an array, empty only when the task genuinely contains
no third-party material.

| Field | Rule |
|---|---|
| `name` | The dependency, sample, dataset, binary or fixture. |
| `source` | URL or origin. |
| `license` | SPDX identifier where one exists. |
| `version_or_hash` | Exact version or content hash. |
| `ai_training_authorization` | Why those terms permit Askable's intended AI-training use. Specific to the licence, not boilerplate. |
