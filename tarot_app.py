import streamlit as st
import random
from PIL import Image
import base64
import os

# ============ 页面设置 ============
st.set_page_config(page_title="Tarot Divination - XinRuoXi", page_icon="🔮", layout="centered")
# ---- 自定义标题字体颜色 ----
st.markdown("""
    <style>
    h1 {
        color: white !important;
        text-shadow: 0px 0px 8px rgba(255, 255, 255, 0.3);
    }
    </style>
""", unsafe_allow_html=True)

# ============ 背景函数 ============
def set_background(image_file):
    with open(image_file, "rb") as file:
        encoded = base64.b64encode(file.read()).decode()
    bg_style = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    </style>
    """
    st.markdown(bg_style, unsafe_allow_html=True)

# ============ 图片加载函数 ============
def load_card_image(path, reversed_=False):
    """加载塔罗牌，支持逆位旋转"""
    img = Image.open(path)
    if reversed_:
        img = img.rotate(180)
    return img


def load_and_crop_back(path):
    """加载并居中裁剪牌背，裁剪比例 0.6:1"""
    img = Image.open(path)
    w, h = img.size
    target_ratio = 0.6  # 宽:高
    new_w = int(h * target_ratio)
    if new_w > w:
        new_h = int(w / target_ratio)
        top = (h - new_h) // 2
        bottom = top + new_h
        left, right = 0, w
    else:
        left = (w - new_w) // 2
        right = left + new_w
        top, bottom = 0, h
    cropped = img.crop((left, top, right, bottom))
    return cropped

# ============ 初始化状态 ============
if "drawn_cards" not in st.session_state:
    st.session_state["drawn_cards"] = []
if "revealed" not in st.session_state:
    st.session_state["revealed"] = []
if "reversed" not in st.session_state:
    st.session_state["reversed"] = []
if "drawn" not in st.session_state:
    st.session_state["drawn"] = False

# ============ 页面逻辑 ============
if not st.session_state["drawn"]:
    # 抽牌前 → 使用浅色背景（默认）
    st.markdown("<h1 style='text-align:center; color:#333;'>🔮 Tarot Divination - RuoXi</h1>", unsafe_allow_html=True)
    question = st.text_input("✨ 你的问题是什么？", key="question_input")
    num_cards = st.number_input("你想抽几张牌？", min_value=1, max_value=5, step=1)
    draw_button = st.button("抽牌！")

    if draw_button and question:
        card_files = [f[:-5] for f in os.listdir("images") if f.endswith(".webp")]
        st.session_state["drawn_cards"] = random.sample(card_files, num_cards)
        st.session_state["reversed"] = [random.choice([True, False]) for _ in range(num_cards)]
        st.session_state["revealed"] = [False] * num_cards
        st.session_state["drawn"] = True
        st.rerun()

else:
    # 抽牌后 → 加载背景图并使用白色字体
    set_background("images/background.jpg")

    st.markdown("<h1 style='text-align:center; color:white;'>🔮 你的塔罗牌结果</h1>", unsafe_allow_html=True)
    cols = st.columns(len(st.session_state["drawn_cards"]))

    for i, card in enumerate(st.session_state["drawn_cards"]):
        with cols[i]:
            if st.session_state["revealed"][i]:
                # 已翻开 → 显示塔罗牌面
                img = load_card_image(
                    os.path.join("images", f"{card}.webp"),
                    reversed_=st.session_state["reversed"][i]
                )
                st.image(img, caption=f"{card} ({'逆位' if st.session_state['reversed'][i] else '正位'})")
            else:
                # 未翻开 → 显示裁剪后的牌背
                back = load_and_crop_back(os.path.join("images", "back.jpg"))
                st.image(back, caption="点击翻开这张牌")
                if st.button(f"翻开第{i+1}张", key=f"flip_{i}"):
                    st.session_state["revealed"][i] = True
                    st.rerun()

    if st.button("🔁 再来一次"):
        st.session_state["drawn"] = False
        st.session_state["drawn_cards"] = []
        st.session_state["revealed"] = []
        st.session_state["reversed"] = []
        st.rerun()
