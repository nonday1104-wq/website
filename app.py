import streamlit as st

# ==========================================
# 1. 🛡️ 這一區塊是你的安全防盾（絕對不能刪除或更動）
# ==========================================
query_params = st.query_params


# ==========================================
# 2. 🤖 這一區塊開始寫你的 AI 機器人程式碼
# ==========================================
st.title("🤖 智能 AI 助理")
st.caption("🚀 經由 Cloudflare 安全網路全程防護中")

# 初始化聊天紀錄（如果記憶體中還沒有紀錄）
if "messages" not in st.session_state:
    st.session_state.messages = []

# 在畫面上渲染過去的對話歷史紀錄
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 接收使用者輸入的訊息
if prompt := st.chat_input("請輸入您的問題..."):
    # 顯示使用者的訊息
    with st.chat_message("user"):
        st.markdown(prompt)
    # 將使用者訊息存入歷史紀錄
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 顯示 AI 的回應
    with st.chat_message("assistant"):
        # 這裡你可以串接 OpenAI, Gemini API 或寫固定的回應規則
        ai_response = f"您好！我收到您的訊息了：『{prompt}』。這是一個串接成功的測試回應！"
        st.markdown(ai_response)
        
    # 將 AI 回應存入歷史紀錄
    st.session_state.messages.append({"role": "assistant", "content": ai_response})
