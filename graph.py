# LangGraph 예제: 주간 회의 도우미
# 노드1: 입력 검증
# 노드2: 회의 정보 / 문구 생성
# 노드3: 회의록 요약
# 노드4: 규칙
# 노드5: 최종 Markdown 조합

from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from db import save_meeting

class MeetingState(TypedDict, total=False):
    title: str
    people: str
    notes: str
    error: str
    meeting_info: str
    summary: str
    actions: str
    result: str

def validate_input(state:MeetingState)->MeetingState:
    title = (state.get('title') or "").strip()
    notes = (state.get('notes') or "").strip()

    if not title:
        return {**state, "error":'제목을 입력하세요.'}

    if not notes:
        return {**state, 'error': '회의록이 비어 있습니다.'}

    return {**state, 'error':''}

def create_meeting(state:MeetingState)->MeetingState:
    title = state['title'].strip()
    names = [p.strip() for p in (state.get('people') or '').split(',') if p.strip()]
    meeting_info = (f'### 회의 생성됨\n'
                f"- 제목: {title}\n"
                f"- 참가자: {','.join(names) or '(없음)'}")
    return {**state, 'meeting_info':meeting_info}

def summarize_notes(state:MeetingState)->MeetingState:
    lines = [ln.strip() for ln in state['notes'].splitlines() if ln.strip()]
    summary = f"발화 {len(lines)}줄 / 앞부분: {lines[0][:50] if lines else ''}"
    return {**state, 'summary':summary}

def extract_actions(state:MeetingState)-> MeetingState:
    keywords = ('예정', '할', 'todo','해야','담당')
    found = []

    for line in state['notes'].splitlines():
        text = line.strip()
        if text and any(k in text.lower() for k in keywords):
            found.append(f'- {text}')
    actions = '\n'.join(found) if found else '- (추출된 액션 없음)'
    return {**state, 'actions':actions}

def compose_result(state:MeetingState) -> MeetingState:
    if state.get('error'):
        return {**state, 'result':f'### 오류\n{state['error']}'}

    result = (
        "### 회의 파이프라인 결과\n\n"
        f"1. 회의 정보\n{state['meeting_info']}\n\n"
        f"2. 요약\n{state['summary']}\n\n"
        f"3. 액션 아이템\n{state['actions']}\n\n"
                     
    )

    return {**state, 'result':result}

def route_after_validate(state:MeetingState)->str:
    return 'error' if state.get('error') else 'ok'

def route_after_compose(state:MeetingState)->str:
    return 'error' if state.get('error') else 'save'

def save_to_db(state:MeetingState)-> MeetingState:
    meeting_id = save_meeting(
        title = state['title'].strip(),
        people = (state.get('people') or "").strip(),
        notes = state['notes'],
        summary = state['summary'],
        actions = state["actions"],
        result = state['result']
    )
    result = state['result'] + f"\n\nDB 저장됨 - meetings.id = {meeting_id}"
    return {**state, "meeting_id":meeting_id, "result":result}


def build_meeting_graph():
    graph = StateGraph(MeetingState)
    graph.add_node('validate',validate_input)
    graph.add_node('create_meeting',create_meeting)
    graph.add_node('summarize',summarize_notes)
    graph.add_node('extract_actions',extract_actions)
    graph.add_node('compose',compose_result)
    graph.add_node('save_to_db',save_to_db)

    graph.add_edge(START, "validate")
    graph.add_conditional_edges(
        'validate', route_after_validate, {'ok': 'create_meeting', 'error': 'compose'}
    )
    graph.add_edge('create_meeting','summarize')
    graph.add_edge('summarize','extract_actions')
    graph.add_edge('extract_actions','compose')
    graph.add_conditional_edge(
        'compose',route_after_compose, {"save":"save_to_db","end":END}
        )
    graph.add_edge('compose',END)
    return graph.compile()


meeting_app = build_meeting_graph()

def run_meeting_pipeline(title:str, people:str, notes:str)->str: # 그래프에 쓰일 함수
    final_state = meeting_app.invoke(
        {
            'title':title, 
            'people':people,
            'notes':notes,
            'error':'',
            'meeting_info':"",
            "summary":"",
            "actions":"",
            "result":""
        }
    )
    return final_state['result']