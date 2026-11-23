# Benchmark v2.0 — preflight, 2026-11-23

**Execution: `BLOCKED_SOURCE` / `NOT_RUN`.** This is a new observation, not a change to the original manifest or the v1 MCP record. Reviewed the v2 source at merge `361ca3b5cae566dcab19effa5bd02ab059e21a5d`; ran its unmodified local validator: **SPEC LINT PASS** (structure only).

## Website entitlement (read only; no submission)

- The authenticated **Subscription → Active unlimited models** table showed the primary GPT Image 2.6 offer **Active**, **Starts Nov 20, 2026**, **Expires Nov 27, 2026**. The UI supplied dates, not an expiry timestamp. Nov 20 was not the expiry.
- In the ordinary image page the selected configuration was **GPT Image 2.6 Sunburst**, 16:9, 1K, Medium, PNG, single output, no reference or element attached. With Unlimited off, the empty form showed `Generate 1`. With Unlimited checked, the submission control displayed `Unlimited` instead of a numeric credit price. The provider [documents this eligible PNG tier](https://higgsfield.ai/blog/gpt-image-2-6-higgsfield) and [no credit deduction for website Unlimited](https://higgsfield.ai/creator-hub/help-center/credits/how-credits-work). This is a preflight observation, not a per-prompt cost or post-generation usage receipt. Recheck the checked switch and unambiguously free submission indicator on each fully populated form.
- No generation, reroll or paid substitute was submitted. **0 jobs, P1 0/18, P2 0/12; 0 incremental benchmark Credits.** No observed post-render reconciliation, since no render occurred. No ratings, winner or Style Bible derived from tests.

## Candidate pins and static review

| Candidate | Reviewed revision | Prompt-stage disposition |
| --- | --- | --- |
| Unimage | [db916e7](https://github.com/huanmu-team/unimage/tree/db916e7ea2764e99e8c379adcb63a8c32f06e7ee) | MIT; use the reviewed Reverse Prompt Mode stage guides with a vision-capable interpreter and stop at first draft. Optional renderer, API-dependent eval helper and repair are excluded. |
| Caph-dev | [27d248d](https://github.com/Caph-dev/image-style-prompt-reverse-engineer/tree/27d248dceb71f19af5de39859dbada6cc779302f) | MIT; Markdown prompt workflow, no required executable or external endpoint. Intentionally abstracts the subject. Preserve this behavior and record its effect on reconstruction rather than silently embellishing its output. |
| Niobium617 | [8eb9b0d](https://github.com/niobium617/prompt-reverse-engineer-skill/tree/8eb9b0d385839992c8c45acf8c1aa7b382eb5a27) | MIT; local-image analyzer with optional network input, separate semantic analysis and local compiler. Deny network, use approved local paths only, and record original output and any common-target syntax adapter separately. |

Static review only. No scripts, installers, external paid APIs or provider calls were run for the candidates. No prompt was produced from an unapproved input. Keep raw and sent prompts separately and lock transformations, three original replacement subjects, and the common inference budget before P1.

## Blocking evidence

The three cases in the merged manifest have no source file/URL, digest or verified analysis/transfer permission. A public work's availability is not proof that it can be sent to a hosted vision tool. Supply a rights-cleared portrait, environment, and prop/action still, with a source/license and processing scope for each. Keep reference files out of Git and out of Higgsfield generation. The ScrapeCreators API remains unrun and is not required if the references are ready.

After source clearance, freeze the inputs and recheck live entitlement before P1. P2 is selected only after blind P1 scores are locked. No account or billing data, browser evidence screenshots, or source media are included here.
