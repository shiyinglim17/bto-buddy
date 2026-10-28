# Model-selection comparison: protocol (pre-registered)

**Status:** written 2026-10-29, **before any model output was generated**. Changes after the
first run are listed in §9 with a reason. Harness: `evaluation/model_selection.py`.

**Purpose:** pick **one** generation model for configurations A–D (REQ-EVL-011, REQ-ARC-011,
REQ-MOD-012). This is a preliminary, small-sample comparison (REQ-MOD-010), not the
evaluation itself.

## 1. Candidates

Facts verified on 2026-10-29 from the providers' own pages (sources in §8).

| | Google AI Studio | GroqCloud |
|---|---|---|
| Model ID | `gemini-3.8-flash` | `openai/gpt-oss-120b` |
| Status | Stable ("New Stable") | Production |
| Weights | Proprietary | Open weights (Apache-2.0) |
| Paid price / 1M tokens (in / out) | $0.75 / $3.75 (rises to $1.50 / $7.50 on 2027-01-01) | $0.15 / $0.60 |
| Structured output | `json_schema` through the OpenAI-compatible endpoint (beta) | `json_schema` with `strict: true` (constrained decoding) |
| Reasoning control | `reasoning_effort` → `thinking_level`; cannot be turned off on 3.x | `reasoning_effort` low / medium / high |
| Rate limits | Not published as a table; shown per account in AI Studio | Developer-plan base: 30 RPM, 1K RPD, 8K TPM, 200K TPD |
| Data use | Free tier: content used to improve products, human review possible, "do not submit sensitive or personal information". Paid tier: not used for training; logged for a limited period for abuse detection | No retention of inference data by default (abuse/troubleshooting logs up to 30 days); Zero Data Retention available to all customers. Training terms are in the Services Agreement, **not verified** here |

**Why these two.** Each is the provider's strongest *stable/production* model that supports
schema-constrained output at a cost that scales (05 and REQ-MOD-001). Preview models
(`gemini-3.1-pro-preview`, `qwen/qwen3.8-27b`) were excluded because they can be withdrawn at
short notice, which would break reproducibility of the A–D runs. `gemini-3.5-flash-lite`
was not chosen as the Google candidate because policy reasoning carries the most weight (35%)
and the scorecard already rewards speed and cost.

**Alternatives not tested:**
- **OpenRouter:** a router, not a model. It would add a second set of provider terms and
  route-dependent behaviour; useful only as a fallback endpoint for the chosen model.
- **Local Ollama:** no Ollama installation on the development machine. The only privacy
  advantage is for real applicant data, which the prototype never processes (fictional
  profiles only; D-054 lets fictional profiles and authored facts go to a provider). A
  locally servable model of acceptable quality (e.g. gpt-oss-20b) needs ~16 GB of memory and
  would be several times slower on a laptop, and a reviewer's machine would vary. Revisit for
  a deployment with real data.
- **Fine-tuning:** no training data exists (and none should be created from HDB text, D-054),
  the KB changes with policy, and the approved design grounds answers in retrieved facts
  rather than in weights. Fine-tuning would also make the baseline a different model from the
  pipeline. Not justified.

## 2. Cases

Dev cases only (`evaluation/benchmark/dev.jsonl`, labels approved 2026-10-29). Held-out files
are not opened (D-064).

**Selection rule, fixed in advance:** for each of the six categories, take the first two cases
in file order that have **different `family_id`s**. Result (12 cases):

| Category | Cases |
|---|---|
| standard | DEV-01, DEV-02 |
| missing_information | DEV-04, DEV-05 |
| policy_exception | DEV-07, DEV-09 |
| misconception | DEV-10, DEV-11 |
| conflicting | DEV-13, DEV-14 |
| out_of_scope | DEV-16, DEV-17 |

The other six dev cases are kept unseen by this comparison for later prompt work.

## 3. Task and inputs (identical for both models)

- **Input sent:** `as_of`, `situation_text`, `question`. Nothing else: **no retrieved facts, no
  rule outputs, no labels** (direct generation, configuration A conditions).
- **Instructions:** one system prompt, version `ms-1` (in the harness). It states the
  assistant's role, the out-of-scope list (D-008), no eligibility determinations, no assumed
  values, and asks for the structured output. It does not contain policy facts.
- **Output schema `ms-1`:** a reduced form of architecture §5 `GenerationOutput` for
  configuration A: `summary`; `claims[{claim_id, text, kind}]`;
  `missing_profile_fields[{field, follow_up_question}]`;
  `profile_conflicts[{fields, detail, clarification_question}]`;
  `out_of_scope_reasons[{code, topic, detail}]`. Enums come from the project's `Topic` and the
  benchmark's profile-field keys. `cited_fact_ids` is left out because there is no KB to cite
  in this condition. The schema is strict-compatible (all properties required, nullable via
  `null`, `additionalProperties: false`) and the same JSON Schema is sent to both providers.

## 4. Inference settings (identical where the APIs allow)

