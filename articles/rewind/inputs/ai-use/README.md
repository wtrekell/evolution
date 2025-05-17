# AI Use & Methodology

## Overview

We use artificial intelligence (AI) tools as part of a structured content development process. This policy outlines when, how, and why AI is used, and clarifies the boundaries of human authorship and editorial accountability. It is designed to support ethical transparency, align with evolving platform and regulatory expectations, and reinforce reader trust.

We use AI in the spirit of collaboration, not automation. We're exploring how AI fits into creative workflows—sometimes to accelerate work, sometimes to challenge assumptions, and always to better understand its capabilities. AI helps us start at a run, but never finishes without rigorous human reflection, curation, and ownership.

## AI Use Methodology

Each article goes through four editorial stages. AI tools are used selectively throughout, and disclosures are tied to the extent and significance of AI involvement.

### Tools Used by Stage

| Tool / Model | Research | Drafting | Structural&nbsp;Editing | Micro-edits | Final&nbsp;Authoring | Visuals | Notes |
|--------------|:-------:|:-------:|:-----------------------:|:-----------:|:--------------------:|:-------:|-------|
| **Perplexity** | ✓ | | | | | | Used to surface sources & location of supporting data |
| **ChatGPT o3** | ✓ | | | | | | Early concept clarification |
| **Gemini 2.5 Pro** | ✓ | | | | | | Deep-dive fact gathering |
| **Claude 3.7 Sonnet** | | ✓ | ✓ | | | | Primary drafting tool |
| **ChatGPT 4.5 (test)** | | ✓ | (exp) | | | | Experimental alt-drafts |
| **Type.ai** | | | | ✓ | ✓ | | Human-led copy-polish & approval |
| **GPT o3-mini** | | | | | | | Generates article "runs" for comparison |
| **GPT o3-mini-high** | | | | | | | Higher-temp variant for runs |
| **Midjourney v6.1 / v7** | | | | | | ✓ | Original images & diagrams |
| **Topaz AI** | | | | | | ✓ | Occasional text-in-image enhancement |

### Authorship Stages

| Stage              | Description                                                                                                                                                                                          |
| ------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **AI Authored**    | An initial draft is generated using models like Claude 3.7 Sonnet or ChatGPT based on structured prompts and source material. This constitutes substantial use and is always disclosed.              |
| **AI Assisted**    | AI (e.g. Claude, ChatGPT) is used to reshape content under explicit direction—refining flow, revising structure, or clarifying meaning. This too is substantial and disclosed.                       |
| **Human-Driven**   | The author edits in tools like Type.ai with light AI suggestions (grammar fixes, synonyms, sentence tweaks). Changes are selective. AI use is minor and editorial control remains human.             |
| **Human Authored** | The final version is fully human-led: no AI is used. This stage includes fact-checking, resolving emotional or ethical concerns, aligning with values, and removing anything misaligned with intent. |

These stages are evaluated with custom tools in `/evolution/resources/article-ethics-py/`, including `generate_runs.py` and `analyze_runs.py`. These scripts calculate retention metrics (how much content is preserved between stages) and model comparisons. All sessions are isolated to prevent contamination or bias.

### Quantitative Analysis

Our retention metrics are calculated using custom Python scripts available in [`/resources/article-ethics-py/`](./resources/article-ethics-py/). These tools measure how much content is preserved between editorial stages:

- **Character retention**: Text similarity at the character level
- **Word retention**: Vocabulary overlap between versions  
- **Sentence retention**: Structural similarity of sentences
- **Paragraph retention**: How many paragraphs remain recognizable

The scripts analyze transformation from:
- Draft → Refined
- Refined → Edited
- Edited → Final
- Each version → Final (for overall metrics)

Note: Current scripts calculate retention percentages. To determine alteration (human contribution), use: 100% - retention%.

## Disclosure Principles

AI use is disclosed when:

* AI-generated text remains in the published version
* AI influenced the structure or focus of a section
* The article was drafted or revised using substantial AI assistance

Disclosures typically include:

* Names of tools and models (e.g., Claude 3.7 Sonnet, GPT-4.5)
* Editorial stages where AI was used
* Approximate extent (e.g., "moderate AI assistance")
* Why AI was used (e.g., to jumpstart structure or expand ideas)
* A link to this policy

Quantitative outputs like retention percentages (from our internal analysis tools) are used for internal accountability. They are estimative and not disclosed without appropriate context.

### Disclosure Examples

Based on retention metrics from our analysis tools:

**High Human Contribution (low retention from draft)**
> This article underwent substantial human revision. Final retention from initial AI draft: [X]%.

**Moderate Human Contribution (medium retention)**
> AI tools assisted in drafting, with significant human editing. Final retention: [X]%.

**Limited Human Revision (high retention)**
> AI-generated content was lightly edited. Final retention: [X]%.

Note: Specific disclosure language should be adapted based on actual retention percentages and context.

## Human Accountability

All outputs are reviewed and finalized by a human author. The final stage of work is where:

* Facts are verified
* Style and voice are aligned
* Emotional tone is assessed
* Misalignment with personal values is corrected

This stage reflects not just technical editing but an emotional and intellectual check-in—ensuring the final work is something the author stands behind. Authorship, accountability, and copyright rest with the human.

## Visual Attribution

Articles include charts showing:
- Content retention across stages
- Human vs AI contribution percentages
- Transformation flow from draft to final

These visualizations are generated automatically by our analysis tools and included at article footers.

## Policy Version History

- **v1.2** (Current) - Added quantitative analysis tools and visual attribution
- **v1.1** - Expanded disclosure categories
- **v1.0** - Initial policy

Last updated: January 2025