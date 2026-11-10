import gradio as gr
import requests

API_URL = 'http://127.0.0.1:8000'

def make_meeting(title: str, people: str) -> str:
    try:
        response = requests.post(f'{API_URL}/meeting',json={'title':title,'people':people})
        response.raise_for_status()
        return response.json()['result']
    except(requests.RequestException, ValueError, KeyError) as e:
        return f'서버 통신 오류: {e}'

def summarize(text: str) -> str:
    try:
        response = requests.post(f'{API_URL}/summarize',json={'text':text})
        response.raise_for_status()
        return response.json()['result']
    except(requests.RequestException, ValueError, KeyError) as e:
            return f'서버 통신 오류: {e}'

def all_meeting(title: str, people: str, text:str) -> str:
    try:
        response = requests.post(f'{API_URL}/pipeline',json={'title':title,'people':people,'text':text})
        response.raise_for_status()
        return response.json()['result']
    except(requests.RequestException, ValueError, KeyError) as e:
            return f'서버 통신 오류: {e}'    
    

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

    with gr.Tab('3.전체'):
        title2 = gr.Textbox(label='제목',value='주간 회의')
        people2 = gr.Textbox(label='참가자(쉼표)', value='김사과, 이메론')
        raw2 = gr.Textbox(label='회의록',lines=6, value='김사과: 목표 공유\n 이메론: API 완료 예정')
        btn3 = gr.Button('요약', variant='primary')
        out3 = gr.Markdown()
        btn3.click(fn=summarize,inputs=[title2,people2,raw2],outputs=out3)

if __name__ == '__main__': # 자체 실행이면 name에 main이 들어가고, import로 실행되면 파일명이 들어감
    demo.launch(server_name='127.0.0.1', server_port=9999)
