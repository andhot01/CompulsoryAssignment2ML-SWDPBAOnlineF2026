# CompulsoryAssignment2ML-SWDPBAOnlineF2026
Contains the compulsory assignment 2 for machine learning





# Intro to project
This project implements an AutoGen based AI agent that helps a software company find research papers based on user specified constraints.
The agent can: - understand requests about research papers
               - extract constraints such as topic, publication year, and citation count
               - use an external tool to search for papers
               - filter results
               - return a structured answer with metadata and short explanation

The system uses the Semantic Scholar API as its external reaserch paper tool and the free tier of Mistral AI as the cloud-based language model.





# Intro to agent
The agent accepts prompts such as:
"Find a paper about retrieval-augmented generation published before 2021 with more than 500 citations."
"Find a recent paper about AI agents using tools."
"Find a paper about LLM agents for software engineering published after 2021 with at least 100 citations."

Then it iterprets the request, calls the tool to search for relevant papers, and filters the results by year and citaion count. After that it selects the best matching paper and returns a structured response containing: title, authors, publication year, citation count, citation source, link, and an explanation of why it matches.

The agent is designed to not only rely on the LLM's internal knowledge. Citation counts and paper metadat come from the tool, not from the LLM.





# Tool/API used
This project uses the Semantic Scholar API to retrieve research paper metadata. Citation counts shown by the agent come from Semantic Scholar API.





# Workflow
The agent follows this workflow:
1. User makes a request with certain topic and constraint requirements.
2. The LLM interprets the request and calls the paper-search tool.
3. A custom Semantic Scholar tool searches for canditate papers.
4. Python code filters the papers by year constraint, citation constraint, exact/before/after conditions, and approximations when relevant.
5. The LLM selects the best remaining paper and formats the final structured response.
6. *If no paper satisfies the constraints, the agent reuturns "no paper found".





# Divided responsibilities
Handled by the LLM:
- Interpreting user requests
- Selecting best valid candidate
- Writing explanation and/or summary

Handled by deterministic code:
- Comparing years
- Comparing citation-counts
- rejecting invalid results
- enforcing structured filtering

Handled by the external tool:
- Retrieving paper metadata
- Providing citation counts
- Providing links and abstracts





# SETUP INSTRUCTIONS
Step 1
Clone the repository:
git clone https://github.com/andhot01/CompulsoryAssignment2ML-SWDPBAOnlineF2026
cd CompulsoryAssignment2ML-SWDPBAOnlineF2026 

Step 2
Create a virtual enviroment:
py -m venv .venv
.venv\Scripts\activate

^^Windows

python3 -m venv .venv
source .venv/bin/activate

^^Mac/Linux

Step 3
Install dependencies:
pip install "autogen-agentchat @ git+https://github.com/patrickstolc/autogen.git@0.2#egg=autogen-agentchat"
pip install autogen==0.3.1
pip install mistralai==1.2.3
pip install ollama==0.3.3
pip install fix-busted-json==0.0.18
pip install requests python-dotenv

Step 4
Configure API keys:
Create a .env file in the project root and add:
MISTRAL_API_KEY=your_mistral_api_key_here

If you also use a Semantic Scholar API key add:
SEMANTIC_SCHOLAR_API_KEY=your_semantic_scholar_api_key_here

And don't commit the .env file to Git

Step 5 
Run the agent:
python main.py

or 

py main.py 

^^Windows

Edit the user_prompt variable in main.py to test different prompts.





# Evaluation
I wrote a small evaluation set of 10 prompt covering:
* broad topics
* narrow topics
* before/after/exact year constraints
* minimum, maximum and approximate citation constraints
* ambiguous requests
* cases where no good papers could be found

I used a manual, but systematic evaluation where I checked the following for each prompt:
The agent: found a relevant paper
           respected the year constraint
           respected the citation constraint
           provided a valid source
           avoided hallucination
           gave a useful explanation




Prompt 1
"Find a paper about artificial intelligence agents with at least 100 citations. Explain why it is relevant."
What the prompt tests - a broad topic with minimum citation constraint and relevance explanation.

Answer
Title: To Be or Not to Be …Human? Theorizing the Role of Human-Like Competencies in Conversational Artificial Intelligence Agents
Authors: Shalini Chandra, Anuragini Shirish, S. Srivastava
Publication Year: 2022
Citation Count: 214
Citation Count Source: Semantic Scholar API
Link: https://www.semanticscholar.org/paper/bfbfc9c12fe5be3c652ba2548ddde5c4f0d0b074
Why It Matches: The paper's title and abstract suggest it explores the role of human-like competencies in conversational AI agents, making it highly relevant to the topic "artificial intelligence agents."
Summary: The paper investigates the importance of human-like characteristics and competencies in conversational AI agents to facilitate smooth user interaction and engagement. It theorizes the key role of cognitive, relational, and emotional competencies and the mediating role of user trust in these relationships. The study uses a sequential mixed methods approach, combining quantitative surveys and qualitative interviews to provide a nuanced understanding of desirable human-like competencies in conversational AI agents.
Uncertainty: None

