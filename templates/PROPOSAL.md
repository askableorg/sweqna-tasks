# Proposal: TASK_NAME

**This file is the record, not the gate.** You propose by message, in six lines
(the format is in your invitation). Once Askable approves it, paste the approval
into this file, fill in the rest, and commit it. That way the thing you were
approved for is in the repository next to the thing you built.

One approved task at a time. Authoring against an unapproved repository is the
most expensive mistake available to you.

## Repository

- **URL:**
- **Full commit SHA:** pinned when you start authoring, not at proposal. Full 40
  characters; everything you cite must resolve at this revision.
- **Licence:**
- **Primary language(s):**
- **Your familiarity:** how you know this project — contributed, ran it in
  production, read it closely. Be specific; "I've used it" is not familiarity.
- **Your contributor relationship, if any:** what you have contributed, and
  confirmation that the question is not about code you wrote or reviewed
  (`AUTHORING.md` §2).
- **Rights basis:** `open-source`, `owned`, or `permissioned` (`AUTHORING.md` §2).
- **Licence flag:** for open source, permissive or copyleft? Copyleft needs a
  decision before you start. AGPL is out.
- **For `permissioned`:** who owns it, and what permission exists. Askable
  confirms this with the owner before authoring starts. Do not attach private
  code to a proposal.

## Question

- **Category:** one of Architecture · Root-Cause Analysis · Code Onboarding ·
  Security Behavior · API Integration · Change Correctness
- **The question, as you would put it to the participant:**
- **The answer, in two or three sentences:** you must already know it. A proposal
  whose answer you have not established is a research plan, not a proposal.

## Why it takes investigation

- **Components involved:** the files, modules, or execution paths a correct
  answer has to cross.
- **Why a simple search is insufficient:** what a grep or a symbol lookup
  returns, and why that is not the answer.
- **Two plausible wrong conclusions:** the ones a competent engineer reaches by
  stopping early. Say what makes each attractive and what kills it.

## Contamination probe

Paste the question into a frontier chat model with no repository access, no
attachments, no follow-ups. Record model, version, date, and the full answer.

- **Result:** how many of your intended required facts it got.
- **Verdict:** if a no-access model answers it, the question is dead. Propose a
  different one rather than arguing that the model was lucky.

## Environment and evidence

- **Mode:** `container` or `source-only`. Source-only needs both: every piece of
  evidence is source analysis, and the category is Architecture or Code
  Onboarding. Say which, and if source-only, why reading settles it. Askable
  signs that off here rather than at submission, because execution is how this
  task type gets its difficulty (`DIFFICULTY.md` §2).
- **Planned runtime experiment:** what you will run, and which wrong conclusion
  it rules out.
- **Dependencies required, and the source of each asset:**
- **Anything that cannot run offline:** say so now, not at submission.

## Related public material

Links to issues, discussions, blog posts, Stack Overflow answers, or benchmark
items that touch this question. Disclose them; do not omit them because they
weaken the proposal. An undisclosed near-duplicate found at review costs the task.

## Effort

- **Estimated author hours:**
- **Estimated independent solve time:**
- **Proposed submission date:**
