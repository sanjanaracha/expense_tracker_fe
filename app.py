import streamlit as st
import requests
import pandas as pd
# import plotly.express as px

BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Expense Tracker", layout="wide")
st.title("Expense Tracker Dashboard")

menu = st.sidebar.selectbox(
    "Choose Option",
    [
        "Add Expense",
        "View Expenses",
        "Update Expense",
        "Delete Expense",
        "Search Expense",
        "Sort Expenses",
        "Analytics",
        "Export CSV"
    ]
)

if menu == "Add Expense":
    st.subheader("Add Expense")

    title = st.text_input("Title")
    amount = st.number_input("Amount", min_value=0.0)
    category = st.selectbox(
        "Category",
        ["Food", "Travel", "Shopping", "Bills", "Health", "Other"]
    )

    if st.button("Add"):
        payload = {
            "title": title,
            "amount": amount,
            "category": category
        }

        res = requests.post(f"{BASE_URL}/expenses", json=payload)

        if res.status_code == 200:
            st.success("Expense Added Successfully")

elif menu == "View Expenses":
    st.subheader("All Expenses")

    res = requests.get(f"{BASE_URL}/expenses")

    if res.status_code == 200:
        data = res.json()
        df = pd.DataFrame(data)
        st.dataframe(df)

elif menu == "Update Expense":
    st.subheader("Update Expense")

    expense_id = st.number_input("Expense ID", min_value=1)
    title = st.text_input("New Title")
    amount = st.number_input("New Amount", min_value=0.0)
    category = st.selectbox(
        "New Category",
        ["Food", "Travel", "Shopping", "Bills", "Health", "Other"]
    )

    if st.button("Update"):
        payload = {
            "title": title,
            "amount": amount,
            "category": category
        }

        res = requests.put(f"{BASE_URL}/expenses/{expense_id}", json=payload)

        if res.status_code == 200:
            st.success("Expense Updated")

elif menu == "Delete Expense":
    st.subheader("Delete Expense")

    expense_id = st.number_input("Expense ID", min_value=1)

    if st.button("Delete"):
        res = requests.delete(f"{BASE_URL}/expenses/{expense_id}")

        if res.status_code == 200:
            st.success("Expense Deleted")

elif menu == "Search Expense":
    st.subheader("Search by Category")

    category = st.selectbox(
        "Category",
        ["Food", "Travel", "Shopping", "Bills", "Health", "Other"]
    )

    if st.button("Search"):
        res = requests.get(f"{BASE_URL}/search?category={category}")

        if res.status_code == 200:
            df = pd.DataFrame(res.json())
            st.dataframe(df)

elif menu == "Sort Expenses":
    st.subheader("Sort Expenses")

    sort = st.selectbox(
        "Sort By",
        ["date_desc", "date_asc", "price_desc", "price_asc"]
    )

    if st.button("Sort"):
        res = requests.get(f"{BASE_URL}/sort?sort_by={sort}")

        if res.status_code == 200:
            df = pd.DataFrame(res.json())
            st.dataframe(df)

# elif menu == "Analytics":
#     st.subheader("Expense Analytics")

#     res = requests.get(f"{BASE_URL}/category-summary")

#     if res.status_code == 200:
#         data = res.json()
#         df = pd.DataFrame(data)

#         pie = px.pie(df, names="category", values="total")
#         st.plotly_chart(pie)

#     res2 = requests.get(f"{BASE_URL}/monthly-summary")

#     if res2.status_code == 200:
#         data2 = res2.json()
#         df2 = pd.DataFrame(data2)

#         bar = px.bar(df2, x="month", y="total")
#         st.plotly_chart(bar)

# elif menu == "Export CSV":
#     st.subheader("Export Expenses")

#     if st.button("Download CSV"):
#         res = requests.get(f"{BASE_URL}/export")

#         with open("expenses.csv", "wb") as f:
#             f.write(res.content)

#         st.success("CSV Downloaded")