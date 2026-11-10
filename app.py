import os
 
import requests
import streamlit as st
 
# ==========================================
# 設定（全部從環境變數讀取，到 Render 的 Environment Variables 設定）
#   BACKEND_URL  : 後端 API 網址，例如 https://api.chatbotai.de5.net/chat
#   BACKEND_KEY  : 後端的驗證金鑰（選填）
#   APP_PASSWORD : 網頁登入密碼（選填，沒設定就不需要密碼）
# ==========================================
BACKEND_URL = os.environ.get("BACKEND_URL", "").strip()
BACKEND_KEY = os.environ.get("BACKEND_KEY", "").strip()
APP_PASSWORD = os.environ.get("APP_PASSWORD", "").strip()
 
st.set_page_config(page_title="智能 AI 助理", page_icon="🤖")
 
 
# ==========================================
# 1. 密碼保護（有設定 APP_PASSWORD 才會啟用）
# ==========================================
if APP_PASSWORD:
    if not st.session_state.get("authed"):
        st.title("🔒 請先登入")
        pwd = st.text_input("密碼", type="password")
        if st.button("登入"):
            if pwd == APP_PASSWORD:
                st.session_state.authed = True
                st.rerun()
            else:
                st.error("密碼錯誤")
        st.stop()
 
 
# ==========================================
# 2. 後端接口（預留位置）
#    約定格式：
#      送出  POST BACKEND_URL
#            {"messages": [{"role": "user", "content": "..."}, ...]}
#      回傳  {"reply": "回覆文字"}
#    之後接 Colab / Ollama / 其他 API，改這個函式就好
# ==========================================
def call_backend(messages):
    # 尚未設定後端 → 示範模式
    if not BACKEND_URL:
        last = messages[-1]["content"]
        return f"（示範模式）我收到您的訊息了：『{last}』。後端尚未連接。"
 
    headers = {"Content-Type": "application/json"}
    if BACKEND_KEY:
        headers["Authorization"] = f"Bearer {BACKEND_KEY}"
 
    try:
        resp = requests.post(
            BACKEND_URL,
            json={"messages": messages},
            headers=headers,
            timeout=60,
        )
        resp.raise_for_status()
        return resp.json().get("reply", "（後端沒有回傳內容）")
    except requests.exceptions.Timeout:
        return "⚠️ 後端回應逾時，請稍後再試。"
    except requests.exceptions.RequestException:
        return "⚠️ 無法連線到後端，請確認後端是否在線。"
    except ValueError:
        return "⚠️ 後端回傳的格式不正確。"
 
 
# ==========================================
# 3. 側邊欄
# ==========================================
with st.sidebar:
    st.header("設定")
    if BACKEND_URL:
        st.success("後端：已連接")
    else:
        st.warning("後端：示範模式")
    if st.button("🗑️ 清除對話"):
        st.session_state.messages = []
        st.rerun()
 
 
# ==========================================
# 4. 主畫面
# ==========================================
st.title("🤖 智能 AI 助理")
st.caption("🚀 經由 Cloudflare 安全網路全程防護中")
 
if "messages" not in st.session_state:
    st.session_state.messages = []
 
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
 
if prompt := st.chat_input("請輸入您的問題..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
 
    with st.chat_message("assistant"):
        with st.spinner("思考中..."):
            reply = call_backend(st.session_state.messages)
        st.markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})
