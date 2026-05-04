import os
import warnings
from dotenv import load_dotenv

load_dotenv()

# Suppress FLAML and cost calculation warnings
warnings.filterwarnings("ignore", message="flaml.automl is not available.*")
warnings.filterwarnings("ignore", message="Cost calculation is not implemented for model.*")

api_key = os.getenv("MISTRAL_API_KEY")


from autogen import ConversableAgent, register_function
from tools.paper_matcher import find_matching_papers

def is_terminate_message(msg):
    content = msg.get("content") or ""
    return "terminate" in content.lower()

LLM_CONFIG = {
    "config_list": [
        {
            "model": "open-mistral-nemo",
            "api_key": api_key,
            "api_type": "mistral",
            "api_rate_limit": 0.25,
            "repeat_penalty": 1.1,
            "temperature": 0.0,
            "seed": 42,
            "stream": False,
            "native_tool_calls": False,
            "cache_seed": None,
        }
    ]
}

assistant = ConversableAgent(
    name="ResearchAssistant",
    system_message=(
        "You are a research paper assistant.\n"
        "You must always use the tool find_matching_papers before answering.\n"
        "Do not answer from memory.\n"
        "Do not invent citation counts, years, authors, or links.\n"
        "Use only information returned by the tool.\n\n"

        "If the tool returns no papers, respond exactly in this format:\n"
        "Result: No matching paper found\n"
        "Reason: No paper satisfied all requested constraints based on the available tool results.\n"
        "Uncertainty: The search results may be incomplete or the query may be too restrictive.\n"
        "TERMINATE\n\n"

        "If the tool returns one or more papers, choose the best matching paper and respond exactly in this format:\n"
        "Title: <paper title>\n"
        "Authors: <comma-separated author list>\n"
        "Publication Year: <year>\n"
        "Citation Count: <number>\n"
        "Citation Count Source: <source>\n"
        "Link: <paper URL>\n"
        "Why It Matches: <2-3 sentences explaining why it satisfies the topic and constraints>\n"
        "Summary: <5-7 sentences if the user asked for a summary; otherwise 2-3 sentences>\n"
        "Uncertainty: <brief note about any uncertainty, or 'None'>\n"
        "TERMINATE"
    ),
    llm_config=LLM_CONFIG,
    is_termination_msg=is_terminate_message,
)

user_proxy = ConversableAgent(
    name="UserProxy",
    llm_config=False,
    human_input_mode="NEVER",
    is_termination_msg=is_terminate_message,
    max_consecutive_auto_reply=1,
)

register_function(
    find_matching_papers,
    caller=assistant,
    executor=user_proxy,
    name="find_matching_papers",
    description=(
        "Search for research papers by topic using Semantic Scholar and deterministically "
        "filter them by publication year and citation count. "
        "Returns only papers that satisfy the given constraints, with title, authors, year, "
        "citation count, citation count source, link, and abstract."
    ),
)

if __name__ == "__main__":
    user_prompt = (
        "Find a paper about retrieval-augmented generation published before 2021 "
        "with more than 500 citations. Summarize its contribution in 5-7 sentences."
    )

    user_proxy.initiate_chat(
        assistant,
        message=user_prompt,
        max_turns=3,
    )