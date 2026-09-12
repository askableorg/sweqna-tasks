# Authoring a SWE Q&A task

Read this alongside `tasks/hello-cache-py/`. Every section below points at the
corresponding file in that example; the example is small and deliberately easy,
but every artefact in it is real and the shapes are the ones we want.

---

## 1. What you are building

One original question about an approved repository, investigated by you, with a
verified answer, the evidence that establishes it, a rubric that grades it, and a
reproducible container so someone else can investigate the same question from the
same starting point.

**Your submission must include the answer.** A question on its own, a generic
explanation, or a repository link is incomplete. The participant produces a
written technical answer; supporting experiments may involve code, but a
production patch is not the deliverable.

What separates a strong task from a weak one:

- **A realistic uncertainty** that takes investigation across components,
  execution paths, or dependencies. A single symbol lookup or a documentation
  quotation is not enough.
- **A conclusion verifiable from the supplied source, configuration and runtime
  evidence.** No private knowledge, no follow-up conversation.
- **An original question**, a pinned runnable environment, and a rubric that
  accepts correct alternative explanations.

---

## 2. Choose the question before you build anything

Order matters. Find the question, establish the answer roughly, run the
contamination probe, then write the proposal. Building an environment for a
question that turns out to be contaminated is the most expensive way to discover
it.

### Where good questions come from

The best source is a codebase you have actually worked in, and a moment where you
were wrong about it. Questions that work tend to share a shape: **the obvious
reading is wrong, and what makes it wrong lives somewhere else.**

In the worked example, `invalidate(prefix)` does two things — it deletes matching
entries and it bumps a store-wide counter. In the interleaving the question asks
about, the deletion is a no-op and the counter bump is decisive. Every wrong
answer comes from reading the half of the function its name advertises.

Useful places to look: a bug you spent a day on; behaviour that contradicts what
a function is named; a guard whose scope is wider than it looks; an interaction
between two subsystems neither of which is surprising alone; a configuration flag
whose effect is not local to where it is read.

### The two-wrong-answers test

Before you go further, write down two plausible wrong conclusions — the ones a
competent engineer reaches by stopping early. If you cannot, the question is
probably too shallow to be worth building.

These two answers do real work later: they become the flawed entries in
`grading-examples.json`, they determine what your reproduction has to
discriminate, and they shape the `fail_condition` on your criteria. Write them
down now and keep them. See `tasks/hello-cache-py/AUTHOR_NOTES.md`.

### Then run the contamination probe

`DIFFICULTY.md` §1. One message, no repository access. If the model answers it,
pick a different question. Do this before the proposal, not after.

### Then propose

Fill `PROPOSAL.md` and send it through Askable. One approved task at a time. Keep
the working repository private. Askable confirms scope, deadline, budget and
submission location — use the assignment details you are given rather than dates
carried over from an older brief.

### Originality and source use

Prefer approved, less widely studied projects you know well. Disclose related
public material — issues, discussions, Stack Overflow answers, benchmark items —
rather than omitting what weakens the proposal; a near-duplicate found at review
costs the task. Do not copy benchmark questions or lightly rewrite an existing
answer. Record source permissions and dependencies in `provenance.json`.

---

## 3. Write `instruction.md`

One self-contained scenario and its central question. Subquestions are fine when
they develop the same investigation. Compare
`tasks/hello-cache-py/instruction.md` as you go.

Include:

- **Where the code is** in the container; the relevant version, configuration,
  inputs, and starting state.
- **The exact uncertainty to resolve** and the scope of the answer. Supply any
  proposed diff or configuration change being evaluated.
- **What the response must contain:** the direct conclusion, the mechanism,
  important conditions and exceptions, and file or symbol references. Ask for
  experimental evidence when the question depends on runtime behaviour.
- **Available tools, permitted experiments, and constraints** needed to interpret
  the result.

**Every graded requirement must be stated here or clearly entailed by it.** This
is the rule the rubric is checked against in both directions at review: nothing
graded that was not asked, nothing essential asked that is not graded.

Use plain English. Do not hide a required behaviour behind vague wording. Do not
manufacture difficulty from output formatting, missing dependencies, or a short
timeout. Ask for documented design rationale only when you supply the
documentation that answers it.

A useful habit: draft the "Your answer must cover" list and your rubric
side by side. If a criterion has no clause to point at, either add the clause or
drop the criterion.

---

## 4. Build the environment

- **Pin everything.** Repository at a full commit SHA, base image by digest,
  dependencies by lockfile or exact version. Record architecture and resource
  requirements in `task.json`.
- **Install at build time.** Runtime must work with no network, no credentials,
  no paid services, no private endpoints. Use local fixtures for external
  integrations.
