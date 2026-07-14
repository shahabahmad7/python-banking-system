"""
Streamlit front-end for bank.py.
Run with:  streamlit run app.py
"""

import streamlit as st
from bank import Bank

st.set_page_config(
    page_title="Ledger & Vault Bank",
    page_icon="🏦",
    layout="centered",
    initial_sidebar_state="expanded",
)

bank = Bank()

# --------------------------------------------------------------------------- #
# THEME  ---  "Ledger & Vault": deep ink background, brass accent, serif
# headers reminiscent of an old bank ledger, monospace for account numbers
# and money amounts (like figures stamped in a passbook).
# --------------------------------------------------------------------------- #
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500;700&display=swap');

    :root {
        --ink: #0E1A2B;
        --surface: #152A42;
        --surface2: #17273D;
        --brass: #C9A227;
        --brass-soft: #E8C766;
        --text: #ECEFF3;
        --muted: #93A1B4;
        --good: #4FAE7E;
        --bad: #D9706C;
        --line: #26374E;
    }

    .stApp {
        background: radial-gradient(circle at 20% -10%, #16283E 0%, var(--ink) 55%);
        color: var(--text);
        font-family: 'Inter', sans-serif;
    }

    section[data-testid="stSidebar"] {
        background: #0B1420;
        border-right: 1px solid var(--line);
    }
    section[data-testid="stSidebar"] * { color: var(--text) !important; }

    h1, h2, h3 {
        font-family: 'Fraunces', serif !important;
        color: var(--brass-soft) !important;
        letter-spacing: 0.2px;
    }

    .ledger-title {
        font-family: 'Fraunces', serif;
        font-weight: 600;
        font-size: 2.1rem;
        color: var(--brass-soft);
        border-bottom: 1px solid var(--line);
        padding-bottom: 0.5rem;
        margin-bottom: 0.25rem;
    }
    .ledger-sub {
        color: var(--muted);
        font-size: 0.95rem;
        margin-bottom: 1.5rem;
    }

    /* card wrapper for content blocks */
    .vault-card {
        background: var(--surface2);
        border: 1px solid var(--line);
        border-radius: 6px;
        padding: 1.4rem 1.5rem;
        margin-bottom: 1.2rem;
    }

    /* stamped account-number badge, the signature element */
    .stamp {
        display: inline-block;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 700;
        font-size: 1.15rem;
        letter-spacing: 2px;
        color: var(--ink);
        background: var(--brass);
        padding: 0.35rem 0.9rem;
        border-radius: 3px;
        border: 1.5px dashed #8A6D14;
        transform: rotate(-1.2deg);
    }

    .figure {
        font-family: 'JetBrains Mono', monospace;
        font-weight: 700;
    }

    .balance-good { color: var(--good); }
    .balance-bad { color: var(--bad); }

    /* inputs */
    .stTextInput input, .stNumberInput input {
        background: var(--surface) !important;
        color: var(--text) !important;
        border: 1px solid var(--line) !important;
        border-radius: 4px !important;
        font-family: 'JetBrains Mono', monospace;
    }
    label, .stMarkdown p { color: var(--text) !important; }

    /* buttons */
    .stButton button, .stFormSubmitButton button {
        background: var(--brass) !important;
        color: var(--ink) !important;
        border: none !important;
        border-radius: 4px !important;
        font-weight: 600 !important;
        font-family: 'Inter', sans-serif !important;
        padding: 0.5rem 1.2rem !important;
        transition: transform 0.08s ease, background 0.15s ease;
    }
    .stButton button:hover, .stFormSubmitButton button:hover {
        background: var(--brass-soft) !important;
        transform: translateY(-1px);
    }

    hr { border-color: var(--line) !important; }

    /* success / error boxes */
    div[data-testid="stAlert"] {
        border-radius: 5px;
        font-family: 'Inter', sans-serif;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------------------------------- #
# SIDEBAR NAVIGATION
# --------------------------------------------------------------------------- #
st.sidebar.markdown("## 🏦 Ledger & Vault")
st.sidebar.caption("A small, honest bank ledger.")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigate",
    [
        "Open an Account",
        "Deposit",
        "Withdraw",
        "Account Details",
        "Update Details",
        "Close Account",
    ],
    label_visibility="collapsed",
)

st.sidebar.markdown("---")
st.sidebar.caption(f"Accounts on file: **{len(Bank.data)}**")

# --------------------------------------------------------------------------- #
# PAGE: OPEN AN ACCOUNT
# --------------------------------------------------------------------------- #
if page == "Open an Account":
    st.markdown('<div class="ledger-title">Open an Account</div>', unsafe_allow_html=True)
    st.markdown('<div class="ledger-sub">Fill in the ledger to open a new account.</div>', unsafe_allow_html=True)

    with st.form("create_form", clear_on_submit=False):
        name = st.text_input("Full name")
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("Age", min_value=0, max_value=120, step=1, value=18)
        with col2:
            pin = st.text_input("Choose a 4-digit PIN", max_chars=4, type="password")
        email = st.text_input("Email")
        submitted = st.form_submit_button("Create account")

    if submitted:
        success, message, info = bank.create_account(name, age, email, pin)
        if success:
            st.success(message)
            st.markdown('<div class="vault-card">', unsafe_allow_html=True)
            st.markdown("**Your account number** (write this down — you'll need it for every transaction):")
            st.markdown(f'<span class="stamp">{info["accountNo"]}</span>', unsafe_allow_html=True)
            st.markdown(
                f"""
                <br><br>
                <span class="figure">Name:&nbsp;&nbsp;&nbsp;&nbsp;{info['name']}</span><br>
                <span class="figure">Email:&nbsp;&nbsp;&nbsp;&nbsp;{info['email']}</span><br>
                <span class="figure">Balance:&nbsp;{info['balance']}</span>
                """,
                unsafe_allow_html=True,
            )
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.error(message)

# --------------------------------------------------------------------------- #
# PAGE: DEPOSIT
# --------------------------------------------------------------------------- #
elif page == "Deposit":
    st.markdown('<div class="ledger-title">Deposit Funds</div>', unsafe_allow_html=True)
    st.markdown('<div class="ledger-sub">Between 1 and 10,000 per transaction.</div>', unsafe_allow_html=True)

    with st.form("deposit_form"):
        acc_no = st.text_input("Account number")
        pin = st.text_input("PIN", max_chars=4, type="password")
        amount = st.number_input("Amount to deposit", min_value=0, step=1)
        submitted = st.form_submit_button("Deposit")

    if submitted:
        success, message, balance = bank.deposit(acc_no, pin, amount)
        if success:
            st.success(message)
            st.markdown(
                f'<div class="vault-card">New balance: '
                f'<span class="figure balance-good">{balance}</span></div>',
                unsafe_allow_html=True,
            )
        else:
            st.error(message)

# --------------------------------------------------------------------------- #
# PAGE: WITHDRAW
# --------------------------------------------------------------------------- #
elif page == "Withdraw":
    st.markdown('<div class="ledger-title">Withdraw Funds</div>', unsafe_allow_html=True)
    st.markdown('<div class="ledger-sub">You can only withdraw what you have.</div>', unsafe_allow_html=True)

    with st.form("withdraw_form"):
        acc_no = st.text_input("Account number")
        pin = st.text_input("PIN", max_chars=4, type="password")
        amount = st.number_input("Amount to withdraw", min_value=0, step=1)
        submitted = st.form_submit_button("Withdraw")

    if submitted:
        success, message, balance = bank.withdraw(acc_no, pin, amount)
        if success:
            st.success(message)
            st.markdown(
                f'<div class="vault-card">New balance: '
                f'<span class="figure balance-good">{balance}</span></div>',
                unsafe_allow_html=True,
            )
        else:
            st.error(message)

# --------------------------------------------------------------------------- #
# PAGE: ACCOUNT DETAILS
# --------------------------------------------------------------------------- #
elif page == "Account Details":
    st.markdown('<div class="ledger-title">Account Details</div>', unsafe_allow_html=True)
    st.markdown('<div class="ledger-sub">Look up everything on file for your account.</div>', unsafe_allow_html=True)

    with st.form("details_form"):
        acc_no = st.text_input("Account number")
        pin = st.text_input("PIN", max_chars=4, type="password")
        submitted = st.form_submit_button("Show details")

    if submitted:
        success, message, info = bank.get_details(acc_no, pin)
        if success:
            st.success(message)
            st.markdown('<div class="vault-card">', unsafe_allow_html=True)
            st.markdown(f'<span class="stamp">{info["accountNo"]}</span>', unsafe_allow_html=True)
            st.markdown(
                f"""
                <br><br>
                <span class="figure">Name:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{info['name']}</span><br>
                <span class="figure">Age:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{info['age']}</span><br>
                <span class="figure">Email:&nbsp;&nbsp;&nbsp;&nbsp;{info['email']}</span><br>
                <span class="figure">Balance:&nbsp;&nbsp;{info['balance']}</span>
                """,
                unsafe_allow_html=True,
            )
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.error(message)

# --------------------------------------------------------------------------- #
# PAGE: UPDATE DETAILS
# --------------------------------------------------------------------------- #
elif page == "Update Details":
    st.markdown('<div class="ledger-title">Update Details</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="ledger-sub">Age, account number, and balance can\'t be changed. '
        'Leave a field blank to keep it as-is.</div>',
        unsafe_allow_html=True,
    )

    with st.form("update_form"):
        acc_no = st.text_input("Account number")
        pin = st.text_input("Current PIN", max_chars=4, type="password")
        st.markdown("—")
        new_name = st.text_input("New name (optional)")
        new_email = st.text_input("New email (optional)")
        new_pin = st.text_input("New 4-digit PIN (optional)", max_chars=4, type="password")
        submitted = st.form_submit_button("Update")

    if submitted:
        success, message, info = bank.update_details(
            acc_no, pin, name=new_name, email=new_email, new_pin=new_pin
        )
        if success:
            st.success(message)
            st.markdown('<div class="vault-card">', unsafe_allow_html=True)
            st.markdown(
                f"""
                <span class="figure">Name:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{info['name']}</span><br>
                <span class="figure">Email:&nbsp;&nbsp;&nbsp;&nbsp;{info['email']}</span><br>
                <span class="figure">PIN:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;****</span>
                """,
                unsafe_allow_html=True,
            )
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.error(message)

# --------------------------------------------------------------------------- #
# PAGE: CLOSE ACCOUNT
# --------------------------------------------------------------------------- #
elif page == "Close Account":
    st.markdown('<div class="ledger-title">Close Account</div>', unsafe_allow_html=True)
    st.markdown('<div class="ledger-sub">This cannot be undone.</div>', unsafe_allow_html=True)

    with st.form("delete_form"):
        acc_no = st.text_input("Account number")
        pin = st.text_input("PIN", max_chars=4, type="password")
        confirm = st.checkbox("I understand this will permanently delete my account.")
        submitted = st.form_submit_button("Delete account")

    if submitted:
        if not confirm:
            st.warning("Please tick the confirmation box to proceed.")
        else:
            success, message, _ = bank.delete_account(acc_no, pin, confirm=True)
            if success:
                st.success(message)
            else:
                st.error(message)