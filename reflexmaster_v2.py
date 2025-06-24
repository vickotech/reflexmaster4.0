
import streamlit as st
import random
import time

st.set_page_config(page_title="ReflexMaster v2", layout="centered")
st.title("🎯 ReflexMaster v2 - Klik Target & Catat Skormu!")

# Inisialisasi leaderboard dalam session_state
if "leaderboard" not in st.session_state:
    st.session_state.leaderboard = []

# Inisialisasi variabel game
for key, default in {
    "player_name": "",
    "score": 0,
    "start_time": None,
    "game_over": False,
    "target_position": (random.randint(0, 4), random.randint(0, 4)),
    "score_saved": False,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# Input nama pemain (hanya jika belum mulai main)
if st.session_state.player_name == "":
    name_input = st.text_input("Masukkan Nama untuk Mulai Bermain:")
    if name_input:
        st.session_state.player_name = name_input.strip()
        st.experimental_rerun()

# Fungsi reset game
def reset_game():
    st.session_state.score = 0
    st.session_state.start_time = time.time()
    st.session_state.game_over = False
    st.session_state.score_saved = False
    st.session_state.target_position = (random.randint(0, 4), random.randint(0, 4))

# Mulai game
if st.button("Mulai Game" if st.session_state.start_time is None else "Mulai Lagi"):
    reset_game()

# Jalankan game selama 20 detik
if st.session_state.start_time:
    elapsed = time.time() - st.session_state.start_time
    remaining = max(0, 20 - elapsed)

    if remaining == 0:
        st.session_state.game_over = True

    if not st.session_state.game_over:
        st.success(f"{st.session_state.player_name} | Waktu tersisa: {int(remaining)} detik | Skor: {st.session_state.score}")

        # Tampilkan grid tombol 5x5, hanya satu yang aktif
        for i in range(5):
            cols = st.columns(5)
            for j in range(5):
                if (i, j) == st.session_state.target_position:
                    if cols[j].button("🎯", key=f"{i}-{j}-{st.session_state.score}"):
                        st.session_state.score += 1
                        st.session_state.target_position = (random.randint(0, 4), random.randint(0, 4))
                else:
                    cols[j].empty()
    else:
        st.subheader(f"⏱️ Waktu Habis! Skor Akhir {st.session_state.player_name}: {st.session_state.score}")

        # Simpan skor ke leaderboard satu kali saja
        if not st.session_state.score_saved:
            st.session_state.leaderboard.append((st.session_state.player_name, st.session_state.score))
            st.session_state.leaderboard = sorted(st.session_state.leaderboard, key=lambda x: x[1], reverse=True)[:5]
            st.session_state.score_saved = True

        st.markdown("## 🏆 Papan Peringkat Top 5")
        for idx, (name, score) in enumerate(st.session_state.leaderboard, start=1):
            st.write(f"**{idx}. {name}** - {score} poin")

        if st.button("Main Lagi"):
            for key in ["player_name", "score", "start_time", "game_over", "score_saved", "target_position"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.experimental_rerun()
