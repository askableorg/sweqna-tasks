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

### Your answer must be a mechanism, not a gap

The most common way a proposal dies, and the hardest one to see from the inside.

A **gap question** asks whether some protection, check or guard exists, and the
answer is that it does not. "Does the contract enforce the configured interval?"
No. "Does this service have any defence against a same-user race?" No. Both feel
like real findings, because finding a missing guard in code you care about *is* a
real finding. Neither makes a usable task.

The reason is that there is nothing to trace. An agent opens the function, sees
no check, and is done. The work you did — reading the whole flow, satisfying
yourself the guard is absent everywhere, knowing it matters — leaves no trace in
the question, because confirming an absence takes one read and a couple of greps.

Three symptoms, and any one of them should send you back to §2:

- **Your answer can be written as "no, there isn't one."**
- **Your rubric criteria all pass or fail together.** Gap questions produce
  rubrics that look thorough and grade a single fact ten times: the value is
  stored here, it is validated there, the function is public, it never compares
  the two, so anyone can call it. That is one fact with nine restatements, and
  every criterion is a single-line read.
- **Your independent-solve estimate is short.** If you think a competent engineer
  settles it in an hour, a frontier agent settles it in a minute.

**The fix is almost never a different repository.** The missing guard is usually
real and usually interesting — it is just the premise, not the answer. Ask what
*follows* from it:

| Gap question (dead) | The same finding as a premise (alive) |
|---|---|
| "Does the contract enforce the settlement interval, or can anyone settle early?" | "Given that anyone can settle at any moment, does settling thirty times across thirty days pay out the same total as settling once? If not, which direction, and who chooses it?" |
| "Does this codebase protect against a same-user race, or is it fully exposed?" | "Two functions here both read a row and then write it. Under concurrent requests one loses updates and the other does not. Which is which, and what makes the difference?" |

Both rewrites share the property the gap versions lack: **the obvious reading is
wrong.** Settlement looks linear in elapsed time and is not, because each leg
truncates independently and the floating rate is re-sampled at every call. Two
read-then-write paths look equally unsafe and are not, because one of them issues
a conditional update whose `WHERE` clause is re-evaluated against the freshly
committed row. In each case what settles it lives somewhere the reader was not
looking — in the rounding, or in the database's isolation semantics, rather than
in the function under suspicion.

That is also what makes them gradeable. A criterion can ask *which* function is
safe and *why*, and a wrong answer fails it for a stated factual reason rather
than for insufficient thoroughness.

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

### If you wrote the code

Knowing a codebase from the inside is the best possible reason to author about
it. It also creates one hazard that is invisible at review, and the control is
not a ban.

**The hazard is where the answer lives.** If you wrote a guard, you may know why
it is there from a design discussion, a PR thread, or a conversation that never
reached the repository. The question then feels perfectly discoverable to you and
is not, and nobody finds out until the independent solver cannot get there. That
breaks the rule that a conclusion must be verifiable from the supplied source
with no private knowledge.

**Two conditions, and then your own code is fair game.**

First, the question must be about *observable behaviour derivable from the
supplied source*. "What happens when this runs" is in. "Why was it designed this
way" is out unless you ship the documentation that answers it. The test is not
who typed the code; it is whether a stranger with the same files reaches the same
conclusion.

Second, list in `AUTHOR_NOTES.md` **what you know about this code that is not in
the repository** — decisions you remember, context from an issue or a chat, an
invariant that was never written down. Then check that list against your answer.
If nothing on it is load-bearing, you are clear. If something is, change the
question rather than hoping nobody notices.

For `rights_basis: owned` this is not optional care, it is the whole control, and
the independent human solve is what enforces it: a second engineer gets
`instruction.md` and the environment and nothing else, including no access to
you. Write for that reader.

Declare the relationship either way — which project, what you wrote or
contributed, and how you know the areas your question touches.

The same reasoning applies more sharply to employer code: do not include it
without approval and the authority to contribute it.

### Which repository you may use

Three paths, and you declare which in `provenance.json` as
`source.rights_basis`. Askable confirms it at proposal, before you build.

**`open-source`** — a public repository under a licence that permits the use.
Record the licence and why its specific terms permit Askable's AI-training use,
not just its name. Permissive licences (MIT, Apache-2.0, BSD) are
straightforward. Copyleft needs a decision before you start rather than at
submission. **AGPL is not accepted**, and the validator rejects it.

**`owned`** — code you own outright. The cleanest option for contamination, since
nothing a model has read can contain it, and the simplest for rights, since there
is nobody else to ask. Still subject to everything else: the question must take
real investigation, and a codebase you wrote last week to be a task is not a
codebase, it is a puzzle.

**`permissioned`** — someone else's private code, with their permission. Name the
owner and point at the permission record. **Askable verifies this with the owner
directly**; your assertion is not the record, and a task whose permission cannot
be confirmed is dropped whatever state it is in. If it is your employer's code,
get that in writing before you propose, not after you have built.

Do not send private code in a proposal. Describe it, and Askable arranges access
once the scope is approved.

### Originality and contamination

Prefer projects you know well. For public repositories, prefer less widely
studied ones: the probe in `DIFFICULTY.md` §1 is the test, but a long-tail project
starts further from the training distribution and is more likely to survive it.

Disclose related public material — issues, discussions, Stack Overflow answers,
benchmark items — rather than omitting what weakens the proposal; a near-duplicate
found at review costs the task. Do not copy benchmark questions or lightly rewrite
an existing answer. Record dependencies in `provenance.json` alongside the source.

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

