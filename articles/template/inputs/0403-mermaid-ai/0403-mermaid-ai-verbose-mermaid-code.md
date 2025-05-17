%%{init: {"flowchart": {"defaultRenderer": "elk"}} }%%
flowchart LR
    %% ELK layout
    classDef primary fill:#266673,stroke:#1C4C56,color:#ffffff
    classDef secondary fill:#7AA3B8,stroke:#5C7C8A,color:#ffffff
    classDef background fill:#EFF5F7,stroke:#B3B8B9,color:#515B61
    classDef accent fill:#FFD700,stroke:#B3A123,color:#000000

    %% Define Subgraph Ideation
    subgraph Ideation["Ideation"]
        perplexityAI("Perplexity AI Research")
        convReading("Conversations or Readings")
        defineTopic["Define Topic"]
        createProtocol["Create Research Protocol"]
        conductExperiments["Conduct Experiments"]
        writeTopic["Write about Topic"]
        createImages["Create Images"]
    end

    %% Define Subgraph Authoring
    subgraph Authoring["Authoring"]
        doInterview["Conduct Interview"]
        createBrief["Create Brief"]
        draftArticle["Draft Article"]
        refineArticle["Refine Article"]
        editArticle["Edit Article"]
        finalEdit["Perform Final Edits"]
    end

    %% Central Roles and Templates
    roles(["Roles"])
    templates(["Templates"])
    archive(["Archive"])

    %% Define Subgraph Processing
    subgraph Processing["Processing"]
        refinement["Refinement Process"]
        repurposing["Repurposing"]

        %% Processing Nodes
        detailedExperiment["Experiment Article - Detailed"]
        theory["Theory"]
        engagingExperiment["Experiment Article - Engaging"]
        thoughtLeadership["Thought Leadership"]
        toolAssessment["Tool Assessment"]
        tutorial["Tutorial"]
    end

    %% Define Relationships Outside Subgraph
    newsletter["Newsletter"]
    perplexityAI --> defineTopic
    convReading --> defineTopic
    defineTopic --> createProtocol & conductExperiments & createImages
    createProtocol --> conductExperiments & initialInventory[("Initial Inventory & Materials")]
    conductExperiments --> initialInventory & writeTopic
    writeTopic --> initialInventory
    createImages --> initialInventory & writeTopic
    initialInventory --> doInterview & draftArticle
    doInterview --> createBrief
    createBrief --> draftArticle
    draftArticle --> refineArticle
    refineArticle --> editArticle
    editArticle --> finalEdit

    %% Roles and Template Inputs
    roles --> doInterview & draftArticle & editArticle
    roles --> repurposing

    %% Processing Subgraph Connections
    createBrief --> refinement
    draftArticle --> refinement & updatedInventory[("Updated Inventory & Materials")]
    refineArticle --> refinement & updatedInventory
    editArticle --> refinement & updatedInventory
    finalEdit --> refinement & updatedInventory & repurposing
   
    %% Templates Connections
    templates <--> detailedExperiment
    templates <--> theory
    templates <--> engagingExperiment
    templates <--> thoughtLeadership
    templates <--> tutorial
    templates <--> toolAssessment

    %% Final Inventory Connections
    updatedInventory --> finalInventory[("Final Inventory & Materials")]
    detailedExperiment --> newsletter
    theory --> newsletter
    engagingExperiment --> newsletter
    thoughtLeadership --> newsletter
    tutorial --> newsletter

    detailedExperiment --> refinement & finalInventory
    theory --> refinement & finalInventory
    engagingExperiment --> refinement & finalInventory
    thoughtLeadership --> refinement & finalInventory
    tutorial --> refinement & finalInventory
    toolAssessment --> refinement & finalInventory
    finalInventory --> archive

    %% Source to Refinement Process
    refinement --> roles
    refinement --> templates

    %% Final Publish Node
    finalEdit --> publish("Publish on Substack")
    detailedExperiment --> publish
    theory --> publish
    engagingExperiment --> publish
    thoughtLeadership --> publish
    tutorial --> publish
    toolAssessment --> publish

    %% Apply Class Definitions
    perplexityAI:::primary
    convReading:::secondary
    defineTopic:::background
    createProtocol:::primary
    conductExperiments:::primary
    writeTopic:::primary
    createImages:::primary
    doInterview:::secondary
    createBrief:::secondary
    draftArticle:::secondary
    refineArticle:::secondary
    editArticle:::background
    finalEdit:::background
    updatedInventory:::primary
    initialInventory:::primary
    finalInventory:::primary
    roles:::primary
    templates:::primary
    archive:::primary
    refinement:::secondary
    repurposing:::background
    detailedExperiment:::secondary
    theory:::secondary
    engagingExperiment:::primary
    thoughtLeadership:::primary
    toolAssessment:::primary
    tutorial:::primary
    newsletter:::accent
    publish:::accent