Relevant paper found? - Yes
Year constraint respected? - None given
Citation constraint respected? - Yes
Valid source provided? - Yes
Hallucination avoided? - Yes
Useful explanation? - Yes



Prompt 2
"Find a paper about LLM agents for software engineering published after 2021 with at least 100 citations. Explain why the paper is relevant and provide the source of the
citation count."
What the prompt tests - a narrow topic with an after-year constraint, a citation minimum and citation source requirement.

Answer
**Title:** Agentless: Demystifying LLM-based Software Engineering Agents
**Authors:** Chun Xia, Yinlin Deng, S. Dunn, Lingming Zhang
**Publication Year:** 2024
**Citation Count:** 332
**Citation Count Source:** Semantic Scholar API
**Link:** https://www.semanticscholar.org/paper/ae50c8e255ba55bdbbb05ea470aa63437534438e
**Why It Matches:** The paper's title and abstract explicitly mention "LLM-based Software Engineering Agents," and it was published in 2024, satisfying the year constraint.
**Summary:** This paper introduces Agentless, a simplistic approach to software development that challenges the complexity of autonomous LLM agents. It outperforms existing agents in terms of performance and cost on the SWE-bench Lite benchmark. The paper also highlights the potential of simple, cost-effective techniques in autonomous software development.
**Uncertainty:** None

Relevant paper found? - Yes
Year constraint respected? - Yes
Citation constraint respected? - Yes
Valid source provided? - Yes
Hallucination avoided? - Yes
Useful explanation? - Yes

Note: ** showed up around the format out of nowhere



Prompt 3
"Find a paper about retrieval-augmented generation published before 2021 with more than 500 citations. Summarize its contribution in 5-7 sentences."
What the prompt tests - before-year constraint with a citation minimum and a summary request.

Answer
Title: Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks
Authors: Patrick Lewis, Ethan Perez, Aleksandara Piktus, F. Petroni, Vladimir Karpukhin, Naman Goyal, Heinrich Kuttler, M. Lewis, Wen-tau Yih, Tim Rocktäschel, Sebastian Riedel, Douwe Kiela
Publication Year: 2020
Citation Count: 13369
Citation Count Source: Semantic Scholar API
Link: https://www.semanticscholar.org/paper/659bf9ce7175e1ec266ff54359e2bd76e0b7ff31
Why It Matches: The paper's title explicitly mentions "Retrieval-Augmented Generation", and it was published in 2020, which is before 2021. It also has more than 500 citations, satisfying all the given constraints.
Summary: The paper introduces a method for retrieval-augmented generation (RAG) using a combination of pre-trained parametric and non-parametric memory for language generation. It fine-tunes and evaluates RAG models on various knowledge-intensive NLP tasks, setting the state-of-the-art on three open domain QA tasks. The results show that RAG models generate more specific, diverse, and factual language than a state-of-the-art parametric-only seq2seq baseline.
Uncertainty: None


Relevant paper found? - Yes
Year constraint respected? - Yes
Citation constraint respected? - Yes
Valid source provided? - Yes
Hallucination avoided? - Yes
Useful explanation? - Yes



Prompt 4
"Find a paper about tool-using AI agents published in 2023 with at least 50 citations. Explain whether it would be useful for someone building autonomous software agents."
What the prompt tests - narrow topic with exact year constraint and explanation request.

Answer
Title: TPTU: Large Language Model-based AI Agents for Task Planning and Tool Usage
Authors: Jingqing Ruan, Yihong Chen, Bin Zhang, Zhiwei Xu, Tianpeng Bao, Guoqing Du, Shiwei Shi, Hangyu Mao, Xingyu Zeng, Rui Zhao
Publication Year: 2023
Citation Count: 62
Citation Count Source: Semantic Scholar API
Link: https://www.semanticscholar.org/paper/dd0612ce863f64b0f69d0d9f708c52e829f6f859
Why It Matches: This paper directly matches the topic of tool-using AI agents and was published in 2023. It has 62 citations, satisfying the constraint of at least 50 citations.
Summary: The paper presents a framework for using Large Language Models (LLMs) in AI agents for task planning and tool usage, demonstrating the potential of these models in complex tasks. It discusses the capabilities needed for LLMs to handle intricate problems and evaluates different agent types using various LLMs.
Uncertainty: None

