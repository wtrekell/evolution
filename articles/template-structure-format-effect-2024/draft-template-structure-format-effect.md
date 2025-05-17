## Template Structure & Format Effects

### Background

As large language models (LLMs) advanced in 2024, so did the methods used to prompt them effectively. A central area of experimentation was the progression from loosely defined requests to structured, highly formatted templates. These templates evolved not only in content but also in markup language, shaping how clearly and creatively models could respond. Trials conducted throughout the year tested variations of markup (XML, JSON, Markdown, YAML, TOML), template rigidity, and specific structural elements to determine their effect on output quality.

---

### Markup Format Comparisons

#### XML and JSON: Early Advances

Minimal XML templates were among the first structured formats introduced. Their clarity and ordered syntax improved adherence to specifications, especially when paired with chain-of-thought (CoT) prompting. Claude benefited most from this format, generating more logically coherent and detailed content. Shortly after, JSON templates took center stage. JSON's compact, unambiguous structure proved effective for encoding both roles and task specifications. GPT-4, while still responding well to XML for step-by-step processes, adapted well to JSON formats, especially in data-heavy or role-based instructions.

#### Full Format Benchmarking

In September, a dedicated experiment tested XML, JSON, TOML, YAML, and Markdown. Results were mixed:

* One evaluation scored YAML and XML highest.
* Another favored TOML, followed by XML and JSON.
* A composite ranking pattern emerged: Claude-XML > TOML-GPT > XML-GPT > JSON-GPT > YAML-GPT.

Despite inconsistencies, JSON-formatted author roles consistently produced top-tier articles in multi-day test events, affirming its utility in precise role specification. XML maintained its strength in guiding GPT through procedural writing, while TOML’s compact syntax showed promise but was less widely supported. YAML performed well with Claude but inconsistently with GPT models.

---

### Rigidity vs Creative Flexibility

As templates became more detailed, output structure and consistency improved. However, too much rigidity often constrained creativity:

* Claude's best-performing templates featured concise numbered sections and flexible bullet points. This format preserved structure without stifling style.
* OpenAI models, especially GPT-4, were more sensitive to over-specified templates, sometimes reverting to generic prose when overloaded with nested requirements.
* Experiments specifying tone often produced unintended template drift, where the model deviated from format to prioritize voice or affect.

One critical failure in a rushed experiment involved poorly designed template updates. These changes, lacking clarity and internal logic, triggered a measurable drop in content quality. The result emphasized that not just structure but **thoughtful structure** is vital.

---

### High-Performing Template Elements

Certain features emerged as consistent contributors to quality:

* **Chain prompting** combined with structured templates elevated clarity and depth.
* **Context-rich guidance**, particularly when cultural depth or multi-day information was included, enhanced both relevance and nuance.
* **Adaptability**, especially in how templates incorporated evolving constraints or events, correlated with stronger narrative cohesion.
* **Progressively layered templates**, beginning with roles, adding outlines, and concluding with tone or audience guidance, produced the most educational and engaging articles.
* Templates that explicitly highlighted goals, avoided unnecessary verbosity, and balanced open sections with structured headers performed best in long-form outputs.

---

### Conclusion

There is no universally superior markup or rigid structure. Instead, the combination of format, structure, and model characteristics determines effectiveness. JSON remains the strongest candidate for defining author roles, while XML and TOML offer unique strengths in procedural or parameter-heavy prompts. The optimal template is both clear and adaptable, striking a deliberate balance between precision and room for creative interpretation.

Ultimately, the most successful templates were not the most complex but the most intentional—those engineered with both structure and narrative flexibility in mind.
