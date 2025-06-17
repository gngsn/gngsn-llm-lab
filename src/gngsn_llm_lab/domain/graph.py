from langgraph.graph import START, END, StateGraph

from gngsn_llm_lab.domain.state import State

graph = StateGraph(State)
graph.add_edge(START, "somewhere_begin")
graph.add_edge("somewhere_end", END)
