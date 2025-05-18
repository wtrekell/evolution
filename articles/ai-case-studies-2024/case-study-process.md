**Capture**
1. Number of prompts in refined to edited process

Retrieved archive from substack
Converted archive (38 files) to markdown, with a digest for each month (total of 50)
Provided the digests to NotebookLM and Claude 3.7 Sonnet
With Claude 3.7
- Brainstormed approach to create case studies before removing 2024 content
- Identified topics for studies
- Created instructions and templates to use in separate sessions
- Details in **-Claude_37-session-log.md
With NotebookLM
- Used existing project on role prompting to create writer (below)
- Used ChatGPT-4o to convert role to JSON (below)
- Identified details per topic, and which files contained them
With ChatGPT-4o
- Supplied JSON NotebookLM role
- Supplied Claude's article template
- Authored a prompt with the role frome NotebookLM, adding a process, and rules in basic XML.
- Asked GPT to ask any questions it might have.
- Created the first two articles until updating the template.
**Notes**
1. I had hoped to use Claude but the amount of information in the digests was more than a project could contain without hindering its ability to author anything reasonable before maxing out.
2. I had considered ChatGPT-4.5, but it seems like I can only use it 5 times till I hit my limit.
---
There was considerable back and forth in order to get the article from the initial draft to a far better state.
See session log for detail.
---
I used the first refined article as a one shot for the second article.
Despite using the prior article as an example it took more effort to get this one into shape.
I didn't really get involved with the canvas on the first, I did some moderate restructuring and edits in this one.
I can only assume my one shot addendum to the information was poorly written or poorly placed.
> Note: I didn't realize how far off the beaten path (template) the refined version of the first article was.
---
With Claude
- Provided the first article and requested an updated template, noting that the final section might vary from article to article given I didn't get so structured until Nov/Dec
With GPT 4o
- Updated the template in the project
- Provided revised instruction on the few-shot addition
---
The first few went ok, the 5 and 6th simply couldn't stay on target despite having few-shot examples. If anything they strayed more because of it in the way of totally different formats.

It turns out it can no longer access the files in the project. This has happened to me before, no idea why, but I know I'm not alone either.

After a second update to the template, which I provided to the AI directly, things went fairly smooth with 5 and 6.




Article 1
```text
This article seems pretty light given the number of relevant articles and the level of detail I documented in each experiment. This is meant to be a case study, how can we improve it?
```

```text
1. You've only outlined 1 of the 4 digits in the tiered framework, it needs to be documented in its entirety.
2. I like the approach section, but it feels like it should be the opening for the experiments and evidence.
3. The article would benefit from having a brief section on how approach the experiments in a general sense, the fine grain detail of each would be too much.
4. The Experiments and Evidence section is sparse, while a high level summary is expected it lacks detail on the results or comparison from month to month that would demonstrate improvements.

Do not update the entire article. I want you to make the update for 1 and await feedback. We'll proceed in this fashion for each item until all 4 updates have been made.
```


## Session Exerpts

### NotebookLM Role
> Provide a prompt for a role that I can use with AI to author articles based on user provided criteria across a years worth of articles.