- **Include what investigation needs:** source, configuration, sample inputs, and
  the tools to inspect and run the relevant behaviour. If the question is about
  runtime behaviour, the participant must be able to produce that behaviour.
- **Start from a clean baseline** and document how to reset.
- **Keep answers out.** Reference answers, rubrics, expected outputs, review
  notes, and development history that reveals the answer stay outside the
  participant image. Explicit `COPY` paths only.
- **Provide build, start, reset and smoke-test commands** in the task `README.md`.
  Run the smoke test in a fresh container and retain the output.

A runnable container is the default. Discuss a source-only exception with Askable
at proposal review.

### Make the behaviour reachable on purpose

If the question turns on an interleaving, a race, or a rare path, the participant
needs a way to produce it deliberately. Timing-dependent evidence is not
evidence: a result that reproduces four times out of five tells you nothing, and
tells a grader less.

The worked example solves this by modelling the slow call as a generator
suspension point and supplying a cooperative `Scheduler`, so "the invalidation
lands during the fetch" is something a participant constructs rather than waits
for. Fix seeds, fix inputs, and prefer controlled scheduling over threads.

---

## 5. Investigate, then write the reference answer

Establish the behaviour before you write the final answer. Trace the relevant
code paths and test your interpretation against the code rather than against your
memory of it.

For any runtime claim, run at least one targeted reproduction that **separates
the correct conclusion from a plausible wrong one.** This is the part authors get
wrong most often: an experiment that confirms your conclusion is worth much less
than one that would have caught you being wrong. In the worked example, printing
an empty key list confirms the conclusion and discriminates nothing — both
candidate explanations predict it. Varying the prefix, and reading the rejection
counter, discriminate.

If the question is architectural and execution adds no meaningful evidence,
document why and get agreement at proposal review. A passing smoke test is not
evidence for the answer.

### Structure of `reference/answer.md`

- **Conclusion** — answer the question directly and state the conditions under
  which the conclusion holds.
- **Mechanism** — the relevant sequence, dependencies, control flow or data flow.
  Connect claims to evidence IDs.
- **Boundaries** — exceptions, configuration-dependent behaviour, and what the
  evidence does not establish.
- **Verification** — the reproduction or source analysis, the observed result,
  and why it supports the conclusion.

Use the length the answer needs. Avoid repository summaries the question did not
ask for and unsupported claims about what the author intended. Write a technical
explanation another engineer can check, not a transcript of your exploration.

The **Boundaries** section carries more weight than its size suggests. It is
where you say what you did not establish, and it is the section a reviewer reads
to decide whether you understood your own evidence.

---

## 6. Evidence records

`reference/evidence.json`. One record per claim that needs support.

| Field | What to record |
|---|---|
| `id` | Stable identifier, `E01`, `E02`, … |
| `claim` | The specific fact this evidence supports |
| `source` | `path`, `symbol`, `commit`, `lines` — repository-relative, at the pinned revision |
| `verification` | The exact command, or the source-analysis steps; inputs and configuration |
| `result` | `observed`, `interpretation`, and `log` — the retained output, or `null` |

Set `result.log` to `null` only for source-only evidence, and make
`verification` describe the analysis in enough detail that someone can repeat it.
The validator enforces that pairing.

Two things to check yourself, because they are the most common defects:

- **Every cited path and symbol exists at the pinned revision**, and the line
  range is the right one. The validator checks existence and bounds; it cannot
  check that line 40 is the line you meant.
- **`interpretation` says what the observation rules out**, not just what it
  shows. `E04` in the worked example is the model: identical output across two
  prefixes rules out prefix scoping; a rejection count of 1 alongside zero
  deletions rules out eviction.

---

## 7. Reproductions

Scripts and logs in `reference/reproductions/`, with a README giving the exact
invocation and expected results.

The participant needs enough tools and inputs to derive the result independently.
They must not receive your completed reproduction or your answer.

**Never change the repository quietly to make your reference answer true.** If
the task required any change to the source, disclose it in
`environment.source_modifications` and in `provenance.json`.

---

## 8. The rubric

`evaluation/rubric.json`, an array of independently checkable criteria. **Aim for
10–15 substantive criteria** for a full task. That is a scope target, not a
quota: do not split one fact into duplicates and do not add trivia to reach a
number. Explain a smaller or larger rubric in `AUTHOR_NOTES.md` — the worked
example runs nine and says why.

Each criterion carries:

- `id` — `R01`, `R02`, … — and `requirement`, the instruction clause it evaluates.
- `claim` — one specific factual requirement.
- `pass_condition` — what a correct answer must establish.
- `acceptable_alternatives` — equivalent explanations, equivalent terminology,
  other valid routes to the same fact.
- `fail_condition` — a material omission or an incorrect claim.
- `evidence_ids` — the supporting reference evidence.
- `required` — `true` or `false`. Every essential fact is required.

