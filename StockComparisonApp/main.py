import streamlit as st
import yfinance as yf
import numpy as np
from datetime import datetime


#Τίτλος της Εφαρμογής
st.title('Enhanced Stock Comparison Tool')

#Sidebar για εισαγωγή δεδομένων
st.sidebar.header('Επιλογές Σύγκρισης Μετοχών')
ticker1 = st.sidebar.text_input('Πληκτρολόγησε το πρώτο χρηματιστηριακό σύμβολο', 'AAPL')
ticker2 = st.sidebar.text_input('Πληκτρολόγησε το δεύτερο χρηματιστηριακό σύμβολο', 'MSFT')
start_date = st.sidebar.date_input('Επιλογή ημερομηνίας έναρξης', datetime(2023, 1,1))
end_date = st.sidebar.date_input('Επιλογή ημερομηνίας λήξης', datetime.today())

#Tabs για την οργάνωση της διεπαφής
tab1,tab2 = st.tabs(["Δεδομένα Μετοχών", "Χρηματοοικονομική Ανάλυση", ])

#Φόρτωση των δεδομένων με τη χρήση yfinance
if st.sidebar.button('Φόρτωση και σύγκριση μετοχών'):
    #Κατέβασμα δεδομένων για τις μετοχές
    stock1_data = yf.download(ticker1, start=start_date, end=end_date)
    stock2_data = yf.download(ticker2, start=start_date, end=end_date)

    # TAB 1: Δεδομένα Μετοχών
    with tab1:
        st.subheader(f"Δεδομένα για {ticker1}")
        st.line_chart(stock1_data['Close'])
        st.write(f"Υψηλό: {stock1_data['High'].max()}, Χαμηλό: {stock1_data['Low'].min()}, Όγκος: {stock1_data['Volume'].sum()}")

        st.subheader(f"Δεδομένα για {ticker2}")
        st.line_chart(stock2_data['Close'])
        st.write(f"Υψηλό: {stock2_data['High'].max()}, Χαμηλό: {stock2_data['Low'].min()}, Όγκος: {stock2_data['Volume'].sum()}")

    # TAB 2: Χρηματοοικονομική Ανάλυση
    with tab2:
        st.subheader('Χρηματοοικονομική Ανάλυση')

        # Υπολογισμός 50-day και 200-day moving averages για τις δύο μετοχές
        stock1_data['50_day_MA'] = stock1_data['Close'].rolling(window=50).mean()
        stock1_data['200_day_MA'] = stock1_data['Close'].rolling(window=200).mean()
        stock2_data['50_day_MA'] = stock2_data['Close'].rolling(window=50).mean()
        stock2_data['200_day_MA'] = stock2_data['Close'].rolling(window=200).mean()

        # Υπολογισμός της μεταβλητότητας (τυπική απόκλιση) των αποδόσεων
        stock1_data['Daily_Returns'] = stock1_data['Close'].pct_change()
        stock2_data['Daily_Returns'] = stock2_data['Close'].pct_change()

        stock1_volatility = stock1_data['Daily_Returns'].std() * np.sqrt(252)  # Annualized volatility
        stock2_volatility = stock2_data['Daily_Returns'].std() * np.sqrt(252)  # Annualized volatility

        # Εμφάνιση των κινητών μέσων όρων και της μεταβλητότητας
        st.write(f"**Κινητός μέσος όρος 50 ημερών για {ticker1}:** {stock1_data['50_day_MA'].iloc[-1]:.2f}")
        st.write(f"**Κινητός μέσος όρος 200 ημερών για {ticker1}:** {stock1_data['200_day_MA'].iloc[-1]:.2f}")
        st.write(f"**Μεταβλητότητα {ticker1} (annualized):** {stock1_volatility:.2f}")

        st.write(f"**Κινητός μέσος όρος 50 ημερών για {ticker2}:** {stock2_data['50_day_MA'].iloc[-1]:.2f}")
        st.write(f"**Κινητός μέσος όρος 200 ημερών για {ticker2}:** {stock2_data['200_day_MA'].iloc[-1]:.2f}")
        st.write(f"**Μεταβλητότητα {ticker2} (annualized):** {stock2_volatility:.2f}")

        # Προαιρετικά: Μπορείς να προσθέσεις και τα γραφήματα αυτών των δεδομένων χρησιμοποιώντας st.line_chart()
        st.line_chart(stock1_data[['Close', '50_day_MA', '200_day_MA']])
        st.line_chart(stock2_data[['Close', '50_day_MA', '200_day_MA']])


# Σχετικά με την εφαρμογή
st.sidebar.write("### Σχετικά με αυτή την εφαρμογή")
st.sidebar.write("""
Αυτή η εφαρμογή παρέχει σύγκριση μετοχών, χρησιμοποιώντας δεδομένα από την Yahoo Finance.
""")

