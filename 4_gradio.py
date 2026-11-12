import gradio as gr
import requests

API_URL = 'http://127.0.0.1:8000'

def call_api(path: str, payload: dict | None = None, method:str='POST') -> str:
     try:
          url = f"{API_URL}{path}"
          if method == 'GET':
            response = requests.get(url,timeout=10)
          else:
            response = requests.post(url,json=payload,timeout=10)
          response.raise_for_status()

          data = response.json()

          if 'markdown' in data:
              return data['markdown']
          if 'result' in data:
              text = data['result']
              meeting_id = data.get('meeting_id') or 0
              if meeting_id:
                  text += f"\n\n_(응답 meeting_id={meeting_id})_"
              return text
          return str(data)
     
     except(requests.RequestException, ValueError, KeyError) as e:
          return f'서버 통신 오류: {e}'

def make_meeting(title: str, people: str) -> str:
    return call_api('/meeting',{'title':title,'people':people})

def summarize(text: str) -> str:
    return call_api('/summarize',{'text':text})

def run_pipeline(title: str, people: str, notes:str) -> str:
    return call_api('/pipeline',{'title':title,'people':people,'notes':notes}) 

def show_meetings() -> str:
    return call_api("/meetings",method='GET')

def show_meeting_detail(meeting_id: float | int) -> str:
    try:
        mid = int(meeting_id)
    except(TypeError, ValueError):
        return '조회할 회의 ID를 숫자로 입력하세요.'
    if mid <= 0:
        return "1 이상의 회의 id를 입력하세요."
    return call_api(f'/meetings/{mid}', method='GET')
    
    

with gr.Blocks(title='Gradio Tabs 미니 예제') as demo:
    gr.Markdown('''# **Gradio + FastAPI 예제**
    FastAPI 서버와 통신하는 Gradio UI입니다.''')

    with gr.Tab('1.회의 생성'):
        with gr.Column():
            title = gr.Textbox(label='제목',value='주간 회의')
            people = gr.Textbox(label='참가자(쉼표)', value='김사과, 이메론')

        btn1 = gr.Button('생성', variant='primary') # variant='primary' 버튼에 색상이 들어감
        out1 = gr.Markdown()
        btn1.click(fn=make_meeting,inputs=[title,people],outputs=out1)

    with gr.Tab('2.간단 요약'):
        raw = gr.Textbox(label='회의록',lines=6, value='김사과: 목표 공유\n 이메론: API 완료 예정')
        btn2 = gr.Button('요약', variant='primary')
        out2 = gr.Markdown()
        btn2.click(fn=summarize,inputs=raw,outputs=out2)

    with gr.Tab('3.전체 파이프라인'):
        gr.Markdown('한 번에 검증 > 회의 생성 > 요약 > 액션추출 > 결과조합을 실행')
        p_title = gr.Textbox(label='제목',value='주간 회의')
        p_people = gr.Textbox(label='참가자(쉼표)', value='김사과, 이메론')
        p_notes = gr.Textbox(label='회의록',lines=6, value='김사과: 목표 공유\n 이메론: API 완료 예정')
        btn3 = gr.Button('파이프라인 실행', variant='primary')
        out3 = gr.Markdown()
        btn3.click(fn=run_pipeline,inputs=[p_title,p_people,p_notes],outputs=out3)

    with gr.Tab('4. 저장된 회의'):
        gr.Markdown('저장된 결과를 조회합니다.')
        btn4 = gr.Button('목록 새로고침')
        out4 = gr.Markdown()
        btn4.click(show_meetings, outputs=out4)

        mid = gr.Number(label='회의 id',value=1, precision=0)
        btn5 = gr.Button('상세 조회')
        out5 = gr.Markdown()
        btn5.click(show_meeting_detail, inputs=mid, outputs=out5)

if __name__ == '__main__': # 자체 실행이면 name에 main이 들어가고, import로 실행되면 파일명이 들어감
    demo.launch(server_name='127.0.0.1', server_port=9999)
