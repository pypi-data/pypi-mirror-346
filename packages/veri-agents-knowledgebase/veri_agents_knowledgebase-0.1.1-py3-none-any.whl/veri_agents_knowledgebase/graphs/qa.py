import logging
from datetime import datetime
from typing import Sequence, Callable

from langchain_core.language_models import (
    LanguageModelLike,
)
from langgraph.graph.graph import CompiledGraph
from langgraph.prebuilt import ToolNode, create_react_agent
from langchain_core.tools import BaseTool

from veri_agents_knowledgebase import Knowledgebase
from veri_agents_knowledgebase.tools import FixedKnowledgebaseWithTagsQuery, FixedKnowledgebaseListDocuments

log = logging.getLogger(__name__)

def create_qa_agent(
    llm: LanguageModelLike,
    knowledgebases: Sequence[Knowledgebase],
    system_prompt: str,
    tools: Sequence[BaseTool | Callable] | None = None,
    **react_kwargs
) -> CompiledGraph:
    tools = list(tools) if tools else []
    for i, knowledgebase in enumerate(knowledgebases):
        tools.append(
            FixedKnowledgebaseWithTagsQuery(
                knowledgebase=knowledgebase,
                num_results=10,
                name_suffix=f"-{i}",
                runnable_config_filter_prefix="filter_",  # TODO: pick your own prefix for the runnable config
            )
        )
        tools.append(
           FixedKnowledgebaseListDocuments(
               knowledgebase=knowledgebase,
               name_suffix=f"-{i}",
               runnable_config_filter_prefix="filter_",  # TODO: pick your own prefix for the runnable config
           ) 
        )
    tool_node = ToolNode(tools)

    system_prompt = system_prompt
    system_prompt += f"""Today's date is: {datetime.now().strftime("%Y-%m-%d")}."""

    return create_react_agent(
        model=llm,
        tools=tool_node,
        prompt=system_prompt,
        **react_kwargs
    )
