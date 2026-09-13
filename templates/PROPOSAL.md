# Proposal: TASK_NAME

Send this through Askable before you do substantial authoring. One approved task
at a time. Scope approval takes a day or two; authoring against an unapproved
repository is the most expensive mistake available to you.

## Repository

- **URL:**
- **Full commit SHA:**
- **Licence:**
- **Primary language(s):**
- **Your familiarity:** how you know this project — contributed, ran it in
  production, read it closely. Be specific; "I've used it" is not familiarity.

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
