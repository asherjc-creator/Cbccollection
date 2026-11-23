
import streamlit as st
import sqlite3
from datetime import datetime
import pandas as pd

# ---------------- CONFIG ----------------
TARGET = 100000
DB_FILE = "cbc_projector_commitments.db"
ADMIN_PASSWORD = "cbc654&"

st.set_page_config(
    page_title="CBC Deshaipet | Media Fund",
    page_icon="✝️",
    layout="centered"
)

# ---------------- DATABASE ----------------
def init_db():
    with sqlite3.connect(DB_FILE) as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS commitments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount INTEGER NOT NULL,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)

def add_commitment(amount, name, phone):
    with sqlite3.connect(DB_FILE) as con:
        con.execute(
            """INSERT INTO commitments
            (amount, name, phone, created_at)
            VALUES (?, ?, ?, ?)""",
            (
                amount,
                name.strip(),
                phone.strip(),
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
        )

def get_commitments():
    with sqlite3.connect(DB_FILE) as con:
        return pd.read_sql_query(
            """SELECT id, amount, name, phone, created_at
            FROM commitments ORDER BY id DESC""",
            con
        )

init_db()

# ---------------- LANGUAGE ----------------
EN = {
    "heading": "CBC Deshaipet, Warangal, Telangana",
    "sub": "Projector & Media Fund Raising",
    "amount": "My commitment (₹)",
    "name": "Name or family name",
    "phone": "Phone number",
    "submit": "✨ Submit my commitment",
    "thank": "Thank you for your generous commitment! We will contact you shortly to collect your donation.",
    "progress": "Commitment progress",
    "admin": "Administration",
    "admin_title": "Commitment records",
    "password": "Administration password",
    "login": "Unlock administration",
    "total": "Total commitments",
    "count": "People committed",
    "fields_error": "Please enter your name and phone number.",
    "min_error": "Please enter ₹10 or more.",
    "admin_note": "Private administration area."
}

TE = {
    "heading": "CBC దేశాయిపేట, వరంగల్, తెలంగాణ",
    "sub": "ప్రొజెక్టర్ & మీడియా నిధుల సమీకరణ",
    "amount": "నా వాగ్దానం (₹)",
    "name": "పేరు లేదా కుటుంబం పేరు",
    "phone": "ఫోన్ నంబర్",
    "submit": "✨ నా వాగ్దానాన్ని నమోదు చేయండి",
    "thank": "మీ ఉదారమైన వాగ్దానానికి ధన్యవాదాలు! మీ విరాళాన్ని స్వీకరించడానికి త్వరలో మిమ్మల్ని సంప్రదిస్తాము.",
    "progress": "వాగ్దానాల పురోగతి",
    "admin": "నిర్వాహకులు",
    "admin_title": "వాగ్దానాల వివరాలు",
    "password": "అడ్మిన్ పాస్‌వర్డ్",
    "login": "నిర్వాహక విభాగంలోకి ప్రవేశించండి",
    "total": "మొత్తం వాగ్దానాలు",
    "count": "వాగ్దానాలు చేసిన వారు",
    "fields_error": "దయచేసి పేరు మరియు ఫోన్ నంబర్ నమోదు చేయండి.",
    "min_error": "దయచేసి ₹10 లేదా అంతకంటే ఎక్కువ నమోదు చేయండి.",
    "admin_note": "నిర్వాహకులకు మాత్రమే."
}

language = st.selectbox(
    "Language / భాష",
    ["English", "తెలుగు"],
    index=0
)

T = EN if language == "English" else TE

# ---------------- DESIGN ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(
        155deg, #fffaf0, #f5ead5 58%, #fff7ed
    );
    color: #47311e;
}

.block-container {
    max-width: 720px;
    padding-top: 1.5rem;
}

h1, h2, h3 {
    color: #67462b !important;
}

[data-testid="stForm"] {
    background: #fffefa;
    border: 1px solid #e7d5b6;
    border-radius: 22px;
    padding: 22px;
    box-shadow: 0 8px 28px #6b482010;
}

div[data-testid="stMetric"] {
    background: #fffefa;
    border: 1px solid #e7d5b6;
    border-radius: 15px;
    padding: 14px;
}

div[data-testid="stProgressBar"] > div > div {
    background: linear-gradient(90deg, #c99b43, #80602d);
}

.stButton button {
    border-radius: 14px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown(
    "<div style='text-align:center;font-size:30px;color:#c19a50'>"
    "✝　🕊　✝</div>",
    unsafe_allow_html=True
)

st.markdown(
    f"<h1 style='text-align:center;font-size:30px'>{T['heading']}</h1>",
    unsafe_allow_html=True
)

st.markdown(
    f"<h3 style='text-align:center'>{T['sub']}</h3>",
    unsafe_allow_html=True
)

# ---------------- PROGRESS ----------------
df = get_commitments()

total = int(df["amount"].sum()) if not df.empty else 0

percentage = min(total / TARGET, 1.0)

st.markdown(f"**{T['progress']}**")

# Display percentage only. No rupee amount.
st.progress(percentage)

st.markdown(
    f"""<div style="
    text-align:center;
    font-size:19px;
    font-weight:650;
    color:#75532e;
    margin-top:-6px">
    {percentage * 100:.1f}% Completed
    </div>""",
    unsafe_allow_html=True
)

# ---------------- COMMITMENT FORM ----------------
with st.form("commitment_form", clear_on_submit=True):

    amount = st.number_input(
        T["amount"],
        min_value=10,
        step=10,
        value=100
    )

    name = st.text_input(
        T["name"],
        max_chars=120
    )

    phone = st.text_input(
        T["phone"],
        max_chars=30
    )

    submitted = st.form_submit_button(
        T["submit"],
        use_container_width=True
    )

if submitted:

    if not name.strip() or not phone.strip():
        st.error(T["fields_error"])

    elif amount < 10:
        st.error(T["min_error"])

    else:
        add_commitment(
            int(amount),
            name,
            phone
        )

        st.success(T["thank"])

        # Celebration effects
        st.balloons()
        st.snow()

        st.rerun()

# ---------------- FOOTER ----------------
st.markdown(
    """<div style="
    text-align:center;
    color:#9b805e;
    font-size:13px;
    margin:22px 0">
    Together in faith · Together in service
    </div>""",
    unsafe_allow_html=True
)

# ---------------- ADMIN ----------------
with st.expander(f"🔐 {T['admin']}", expanded=False):

    st.caption(T["admin_note"])

    password = st.text_input(
        T["password"],
        type="password",
        key="admin_password"
    )

    if st.button(T["login"], key="admin_unlock"):

        st.session_state.admin_unlocked = (
            password == ADMIN_PASSWORD
        )

        if not st.session_state.admin_unlocked:
            st.error("Incorrect password.")

    if st.session_state.get("admin_unlocked", False):

        st.subheader(T["admin_title"])

        current = get_commitments()

        sum_now = (
            int(current["amount"].sum())
            if not current.empty else 0
        )

        st.metric(T["total"], f"₹{sum_now:,.0f}")

        st.metric(T["count"], len(current))

        if not current.empty:

            view = current.rename(columns={
                "id": "ID",
                "amount": "Amount (₹)",
                "name": "Name / Family",
                "phone": "Phone",
                "created_at": "Date & time"
            })

            st.dataframe(
                view,
                use_container_width=True,
                hide_index=True
            )

            st.download_button(
                "Download CSV",
                current.to_csv(index=False).encode("utf-8"),
                file_name="cbc_commitments.csv",
                mime="text/csv"
            )

        else:
            st.info("No commitments yet.")