Relevant paper found? - Yes
Year constraint respected? - Yes
Citation constraint respected? - Yes
Valid source provided? - Yes
Hallucination avoided? - Yes
Useful explanation? - Yes



Prompt 5
"Find a paper about natural language processing published in 2020 with at least 500 citations. Give a short explanation of why it matches."
What the prompt tests - broad topic with an exact year constraint, high citation count and explanation request.

Answer
Title: Domain-Specific Language Model Pretraining for Biomedical Natural Language Processing
Authors: Yu Gu, Robert Tinn, Hao Cheng, Michael R. Lucas, N. Usuyama, Xiaodong Liu, Tristan Naumann, Jianfeng Gao, Hoifung Poon
Publication Year: 2020
Citation Count: 2393
Citation Count Source: Semantic Scholar API
Link: https://www.semanticscholar.org/paper/a2f38d03fd363e920494ad65a5f0ad8bd18cd60b
Why It Matches: The paper's title explicitly mentions "natural language processing," and it was published in 2020, satisfying the given constraints. It has a high citation count of 2393.
Summary: The paper presents a method for pretraining large neural language models specifically for the biomedical domain, demonstrating substantial gains over using general-domain language models. It introduces a comprehensive biomedical NLP benchmark and achieves state-of-the-art results across various tasks. The authors also release their models and create a leaderboard to facilitate research in biomedical NLP.
Uncertainty: None

Relevant paper found? - Yes
Year constraint respected? - Yes
Citation constraint respected? - Yes
Valid source provided? - Yes
Hallucination avoided? - Yes
Useful explanation? - Yes



Prompt 6
"Find a recent paper about AI agents using tools and explain whether it would be useful for building autonomous software agents."
What the prompt tests - ambiguous request (recent - meaning max 2-3 years ago).

Answer
Title: Paper2Agent: Reimagining Research Papers As Interactive and Reliable AI Agents
Authors: Jiacheng Miao, Joe R. Davis, J. Pritchard, James Zou
Publication Year: 2025
Citation Count: 22
Citation Count Source: Semantic Scholar API
Link: https://www.semanticscholar.org/paper/9ccda7b4f093ceb80d057aba41570f437536a867
Why It Matches: The paper's title and abstract explicitly mention "AI agents" and "tools," and it was published in 2025, which satisfies the constraint of being a recent paper.
Summary: The paper introduces Paper2Agent, a framework that converts research papers into AI agents, enabling them to act as knowledgeable research assistants. It demonstrates the effectiveness of Paper2Agent by creating agents that can interpret genomic variants and carry out single-cell and spatial transcriptomics analyses, and even identify new splicing variants associated with ADHD risk. This shows that the paper is relevant to building autonomous software agents, as it demonstrates how to create AI agents from research papers.
Uncertainty: None

Relevant paper found? - Yes
Year constraint respected? - Yes - recent - last year qualifies
Citation constraint respected? - None given
Valid source provided? - Yes
Hallucination avoided? - Yes
Useful explanation? - Yes



Prompt 7
"Find a paper about retrieval-augmented generation published after 2022 with fewer than 200 citations. Explain why it matches the request."
What the prompt tests - maximum citation constraint.

Answer
Result: No matching paper found
Reason: No paper satisfied all requested constraints based on the available tool results.
Uncertainty: The search results may be incomplete or the query may be too restrictive.

Answer when year tweaked to 2024
Title: MedRAG: Enhancing Retrieval-augmented Generation with Knowledge Graph-Elicited Reasoning for Healthcare Copilot
Authors: Xuejiao Zhao, Siyan Liu, Su-Yin Yang, C. Miao
Publication Year: 2025
Citation Count: 133
Citation Count Source: Semantic Scholar API
Link: https://www.semanticscholar.org/paper/da83852315c884c73dc527a4b7bc1209fbb037c3
Why It Matches: This paper matches the request because it is about retrieval-augmented generation, published in 2025, and has 133 citations, which is fewer than 200.
Summary: The paper presents MedRAG, a retrieval-augmented generation model enhanced with knowledge graph-elicited reasoning for the medical domain. It improves diagnostic accuracy and specificity by integrating a hierarchical diagnostic knowledge graph with retrieved electronic health records and a large language model. The model reduces misdiagnosis rates and outperforms state-of-the-art methods on public and private datasets.
Uncertainty: None

Gave the same answer when the original prompt was run again.

Relevant paper found? - Partially
Year constraint respected? - Yes 
Citation constraint respected? - Yes
Valid source provided? - Yes
Hallucination avoided? - Yes
Useful explanation? - Yes