**Do not put the answer in the question.** The opposite of hiding a requirement,
and just as fatal. A scenario that says "this stores state with no locking of any
kind, and the deduplication field is never referenced anywhere" and then asks
whether the code is exposed has already answered itself; so has a question phrased
"does it enforce the interval, *or can anyone call it early?*". State the
situation and the observable symptom. Let the participant establish the
mechanism, and keep your findings for `reference/answer.md`.

Use plain English. Do not hide a required behaviour behind vague wording. Do not
manufacture difficulty from output formatting, missing dependencies, or a short
timeout. Ask for documented design rationale only when you supply the
documentation that answers it.

A useful habit: draft the "Your answer must cover" list and your rubric
side by side. If a criterion has no clause to point at, either add the clause or
drop the criterion.

---

## 4. Build the environment

### First decide: does the participant run the code, or read it?

Two modes, set in `task.json` as `environment.mode`. The rule is not a judgement
call, and the validator enforces it:

| | `container` | `source-only` |
|---|---|---|
| The participant | runs the code | reads the code |
| You ship | a Dockerfile pinned by digest | a `fetch-source.sh` and a checksummed archive |
| Allowed when | always | **every** evidence record is source analysis, **and** the category is Architecture or Code Onboarding |
| Scaffold | `./scripts/new-task.sh my-task` | `./scripts/new-task.sh --source-only my-task` |

**If a single evidence record has a non-null `result.log`, you need a
container.** A runtime claim needs a runtime, and a claim you could not execute
is a claim you did not verify.

**And source-only is restricted to Architecture and Code Onboarding.** Root-Cause
Analysis, Change Correctness, Security Behavior and API Integration are settled by
running the code; the validator rejects source-only in those categories.

That restriction is not house preference. The production benchmark in this task
type builds a Docker image per task so the software "can be built, run, and
tested", and states outright that "simple codebase exploration is insufficient to
solve these" — execution is how it makes questions hard, not how it checks them
afterwards (`DIFFICULTY.md` §2). A question you can settle by reading is, on
average, an easier and more contaminable question.

So source-only is the narrow case, not the convenient one. It is for a task whose
answer genuinely rests on reading and which survives the contamination probe
without the crutch of runtime evidence. You write down why in
`environment.source_acquisition.rationale`, and Askable signs it off at proposal
rather than taking your word for it. Expect more source-only proposals to die at
§2 than container ones.

Askable handles harness packaging either way. You are not building the evaluation
rig.

### If you are shipping a container

- **Pin everything.** Repository at a full commit SHA, base image by digest,
  dependencies by lockfile or exact version. Record architecture and resource
  requirements in `task.json`.
- **Install at build time.** Runtime must work with no network, no credentials,
  no paid services, no private endpoints. Use local fixtures for external
  integrations.
- **The build must work for someone who is not you.** Askable rebuilds your image
  from your repository and nothing else: no SSH agent, no registry login, no
  personal token, no `--mount=type=ssh` or `--mount=type=secret`. If a rebuild
  needs a credential you hold, the task is not reproducible and the validator
  rejects it. Everything the build reads must already be in the build context.
- **Private source and private dependencies get vendored, not fetched.** Your
  authoring repository is private — that is the point of it — so the pinned
  source is committed under `environment/`, private or not. A dependency you
  cannot install without a credential is handled the same way: pack it at a
  pinned commit, commit the artefact, and point the lockfile at that local path.
  Record each one in `provenance.json` with its own rights basis. A private
  dependency fetched during the build is the most common reason an otherwise
  good container cannot be rebuilt.
- **Include what investigation needs:** source, configuration, sample inputs, and
  the tools to inspect and run the relevant behaviour. If the question is about
  runtime behaviour, the participant must be able to produce that behaviour.
- **Start from a clean baseline** and document how to reset.
- **Keep answers out.** Reference answers, rubrics, expected outputs, review
  notes, and development history that reveals the answer stay outside the
  participant image. Explicit `COPY` paths only.
- **Provide build, start, reset and smoke-test commands** in the task `README.md`.
  Run the smoke test in a fresh container and retain the output.

### If you are shipping source only

- **`environment/fetch-source.sh`** clones the repository, checks out the full
  SHA, strips `.git`, and produces a deterministic archive.
- **Record the archive's SHA-256** in `environment.source_acquisition.archive_sha256`
  so the tree can be verified later with no network.
- **Say what the participant needs to read it.** If the answer depends on a
  generated file, a build artefact, or a vendored dependency, either include it
  or you are in container territory after all.

State your mode in `PROPOSAL.md` and let Askable confirm it at scope approval.
Discovering at submission that your source-only task needed a runtime is an
expensive way to find out.

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

For the flawed answers, use the two wrong conclusions you wrote down in §2.

Then run the self-check (`DIFFICULTY.md` §5): three agent attempts, every answer
graded against this rubric. **Commit the rubric before you run it** — the order
is visible in your history and it is what keeps the exercise honest.

When an attempt fails, add its answer to `grading-examples.json` labelled
`flawed_agent_<what it got wrong>`. That is the best entry in the file: you did
not construct it with your own criteria in mind, so it tests the rubric in a way
a strawman cannot. Most rubric defects you would otherwise meet at review surface
in this step.

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
| `calibration/self-check.json` | Three or more graded agent attempts, `authoritative: false` |
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
- [ ] Self-check run: at least three attempts, every answer graded, rubric
      committed first. Not 3/3, and any failed answer harvested into
      `grading-examples.json`.
- [ ] All files present, JSON parses, paths and evidence IDs resolve.
- [ ] Provenance, attestations, AI disclosure and actual effort recorded.
- [ ] Handoff identifies the exact submission commit, checks performed, and known
      limitations.