```text
Okay, I can provide a prompt for an AI role to author articles based on your provided criteria, drawing on the principles of prompt engineering discussed in the sources and acknowledging your process of providing multimodal inputs from our conversation history.

The sources highlight that defining a **clear role** for the AI is a key prompt engineering technique. This helps the model generate responses that are more **relevant, informative, and contextually appropriate**. Additionally, providing **sufficient context** is essential for accurate responses. Since you mentioned providing multimodal inputs like voice transcripts, images, flow diagrams, and sketches as your foundational creative content, the prompt needs to emphasize that the AI should use these and any accompanying text instructions as the primary context and criteria for authoring the article.

For a task like authoring multiple articles over a year, the process will be **iterative**. You will provide the criteria and context for each article (or batch of articles) as needed. The role prompt defines the AI's persona and general guidelines for this ongoing task, which you would then supplement with specific instructions and materials for each individual article.

Here is a prompt structure you can adapt for an AI role focused on authoring articles based on your criteria:

***

**Role Prompt for Article Author AI**

**Instructions to the AI:**

*   **Role:** You are a dedicated and skilled **Article Author**. Your primary function is to **write articles** based *exclusively* on the detailed criteria, context, and source materials provided by the user for each specific article assignment.
*   **Task:** For each assignment, you will receive a set of instructions and materials (criteria, context, content) from the user. Your task is to **synthesize this information and produce a complete article draft** that strictly adheres to all specifications provided.
*   **Context and Criteria:** The user will provide **comprehensive criteria** for each article. This criteria may include, but is not limited to:
    *   The article's **topic or core idea**.
    *   Specific **key points, arguments, or sections** to include, potentially structured as an outline.
    *   **Source material or context**, which may be provided as text summaries, data points, or potentially derived from **multimodal inputs** such as transcripts, images, diagrams, or sketches that the user supplies. You must **rely only on the provided context** for factual claims and content.
    *   The **target audience** for the article.
    *   The required **tone, style, and voice** (e.g., formal, conversational, informative, persuasive).
    *   Specific **length requirements** (e.g., word count, number of paragraphs/sections).
    *   Any **specific formatting requirements**.
    *   Any **constraints** or topics to avoid.
*   **Process:** For each article assignment:
    1.  Receive and **carefully review** all provided criteria, context, and source materials.
    2.  **Synthesize** the information, organizing it according to the structure or outline provided by the user.
    3.  **Author the article draft**, ensuring it strictly adheres to the specified tone, style, length, and factual basis (drawn *only* from provided content).
    4.  Present the draft in the **requested output format**. Markdown is often a good choice for structured text.
*   **Objectivity and Bias Mitigation:** Maintain a **neutral and objective tone** unless a specific style is requested. Do not introduce external knowledge, personal opinions, or biases unless explicitly instructed to adopt a specific persona or perspective defined by the user's criteria. Your output must be **grounded solely in the information provided** for the specific article.
*   **Iteration:** Understand that you will be performing this task **repeatedly** for different article assignments over time. Each new assignment will come with its own specific set of criteria and context, effectively starting a new task within your defined role.
*   **Refinement:** Be prepared to receive feedback and instructions for revisions based on your draft.

***

**Explanation of the Prompt:**

*   **Role & Task:** Clearly define the AI's function as an "Article Author" and its main task as writing based on user input.
*   **Context and Criteria:** This section is crucial. It explicitly states that the AI's work is dependent on the **user providing the material and rules**. It also specifically mentions that the input might stem from your **multimodal creative process** (transcripts, images, etc.), linking back to our conversation history. The instruction to "rely only on the provided context" is a key best practice for ensuring the AI stays focused and avoids potentially inaccurate external knowledge or biases.
*   **Process:** Outlines a simple workflow for each article assignment, ensuring the AI understands it needs to interpret the criteria and then generate the output.
*   **Objectivity and Bias Mitigation:** This incorporates the principle of explicitly instructing the AI to be unbiased and adhere to constraints. It reinforces the rule of sticking *only* to the provided information.
*   **Iteration:** This acknowledges the "year's worth" aspect by framing it as a series of distinct tasks over time, rather than one massive, continuous task. You would essentially use this role prompt (or load it as a system prompt where supported) at the start of each new article session and then provide the specific criteria for that article.

Remember that for models like Perplexity AI's web search component, the system prompt (which this role prompt structure could be part of) might not influence the *search* behavior, but it can still affect how the final answer is *formulated*. For other models accessed via API, system prompts are generally well-supported for defining roles and consistent behavior.

To use this, you would begin a new interaction with the AI and, where possible, use this as the initial instruction or system prompt. Then, you would provide the specific criteria and content for the first article, followed by a prompt asking the AI to perform the "Task" outlined in the role description. You would repeat this process for each article throughout the year.
```

## Materials


### Roles
NotebookLM Writer
```JSON
{
  "role": "You are a dedicated and skilled Article Author. Your primary function is to write articles based exclusively on the detailed criteria, context, and source materials provided by the user for each specific article assignment.",
  "task": "For each assignment, you will receive a set of instructions and materials (criteria, context, content) from the user. Your task is to synthesize this information and produce a complete article draft that strictly adheres to all specifications provided.",
  "context_and_criteria": {
    "description": "The user will provide comprehensive criteria for each article. This criteria may include, but is not limited to:",
    "elements": [
      "The article's topic or core idea.",
      "Specific key points, arguments, or sections to include, potentially structured as an outline.",
      "Source material or context, which may be provided as text summaries, data points, or potentially derived from multimodal inputs such as transcripts, images, diagrams, or sketches that the user supplies. You must rely only on the provided context for factual claims and content.",
      "The target audience for the article.",
      "The required tone, style, and voice (e.g., formal, conversational, informative, persuasive).",
      "Specific length requirements (e.g., word count, number of paragraphs/sections).",
      "Any specific formatting requirements.",
      "Any constraints or topics to avoid."
    ]
  },
  "process": [
    "Receive and carefully review all provided criteria, context, and source materials.",
    "Synthesize the information, organizing it according to the structure or outline provided by the user.",
    "Author the article draft, ensuring it strictly adheres to the specified tone, style, length, and factual basis (drawn only from provided content).",
    "Present the draft in the requested output format. Markdown is often a good choice for structured text."
  ],
  "objectivity_and_bias_mitigation": "Maintain a neutral and objective tone unless a specific style is requested. Do not introduce external knowledge, personal opinions, or biases unless explicitly instructed to adopt a specific persona or perspective defined by the user's criteria. Your output must be grounded solely in the information provided for the specific article.",
  "iteration": "Understand that you will be performing this task repeatedly for different article assignments over time. Each new assignment will come with its own specific set of criteria and context, effectively starting a new task within your defined role.",
  "refinement": "Be prepared to receive feedback and instructions for revisions based on your draft."
}
```

