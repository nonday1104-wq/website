import streamlit as st
import requests
import datetime
from streamlit_autorefresh import st_autorefresh

# ---------------------------------------------------------
# 1. 頁面與組態設定
# ---------------------------------------------------------
st.set_page_config(page_title="Local AI 多人群聊室", layout="wide")

# 設定自動刷新（每 2000 毫秒 / 2 秒刷新一次畫面，以同步其他人發送的訊息）
st_autorefresh(interval=2000, key="chat_autorefresh")

OLLAMA_API_URL = "http://localhost:11434/api/generate"

# ---------------------------------------------------------
# 2. 全局跨使用者共享狀態 (Global Cross-Session State)
# Streamlit 預設 SessionState 不共享，此處用 @st.cache_resource 建立全域記憶體紀錄
# ---------------------------------------------------------
@st.cache_resource
def get_global_chat_history():
    # 回傳一個跨 Session 共享的 list 容器
    return []

global_messages = get_global_chat_history()

# ---------------------------------------------------------
# 3. 側邊欄：使用者名稱與模型選擇
# ---------------------------------------------------------
st.sidebar.title("聊天室設定")
user_name = st.sidebar.text_input("輸入你的暱稱", value="User_1")
selected_model = st.sidebar.selectbox("選擇本地 AI 模型", ["qwen2.5:7b", "phi3:mini", "qwen2.5:3b"])
trigger_ai = st.sidebar.checkbox("自動標記 AI 回應（任何訊息皆觸發 AI）", value=False)

if st.sidebar.button("清空歷史紀錄"):
    global_messages.clear()
    st.rerun()

# ---------------------------------------------------------
# 4. 主畫面：顯示所有對話紀錄
# ---------------------------------------------------------
st.title("💬 本地 AI 多人線上群聊室")
st.caption(f"目前線上模型：`{selected_model}` | 自動更新中...")

# 繪製歷史訊息
chat_container = st.container()
with chat_container:
    for msg in global_messages:
        role = msg["role"]
        name = msg["name"]
        content = msg["content"]
        time_str = msg["time"]
        
        avatar = "🤖" if role == "assistant" else "👤"
        with st.chat_message(role, avatar=avatar):
            st.markdown(f"**{name}** `<{time_str}>`\n\n{content}")

# ---------------------------------------------------------
# 5. 訊息輸入與 AI 推論邏輯
# ---------------------------------------------------------
user_input = st.chat_input("輸入訊息...（提示：輸入 @AI 可指定 AI 回覆）")

if user_input:
    now_str = datetime.datetime.now().strftime("%H:%M:%S")
    
    # A. 記錄使用者的發言
    global_messages.append({
        "role": "user",
        "name": user_name,
        "content": user_input,
        "time": now_str
    })
    
    # B. 判斷是否觸發 AI 運算
    if "@AI" in user_input or trigger_ai:
        # 組合給 AI 的上下文（Context Prompt）
        prompt_context = "以下是群聊紀錄，請以 AI 助理的角色簡短且精準地回覆最新訊息：\n\n"
        for m in global_messages[-6:]: # 取最近 6 條訊息避免 context 過長
            prompt_context += f"{m['name']}: {m['content']}\n"
        prompt_context += "AI:"

        with st.spinner(f"🤖 AI ({selected_model}) 正在思考中..."):
            try:
                response = requests.post(
                    OLLAMA_API_URL,
                    json={
                        "model": selected_model,
                        "prompt": prompt_context,
                        "stream": False
                    },
                    timeout=60
                )
                if response.status_str == 200 or response.status_code == 200:
                    ai_reply = response.json().get("response", "（AI 未回傳內容）")
                else:
                    ai_reply = f"[錯誤] Ollama 回傳狀態碼 {response.status_code}"
            except Exception as e:
                ai_reply = f"[連線失敗] 無法連線至本地 Ollama 服務: {str(e)}"

        # C. 記錄 AI 的發言
        global_messages.append({
            "role": "assistant",
            "name": f"AI ({selected_model})",
            "content": ai_reply,
            "time": datetime.datetime.now().strftime("%H:%M:%S")
        })

    st.rerun()
