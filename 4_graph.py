# LangGraph 예제: 주간 회의 도우미
# 노드1: 입력 검증
# 노드2: 회의 정보 / 문구 생성
# 노드3: 회의록 요약
# 노드4: 규칙
# 노드5: 최종 Markdown 조합

from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class MeetingState(TypedDict, total=False):
    title: str
    people: str
    lines: str

def check_input():
    pass

def make_text():
    pass

def summarize():
    pass

def show_rules():
    pass

def final_md():
    pass

builder = StateGraph(MeetingState)
builder.add_node('check_input',check_input)
builder.add_node('make_text',make_text)

builder.add_edge(START, check_input)
builder.add_edge(check_input,make_text)
builder.add_edge(make_text,END)

meeting_graph = builder.compile()