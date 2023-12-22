import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import numpy as np
import time
from PIL import Image


if 'current_color_index' not in st.session_state:
    st.session_state['current_color_index'] = 0
    st.session_state['seed'] = np.random.randint(1000)
    
np.random.seed(st.session_state['seed'])
all_colors = np.random.rand(10, 3)
    
image_path = 'data/bag1.png'  # 必要に応じてパスを調整してください
image = Image.open(image_path)
if image.mode != 'RGBA':
    image = image.convert('RGBA')
    
image_path2 = 'data/background1.png'  # 必要に応じてパスを調整してください
image2 = Image.open(image_path2)
if image2.mode != 'RGBA':
    image2 = image.convert('RGBA')

colors_init = np.random.rand(3, 3) 
colors_init2 = np.random.rand(3, 3) 


st.set_page_config(layout="wide")
placeholder = st.empty()

# 四角形をプロットし、PNG画像を重ねる関数を定義する
def plot_colored_rectangles_with_image(colors):
    plt.close('all')
    fig, ax = plt.subplots(figsize=(6, 2))

    for i, color in enumerate(reversed(colors)):
        rect = Rectangle((i+1, 0), 1, 1, facecolor=color)
        # rect = Rectangle((len(colors) - i, 0), 1, 1, facecolor=color)
        ax.add_patch(rect)

    image_array = np.array(image)
    im = OffsetImage(image_array, zoom=0.65)  # 必要に応じてズームを調整
    ab = AnnotationBbox(im, (2.5, 0.52), frameon=False, box_alignment=(0.5,0.5))
    ax.add_artist(ab)

    image_array = np.array(image2)
    im = OffsetImage(image_array, zoom=0.43)  # 必要に応じてズームを調整
    ab = AnnotationBbox(im, (1.5, 0.5), frameon=False, box_alignment=(0.5,0.5))
    ax.add_artist(ab)
    
    ax.set_xlim(0, 4)
    ax.set_ylim(0, 1)
    ax.axis('off')
    return fig

if 'buttons_visible' not in st.session_state:
    st.session_state['buttons_visible'] = True
if 'running' not in st.session_state:
    st.session_state['running'] = "init"

st.markdown("""
    <style>
    div.stButton > button:first-child {
        # border: none;
        color: white;
        padding: 5px 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 24px;
        margin: 4px 2px;
        # transition-duration: 0.1s;
        cursor: pointer;
        border-radius: 12px;
        background-color: #07785f;
    }
    </style>
    """, unsafe_allow_html=True)

# カラムの設定
col1, col2, col3 = st.columns(3)

with col1:
    if st.button('START'):
        st.session_state['running'] = "START"
        plt.close(st.session_state.get('fig', plt.figure()))
with col2:
    if st.button('STOP'):
        st.session_state['running'] = "STOP"
        st.session_state['buttons_visible'] = False  # STOPが押されたらボタンを隠す
with col3:
    if st.button('RESET'):
        st.session_state['running'] = "init"
        st.session_state['current_color_index'] = 0 
        st.session_state['buttons_visible'] = True  # RESETでボタンを再表示
        st.session_state['seed'] = np.random.randint(1000)
        st.experimental_rerun()

while True:
    if st.session_state['running'] == "START":
        time.sleep(0.6)
        plt.close(st.session_state.get('fig', plt.figure()))

        # 現在の色を選択
        colors = all_colors[st.session_state['current_color_index']:st.session_state['current_color_index'] + 3]

        # インデックスを更新
        st.session_state['current_color_index'] += 1
        if st.session_state['current_color_index'] > (len(all_colors) - 3):
            st.session_state['current_color_index'] = 0

    elif st.session_state['running']=="STOP":
        if 18 <= (time.localtime().tm_hour + 9) % 24 < 24:
            colors = [
                (149/255, 130/255, 114/255),  # rgb(149, 130, 114)
                (176/255, 159/255, 143/255),  # rgb(176, 159, 143)
                (101/255, 99/255, 102/255)    # rgb(101, 99, 102)
            ]
        else:
            colors = all_colors[st.session_state['current_color_index']:st.session_state['current_color_index'] + 3]
    else:
        colors = [(1, 1, 1)]
    
    st.session_state['fig'] = plot_colored_rectangles_with_image(colors)
    placeholder.pyplot(st.session_state['fig'])
    
    
