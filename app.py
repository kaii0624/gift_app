import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import numpy as np
import time
from PIL import Image

# 事前に用意されたPNG画像をロードする
image_path = 'data/bag1.png'  # 必要に応じてパスを調整してください
image = Image.open(image_path)
if image.mode != 'RGBA':
    image = image.convert('RGBA')
    
image_path2 = 'data/background1.png'  # 必要に応じてパスを調整してください
image2 = Image.open(image_path2)
if image2.mode != 'RGBA':
    image2 = image.convert('RGBA')

# 四角形をプロットし、PNG画像を重ねる関数を定義する
def plot_colored_rectangles_with_image():
    fig, ax = plt.subplots(figsize=(6, 2))
    
    colors = np.random.rand(3, 3)  # 3つのランダムな色を生成
    for i, color in enumerate(colors):
        rect = Rectangle((i+1, 0), 1, 1, facecolor=color)
        ax.add_patch(rect)


    # PIL画像を配列に変換し、OffsetImageを作成
    image_array = np.array(image)
    im = OffsetImage(image_array, zoom=0.65)  # 必要に応じてズームを調整
    ab = AnnotationBbox(im, (2.5, 0.52), frameon=False, box_alignment=(0.5,0.5))
    ax.add_artist(ab)
                # PIL画像を配列に変換し、OffsetImageを作成
    image_array = np.array(image2)
    im = OffsetImage(image_array, zoom=0.43)  # 必要に応じてズームを調整
    ab = AnnotationBbox(im, (1.5, 0.5), frameon=False, box_alignment=(0.5,0.5))
    ax.add_artist(ab)
    
    ax.set_xlim(0, 4)
    ax.set_ylim(0, 1)
    ax.axis('off')
    return fig

# 状態変数を初期化する
if 'running' not in st.session_state:
    st.session_state['running'] = False
    st.session_state['fig'] = plot_colored_rectangles_with_image()

# スタートとストップのボタン
# ボタン用の画像をロードする
start_button_image = Image.open('data/start.png')
stop_button_image = Image.open('data/stop.png')

col1, col2 = st.columns(2)
with col1:
    if st.button('スタート'):
        st.session_state['running'] = True
with col2:
    if st.button('ストップ'):
        st.session_state['running'] = False

# 図のためのプレースホルダー
placeholder = st.empty()

# 色を0.5秒ごとに更新する
while st.session_state['running']:
    st.session_state['fig'] = plot_colored_rectangles_with_image()
    placeholder.pyplot(st.session_state['fig'])
    time.sleep(0.5)
    plt.close(st.session_state['fig'])

# 常に状態にある図を表示する
placeholder.pyplot(st.session_state['fig'])
