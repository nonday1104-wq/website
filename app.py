import streamlit as st

# 取得網址後方的參數
query_params = st.query_params

# 檢查金鑰是否正確
if query_params.get("key") != "safe123":
    st.error("🔒 拒絕存取：此應用程式僅允許透過官方 Cloudflare 安全入口網站存取。")
    st.stop() # 直接中斷執行，不加載任何 UI 資源

# 金鑰正確才執行下方的原本程式
st.title("網站")
st.write("網站部署成功")