Criteria are scored met or unmet. A task passes when every required criterion is
met and the answer contains no material contradiction of those requirements.
Optional criteria are diagnostic only.

**Wording, length, and matching your preferred implementation must not determine
correctness.** `acceptable_alternatives` is where you prove that. If a criterion
has an empty alternatives list, ask whether you are grading a fact or a phrasing.
In the worked example, calling the counter an "epoch" passes; reaching the
distinction by reasoning about ordering rather than by reading the counter
passes; instrumenting the store instead of varying the prefix passes.

Three failure modes to check for before you submit:

- **Grading the conclusion only.** `G04` in the worked example reaches the right
  outcome through a mechanism that is not operating. A rubric with no mechanism
  criteria passes it. Yours must not.
- **Grading one fact twice.** If two criteria fail together on every answer you
  can imagine, they are one criterion.
- **Grading what was not asked.** Every `requirement` field must quote or
  paraphrase a clause that is actually in `instruction.md`.

### Worked shape

From `tasks/hello-cache-py/evaluation/rubric.json`, criterion `R05`:

| Field | Value |
|---|---|
| `requirement` | State whether the prefix passed to invalidate changes the outcome, and why. |
| `claim` | The prefix is irrelevant because invalidate increments one store-wide generation unconditionally, even when no key matched. |
| `pass_condition` | States the outcome is unchanged for any prefix, and grounds it in the generation being global and incremented outside the deletion loop regardless of whether entries matched. |
| `acceptable_alternatives` | Describes the counter as a global epoch; or makes the point by observing that an invalidation dropping zero entries still moves the counter. |
| `fail_condition` | Says the key survives when the prefix does not match, or that the prefix is scoped to the keys it deletes. |
| `evidence_ids` / `required` | `E03`, `E04` / `true` |

Note what it does not do: it does not require a particular sentence, and it does
not grade anything the instruction did not ask about.

---

## 9. Test the rubric before you submit

`evaluation/grading-examples.json`: your reference answer, one correct
paraphrase, and two plausible flawed answers. Label every criterion met or unmet
for each, and explain every failure.

- **The reference and the paraphrase must pass.** If the paraphrase fails, the
  rubric is grading your wording.
- **The flawed answers must fail for factual reasons.** If you cannot name the
  fact each one gets wrong, it is a strawman and it proves nothing.

Write the paraphrase in a genuinely different register from your reference —
different vocabulary, different order, a different route to the same evidence.
That is the point of it.

For the flawed answers, use the two wrong conclusions you wrote down in §2. If
you ran a self-check and the model produced a wrong answer, **use that** — an
authentic wrong answer is a better test of the rubric than one you constructed,
because you did not write it with your own criteria in mind.

Askable checks your labels and uses separate responses to validate automated
judging.

---

## 10. Package and check

| Path | Required content |
|---|---|
| `PROPOSAL.md` | The approved scope and repository proposal |
| `README.md` | Build/start/reset/smoke commands, prerequisites, file map |
| `instruction.md` | The complete participant-facing scenario and response requirements |
| `task.json` | Task ID, revision, category, languages, repo URL and SHA, environment, author, AI tools, status |
| `environment/` | Dockerfile, dependency locks, source acquisition or snapshot, setup and smoke scripts, participant inputs |
| `reference/` | `answer.md`, `evidence.json`, reproductions and logs |
| `evaluation/` | `rubric.json`, `grading-examples.json` |
| `provenance.json` | Origin, version/hash, licence, permission basis for every asset |
| `AUTHOR_NOTES.md` | Investigation summary, wrong conclusions, rubric mapping, contamination probe, effort log, limitations, self-check disclosure |
| `attestations/` | Contributor declarations bound to the task revision |

Field-by-field detail is in `schema/FIELDS.md`. Then:

```bash
./scripts/validate-task.sh tasks/my-task
```

### Final checklist

- [ ] Repository and proposal approved; source commit pinned.
- [ ] Contamination probe run and recorded, with the model's full answer.
- [ ] Question is original, self-contained, and needs real investigation.
- [ ] A fresh container builds and runs offline; build, reset and smoke work.
- [ ] The participant has every tool and input needed, and no answer or rubric
      leakage.
- [ ] The reference answers every requested part and makes no unsupported claim.
- [ ] Every essential claim has a valid citation and, where needed, reproducible
      runtime evidence that discriminates.
- [ ] Each criterion maps to a clause of the question and to evidence; every
      essential requirement is covered.
- [ ] Reference and paraphrase pass; two flawed answers fail for documented
      factual reasons.
- [ ] All files present, JSON parses, paths and evidence IDs resolve.
- [ ] Provenance, attestations, AI disclosure and actual effort recorded.
- [ ] Handoff identifies the exact submission commit, checks performed, and known
      limitations.
