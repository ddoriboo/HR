from openai import OpenAI
import streamlit as st
import time

assistant_id = "asst_dEdsDLUFiJfPdb53cJ195yVF"

st.set_page_config(page_title="KPMG HR Demo", page_icon="🪣", layout="wide")
st.markdown(
    """
    <style>
    .css-1jc7ptx, .e1ewe7hr3, .viewerBadge_container__1QSob,
    .styles_viewerBadge__1yB5_, .viewerBadge_link__1S137,
    .viewerBadge_text__1JaDK {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    client = OpenAI(api_key=openai_api_key)
    thread_id = st.text_input("Thread ID")
    thread_btn = st.button("신규 스레드 생성")

    if thread_btn: 
        thread = client.beta.threads.create()
        thread_id = thread.id
        st.subheader(f"{thread_id}", divider="rainbow")
        st.info("스레드가 생성되었습니다.")

st.title("💬⛏️🪣🧹🔍 삼구 HR 인력 배치 챗봇")
st.caption("🚀 KPMG AI Center Demo")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "안녕하세요! 저는 삼구 HR 챗봇입니다. 용역 특성에 맞는 적합한 인력을 추천해드립니다😊."}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()
    
    if not thread_id:
        st.info("Please add your thread ID to continue.")
        st.stop()
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    response = client.beta.threads.messages.create(
        thread_id, 
        role="user", 
        content=prompt,
    )
    
    run = client.beta.threads.runs.create(
       thread_id=thread_id,
       assistant_id=assistant_id,
       tools=[{"type": "code_interpreter"}],
    )
    
    run_id = run.id
    
    with st.spinner("AI가 답변을 생성 중입니다..."):
        while True: 
            run = client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run_id
            )
            if run.status == "completed":
                break
            else: 
                time.sleep(2)
    
    thread_messages = client.beta.threads.messages.list(thread_id)
    assistant_message = thread_messages.data[0].content[0].text.value
    
    st.session_state.messages.append({"role": "assistant", "content": assistant_message})
    st.chat_message("assistant").write(assistant_message)
    msg = thread_messages.data[0].content[0].text.value
    print(msg)
