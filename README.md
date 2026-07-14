# Python Banking System

A simple banking application built with Python and Streamlit. It lets users create an account, deposit funds, withdraw funds, view account details, update personal information, and close an account.

## Features

- Create a new bank account
- Deposit money securely
- Withdraw money with balance checks
- View account details
- Update name, email, or PIN
- Delete an account after confirmation
- Data is stored locally in JSON format

## Project Structure

- `app.py` - Streamlit web interface
- `bank.py` - Core banking logic and JSON data handling
- `data.json` - Persistent account data storage

## How to Run

1. Install the required dependencies:
   ```bash
   pip install streamlit
   ```
2. Start the app:
   ```bash
   streamlit run app.py
   ```

## Notes

This project is a beginner-friendly example of combining a Python backend with a simple interactive front end. It is useful for learning about form handling, state management, file-based storage, and basic banking workflows.

