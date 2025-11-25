# basic imports
import os
import re
from dotenv import load_dotenv
import streamlit as st
from datetime import datetime

# langchain imports
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama

load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY", "")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", None)

# Debug Flags
os.environ["LANGCHAIN_TRACING_V2"] = os.getenv("LANGCHAIN_TRACING_V2", "false")
if OPENAI_API_KEY:
    os.environ["OPENAI_API_KEY"] = ""
if LANGCHAIN_API_KEY:
    os.environ["LANGCHAIN_API_KEY"] = ""

st.set_page_config(page_title="Therapy Assistant — LangChain + Llama2", layout="wide")

# Keyword Flags
CRISIS_KEYWORDS = [
    r"\bkill myself\b", r"\bkill myself\b", r"\bsuicid(e|al)\b", r"\bend my life\b",
    r"\bi can't go on\b", r"\bharm myself\b", r"\bwant to die\b", r"\boverdose\b",
    r"\bself[- ]harm\b", r"\bno reason to live\b"
]

def detect_crisis(text: str) -> bool:
    t = text.lower()
    for pattern in CRISIS_KEYWORDS:
        if re.search(pattern, t):
            return True
    return False

def format_history(history):
    
    out = []
    for msg in history[-10:]:  # keeping last 10 conversations
        ts = msg.get("time", "")
        role = msg["role"]
        text = msg["text"]
        out.append(f"[{ts}] {role.upper()}: {text}")
    return "\n".join(out)

# Prompt TEmplate
therapist_system = (
    "You are a compassionate, non-judgmental therapeutic assistant. "
    "Use active listening, reflective statements, empathy, and practical, evidence-informed coping "
    "strategies (like grounding, breathing, scheduling small activities, CBT-style reframing) where appropriate. "
    "Always clarify when unsure, ask gentle follow-up questions, summarize the client's concerns, and offer "
    "options (e.g., short coping steps now, longer-term strategies, or referral to a professional). "
    "Do NOT provide medical, legal, or diagnostic statements. If the user expresses suicidal ideation, self-harm, "
    "or immediate danger, follow safety guidance: encourage contacting emergency services and provide crisis resources. "
    "Keep responses brief (2–6 short paragraphs) and supportive. Ask permission before giving exercises or worksheets."
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", therapist_system),
        ("user", "Conversation history:\n{history}\n\nCurrent user message: {current_message}\n\nRespond as a caring therapist.")
    ]
)

# LLM Setup
try:
    if OLLAMA_BASE_URL:
        os.environ["OLLAMA_BASE_URL"] = OLLAMA_BASE_URL
    llm = Ollama(model="llama2", verbose=False)  
except Exception as e:
    st.warning("Could not initialize Ollama LLM. Check your environment and model name.")
    llm = None

output_parser = StrOutputParser()
chain = prompt | (llm if llm is not None else llm) | output_parser  

# Session state initialization
if "history" not in st.session_state:
    st.session_state.history = []
if "last_response" not in st.session_state:
    st.session_state.last_response = ""

# Interface
st.title("AI Therapy Assistant (LangChain + Llama2)")
st.caption("A supportive conversational assistant. Not a replacement for a licensed therapist.")

col1, col2 = st.columns([3,1])

with col1:
    with st.expander("Important — Safety & Limits", expanded=False):
        st.write(
            """
            • This assistant provides supportive conversation and coping suggestions, **not** medical diagnosis or therapy.
            • If you or someone else is in immediate danger call local emergency services (e.g., **112** in India, **911** in the US).
            • For urgent suicidal thoughts, please contact a crisis helpline right away or a local emergency service.
            """
        )
    # Conversation display
    st.subheader("Conversation")
    chat_container = st.container()
    with chat_container:
        if st.session_state.history:
            for msg in st.session_state.history:
                role = msg["role"]
                ts = msg.get("time", "")
                if role == "user":
                    st.markdown(f"**You**  <span style='color:gray;font-size:12px'> {ts}</span>", unsafe_allow_html=True)
                    st.write(msg["text"])
                else:
                    st.markdown(f"**Assistant**  <span style='color:gray;font-size:12px'> {ts}</span>", unsafe_allow_html=True)
                    st.info(msg["text"])
        else:
            st.info("Say hi to start a conversation. Example: 'I've been feeling anxious about work lately.'")

    # Input box
    user_input = st.text_area("Your message", height=120, key="user_input")

    col_submit, col_reset, col_export = st.columns([1,1,1])
    with col_submit:
        send = st.button("Send")
    with col_reset:
        clear = st.button("Reset conversation")
    with col_export:
        export = st.button("Export conversation (.txt)")