Prompt 8
"Find a paper about AI agents with approximately 100 citations published after 2021. Explain any uncertainty in the match."
What the prompt tests - approximation (should be plus minus 20%)

Answer
Title: A Survey of WebAgents: Towards Next-Generation AI Agents for Web Automation with Large Foundation Models
Authors: Liang-bo Ning, Ziran Liang, Zhuohang Jiang, Haohao Qu, Yujuan Ding, Wenqi Fan, Xiao Wei, Shanru Lin, Hui Liu, Philip S. Yu, Qing Li
Publication Year: 2025
Citation Count: 96
Citation Count Source: Semantic Scholar API
Link: https://www.semanticscholar.org/paper/ee88a623365270dc72f906d85c371d3084db7f3d
Why It Matches: The paper's title and abstract clearly indicate that it focuses on AI agents, and its publication year is 2025, satisfying the 'after 2021' constraint. The citation count of 96 is close to the target of 100.
Summary: The paper surveys recent research on WebAgents, which are AI agents designed to automate web tasks using large foundation models. It explores architectures, training methods, and trustworthiness aspects of these agents, highlighting their potential to enhance daily life convenience.
Uncertainty: None

Relevant paper found? - Yes
Year constraint respected? - Yes 
Citation constraint respected? - Yes, 20% give or take 96 is in the 80 -120 range
Valid source provided? - Yes
Hallucination avoided? - Yes
Useful explanation? - Yes



Prompt 9
"Find a paper about retrieval-augmented generation published before 2008 with more than 5000 citations. Summarize its contribution."
What the prompt tests - probably no valid result, potential for invented answer or hallucination.

Answer
Result: No matching paper found
Reason: No paper satisfied all requested constraints based on the available tool results.
Uncertainty: The search results may be incomplete or the query may be too restrictive.

Relevant paper found? - No
Year constraint respected? -  N/A
Citation constraint respected? - N/A
Valid source provided? - N/A
Hallucination avoided? - Yes
Useful explanation? - Yes



Prompt 10
"Find an important paper about AI systems and explain why it matters."
What the prompt tests - ambiguous and subjective topic, underspecified request.

Answer
Title: Artificial Intelligence and Ethics: A Comprehensive Reviews of Bias Mitigation,Transparency, and Accountability in AI Systems
Authors: George Benneh Mensah
Publication Year: 2024
Citation Count: 76
Citation Count Source: Semantic Scholar API
Link: https://www.semanticscholar.org/paper/9f1b1fd579ab07cb8fc647f635c8bd4d4abcc4a0
Why It Matches: The paper's title explicitly mentions "Artificial Intelligence and Ethics," focusing on bias mitigation, transparency, and accountability in AI systems, which aligns perfectly with the search topic "AI systems."
Summary: This paper provides a comprehensive review of bias mitigation, transparency, and accountability in AI systems, making it highly relevant to the topic. It discusses the importance of addressing these ethical considerations for responsible AI deployment.
Uncertainty: None

Relevant paper found? - Yes
Year constraint respected? -  None given
Citation constraint respected? - None given
Valid source provided? - Yes
Hallucination avoided? - Yes
Useful explanation? - Yes





# Reflection
The agent worked mostly as expected. The combination of AutoGen, Mistral and Semantic Scholar tool made it possible to retrieve paper information without relying only on LLM memory.

What worked well:
- The tool was used succesfully for retrieving metadata and citation counts
- Deterministic filtering worked well for year and citation constraints
- The agent usually returned relevant papers and structured answers
- No hallucinated citation counts were observed during evaluation

What failed/was unrelieable:
- Early in development, the agent got stuck in a loop and repeated the same answer/request
- One prompt initially returned "no matching paper" even though a valid result was later found on another run

How often did the agent need tool calls?
The agent needed tool calls for every paper-finding task, since the assigment required the use of an external tool.

Did the LLM hallucinate?
In testing, the model did not hallucinate citation counts or paper metadata. This was mainly prevented by forcing the agent to use the tool and by structuring the output around tool-returned fields.

Incorrect answers were prevented by:
- using Semantic Scholar for paper metadata
- using deterministic filtering for year and citation constraints
- requiring citation data to come from the tool 
- returning "no matching paper found" when no valid papar passed the filters

What I would improve with more time:
Probably support input change from the command line instead of always editing main.py.
Also maybe comparison of multiple candidate papers instead of returning only one.





# Contribution
Commit history can be found on GitHub: https://github.com/andhot01/CompulsoryAssignment2ML-SWDPBAOnlineF2026/compare/dd3d58646a64c7ace93984aee1fdd67fd90fdaed...3a9a641bf19e009b58fbf9df1bc58a26ddd299e3 