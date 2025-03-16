import re
import streamlit as st
import random
import string 
import pyperclip

st.set_page_config(page_title="Password Strength Meter",page_icon="🔑",layout="centered")

st.title('🛡️🔑 **Secure Password Strength Meter**')

st.write("Generate a secure password and check its strength instantly.")  

st.write("----") 

def password_generator(lenght):
    characters = string.ascii_letters + string.digits + "!@#$%^&*()-_=+[]{}|;:,.<>?/~`"
    return ''.join(random.choice(characters) for _ in range(lenght))


st.markdown("""
    <style>
        .stTextInput>div>div>input {text-align: center;}
        p {text-align: center;}  
         h1 {color: #3498db; text-align: center;}
        .stButton>button {background-color: #3498db ; color:white; width: 100%; border-radius: 10px;}
    </style>
""", unsafe_allow_html=True)


length = st.slider('Select Password Length', min_value=8, max_value=32, value=12)

# Initialize session state variables
if "password" not in st.session_state:
    st.session_state.password = None
if "copied" not in st.session_state:
    st.session_state.copied = False  # Track if the password is copied

# Generate Password button
if st.button('Generate Password'):
    st.session_state.password = password_generator(length)  # Store generated password
    st.session_state.copied = False  # Reset copy state when generating a new password
    st.success(f'Generated Password: {st.session_state.password}')

# Show "Copy to Clipboard" button only if a password is generated and not copied
if st.session_state.password and not st.session_state.copied:
    if st.button('Copy to Clipboard'):
        pyperclip.copy(st.session_state.password)  # Copy existing password
        st.session_state.copied = True  # Mark as copied
        st.rerun()  # Correct method to refresh the UI and remove the button


def check_password_strength(password):
    score = 0
    
    common_passwords = ["password", "123456", "qwerty", "abc123", "12345678", "123456789",]

    if password.lower() in common_passwords:
        return "❌ Avoid using common passwords."
    
    # Length Check
    if len(password) >= 8:
        score += 1
    else:
        return "❌ Password should be at least 8 characters long."
    
    # Upper & Lowercase Check
    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score += 1
    else:
        return "❌ Include both uppercase and lowercase letters."
    
    # Digit Check
    if re.search(r"\d", password): # \d for digits = [0-9]
        score += 1
    else:
        return "❌ Add at least one number (0-9)."
    
    # Special Character Check
    if re.search(r"[!@#$%^&*]", password): # r for raw string
        score += 1
    else:
        return "❌ Include at least one special character (!@#$%^&*)."
    
    # Strength Rating
    if score == 4:
        return "✅ Strong Password!"
    elif score == 3:
        return  "⚠️ Moderate Password - Consider adding more security features."
    else:
        return "❌ Weak Password - Improve it using the suggestions above."

# Get user input
password = st.text_input("Enter your password: ",type="password")

if st.button("Check Password Strength"):
    if password:
        result = check_password_strength(password)
        if result:
           st.write(result)
        elif result == "Strong":
            st.success(result) 
            st.balloons() # Display balloons
        elif result == "Moderate":
            st.warning(result)
            st.error("Weak Password - Improve it using these tips:")
            for tip in result.split("\n"):
                st.write(tip)
    else:
        st.warning("Please enter a password.")


st.write("-----")

st.markdown("""
    <div style='text-align: center; color: #777; font-size: 14px;'>
        <p>Developed with ❤️ by <a style='text-decoration: none;' href='https://github.com/Muhammad-Fraooq'>Muhammad Farooq</a> | © 2025</p>
    </div>
""", unsafe_allow_html=True)