with col2:
    st.subheader("Quick tools")
    st.write("- Try: 'I'm feeling overwhelmed and can't sleep.'")
    st.write("- Try: 'I had an argument with my partner...'")
    st.write("")
    st.markdown("**Settings**")
    temp = st.slider("Creativity (temperature)", 0.0, 1.0, 0.2, 0.05)
    max_tokens = st.slider("Max tokens", 128, 2048, 512, 64)

# handle reset
if clear:
    st.session_state.history = []
    st.session_state.last_response = ""
    st.success("Conversation reset.")

# handle export
if export:
    if not st.session_state.history:
        st.warning("No conversation to export.")
    else:
        txt_lines = []
        for m in st.session_state.history:
            txt_lines.append(f"[{m.get('time','')}] {m['role'].upper()}: {m['text']}")
        txt = "\n\n".join(txt_lines)
        st.download_button("Download conversation as .txt", txt, file_name="therapy_conversation.txt")

# send flow
if send and user_input:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.history.append({"role": "user", "text": user_input, "time": now})

    # crisis detection
    if detect_crisis(user_input):
        crisis_msg = (
            "I'm really sorry you're feeling this way. If you are in immediate danger, please contact local emergency services now "
            "(for example, 112 in India or 911 in the US). If you can, reach out to someone you trust or a local crisis hotline. "
            "Would you like me to provide some grounding steps you can try right now, or resources to contact a professional?"
        )
        st.session_state.history.append({"role": "assistant", "text": crisis_msg, "time": now})
        st.experimental_rerun()

    
    # We limit how many previous exchanges we include to avoid token bloat.
    history_text = format_history(st.session_state.history[:-1])  
    current_message = st.session_state.history[-1]["text"]

    question_payload = {
        "history": history_text,
        "current_message": current_message
    }

    
    try:
        
        response = chain.invoke(
            {"history": history_text, "current_message": current_message}
        )
        assistant_text = response if isinstance(response, str) else str(response)
    except Exception as e:
        assistant_text = (
            "Sorry — I couldn't reach the language model backend. "
            "Please check your model and environment settings. Error: " + str(e)
        )

    now_resp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.history.append({"role": "assistant", "text": assistant_text, "time": now_resp})
    st.session_state.last_response = assistant_text

    # Rerun so the new messages are shown in the interface
    st.experimental_rerun()

# If there is a last_response show a small follow up interface
if st.session_state.last_response:
    with st.expander("Options after reply", expanded=False):
        st.write("• If you'd like the assistant to continue, type more or ask it to 'reflect' or 'summarize'.")
        if st.button("Ask assistant to summarize last reply"):
            summary_prompt = "Please produce a short, clear 2-3 sentence summary of your last reply."
            # Add a user request for summary
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.session_state.history.append({"role": "user", "text": summary_prompt, "time": now})
            try:
                response = chain.invoke({"history": format_history(st.session_state.history[:-1]), "current_message": summary_prompt})
                st.session_state.history.append({"role": "assistant", "text": response, "time": now})
            except Exception as e:
                st.session_state.history.append({"role": "assistant", "text": f"Error: {e}", "time": now})
            st.experimental_rerun()

# Footer
st.markdown("---")
st.write("Built with LangChain + Ollama (Llama2). Make sure your model server and API keys are configured.")
st.caption("Remember: this tool is supportive only — for professional help, seek a licensed mental health provider.")