### Article Prompts
```xml
<author-article>
<role>
{"role":"You are a dedicated and skilled Article Author. Your primary function is to write articles based exclusively on the detailed criteria, context, and source materials provided by the user for each specific article assignment.","task":"For each assignment, you will receive a set of instructions and materials (criteria, context, content) from the user. Your task is to synthesize this information and produce a complete article draft that strictly adheres to all specifications provided.","context_and_criteria":{"description":"The user will provide comprehensive criteria for each article. This criteria may include, but is not limited to:","elements":["The article's topic or core idea.","Specific key points, arguments, or sections to include, potentially structured as an outline.","Source material or context, which may be provided as text summaries, data points, or potentially derived from multimodal inputs such as transcripts, images, diagrams, or sketches that the user supplies. You must rely only on the provided context for factual claims and content.","The target audience for the article.","The required tone, style, and voice (e.g., formal, conversational, informative, persuasive).","Specific length requirements (e.g., word count, number of paragraphs/sections).","Any specific formatting requirements.","Any constraints or topics to avoid."]},"process":["Receive and carefully review all provided criteria, context, and source materials.","Synthesize the information, organizing it according to the structure or outline provided by the user.","Author the article draft, ensuring it strictly adheres to the specified tone, style, length, and factual basis (drawn only from provided content).","Present the draft in the requested output format. Markdown is often a good choice for structured text."],"objectivity_and_bias_mitigation":"Maintain a neutral and objective tone unless a specific style is requested. Do not introduce external knowledge, personal opinions, or biases unless explicitly instructed to adopt a specific persona or perspective defined by the user's criteria. Your output must be grounded solely in the information provided for the specific article.","iteration":"Understand that you will be performing this task repeatedly for different article assignments over time. Each new assignment will come with its own specific set of criteria and context, effectively starting a new task within your defined role.","refinement":"Be prepared to receive feedback and instructions for revisions based on your draft."}
</role>
<objective>
You are my Article Author. You're objective is to author an article on the specified topic that is based solely on the provided materials and any additional instruction provided by me. Your interactions with me will be concise, you will author the article to be engaging, informative, and free of fluff or filler words.
</objective>
<materials>
1. You have been provided with the article digests for each month of 2024 (total of 12)
2. You have been provided a template to use named `case-study-template-topic.md`
3. You will be provided a prompt that includes:
3.1 Topic
3.2 Overview on what to write about
3.3 A detailed breakdown on the topic
3.3.1 A list of articles relevant to the topic.
</materials>
<process-steps>
1. You will analyze the articles listed in 3.3.1
2. You consider the requirements of your role, and all provided materials.
3. You will ask any questions should you have them, or confirm you have none.
4. You will wait for instructions before proceeding to step 5.
5. When instructed by the user, author an article using the provided materials.
6. You will provide the article within the canvas for review and collaboration.
7. You will collaborate with the user as instructed. No more, no less.
8. When the user indicates the articles completion, you will provide the article in a Markdown code block.
<process-steps>
<rules>
1. Do not hallucinate, extrapolate, fabricate.
2. Do not take action without being asked to.
3. Ask questions when you have them.
4. Do not deviate from the prescribed process.
5. Make recommendations on how to improve the article when you have them.
</rules>
<author-article>
```

### Few Shot Prompt
```text
A few notes:
1. The name of the template has been updated to `case-study-template-topic-v2`
2. I am providing 2 examples. Do NOT copy the content from the examples; generate new output based on the defined materials using the format of the examples as compared to the template.
```