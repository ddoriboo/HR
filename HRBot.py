import streamlit as st
from openai import OpenAI
import time

assistant_id = "asst_dEdsDLUFiJfPdb53cJ195yVF"

# GitHub 링크 제거를 위한 설정
st.set_page_config(page_title="KPMG HR Demo", page_icon="🪣", layout="wide", menu_items=None)

# CSS를 사용하여 GitHub 링크와 다른 불필요한 요소들을 숨김
st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .css-1jc7ptx, .e1ewe7hr3, .viewerBadge_container__1QSob,
    .styles_viewerBadge__1yB5_, .viewerBadge_link__1S137,
    .viewerBadge_text__1JaDK {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# OpenAI 클라이언트 초기화
openai_api_key = st.secrets["openai"]["api_key"]
client = OpenAI(api_key=openai_api_key)

# 세션 상태 초기화
if "thread_id" not in st.session_state:
    thread = client.beta.threads.create()
    st.session_state.thread_id = thread.id

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "안녕하세요! 저는 삼구 HR 챗봇입니다. 용역 특성에 맞는 적합한 인력을 추천해드립니다😊."}]

st.title("💬⛏️🪣🧹🔍 삼구 HR 인력 배치 챗봇")
st.caption("🚀 KPMG AI Center Demo")

# 타이핑 효과 함수
def simulate_typing(text, speed=0.01):
    placeholder = st.empty()
    for i in range(len(text) + 1):
        placeholder.markdown(text[:i] + "▌")
        time.sleep(speed)
    placeholder.markdown(text)

# 메시지 표시
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).markdown(msg["content"])

# 사용자 입력 처리
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").markdown(prompt)
    
    # OpenAI API 요청
    response = client.beta.threads.messages.create(
        st.session_state.thread_id, 
        role="user", 
        content=prompt,
    )
    
    run = client.beta.threads.runs.create(
       thread_id=st.session_state.thread_id,
       assistant_id=assistant_id,
       tools=[{"type": "code_interpreter"}],
    )
    
    run_id = run.id
    
    # 응답 대기
    with st.spinner("AI가 답변을 생성 중입니다..."):
        while True: 
            run = client.beta.threads.runs.retrieve(
                thread_id=st.session_state.thread_id,
                run_id=run_id
            )
            if run.status == "completed":
                break
            else: 
                time.sleep(0.5)
    
    # 응답 처리
    thread_messages = client.beta.threads.messages.list(st.session_state.thread_id)
    assistant_message = thread_messages.data[0].content[0].text.value
    
    st.session_state.messages.append({"role": "assistant", "content": assistant_message})
    with st.chat_message("assistant"):
        simulate_typing(assistant_message, speed=0.01)  # 속도 조절 가능
