import streamlit as st
from streamlit_image_select import image_select
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import numpy as np
import time
from PIL import Image
placeholder = st.empty()

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
        
    t = time.localtime().tm_hour
    #現在の時刻が12時から18時の間なら、
    if 12 <= t < 18:
        #PIL画像を配列に変換し、OffsetImageを作成
        rect = Rectangle((1, 0), 1, 1, facecolor='green')
        ax.add_patch(rect)
        rect = Rectangle((2, 0), 1, 1, facecolor='blue')
        ax.add_patch(rect)
        rect = Rectangle((3, 0), 1, 1, facecolor='red')
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

# 画像をボタンとして使用するためのカスタム関数
def image_button(image, key, action=None):
    # 画像を表示
    col = st.empty()
    col.image(image, use_column_width=True)

    # ユーザーが画像をクリックしたかどうかを検出
    if col.button("", key=key):
        # 指定されたアクションを実行
        if action:
            action()

image_paths = ['data/start.jpg', 'data/stop.jpg']
images = [Image.open(path) for path in image_paths]
selected_index = image_select("", images, return_value="index")

# 選択された画像のインデックスに基づいて条件分岐
if selected_index == 0:
    st.session_state['running'] = True
else:
    st.session_state['running'] = False

# 色を0.5秒ごとに更新する
while st.session_state['running']:
    st.session_state['fig'] = plot_colored_rectangles_with_image()
    placeholder.pyplot(st.session_state['fig'])
    time.sleep(0.5)
    plt.close(st.session_state['fig'])

# 常に状態にある図を表示する
placeholder.pyplot(st.session_state['fig'])
