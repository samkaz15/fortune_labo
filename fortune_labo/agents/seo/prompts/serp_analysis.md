# Prompt — SERP Analysis

## Task
For a given keyword, determine why the current top results rank and whether
fortune_labo can beat them **without violating positioning**.

## Capture
- Result types present (organic, map pack, images, video, AI overview, FAQ)
- Top 5: URL, content type, apparent intent match, approximate length, heading skeleton
- Structured data in use
- Domain class: national media / shrine official / individual practitioner / aggregator / AI-content site
- Freshness signals
- **The gap: what none of the top results provide**

## Required judgments

**1. Intent.** What does the searcher actually want? If an AI overview fully
answers it, informational targeting is low-value — prefer queries whose answer is
a *judgment* or a *first-hand impression*, which AI overviews cannot resolve.

**2. Winnability.** Be honest. If shrine official sites or a map pack own the
SERP and fortune_labo has no differentiator, say so and recommend dropping it.

**3. Differentiation basis.** State specifically why a competitor with AI but no
visits could not produce the page you are proposing. If you cannot state this,
the keyword fails the one-line test.

## Output
`seo_opportunity` with `type: "serp"`, populated `evidence` (source:
`serp_observation`, with observation date), and an explicit `moat_alignment`.
