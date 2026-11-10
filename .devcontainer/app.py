import streamlit as st

st.set_page_config(page_title="智能 AI 助理", page_icon="🤖")

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
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 顯示 AI 的回應
    with st.chat_message("assistant"):
        # 這裡可以串接 OpenAI、Gemini API 或寫固定的回應規則
        # API 金鑰請放在 Render 的 Environment Variables，不要寫在程式碼裡
        ai_response = f"您好！我收到您的訊息了：『{prompt}』。這是一個串接成功的測試回應！"
        st.markdown(ai_response)

    st.session_state.messages.append({"role": "assistant", "content": ai_response})
