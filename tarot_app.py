import streamlit as st
import random
from PIL import Image
import base64
import os

# ============================
# 🌟 Tarot App - Simple Final Version
# ============================
# ✅ 背景只在抽牌后显示
# ✅ 背景时字体自动变白
# ✅ 每张牌底下有一个“翻开这张牌”按钮
# ✅ 自动调整图片大小
# ============================

st.set_page_config(page_title="塔罗抽牌占卜", page_icon="🔮", layout="centered")


# ---- 背景设置函数 ----
def set_background(image_file):
    """设置背景图（base64嵌入CSS）"""
    with open(image_file, "rb") as f:
        encoded_string = base64.b64encode(f.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/png;base64,{encoded_string});
            background-size: cover;
            background-position: center;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# ---- 加载塔罗牌图片 ----
def load_card_image(image_path, reversed_=False):
    img = Image.open(image_path)
    img = img.resize((350, 500))
    if reversed_:
        img = img.rotate(180)
    return img


# ---- 页面标题 ----
st.markdown("<h1 style='text-align: center;'>🔮 塔罗抽牌占卜</h1>", unsafe_allow_html=True)

# ---- 输入 ----
question = st.text_input("✨ 你的问题是什么？")
num_cards = st.number_input("你想抽几张牌？", min_value=1, max_value=10, step=1, value=1)

# ---- 抽牌按钮 ----
if st.button("抽牌！"):
    # 设置背景
    set_background("images/background.png")

    # 设置白色字体
    st.markdown(
        """
        <style>
        html, body, [class*="st-"], label, p, span, h1, h2, h3, h4, h5, h6 {
            color: white !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # 随机抽牌
    tarot_files = [f for f in os.listdir("images") if f.endswith(".webp")]
    selected_cards = random.sample(tarot_files, num_cards)

    # 初始化状态
    st.session_state["drawn_cards"] = selected_cards
    st.session_state["revealed"] = [False] * num_cards
    st.session_state["reversed"] = [random.choice([True, False]) for _ in range(num_cards)]


# ---- 显示抽牌区 ----
if "drawn_cards" in st.session_state:
    cols = st.columns(len(st.session_state["drawn_cards"]))

    for i, card in enumerate(st.session_state["drawn_cards"]):
        with cols[i]:
            if st.session_state["revealed"][i]:
                # 翻开后的正反位显示
                img = load_card_image(
                    os.path.join("images", f"{card}"),
                    reversed_=st.session_state["reversed"][i],
                )
                st.image(
                    img,
                    caption=f"{card}（{'逆位' if st.session_state['reversed'][i] else '正位'}）",
                )
            else:
                # 未翻开 → 显示牌背
                back = load_card_image(os.path.join("images", "back.png"))
                st.image(back, caption="未翻开的牌")
                # 翻开按钮
                if st.button("翻开这张牌", key=f"flip_{i}"):
                    st.session_state["revealed"][i] = True
