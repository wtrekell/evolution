%%{init: {"flowchart": {"defaultRenderer": "elk"}} }%%
flowchart LR
    classDef primary fill:#266673,stroke:#1C4C56,color:#ffffff
    classDef secondary fill:#7AA3B8,stroke:#5C7C8A,color:#ffffff
    classDef tertiary fill:#FFD700,stroke:#B3A123,color:#000000
    classDef neutral fill:#EFF5F7,stroke:#B3B8B9,color:#515B61

    Topic("Select Topic"):::tertiary --> Idea

    subgraph Idea["Ideation"]
        PAI(["Perplexity AI"])
        OA(["Online Articles"])
        RE(["Research & Experiment"])
        Sum(["Write Summary"])
        PAI & OA & RE --> Sum
    end

    Idea --> IArch[("Initial Archive")]
    IArch --> Auth

    subgraph Auth["Authoring"]
        IB(["Interview Brief"])
        DA(["Draft Article"])
        RA(["Refined Article"])
        EA(["Edited Article"])
        FA(["Final Article"])
        IB --> DA & RA & EA
        DA --> RA
        RA --> EA
        EA --> FA
    end

    Auth --> UArch[("Updated Archive")]
    UArch --> Proc

    subgraph Proc["Processing"]
        ED(["Experiment Details"]) --> TL(["Thought Leadership"])
        ED --> EN(["Experiment Narrative"]) & TA(["Tool Assessment"]) & Tut(["Tutorial"])
        TA <--> Tut
        Th(["Theory"]) -.-> TL
    end

    Proc --> Pub[Publish]:::tertiary
    UArch --> FArch[("Final Archive")]

    Roles(["Roles"]) & Temp(["Templates"]) --> Auth & FArch
    Temp --> Proc
    Refine(["Refinement Process"]):::neutral

    %% Source to Refinement Process
    Auth & Proc --> Refine --> Roles & Temp

    %% Apply Class Definitions
    PAI:::primary
    OA:::secondary
    RE:::primary
    Sum:::neutral
    IB:::secondary
    DA:::secondary
    RA:::secondary
    EA:::secondary
    FA:::secondary
    UArch:::primary
    IArch:::primary
    FArch:::primary
    Roles:::primary
    Temp:::primary
    Refine:::neutral
    ED:::secondary
    Th:::secondary
    EN:::primary
    TL:::primary
    TA:::primary
    Tut:::primary