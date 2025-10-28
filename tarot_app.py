import streamlit as st
import random
import os
from PIL import Image

# ---- 页面设置 ----
st.set_page_config(page_title="Tarot Divination - RuoXi", layout="wide")

# ---- 背景函数 ----
def set_background(image_path):
    with open(image_path, "rb") as file:
        data = file.read()
    encoded = data.hex()
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


# ---- 加载图片（强制逆位旋转180°） ----
def load_card_image(path, reversed_=False):
    img = Image.open(path).convert("RGBA")
    if reversed_:
        img = img.transpose(Image.ROTATE_180)
    return img

# ---- 修改这个函数 ----
def load_and_crop_back(path, target_aspect_ratio=0.575): # 添加一个 target_aspect_ratio 参数
    img = Image.open(path)
    width, height = img.size

    # 计算目标宽度或高度
    # 优先保持宽度，然后计算所需高度
    target_height = int(width / target_aspect_ratio)

    # 如果原图高度不足，则以原图高度为基准，裁剪宽度
    if target_height > height:
        target_width_based_on_height = int(height * target_aspect_ratio)
        left = (width - target_width_based_on_height) / 2
        top = 0
        right = (width + target_width_based_on_height) / 2
        bottom = height
        img = img.crop((left, top, right, bottom))
    else:
        # 裁剪高度，保持居中
        top = (height - target_height) / 2
        bottom = (height + target_height) / 2
        left = 0
        right = width
        img = img.crop((left, top, right, bottom))

    return img

# ---- 塔罗牌定义 ----
# ... (其余代码保持不变) ...


# ---- 塔罗牌定义 ----
tarot_cards = [
    # Major Arcana
    "The_Fool", "The_Magician", "The_High_Priestess", "The_Empress", "The_Emperor",
    "The_Hierophant", "The_Lovers", "The_Chariot", "Strength", "The_Hermit",
    "Wheel_of_Fortune", "Justice", "The_Hanged_Man", "Death", "Temperance",
    "The_Devil", "The_Tower", "The_Star", "The_Moon", "The_Sun",
    "Judgement", "The_World",

    # Wands
    "Ace_of_Wands", "Two_of_Wands", "Three_of_Wands", "Four_of_Wands", "Five_of_Wands",
    "Six_of_Wands", "Seven_of_Wands", "Eight_of_Wands", "Nine_of_Wands", "Ten_of_Wands",
    "Page_of_Wands", "Knight_of_Wands", "Queen_of_Wands", "King_of_Wands",

    # Cups
    "Ace_of_Cups", "Two_of_Cups", "Three_of_Cups", "Four_of_Cups", "Five_of_Cups",
    "Six_of_Cups", "Seven_of_Cups", "Eight_of_Cups", "Nine_of_Cups", "Ten_of_Cups",
    "Page_of_Cups", "Knight_of_Cups", "Queen_of_Cups", "King_of_Cups",

    # Swords
    "Ace_of_Swords", "Two_of_Swords", "Three_of_Swords", "Four_of_Swords", "Five_of_Swords",
    "Six_of_Swords", "Seven_of_Swords", "Eight_of_Swords", "Nine_of_Swords", "Ten_of_Swords",
    "Page_of_Swords", "Knight_of_Swords", "Queen_of_Swords", "King_of_Swords",

    # Pentacles
    "Ace_of_Pentacles", "Two_of_Pentacles", "Three_of_Pentacles", "Four_of_Pentacles", "Five_of_Pentacles",
    "Six_of_Pentacles", "Seven_of_Pentacles", "Eight_of_Pentacles", "Nine_of_Pentacles", "Ten_of_Pentacles",
    "Page_of_Pentacles", "Knight_of_Pentacles", "Queen_of_Pentacles", "King_of_Pentacles"
]


