# /meeting
# /summarize
# uvicorn 4_fastapi:app --reload --port 8000

from fastapi import FastAPI
from pydantic import BaseModel
#from 4_graph import graph

app = FastAPI(title='회의 관리 API')

class MeetingRequest(BaseModel):
    title: str
    people: str

class SummaryRequest(BaseModel):
    text: str

class AllRequest(BaseModel):
    title: str
    people: str
    text: str

def make_meeting(title: str, people: str) -> str:
    title = (title or "").strip()
    if not title:
        return '제목을 입력하세요'

    names = [p.strip() for p in (people or '').split(',') if p.strip()]
    return (f'### 회의 생성됨\n'
            f"- 제목: {title}\n"
            f"- 참가자: {','.join(names) or '(없음)'}")

def summarize(text: str) -> str:
    text = (text or "").strip()
    if not text:
        return '회의록이 비어 있습니다.'
    lines = [ln for ln in text.splitlines() if ln.strip()]
    return f"발화 {len(lines)}줄 / 앞부분: {lines[0][:50] if lines else ''}"

def all(title: str, people: str, text:str) -> str:
    title = (title or "").strip()
    if not title:
        return '제목을 입력하세요'

    names = [p.strip() for p in (people or '').split(',') if p.strip()]

    text = (text or "").strip()
    if not text:
        return '회의록이 비어 있습니다.'
    lines = [ln for ln in text.splitlines() if ln.strip()]

    return (f'### 회의 생성됨\n'
            f"- 제목: {title}\n"
            f"- 참가자: {','.join(names) or '(없음)'}"
            f"발화 {len(lines)}줄 / 앞부분: {lines[0][:50] if lines else ''}")

@app.post('/meeting')
def create_meeting(request: MeetingRequest):
    return {"result":make_meeting(request.title, request.people)}

@app.post('/summarize')
def summarize_meeting(request: SummaryRequest):
    return {"result":summarize(request.text)}

@app.post('/pipeline')
def all_meeting(request: AllRequest):
    return {"result":all(request.title, request.people, request.text)}