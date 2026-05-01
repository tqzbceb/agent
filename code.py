from langgraph.graph import StateGraph, END
from typing import TypedDict, List

# 定义状态：系统流转的上下文
class AgentState(TypedDict):
    topic: str
    draft: str
    feedback: str
    is_approved: bool

# Agent 1: 选题专家 (基于热点)
def topic_agent(state: AgentState):
    # 逻辑：分析热点，确定主题
    return {"topic": "AI在办公场景的应用趋势"}

# Agent 2: 内容创作专家
def writer_agent(state: AgentState):
    # 逻辑：调用模型撰写长文
    return {"draft": "这是一篇关于AI如何提升效率的深度文章..."}

# Agent 3: 质控/合规专家 (闭环校验)
def reviewer_agent(state: AgentState):
    # 逻辑：长链路推理，检查逻辑错误与合规性
    if "违规词" in state['draft']:
        return {"is_approved": False, "feedback": "含有敏感词"}
    return {"is_approved": True}

# 构建工作流图 (核心逻辑：协同)
workflow = StateGraph(AgentState)
workflow.add_node("选题", topic_agent)
workflow.add_node("撰写", writer_agent)
workflow.add_node("审核", reviewer_agent)

# 设置流转逻辑
workflow.set_entry_point("选题")
workflow.add_edge("选题", "撰写")
workflow.add_edge("撰写", "审核")
workflow.add_conditional_edges("审核", lambda x: "end" if x['is_approved'] else "撰写")
workflow.add_edge("审核", END)

app = workflow.compile()