# ---- 含关键词的含义库（示例，可扩充）----
tarot_meanings = {
    # Major Arcana
    "The_Fool": ["新开始", "冒险", "自由"],
    "The_Magician": ["创造力", "意志力", "潜能"],
    "The_High_Priestess": ["直觉", "秘密", "潜意识"],
    "The_Empress": ["丰饶", "爱", "创造"],
    "The_Emperor": ["权威", "稳定", "控制"],
    "The_Hierophant": ["传统", "信仰", "学习"],
    "The_Lovers": ["关系", "选择", "融合"],
    "The_Chariot": ["胜利", "自制", "前进"],
    "Strength": ["勇气", "耐心", "温柔的力量"],
    "The_Hermit": ["自省", "智慧", "孤独"],
    "Wheel_of_Fortune": ["命运", "循环", "变化"],
    "Justice": ["公平", "真相", "因果"],
    "The_Hanged_Man": ["放下", "牺牲", "不同视角"],
    "Death": ["结束", "转变", "重生"],
    "Temperance": ["平衡", "节制", "融合"],
    "The_Devil": ["束缚", "诱惑", "欲望"],
    "The_Tower": ["崩塌", "突变", "觉醒"],
    "The_Star": ["希望", "疗愈", "信念"],
    "The_Moon": ["迷雾", "幻觉", "潜意识"],
    "The_Sun": ["喜悦", "成功", "能量"],
    "Judgement": ["觉醒", "救赎", "评估"],
    "The_World": ["完成", "整合", "圆满"],

    # Wands
    "Ace_of_Wands": ["灵感", "新机会", "动力"],
    "Two_of_Wands": ["计划", "远见", "选择"],
    "Three_of_Wands": ["进展", "扩展", "远航"],
    "Four_of_Wands": ["庆祝", "安稳", "成果"],
    "Five_of_Wands": ["竞争", "冲突", "分歧"],
    "Six_of_Wands": ["胜利", "认可", "自信"],
    "Seven_of_Wands": ["防御", "坚持", "勇气"],
    "Eight_of_Wands": ["速度", "行动", "变化"],
    "Nine_of_Wands": ["警觉", "韧性", "疲惫"],
    "Ten_of_Wands": ["负担", "责任", "压力"],
    "Page_of_Wands": ["热情", "探索", "学习"],
    "Knight_of_Wands": ["冒险", "冲动", "热血"],
    "Queen_of_Wands": ["自信", "魅力", "领导力"],
    "King_of_Wands": ["远见", "权威", "掌控"],

    # Cups
    "Ace_of_Cups": ["爱", "情感", "新关系"],
    "Two_of_Cups": ["结合", "伙伴", "互信"],
    "Three_of_Cups": ["友谊", "庆祝", "团结"],
    "Four_of_Cups": ["冷漠", "反思", "厌倦"],
    "Five_of_Cups": ["失落", "遗憾", "悲伤"],
    "Six_of_Cups": ["回忆", "纯真", "过去"],
    "Seven_of_Cups": ["幻想", "诱惑", "选择"],
    "Eight_of_Cups": ["离开", "放下", "寻找意义"],
    "Nine_of_Cups": ["满足", "愿望成真", "感恩"],
    "Ten_of_Cups": ["幸福", "和谐", "家庭圆满"],
    "Page_of_Cups": ["浪漫", "想象", "情感讯息"],
    "Knight_of_Cups": ["追求", "浪漫", "理想主义"],
    "Queen_of_Cups": ["同理心", "关怀", "直觉"],
    "King_of_Cups": ["情绪平衡", "智慧", "慈悲"],

    # Swords
    "Ace_of_Swords": ["真相", "突破", "决断"],
    "Two_of_Swords": ["犹豫", "平衡", "僵局"],
    "Three_of_Swords": ["心碎", "失望", "真相"],
    "Four_of_Swords": ["休息", "疗愈", "沉思"],
    "Five_of_Swords": ["冲突", "失败", "策略"],
    "Six_of_Swords": ["离开", "过渡", "疗愈旅程"],
    "Seven_of_Swords": ["欺骗", "隐秘", "独立思考"],
    "Eight_of_Swords": ["束缚", "恐惧", "受限"],
    "Nine_of_Swords": ["焦虑", "失眠", "担忧"],
    "Ten_of_Swords": ["结束", "崩溃", "释放"],
    "Page_of_Swords": ["观察", "警觉", "好奇"],
    "Knight_of_Swords": ["急切", "行动", "冲突"],
    "Queen_of_Swords": ["理性", "独立", "真相"],
    "King_of_Swords": ["权威", "逻辑", "判断"],

    # Pentacles
    "Ace_of_Pentacles": ["新机会", "物质丰盛", "基础"],
    "Two_of_Pentacles": ["平衡", "适应", "灵活"],
    "Three_of_Pentacles": ["合作", "团队", "学习"],
    "Four_of_Pentacles": ["安全", "占有", "保守"],
    "Five_of_Pentacles": ["贫困", "孤立", "挑战"],
    "Six_of_Pentacles": ["给予", "分享", "平衡"],
    "Seven_of_Pentacles": ["等待", "评估", "成长"],
    "Eight_of_Pentacles": ["专注", "学习", "技能"],
    "Nine_of_Pentacles": ["自立", "享受", "成就"],
    "Ten_of_Pentacles": ["财富", "家庭", "传承"],
    "Page_of_Pentacles": ["学习", "机会", "实践"],
    "Knight_of_Pentacles": ["责任", "耐心", "稳定"],
    "Queen_of_Pentacles": ["关怀", "安全感", "现实感"],
    "King_of_Pentacles": ["富足", "成就", "可靠"],
}
                          


