# From Basic Rating Systems to a Nuanced Model Evaluation Framework

Throughout 2024, model evaluations evolved from basic self-assessment scoring into a robust, multi-layered analysis of capabilities and biases across GPT-4, Claude, and other top-tier models. The initial experiments began with simple prompts and single-dimensional evaluations. However, these quickly revealed limitations in consistency, contextual sensitivity, and the ability to capture nuanced performance differences.

What began as simple self-rating exercises transformed into a rigorous, comparative testing regime. Over the year, the team developed and refined evaluation methods—including dimensional rubrics, scoring scale experiments, and model self-analysis—to surface clearer distinctions in model performance. This article traces that journey and offers a decision-making framework to guide model use for specific content needs.

## Challenge

The initial challenge in comparing model performance was ensuring reliable and interpretable scoring. Early on, models frequently misunderstood or loosely applied scoring criteria. This inconsistency made it difficult to distinguish true performance gaps. For instance, scoring distributions often clustered at the high end—typically 4s and 5s out of 5—reducing the evaluative resolution between merely good and genuinely great outputs.

Ties in top scores became a persistent issue, particularly when evaluating top-tier completions. In many sessions, all outputs were rated nearly identically despite substantive qualitative differences. Session resets and limited context windows—particularly with Claude—undermined scoring consistency. And without grounded reference examples, models defaulted to generous interpretations of quality, amplifying tendencies toward over-scoring and model favoritism.

## Experiments & Evidence

### Approach

Evaluation consistency was improved through a series of rubric redesigns, scale experiments, and prompt engineering strategies. Testing evolved from basic single-score assessments to richer, multi-dimensional evaluations supported by peer-ranking mechanisms. Each iteration aimed to increase differentiation and reduce rating inflation.

* **Detailed Rubrics:** Introduced anchored dimensions like Accuracy, Cultural Sensitivity, and Engagement
* **Refined Scales:** Switched between 1–5, 1–3, 1–4, and 100-point systems to reduce clustering
* **Iterative Recalibration:** Used model self-analysis to reset endpoints and benchmark scores
* **Task Breakdown:** Decomposed complex scoring into smaller, manageable subtasks

Experiments were grouped chronologically to reflect shifts in strategy and insight gained month to month.

Additional refinements emerged through collaborative and model-specific adjustments. Early evaluations required high- and low-quality output examples to ground interpretations of scoring scales. Claude and GPT-4 co-developed initial rubric dimensions, refining definitions over time to reduce variance. Calibration became model-specific: Claude's persistent top-heavy scores prompted narrower rating lanes; Gemini was excluded after erratic formatting broke scoring protocols; GPT-4o’s tendency for ties led to “editor instruction” tie-break techniques. Chain-of-Thought–style rubrics trialed in August and September yielded more consistent scoring than legacy frameworks. Claude’s scoring also evolved—from a 100-point baseline to a 200-point scale by November—offering more precise differentiation across dimensions.

### January: Initial Model Scoring Tests

* Gemini Pro v1 introduced creative flourishes such as self-titling and Arabic phrases, but struggled with template structure and word count discipline.

The year began with models rating their own outputs using a basic 1–5 scale. Initial prompts were narrowly scoped and evaluation dimensions were loosely defined.

* Scoring inconsistency was immediately evident.
* All models demonstrated a generosity bias, rarely using the lower end of the scale.
* GPT-4 offered clearer reasoning in its rationales; Claude favored more optimistic evaluations.

These results prompted a shift toward multi-dimension scoring to surface deeper quality signals.

### April: Dimensional Rubrics & Anchor Testing

* ChatGPT-4 displayed an amusing tendency to favor XML formatting, jokingly self-describing as a "recovering XSLT addict." It also exhibited notable word-count inflation under structured prompt conditions.

Rubrics now included defined criteria—Accuracy, Context Fit, Clarity, and Originality—each with score anchors. Models scored each other across all dimensions.

* Claude consistently over-scored peer outputs by 10–15 points (on 100-point scale).
* GPT-4 better distinguished contextual fit and analytical depth.
* Anchor-based rubrics helped mitigate clustering, but ties in top-tier outputs remained common.

This round confirmed the need for recalibration exercises and scoring diversity prompts.

### July: Chain-of-Thought Rubrics

* Claude's behavior included frequent self-apology rituals and a consistent pattern of generous self-scoring. It also stood out for its success in deducing the four-digit complexity legend embedded in prompt instructions.

Chain-of-Thought (CoT) scoring prompts were introduced, asking models to reason before rating. This method was tested alongside traditional direct scoring.

* CoT prompts improved intra-model consistency and highlighted inconsistencies and blind spots in the existing rubric design.
* Self-reflection sequences helped surface latent biases.
* Models proposed rubric improvements that were incorporated in later trials.

Results showed CoT rubrics improved score distribution variance and made model preferences more transparent.

### October: Recalibration and Top-N Differentiation

* GPT-4o demonstrated improved markdown-table fidelity over time and learned to use prompt instructions strategically to resolve scoring ties.

To reduce tied scores, models were asked to rank top outputs, then re-score based on relative quality.

* Claude remained prone to over-ranking its own completions.
* GPT-4 showed stronger alignment to rubric anchors after recalibration.
* Ranking prompts improved discrimination between high-quality but subtly different outputs.

These findings supported the introduction of forced-ranking and hybrid CoT-anchored scoring in final evaluations. Additionally, o1-preview emerged as particularly strong in synthesizing merged templates and rationalizing layered evaluation guidelines.

## Monthly Model Performance Patterns

