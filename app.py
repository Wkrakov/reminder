import streamlit as st
import json
import os
from datetime import datetime, timedelta

# Инициализация session_state
if 'reminders' not in st.session_state:
    st.session_state.reminders = []
    # Загрузка при первом запуске
    DATA_FILE = "reminders.json"
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                st.session_state.reminders = json.load(f)
        except:
            st.session_state.reminders = []

def save_reminders():
    DATA_FILE = "reminders.json"
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(st.session_state.reminders, f, ensure_ascii=False, indent=2)

st.set_page_config(page_title="Студенческая Напоминалка", layout="wide")
st.title("📚 Студенческая Напоминалка")
st.markdown("---")

CATEGORIES = ["учёба", "экзамены", "личное", "прочее"]

# Боковая панель с фильтром
st.sidebar.header("🔍 Фильтр")
filter_cat = st.sidebar.selectbox("Категория:", ["Все"] + CATEGORIES)

# Форма добавления
st.header("➕ Добавить напоминание")
col1, col2 = st.columns(2)
with col1:
    text = st.text_input("Задача:", placeholder="Например: Выучить HSK 4")
with col2:
    date_str = st.text_input("Дата/время:", "2026-03-14 20:30")

col3, col4, col5 = st.columns(3)
with col3:
    category = st.selectbox("Категория:", CATEGORIES)
with col4:
    repeat = st.selectbox("Повтор:", ["none", "daily", "weekly"])
with col5:
    if st.button("➕ Добавить", use_container_width=True):
        if text and date_str:
            try:
                dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
                reminder = {
                    "id": len(st.session_state.reminders) + 1,
                    "text": text,
                    "datetime": dt.strftime("%Y-%m-%d %H:%M"),
                    "category": category,
                    "repeat": repeat,
                    "done": False
                }
                st.session_state.reminders.append(reminder)
                save_reminders()
                st.success("✅ Добавлено!")
                st.rerun()
            except ValueError:
                st.error("❌ Формат: ГГГГ-ММ-ДД ЧЧ:ММ")
        else:
            st.warning("⚠️ Заполните все поля!")

# ✅ ИСПРАВЛЕННЫЙ список с УДАЛЕНИЕМ
st.header("📋 Напоминания")
filtered_reminders = [r for r in st.session_state.reminders 
                     if filter_cat == "Все" or r["category"] == filter_cat]

if not filtered_reminders:
    st.info("😊 Нет напоминаний")
else:
    # Сортировка по дате
    filtered_reminders.sort(key=lambda x: x["datetime"])
    
    for i, r in enumerate(filtered_reminders):
        with st.container():
            col1, col2, col3, col4 = st.columns([1, 4, 2, 1])
            
            # ✅ Чекбокс выполненной задачи
            with col1:
                if st.checkbox("✓", key=f"done_{r['id']}", value=r["done"]):
                    for rem in st.session_state.reminders:
                        if rem["id"] == r["id"]:
                            rem["done"] = True
                    save_reminders()
                    st.rerun()
            
            # Текст напоминания
            with col2:
                status = "✅" if r["done"] else "⏳"
                repeat_icon = {"daily": "🔄", "weekly": "📅", "none": ""}[r["repeat"]]
                st.markdown(f"**{status} {r['datetime']}** {repeat_icon} **[{r['category'].title()}]** {r['text']}")
            
            with col3:
                st.caption(f"Повтор: {r['repeat']}")
            
            # ✅ КНОПКА УДАЛЕНИЯ — РАБОТАЕТ!
            with col4:
                if st.button("🗑️", key=f"delete_{r['id']}"):
                    st.session_state.reminders = [rem for rem in st.session_state.reminders if rem["id"] != r["id"]]
                    save_reminders()
                    st.success(f"🗑️ Удалено: {r['text']}")
                    st.rerun()

# Информация о количестве
st.sidebar.markdown(f"**Всего задач:** {len(st.session_state.reminders)}")