# ---- 初始化 session ----
if "drawn" not in st.session_state:
    st.session_state["drawn"] = False
if "drawn_cards" not in st.session_state:
    st.session_state["drawn_cards"] = []
if "revealed" not in st.session_state:
    st.session_state["revealed"] = []
if "reversed" not in st.session_state:
    st.session_state["reversed"] = []

# ---- 背景 ----
set_background("images/background.jpg")

# ---- 标题 ----
st.markdown("<h1 style='text-align:center; color:white;'>🔮 Tarot Divination - RuoXi</h1>", unsafe_allow_html=True)

# ---- 输入区 ----
question = st.text_input("✨ 你的问题是什么？")
num_cards = st.number_input("你想抽几张牌？", min_value=1, max_value=9, value=1, step=1)

# ---- 抽牌按钮 ----
if st.button("抽牌！"):
    st.session_state["drawn"] = True
    st.session_state["drawn_cards"] = random.sample(tarot_cards, num_cards)
    st.session_state["reversed"] = [random.choice([True, False]) for _ in range(num_cards)]
    st.session_state["revealed"] = [False for _ in range(num_cards)]
    st.rerun()

# ---- 抽牌后展示 ----
if st.session_state["drawn"]:
    # ... 其他代码 ...
    cols = st.columns(len(st.session_state["drawn_cards"]))
    for i, card in enumerate(st.session_state["drawn_cards"]):
        with cols[i]:
            if st.session_state["revealed"][i]:
                # 先获取这张牌是否逆位
                reversed_ = st.session_state["reversed"][i]
                
                # 将 reversed_ 状态传入函数！
                img_path = os.path.join("images", f"{card}.webp")
                img = load_card_image(img_path, reversed_=reversed_) # <-- 修改这一行
                
                st.image(img, caption=f"{card.replace('_', ' ')} ({'逆位' if reversed_ else '正位'})")

            

                keywords = tarot_meanings.get(card, [])
                if keywords:
                    st.markdown(
                        f"<div style='text-align:center; color:#fff; font-size:14px; margin-top:5px;'>"
                        + " · ".join(keywords) +
                        "</div>",
                        unsafe_allow_html=True
                    )
            else:
                back = load_and_crop_back(os.path.join("images", "back.jpg"))
                st.image(
                    back,
                    caption="点击翻开这张牌",
                    use_container_width=False,
                    width=230   # ← 保持与塔罗牌相同
                )
                if st.button(f"翻开第{i+1}张", key=f"flip_{i}"):
                    st.session_state["revealed"][i] = True
                    st.rerun()



    # 再来一次按钮
    if st.button("🔁 再来一次"):
        st.session_state["drawn"] = False
        st.session_state["drawn_cards"] = []
        st.session_state["revealed"] = []
        st.session_state["reversed"] = []
        st.rerun()

else:
    st.markdown(
        "<div style='text-align:center; background-color:#524e3e; color:white; "
        "padding:10px 20px; border-radius:10px; display:inline-block;'>"
        "请先点击上方『抽牌！』按钮进行抽牌 🌟</div>",
        unsafe_allow_html=True
    )

# ---- 左下角推广信息 ----
st.markdown("""
<div style='position: fixed; bottom: 15px; left: 15px; 
background-color: rgba(20, 20, 30, 0.55); 
padding: 10px 15px; border-radius: 10px; 
color: #ffffff; font-size: 14px; z-index:9999;
box-shadow: 0 0 6px rgba(255,255,255,0.2);'>
💬 如果你希望获得专业塔罗咨询：<b>XinRuoXi_111</b>
</div>
""", unsafe_allow_html=True)
