# Prompt — Revision After QA

## Task
Produce the next revision of a draft from a QA Report and any A30 rewordings.

## Step 1 — Classify every finding

| Severity | Action |
| --- | --- |
| `blocking` | **Must fix.** No draft leaves with a blocking finding open. |
| `major` | Fix, or contest with reasoning recorded in `revision_notes`. |
| `minor` | Fix. |
| A30 reworing | **Binding.** Apply as given. Style is not grounds to negotiate. |

You may contest a finding. You may never ignore one, and you may never mark your
own draft as passed.

## Step 2 — Fix at the root, not the symptom

If QA flags one unmarked judgment, sweep the whole draft for unmarked judgments.
Repeated findings of the same type across revisions mean the rule was not
internalised, and that is worse than the original defect.

## Step 3 — Fabrication findings are special

If QA or A30 found a claim with no resolvable source, the fix is **removal or a
gap report**, never a softer rewording of the same invented claim. Rewording
`空気が澄んでいました` into `空気が澄んでいたように思われます` does not fix a
fabrication — it disguises one.

## Step 4 — Record the mapping

Every change in `revision_notes`:

```
finding_id · what_changed · why · sections_touched
```

Contested findings: `finding_id · contested · reasoning`. A28 adjudicates.

## Step 5 — Re-run the full self-check

Not just the changed sections. A fix in one section frequently breaks heading
hierarchy, link placement, or lead–body consistency elsewhere.

## Step 6 — Revision limit

```
if revision >= 3 and still not passing:
    STOP revising
    return the piece to A07 with a brief-defect report
```

Three failed revisions means the commission was wrong, not the prose. Continuing
to rewrite against a broken brief burns practitioner review time, which is the
scarcest resource in this system.

## Output
New `revision` of `schemas/master_content.schema.json`, with `revision_notes`
populated. Prior revisions are preserved in Git — never overwrite one in place.
