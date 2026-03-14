import streamlit as st
import json
import os
from datetime import datetime, timedelta

DATA_FILE = "reminders.json"
CATEGORIES = ["учёба", "экзамены", "личное", "прочее"]

@st.cache_data(ttl=60)
def load_reminders():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

def save_reminders(reminders):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(reminders, f, ensure_ascii=False, indent=2)

st.set_page_config(page_title="Студенческая Напоминалка", layout="wide")
st.title("📚 Студенческая Напоминалка")
st.markdown("---")

# Боковая панель с фильтром
st.sidebar.header("🔍 Фильтр")
filter_cat = st.sidebar.selectbox("Категория:", ["Все"] + CATEGORIES)

# Форма добавления напоминания
st.header("➕ Добавить напоминание")
col1, col2 = st.columns(2)
with col1:
    text = st.text_input("Задача:", placeholder="Например: Выучить HSK 4")
with col2:
    date_str = st.text_input("Дата/время:", "2026-03-14 20:30", 
                           placeholder="ГГГГ-ММ-ДД ЧЧ:ММ")

col3, col4, col5 = st.columns(3)
with col3:
    category = st.selectbox("Категория:", CATEGORIES, key="add_cat")
with col4:
    repeat = st.selectbox("Повтор:", ["none", "daily", "weekly"], key="add_repeat")
with col5:
    if st.button("➕ Добавить", use_container_width=True):
        if text and date_str:
            try:
                dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
                reminders = load_reminders()
                reminder = {
                    "id": len(reminders) + 1,
                    "text": text,
                    "datetime": dt.strftime("%Y-%m-%d %H:%M"),
                    "category": category,
                    "repeat": repeat,
                    "done": False
                }
                reminders.append(reminder)
                save_reminders(reminders)
                st.success("✅ Напоминание добавлено!")
                st.rerun()
            except ValueError:
                st.error("❌ Неверный формат даты: ГГГГ-ММ-ДД ЧЧ:ММ")
        else:
            st.warning("⚠️ Заполните задачу и дату!")

# Список напоминаний
st.header("📋 Ваши напоминания")
reminders = load_reminders()
filtered_reminders = [r for r in reminders if filter_cat == "Все" or r["category"] == filter_cat]

if not filtered_reminders:
    st.info("😊 Напоминаний пока нет. Добавьте первое!")
else:
    for r in sorted(filtered_reminders, key=lambda x: x["datetime"]):
        with st.container():
            col1, col2, col3, col4 = st.columns([1, 5, 2, 1])
            
            with col1:
                r["done"] = st.checkbox("✓", value=r["done"], 
                                      key=f"done_{r['id']}", 
                                      on_change=lambda id=r['id']: toggle_done(id))
            
            with col2:
                status = "✅" if r["done"] else "⏳"
                repeat_icon = {"daily": "🔄", "weekly": "📅", "none": ""}[r["repeat"]]
                st.markdown(f"**{status} {r['datetime']}** {repeat_icon} **[{r['category'].title()}]** {r['text']}")
            
            with col3:
                st.caption(f"Повтор: {r['repeat']}")
            
            with col4:
                if st.button("🗑️", key=f"del_{r['id']}"):
                    new_reminders = [rem for rem in reminders if rem["id"] != r["id"]]
                    save_reminders(new_reminders)
                    st.rerun()

def toggle_done(reminder_id):
    reminders = load_reminders()
    for r in reminders:
        if r["id"] == reminder_id:
            r["done"] = not r["done"]
            save_reminders(reminders)
            st.rerun()
