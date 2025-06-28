# -*- coding: utf-8 -*-
"""
Created on Sat Jun 28 14:21:11 2025

@author: kawano1324
"""

import streamlit as st
import random

# ---------------------- データ定義 ----------------------
transition_rules = {
    "C": ["G", "Am", "F", "Em", "Dm"],
    "G": ["C", "Em", "Am", "D"],
    "Am": ["F", "G", "C", "Dm", "E"],
    "F": ["G", "Em", "C", "Am", "Dm"],
    "Em": ["Am", "F", "G", "C"],
    "D": ["G", "Em", "A"],
    "A": ["D", "F", "Am"],
    "Dm": ["G", "C", "Am", "Em"],
    "E": ["Am", "F", "C"]
}

emotion_to_start_chord = {
    "明るい": ("C", "C"),
    "切ない": ("F", "F"),
    "楽しい": ("G", "G"),
    "情熱的": ("Em", "Em"),
    "郷愁的": ("Am", "Am"),
    "静かな": ("Dm", "Dm")
}

strumming_patterns = {
    "slow": ["↓×↓↑↓↑↓", "↓×↓×↓↑×↑"],
    "medium": ["↓↑↓↑↓↑×↑", "↓×↓↑×↑↓↑"],
    "fast": ["↓↑↓↑↓↑↓↑", "↓↑↓↑×↑↓↑"]
}

guitar_tabs = {
    "C": ["e|--0--", "B|--1--", "G|--0--", "D|--2--", "A|--3--", "E|-----"],
    "G": ["e|--3--", "B|--3--", "G|--0--", "D|--0--", "A|--2--", "E|--3--"],
    "Am": ["e|--0--", "B|--1--", "G|--2--", "D|--2--", "A|--0--", "E|-----"],
    "F": ["e|--1--", "B|--1--", "G|--2--", "D|--3--", "A|--3--", "E|--1--"],
    "Em": ["e|--0--", "B|--0--", "G|--0--", "D|--2--", "A|--2--", "E|--0--"],
    "D": ["e|--2--", "B|--3--", "G|--2--", "D|--0--", "A|-----", "E|-----"],
    "A": ["e|--0--", "B|--2--", "G|--2--", "D|--2--", "A|--0--", "E|-----"],
    "Dm": ["e|--1--", "B|--3--", "G|--2--", "D|--0--", "A|-----", "E|-----"],
    "E": ["e|--0--", "B|--0--", "G|--1--", "D|--2--", "A|--2--", "E|--0--"]
}

famous_progressions = {
    "丸の内進行": ["F", "G", "Em", "Am"],
    "小室進行": ["C", "G", "Am", "F"],
    "王道進行": ["C", "G", "Am", "F"],
    "カノン進行": ["C", "G", "Am", "Em", "F", "C", "F", "G"]
}

# ---------------------- Streamlit UI ----------------------
st.title("🎸 ギターコード進行生成AI")
st.write("歌詞と感情、テンポを選ぶと、それに合ったコード進行・ストローク・TABを生成します。")

lyrics = st.text_input("🎵 歌詞（例：静かな夜にあなたを思う）", "")
emotion = st.selectbox("😌 感情", list(emotion_to_start_chord.keys()))
bpm = st.slider("🎵 BPM（テンポ）", min_value=60, max_value=150, value=100)
use_famous = st.checkbox("🎼 有名コード進行を使う（例：丸の内進行、小室進行）", value=False)

if bpm < 80:
    bpm_category = "slow"
elif bpm < 110:
    bpm_category = "medium"
else:
    bpm_category = "fast"

if st.button("▶ コード進行を生成！"):
    start_chord, key = emotion_to_start_chord[emotion]

    if use_famous:
        name, pattern = random.choice(list(famous_progressions.items()))
        st.subheader(f"🎶 選ばれた進行パターン: {name}")
        full_progression = [pattern[i:i+2] for i in range(0, min(8, len(pattern)), 2)]
    else:
        full_progression = []
        current_chord = start_chord
        for _ in range(8):
            num_chords = random.randint(1, 3)
            measure_chords = [current_chord]
            for _ in range(num_chords - 1):
                next_candidates = transition_rules.get(current_chord, list(transition_rules.keys()))
                current_chord = random.choice(next_candidates)
                measure_chords.append(current_chord)
            current_chord = measure_chords[-1]
            full_progression.append(measure_chords)

    selected_strumming = random.choice(strumming_patterns[bpm_category])

    st.markdown(f"**🎵 キー：{key}　|　感情：{emotion}　|　BPM：{bpm}（{bpm_category}）**")
    
    st.subheader("🎼 コード進行（8小節）")
    for i, measure in enumerate(full_progression, 1):
        st.write(f"{i}小節目: {' - '.join(measure)}")

    st.subheader("🎸 ストロークパターン")
    st.code(selected_strumming)

    st.subheader("📘 TAB譜")
    used_chords = sorted(set(chord for measure in full_progression for chord in measure))
    for chord in used_chords:
        if chord in guitar_tabs:
            st.markdown(f"**{chord}**")
            st.code("\n".join(guitar_tabs[chord]))
