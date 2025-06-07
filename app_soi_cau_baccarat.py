
import streamlit as st

# Tiêu đề
st.set_page_config(page_title="Soi cầu Baccarat", layout="centered")
st.title("🔮 Soi cầu Baccarat thông minh")
st.markdown("Ứng dụng tự động phân tích cầu Baccarat và dự đoán kết quả ván tiếp theo (P = Player, B = Banker, T = Tie).")

# Nhập kết quả lịch sử
history_input = st.text_input("Nhập chuỗi kết quả (vd: P B P P B T ...)", "")

def clean_history(raw_text):
    items = raw_text.upper().split()
    return [i for i in items if i in ["P", "B", "T"]]

# Phân tích các quy luật cầu phổ biến
def detect_cau_bet(history):
    if len(history) < 3:
        return False
    last = history[-1]
    return all(h == last for h in history[-3:])

def detect_cau_nhay(history):
    if len(history) < 4:
        return False
    return history[-1] != history[-2] and history[-2] == history[-3] and history[-3] != history[-4]

def detect_cau_doi(history):
    if len(history) < 4:
        return False
    return history[-1] == history[-2] and history[-3] == history[-4] and history[-1] != history[-3]

def detect_cau_buoc_thang(history):
    if len(history) < 6:
        return False
    pattern = history[-6:]
    return pattern == ["P","B","B","P","B","B"] or pattern == ["B","P","P","B","P","P"]

def detect_cau_xuong_ca(history):
    if len(history) < 5:
        return False
    return history[-2] == "T" or history[-4] == "T"

def detect_cau_doi_xung(history):
    if len(history) < 5:
        return False
    return history[-1] == history[-5] and history[-2] == history[-4]

# Dự đoán theo cầu
def smart_predict(history):
    if detect_cau_bet(history):
        return f"🔁 Cầu bệt → Dự đoán: {history[-1]}"
    elif detect_cau_nhay(history):
        return f"🔃 Cầu nhảy 1-1 → Dự đoán: {history[-2]}"
    elif detect_cau_doi(history):
        return f"👯 Cầu đôi → Dự đoán: {'P' if history[-1]=='B' else 'B'}"
    elif detect_cau_buoc_thang(history):
        return f"📈 Cầu bước thang → Dự đoán: {'P' if history[-1]=='B' else 'B'}"
    elif detect_cau_doi_xung(history):
        return f"🔁 Cầu đối xứng → Dự đoán: {history[-3]}"
    elif detect_cau_xuong_ca(history):
        return f"🐟 Có Tie đan xen → Dự đoán: {'T' if history[-1] != 'T' else history[-2]}"
    else:
        return "🤷 Không phát hiện cầu rõ → Dự đoán ngẫu nhiên: P hoặc B"

# Xử lý và hiển thị
history = clean_history(history_input)
if history:
    st.markdown(f"✅ Lịch sử ({len(history)} ván): `{history}`")
    result = smart_predict(history)
    st.success(result)
else:
    st.warning("Hãy nhập ít nhất 4 kết quả (P, B hoặc T) để phân tích.")