| Setting | Value | Note |
|---|---|---|
| Endpoint | OpenAI-compatible `/chat/completions` | Same client code for both (stdlib HTTP) |
| `temperature` | 0 | Architecture §9 |
| `reasoning_effort` | `low` | Same label for both. Internal compute differs by model; recorded, not equalised |
| `max_completion_tokens` | 6000 | Includes reasoning tokens |
| `response_format` | `json_schema`, `strict: true` | |
| Runs | 1 per case per model | Speed priority; limitation in §7 |
| Retry | One retry with the validation error, as architecture §9 | First-attempt and after-retry validity both recorded |

## 5. Scorecard (weights from 04 §6.3)

Scoring is done **blind**: outputs are shown as "System 1 / System 2" with a random,
per-run assignment stored in a key file that is read only after scoring. Scored against the
approved dev labels (`key_points`, `prohibited_conclusions`, `required_missing_fields`,
`expected_conflicts`, `out_of_scope`, `expected_behaviour`). The coding agent scores; the
developer spot-checks and can override. The scorer is not either candidate model.

| Criterion | Weight | Per-case measure | Aggregate |
|---|---|---|---|
| Policy reasoning accuracy | 35% | Key points: 1 conveyed correctly, 0.5 partly, 0 absent or wrong; case score = mean. **Any critical prohibited conclusion sets the case to 0.** Major prohibited conclusions are counted | Mean over 12 cases |
| Structured-output reliability | 25% | First attempt parses and validates against schema `ms-1` | Valid / 12 |
| Uncertainty handling | 20% | 1 / 0.5 / 0 on the case's expected behaviour: missing fields asked (recall over `required_missing_fields`), conflict flagged neutrally, out-of-scope declined and redirected without computing, answerable case answered without over-abstaining, no unhedged definitive claim on an unknown | Mean over 12 cases |
| Latency | 10% | Wall-clock per successful call | 10 × (best median / this median) |
| Estimated cost | 10% | Tokens (incl. reasoning) × paid list price | 10 × (cheapest mean / this mean) |

## 6. Minimum acceptance (applied before the weighted total)

A model is **not acceptable**, whatever its total, if any of these holds:
1. fewer than 12/12 outputs valid after the one retry, or fewer than 11/12 valid on the first
   attempt;
2. 4 or more of 12 cases with a critical prohibited conclusion (critical-error rate ≥ 33%);
3. policy reasoning accuracy below 0.50.

Thresholds 2 and 3 are deliberately loose because this is direct generation without evidence:
errors from missing policy knowledge are expected and are what configurations B–D address.
If both models fail, both are reported and the comparison is not used to choose; the decision
goes back to the developer. If both pass and their weighted totals are within 5 points, the
model with fewer critical errors is preferred, then the one with better uncertainty handling.

## 7. Known limitations

- 12 cases, one run each: no statistical power; differences of one or two cases are noise.
- Agent scoring against labels; blind but not independent of the label author. Developer
  spot-check required.
- `reasoning_effort: low` is a matched label, not matched compute.
- Latency depends on time of day, network path from Singapore to US endpoints and account
  tier; it is a snapshot.
- Prices are list prices on 2026-10-29; Gemini 3.8 Flash's doubles on 2027-01-01.

## 8. Sources (accessed 2026-10-29)

- Gemini pricing (last updated 2026-10-27): https://ai.google.dev/gemini-api/docs/pricing
- Gemini models (last updated 2026-10-22): https://ai.google.dev/gemini-api/docs/models
- Gemini OpenAI compatibility: https://ai.google.dev/gemini-api/docs/openai
- Gemini rate limits: https://ai.google.dev/gemini-api/docs/rate-limits
- Gemini API terms (last modified 2026-04-28): https://ai.google.dev/gemini-api/terms
- Groq models: https://console.groq.com/docs/models
- Groq structured outputs: https://console.groq.com/docs/structured-outputs
- Groq rate limits: https://console.groq.com/docs/rate-limits
- Groq data handling: https://console.groq.com/docs/your-data

## 9. Changes after the first run

None change the cases, prompt, schema, settings or scoring. All were made before any model
output had been seen.

1. **Aborted attempt `20261028T200613Z` (deleted).** Gemini returned HTTP 503, and the
   harness crashed because Gemini's error body is a JSON list. No case output was produced.
   Fixed: error bodies are wrapped, and network timeouts are recorded as status 0 and retried
   instead of crashing.
2. **User-Agent.** Groq's CDN rejects urllib's default agent (Cloudflare error 1010, HTTP
   403). The harness now sends the honest identifier `bto-buddy-model-selection/0.1`.
3. **Timeout 120 s → 240 s.** On 2026-10-29 around 20:00 UTC, `gemini-3.8-flash` took 25–104 s
   to answer a one-word probe on both the native and the compatible endpoint (an earlier call
   got HTTP 503). The provider was loaded or the account was queued. A 120 s timeout would
   have recorded most Gemini calls as failures caused by the network rather than the model.
   Latency is still measured and scored as observed.
4. **One process per provider**, writing into the same run directory (`--run-id`), so a slow
   provider doesn't delay the other. Each process writes its own `metadata_<slug>.json`.
