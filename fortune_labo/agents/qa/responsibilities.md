# QA Agent — Responsibilities

The six layers run **in this order**. A blocking finding in layers 1–3 stops the
run: there is no point checking heading hierarchy on a piece with a fabricated
visit claim.

---

## Layer 1 — Compliance / Risk QA (delegated to A30)

**A28 does not adjudicate this layer.** It packages the artifact, sends it to A30,
and enforces the returned verdict. A28 cannot downgrade or overrule an A30
blocking finding.

Surfaces sent: title, H1, every heading, lead, body, FAQ, CTA, meta description,
disclaimer — and for channel assets: hook, caption, on-screen text, slide text,
thumbnail, video title, hashtags.

| Check | Severity |
| --- | --- |
| Fear framing (`行かないと運気が下がる`) | **Blocking** |
| Guaranteed outcome (`必ず`, `絶対`, `願いが叶う`) | **Blocking** |
| Efficacy ranking or shrine comparison | **Blocking** |
| Medical claim or implied medical outcome | **Blocking** |
| Financial claim or investment/purchase advice | **Blocking** |
| Legal position stated | **Blocking** |
| Major life decision instructed (`別れるべき`) | **Blocking** |
| Excessive anxiety framing | **Blocking** |
| Fabricated testimonial, review count, or result claim | **Blocking** |
| Unmarked judgment presented as fact | **Blocking** |
| Missing disclaimer where required | **Blocking** |
| Missing divinatory basis on a forecast | **Blocking** |
| Untrue scarcity or urgency | **Blocking** |
| Required sponsorship disclosure absent | **Blocking** |
| Client-identifying detail without recorded consent | **Blocking** |

The dividing line: **"visiting is good" is permitted. "not visiting is bad" is
not.**

---

## Layer 2 — Fact QA

| Check | What A28 verifies | Severity |
| --- | --- | --- |
| Fact vs inference | Every factual statement is marked as fact, judgment, or general tendency | Blocking if a judgment reads as fact |
| Source presence | Every `research` section has a citable source | Blocking |
| Source resolves | The cited source actually says this | Blocking |
| Numbers | Figures match the source; no rounded-into-precision | Blocking |
| Dates | Visit dates, festival dates, publication dates internally consistent and real | Blocking |
| Proper nouns | Shrine names, deity names, place names, person names correct | Major |
| Access details | Directions, hours, fees traceable to a source | Major |
| Currency | Time-bound facts still true as of the check date | Major |
| Internal consistency | The piece does not contradict itself, or a published page | Major |

**A number with no source is treated as invented.** "Approximately" does not
convert an unsourced figure into a sourced one.

---

## Layer 3 — First-hand verification

The layer that protects the moat. Runs against
[`master_content.source_map`](../content-production/schemas/master_content.schema.json).

| Check | Severity |
| --- | --- |
| Every `visit_notes` section has a resolvable `source_reference` | **Blocking** |
| Every `practitioner_judgment` section has a resolvable `source_reference` | **Blocking** |
| `verbatim_anchor` actually supports the claim made | **Blocking** |
| No detail present in the draft that is absent from the source (extrapolation) | **Blocking** |
| Visit date present and matching the visit record | **Blocking** |
| Photo permission `confirmed` for every image used | **Blocking** |
| No imagery generated to depict a real place | **Blocking** |
| First-hand claims in channel assets trace to the same source map | **Blocking** |

**The extrapolation check is the hard one.** Source says "December morning, frost
on the approach"; draft says "the air was silent". Plausible, atmospheric,
unsourced — and blocking. A28 compares claim against anchor, not vibe against
vibe.

---

## Layer 4 — Editorial QA

| Check | Severity |
| --- | --- |
| Typos, okurigana, punctuation | Minor |
| Japanese naturalness; no translationese | Major |
| 敬体/常体 consistency | Minor |
| Logical flow; sections in an order that builds | Major |
| Redundancy — same point made twice | Minor |
| Sentence length; runaway sentences split | Minor |
| Paragraph and screen rhythm | Minor |
| Terminology consistency (one term per concept) | Minor |
| **Information sufficiency** — does the piece actually answer `target_question`? | **Blocking** |
| **Padding** — sections that exist to add length | Major |
| Heading informativeness | Minor |
| Lead delivers the answer where a short answer exists | Major |
| FAQ answers standalone | Major |
| Brand voice consistent with the practitioner | Major |