| Month     | Highlights                                                                                                                                                                                                                                                                          |
| --------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Early     | ChatGPT-4 consistently outperformed GPT-3.5, Claude, and Bard/Gemini in depth and coherence.                                                                                                                                                                                        |
| May       | GPT-4 scored higher than GPT-4o and Claude on Greenery Day and Vesak tasks.                                                                                                                                                                                                         |
| July      | Claude led across role-based inputs; legacy GPT-4 showed least consistency.                                                                                                                                                                                                         |
| August    | Claude 3.5 Sonnet and GPT-4o improved with complexity; “Super” prompts scored highest.                                                                                                                                                                                              |
| September | TOML templates outperformed YAML; “Ct.md” beat “GPTt.md” in structure tests.                                                                                                                                                                                                        |
| October   | Neutral and Professional tones outperformed Creative and Excited in clarity and stability.                                                                                                                                                                                          |
| November  | GPT-4o best integrated cultural nuance, favoring Claude outputs under vague prompts.                                                                                                                                                                                                |
| December  | Claude improved linearly with prompt complexity (1111 → 3333); GPT-4o peaked at mid-range, suggesting diminishing returns. December's analysis also confirmed that role complexity had the strongest overall impact on output quality, though optimal combinations varied by model. |

## Findings

### Scoring Behavior Variability

* Early prompts led to inflated scores due to lack of grounded context.
* GPT-4 was more consistent across sessions, especially in applying anchor definitions.
* Claude frequently gave top scores across all dimensions, reducing differentiation.

### Evaluation Method Impact

* CoT rubrics increased introspection and score distribution.
* Multi-dimensional scoring revealed strengths in GPT-4's clarity and analytical depth.
* Peer evaluations introduced subtle biases but were mitigated by calibration rounds.

### Contextual Sensitivity

* Longer context windows improved rating stability.
* Claude’s session resets limited longitudinal evaluation.
* Task decomposition made evaluation outputs more reliable and easier to compare.

## Framework

The final evaluation framework allows content teams to select models based on task complexity, tone requirements, and scoring clarity. It includes two components: model capability coding and rubric fit coding.

### Model Capability Coding

| Code | Description                                               | Best Use Cases                                |
| ---- | --------------------------------------------------------- | --------------------------------------------- |
| 1    | High generosity, limited discrimination                   | Early-stage ideation, user-friendly summaries |
| 2    | Balanced scoring, moderate contextual sensitivity         | Informative tasks, explainer content          |
| 3    | High clarity and rubric fidelity                          | Evaluative tasks, benchmarking                |
| 4    | Deep analytical insight with fine-grained differentiation | Critical reviews, technical analysis          |

### Rubric Fit Coding

| Code | Description                                 | Best Use Cases                         |
| ---- | ------------------------------------------- | -------------------------------------- |
| 1    | Loose interpretation, general positivity    | Quick reviews, low-stakes evaluations  |
| 2    | Clear dimensions but weak anchors           | Semi-structured content scoring        |
| 3    | Strong dimensional anchors, some overlap    | Standardized model comparisons         |
| 4    | High-resolution rubric with CoT integration | Final-stage QA, performance baselining |

To use the framework: select model capability code based on task needs, then pair it with the most appropriate rubric fit code.

* **3-4 pairing**: Produces robust benchmarking evaluations
* **1-1 pairing**: Generates friendly but low-resolution reviews

## Implications & Recommendations

The evolution from single-score evaluations to CoT-driven, multi-dimensional frameworks revealed structural biases and scoring inconsistencies across model types. These insights provide practical strategies for evaluating AI-generated content more reliably and ensuring greater consistency across workflows.

**Recommendations:**

* Use CoT-style prompts to reduce generosity bias and expose subtle quality differences
* Apply multi-dimension scoring for deeper quality insights across varied content types
* Calibrate rubric anchors regularly using benchmark examples and forced-ranking rounds
* Select models using a structured capability/rubric framework tied to specific content goals

## Next Steps

* Expand framework testing to include more models (e.g., Gemini, Mistral)
* Develop tooling for auto-calibration of rubric anchors
* Test longitudinal evaluation protocols across persistent sessions
* Apply decision framework to real-time editorial workflows
* Investigate model behavior under different role/task archetypes

---

## Appendix: Monthly Trial Summary

| **Month** | **Focus**                        | **Key Evaluation Shifts**                                 | **Highlight Finding**                                        |
|-----------|----------------------------------|------------------------------------------------------------|--------------------------------------------------------------|
| Jan ’24   | Initial Scoring Systems          | Single-score self-ratings; no scale anchors                | Generosity bias masked performance differences               |
| Apr ’24   | Rubric Anchors & XML Bias        | Anchor-based dimensions; GPT-4’s XML formatting            | XML + anchors → increased word count and clearer structure   |
| Jul ’24   | Chain-of-Thought Scoring         | CoT rubrics; self-reflection and recalibration             | CoT improved rubric consistency and exposed scoring gaps     |
| Aug ’24   | Prompt Complexity Effects        | Super prompts; complexity scaling across models            | Claude 3.5 and GPT-4o both improved with increased structure |
| Sep ’24   | Format & Template Testing        | TOML vs. YAML; Ct.md vs. GPTt.md templates                 | TOML and Ct.md templates consistently scored highest         |
| Oct ’24   | Tie-Breaking & Table Fidelity    | GPT-4o markdown table fixes; tone-based scoring            | Professional/Neutral tones boosted clarity and consistency   |
| Nov ’24   | Cultural Nuance & Role Depth     | Complex role handling; vague prompts under scrutiny        | GPT-4o favored Claude’s nuanced outputs in fuzzy contexts    |
| Dec ’24   | Complexity & Role Specificity    | Layered prompt design with 1111 → 3333 sequences           | Role complexity had the strongest impact on final scores     |
