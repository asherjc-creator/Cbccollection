import sqlite3
from datetime import datetime
import pandas as pd
import streamlit as st

# ---------------- CONFIG ----------------
TARGET = 100000
DB_FILE = "cbc_projector_commitments.db"
ADMIN_PASSWORD = "cbc654&"

st.set_page_config(
    page_title="CBC Deshaipet | Media Fund",
    page_icon="✝️",
    layout="centered",
)

# ---------------- DATABASE ----------------
def init_db():
    with sqlite3.connect(DB_FILE) as con:
        con.execute(
            """
            CREATE TABLE IF NOT EXISTS commitments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount INTEGER NOT NULL,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )


def add_commitment(amount: int, name: str, phone: str):
    with sqlite3.connect(DB_FILE) as con:
        con.execute(
            """
            INSERT INTO commitments (amount, name, phone, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (
                amount,
                name.strip(),
                phone.strip(),
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            ),
        )


def get_commitments() -> pd.DataFrame:
    with sqlite3.connect(DB_FILE) as con:
        return pd.read_sql_query(
            """
            SELECT id, amount, name, phone, created_at
            FROM commitments
            ORDER BY id DESC
            """,
            con,
        )


init_db()

# ---------------- LANGUAGE ----------------
TEXTS = {
    "తెలుగు": {
        "toggle_label": "భాష / Language",
        "heading": "CBC దేశాయిపేట, వరంగల్, తెలంగాణ",
        "sub": "ప్రొజెక్టర్ & మీడియా నిధుల సమీకరణ",
        "amount": "మొత్తం (₹)",
        "name": "పేరు లేదా కుటుంబం నుండి",
        "phone": "ఫోన్ నంబర్",
        "submit": "✨ నా వాగ్దానాన్ని సమర్పించండి",
        "thank": "మీ విరాళ వాగ్దానానికి ధన్యవాదాలు! మీ విరాళాన్ని సేకరించడానికి మేము త్వరలో మిమ్మల్ని సంప్రదిస్తాము.",
        "progress": "విరాళాల పురోగతి",
        "completed": "పూర్తయింది",
        "admin": "నిర్వాహకులు",
        "admin_title": "వాగ్దానాల జాబితా",
        "password": "అడ్మిన్ పాస్‌వర్డ్",
        "login": "ప్రవేశించండి",
        "close_admin": "మూసివేయండి",
        "wrong_pw": "సరికాని పాస్‌వర్డ్.",
        "total": "మొత్తం వాగ్దానాలు",
        "count": "వాగ్దానం చేసిన వారు",
        "no_data": "ఇంకా ఎటువంటి వాగ్దానాలు నమోదు కాలేదు.",
        "fields_error": "దయచేసి పేరు మరియు ఫోన్ నంబర్ నమోదు చేయండి.",
        "min_error": "దయచేసి చెల్లుబాటు అయ్యే మొత్తాన్ని (కనీసం ₹10) నమోదు చేయండి.",
        "admin_note": "నిర్వాహకులకు మాత్రమే పరిమితం.",
        "footer": "విశ్వాసంలో కలిసి · సేవలో కలిసి",
        "download": "CSV డౌన్‌లోడ్ చేయండి",
    },
    "English": {
        "toggle_label": "Language / భాష",
        "heading": "CBC Deshaipet, Warangal, Telangana",
        "sub": "Projector & Media Fund Raising",
        "amount": "Amount (₹)",
        "name": "Name or from family",
        "phone": "Phone",
        "submit": "✨ Submit my commitment",
        "thank": "Thank you for your donation commitment! We will contact you shortly to collect your donation.",
        "progress": "Donation progress",
        "completed": "Completed",
        "admin": "Administration",
        "admin_title": "Committed members",
        "password": "Administration password",
        "login": "Unlock",
        "close_admin": "Close",
        "wrong_pw": "Incorrect password.",
        "total": "Total commitments",
        "count": "People committed",
        "no_data": "No commitments yet.",
        "fields_error": "Please enter your name and phone number.",
        "min_error": "Please enter a valid amount of at least ₹10.",
        "admin_note": "Private administration area.",
        "footer": "Together in faith · Together in service",
        "download": "Download CSV",
    },
}

if "lang" not in st.session_state:
    st.session_state.lang = "తెలుగు"

if "just_committed" not in st.session_state:
    st.session_state.just_committed = False

if "admin_unlocked" not in st.session_state:
    st.session_state.admin_unlocked = False

if "show_admin_panel" not in st.session_state:
    st.session_state.show_admin_panel = False

# ---------------- DESIGN (WARM CHRISTIAN THEME) ----------------
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(155deg, #fffaf3 0%, #f6ead6 55%, #fff6ea 100%);
        color: #47311e;
    }

    .block-container {
        max-width: 720px;
        padding-top: 1.4rem;
        padding-bottom: 3rem;
    }

    h1, h2, h3 {
        color: #654328 !important;
    }

    .warm-card {
        background: rgba(255, 253, 249, 0.92);
        border: 1px solid #e6d2b1;
        border-radius: 22px;
        padding: 20px 22px;
        box-shadow: 0 10px 28px rgba(107, 72, 32, 0.08);
        margin-bottom: 18px;
    }

    [data-testid="stForm"] {
        background: #fffdf9;
        border: 1px solid #e6d2b1;
        border-radius: 22px;
        padding: 24px;
        box-shadow: 0 10px 28px rgba(107, 72, 32, 0.08);
    }

    div[data-testid="stMetric"] {
        background: #fffdf9;
        border: 1px solid #e6d2b1;
        border-radius: 15px;
        padding: 14px;
    }

    div[data-testid="stProgressBar"] > div > div {
        background: linear-gradient(90deg, #d4a349, #866127);
    }

    .stButton > button, .stFormSubmitButton > button {
        border-radius: 13px;
        border: 1px solid #d7bc8e;
        background: linear-gradient(180deg, #fffaf0, #f3e2c3);
        color: #54371f;
        font-weight: 600;
    }

    .stButton > button:hover, .stFormSubmitButton > button:hover {
        border-color: #b88b3d;
        background: linear-gradient(180deg, #fff4de, #ead2a8);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------- LANGUAGE TOGGLE ----------------
top_left, top_right = st.columns([2.5, 1.5])
with top_right:
    selected_lang = st.selectbox(
        TEXTS[st.session_state.lang]["toggle_label"],
        ["తెలుగు", "English"],
        index=0 if st.session_state.lang == "తెలుగు" else 1,
        label_visibility="collapsed",
    )
    if selected_lang != st.session_state.lang:
        st.session_state.lang = selected_lang
        st.rerun()

T = TEXTS[st.session_state.lang]

# ---------------- HEADER ----------------
st.markdown(
    """
    <div class="warm-card" style="text-align:center;">
        <div style="font-size:28px;color:#b88b3d;letter-spacing:10px;margin-bottom:6px;">
            ✝ 🕊 ✝
        </div>
        <h1 style="margin:0;font-size:28px;line-height:1.3;">{heading}</h1>
        <h3 style="margin:8px 0 0 0;font-size:18px;font-weight:500;color:#7c5838 !important;">
            {sub}
        </h3>
    </div>
    """.format(heading=T["heading"], sub=T["sub"]),
    unsafe_allow_html=True,
)

# ---------------- POST-SUBMISSION CELEBRATION ----------------
if st.session_state.just_committed:
    st.success(f"✨ {T['thank']}")
    st.balloons()
    st.snow()
    st.session_state.just_committed = False

# ---------------- COMMITMENT FORM ----------------
with st.form("commitment_form", clear_on_submit=True):
    amount = st.number_input(
        T["amount"],
        step=10,
        value=100,
    )
    name = st.text_input(
        T["name"],
        max_chars=120,
    )
    phone = st.text_input(
        T["phone"],
        max_chars=30,
    )
    submitted = st.form_submit_button(
        T["submit"],
        use_container_width=True,
    )

if submitted:
    if not name.strip() or not phone.strip():
        st.error(T["fields_error"])
    elif amount is None or amount < 10:
        st.error(T["min_error"])
    else:
        add_commitment(int(amount), name, phone)
        st.session_state.just_committed = True
        st.rerun()

# ---------------- PROGRESS BAR AT BOTTOM ----------------
df = get_commitments()
total = int(df["amount"].sum()) if not df.empty else 0
percentage = min(total / TARGET, 1.0)

st.markdown(
    """
    <div class="warm-card" style="margin-top:18px;">
        <div style="font-weight:700;font-size:16px;color:#5e3f25;margin-bottom:8px;">
            {label}
        </div>
    """.format(label=T["progress"]),
    unsafe_allow_html=True,
)
st.progress(percentage)
st.markdown(
    """
        <div style="text-align:center;font-size:20px;font-weight:700;color:#785227;margin-top:6px;">
            {pct:.1f}% {done}
        </div>
    </div>
    """.format(pct=percentage * 100, done=T["completed"]),
    unsafe_allow_html=True,
)

# ---------------- FOOTER + BOTTOM-LEFT ADMIN BUTTON ----------------
st.markdown(
    """
    <div style="text-align:center;color:#8e704c;font-size:13px;margin:10px 0 18px 0;">
        {footer}
    </div>
    """.format(footer=T["footer"]),
    unsafe_allow_html=True,
)

bottom_left, _ = st.columns([1.4, 3.6])
with bottom_left:
    if st.button(f"🔐 {T['admin']}", key="bottom_left_admin_btn"):
        st.session_state.show_admin_panel = not st.session_state.show_admin_panel

# ---------------- PASSWORD-PROTECTED ADMIN VIEW ----------------
if st.session_state.show_admin_panel:
    st.markdown('<div class="warm-card">', unsafe_allow_html=True)
    st.subheader(f"🔐 {T['admin']}")
    st.caption(T["admin_note"])

    if not st.session_state.admin_unlocked:
        password = st.text_input(
            T["password"],
            type="password",
            key="admin_password_input",
        )
        col_unlock, col_close = st.columns([1, 1])
        with col_unlock:
            if st.button(T["login"], key="admin_login_btn", use_container_width=True):
                if password == ADMIN_PASSWORD:
                    st.session_state.admin_unlocked = True
                    st.rerun()
                else:
                    st.error(T["wrong_pw"])
        with col_close:
            if st.button(T["close_admin"], key="admin_close_locked_btn", use_container_width=True):
                st.session_state.show_admin_panel = False
                st.rerun()
    else:
        st.subheader(T["admin_title"])
        sum_now = int(df["amount"].sum()) if not df.empty else 0

        m1, m2 = st.columns(2)
        with m1:
            st.metric(T["total"], f"₹{sum_now:,.0f}")
        with m2:
            st.metric(T["count"], len(df))

        if not df.empty:
            view = df.rename(
                columns={
                    "id": "ID",
                    "amount": "Amount (₹)",
                    "name": "Name / Family",
                    "phone": "Phone",
                    "created_at": "Date & Time",
                }
            )
            st.dataframe(view, use_container_width=True, hide_index=True)

            st.download_button(
                T["download"],
                df.to_csv(index=False).encode("utf-8"),
                file_name="cbc_deshaipet_commitments.csv",
                mime="text/csv",
            )
        else:
            st.info(T["no_data"])

        if st.button(T["close_admin"], key="admin_close_unlocked_btn"):
            st.session_state.show_admin_panel = False
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
