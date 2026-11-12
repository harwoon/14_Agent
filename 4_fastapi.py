# /meeting
# /summarize
# uvicorn 4_fastapi:app --reload --port 8000
from contextlib import asynccontextmanager #데코레이터 추가용
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from graph import run_meeting_pipeline
from db import (init_db, list_meetings, format_meetings_markdown, get_meeting)

@asynccontextmanager
async def lifespan(_app: FastAPI): #서버시작될 때 해당 처리를 한 후 시작하도록
    init_db()
    yield

app = FastAPI(title='회의 관리 API',lifespan=lifespan)

class MeetingRequest(BaseModel):
    title: str
    people: str

class SummaryRequest(BaseModel):
    text: str

class PipelineRequest(BaseModel):
    title: str
    people: str
    notes: str

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

@app.post('/meeting')
def create_meeting(request: MeetingRequest):
    return {"result":make_meeting(request.title, request.people)}

@app.post('/summarize')
def summarize_meeting(request: SummaryRequest):
    return {"result":summarize(request.text)}

@app.post('/pipeline')
def run_pipeline(request: PipelineRequest):
    return {
        "result":run_meeting_pipeline(
            title = request.title,
            people = request.people,
            notes = request.notes
        )
    }

@app.get('/meetings')
def meetings_list(limit: int=20):
    rows = list_meetings(limit=limit)
    return {
        'items': rows,
        'markdown': format_meetings_markdown(rows),
        "result": format_meetings_markdown(rows)
    }

@app.get('/meetings/{meeting_id}')
def meetings_detail(meeting_id:int):
    row = get_meeting(meeting_id)

    if row is None:
        raise HTTPException(status_code=404,detail=f'회의 #{meeting_id} 없음')
    detail = format_meetings_markdown(row)
    return {'item':row, "markdown":detail, "result":detail}