Information sufficiency is blocking because a page that ranks and does not answer
the question is the specific failure this pipeline exists to avoid.

---

## Layer 5 — SEO QA

Checked **against the brief**, not against generic SEO practice.

| Check | Severity |
| --- | --- |
| Primary keyword present and natural in H1, lead, and ≥1 H2 | Major |
| No keyword stuffing or unnatural density | Major |
| Search intent matches `content_intent` | **Blocking** |
| Title ≤ 60 chars, compliance-clean, keyword natural | Blocking if non-compliant |
| Meta description ≤ 120 chars, accurate, not overselling | Major |
| Heading hierarchy valid; one H1; no level skipping | Major |
| Every brief internal link present | Major |
| Booking-page link present (Tier A/B) | **Blocking** |
| Anchor text descriptive; no `こちら` | Minor |
| **Cannibalisation** — no published URL already targets this cluster | **Blocking** |
| Canonical intent stated | Major |
| Structured data intent matches the brief | Major |
| Featured-snippet block present where briefed, and not a guarantee | Major |

Cannibalisation is blocking because it is far cheaper to catch here than after
two of the site's own pages start competing.

---

## Layer 6 — Technical QA (detect; **Codex** implements)

A28 detects and specifies. It never implements. Findings are emitted as
`technical_issue` artifacts using
[`../seo/schemas/technical_issue.schema.json`](../seo/schemas/technical_issue.schema.json),
so Codex receives one format regardless of which agent found the problem.

| Surface | Checks |
| --- | --- |
| HTML | Heading semantics, list semantics, `alt` text present and descriptive |
| Structured data | Schema type matches content type; required properties present; validates; `author` → `Person` |
| Metadata | `title`, `meta description`, `canonical`, `robots`, Open Graph |
| Internal links | Targets resolve, no 404s, no redirect chains |
| URLs | Slug sane; no ranking URL changed without a redirect instruction |
| Images | Sized, compressed, `alt` present, permission confirmed |
| WordPress | Block/template integrity, category and tag assignment, publish state |
| API / integration | Any operation touching production is authenticated, scoped, and dry-runnable |

Every technical finding carries **acceptance criteria and a verification method**.
A technical issue without one is incomplete and A28 does not emit it
(`../seo/integrations.md` §Codex handoff).

---

## Layer 7 — SNS QA (channel assets only)

| Check | Severity |
| --- | --- |
| Character count within `character_limit` | **Blocking** |
| Video within duration budget | Blocking |
| Format matches the channel (carousel, thread, short video…) | Major |
| Hook present and compliance-clean | **Blocking** |
| CTA appropriate to the channel objective | Major |
| Hashtags: count sane, none implying a guarantee | **Blocking** if guarantee |
| On-screen text and thumbnail compliance-swept | **Blocking** |
| Every first-hand claim traceable | **Blocking** |
| Attribution markers present on judgments | **Blocking** |
| Disclaimer present where a judgment appears | **Blocking** |
| Post is whole on its own, not an excerpt | Major |
| Photo permission confirmed for visual channels | **Blocking** |
| Brand tone consistent across channels | Major |
| **LINE**: A30 review completed | **Blocking** |
| Not a verbatim cross-post of another channel | Major |

---

## Cross-cutting: routing

Every finding names the agent that must fix it. A finding routed to nobody is an
incomplete finding.

| Finding type | Owner |
| --- | --- |
| Compliance | A30 adjudicates → A08 / A10 applies the binding reworing |
| Fabrication, unsourced claim | A08 |
| Missing source material | A08 → A07 (gap report) |
| Wrong angle, wrong persona, ambiguous brief | A07 |
| Cannibalisation, keyword, internal link architecture | A06 |
| HTML, schema, metadata, WordPress, redirects | **Codex** |
| Channel format, hashtags, hooks | A10 |
| Photo permission | Human |
