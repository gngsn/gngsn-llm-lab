from langchain import hub
from langchain.agents import create_react_agent

from gngsn_llm_lab.domain.llm import llm
from gngsn_llm_lab.entity.toolkit import toolkit

# 시스템 메시지 생성
prompt_template = hub.pull("langchain-ai/sql-agent-system-prompt")
system_message = prompt_template.format(dialect="SQLite", top_k=5)

agent_executor = create_react_agent(
    llm,
    toolkit.get_tools(),
    state_modifier=system_message
)
