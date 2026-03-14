import streamlit as st
import json
import os
from datetime import datetime, timedelta

# 🎨 Стили под твою цветовую гамму
st.markdown("""
    <style>
    .main .block-container {
        padding-top: 2rem;
        background: linear-gradient(135deg, #CCE5FF 0%, #E8EBFF 100%);
    }
    .stButton > button {
        background: linear-gradient(45deg, #949CFF, #7A85E0);
        color: white !important;
        border-radius: 12px;
        border: none;
        height: 42px;
        font-weight: bold;
        box-shadow: 0 4px 8px rgba(148, 156, 255, 0.3);
    }
    .stButton > button:hover {
        background: linear-gradient(45deg, #7A85E0, #949CFF);
        box-shadow: 0 6px 12px rgba(148, 156, 255, 0.4);
    }
    .stTextInput > div > div > input, 
    .stSelectbox > div > div > select,
    .stDateInput > div > div > input {
        border-radius: 12px !important;
        border: 2px solid #949CFF !important;
        background-color: #E8EBFF !important;
        color: #F2749B !important;
    }
    h1, h2, h3 {
        color: #F2749B !important;
        font-family: 'sans-serif' !important;
    }
    .stMarkdown {
        color: #F2749B !important;
    }
    .stSuccess {
        background-color: #E8EBFF;
        border-radius: 10px;
        border-left: 4px solid #949CFF;
    }
    </style>
""", unsafe_allow_html=True)

# Инициализация
if 'reminders' not in st.session_state:
    st.session_state.reminders = []
    DATA_FILE = "reminders.json"
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                st.session_state.reminders = json.load(f)
        except:
            pass

def save_reminders():
    DATA_FILE = "reminders.json"
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(st.session_state.reminders, f, ensure_ascii=False, indent=2)

st.set_page_config(page_title="Студенческая Напоминалка", layout="wide")

# 🎨 Заголовок с градиентом твоих цветов
st.markdown("""
    <div style='text-align: center; padding: 2rem;'>
        <h1 style='
            background: linear-gradient(90deg, #949CFF, #F2749B, #CCE5FF); 
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-size: 3rem;
            margin: 0;
        '>
        📚 Студенческая Напоминалка
        </h1>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")
CATEGORIES = ["учёба", "экзамены", "личное", "прочее"]

# Боковая панель
st.sidebar.title("🔍 Фильтр")
st.sidebar.markdown("─" * 30)
filter_cat = st.sidebar.selectbox("Категория:", ["Все"] + CATEGORIES)

# Форма добавления
st.header("➕ Добавить напоминание")
col1, col2 = st.columns(2)
with col1:
    text = st.text_input("📝 Задача:", placeholder="Например: Выучить HSK 4")
with col2:
    date_str = st.text_input("🕐 Дата/время:", "2026-03-14 20:30")

col3, col4, col5 = st.columns([1,1,1])
with col3:
    category = st.selectbox("🏷️ Категория:", CATEGORIES)
with col4:
    repeat = st.selectbox("🔁 Повтор:", ["none", "daily", "weekly"])
with col5:
    if st.button("➕ Добавить напоминание", use_container_width=True):
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
                st.success("✅ Напоминание добавлено!")
                st.rerun()
            except ValueError:
                st.error("❌ Формат даты: ГГГГ-ММ-ДД ЧЧ:ММ")
        else:
            st.warning("⚠️ Заполните задачу и дату!")

# Список напоминаний
st.header("📋 Ваши напоминания")
filtered_reminders = [r for r in st.session_state.reminders 
                     if filter_cat == "Все" or r["category"] == filter_cat]

if not filtered_reminders:
    st.info("😊 Пока нет напоминаний. Добавьте первое!")
else:
    filtered_reminders.sort(key=lambda x: x["datetime"])
    
    for r in filtered_reminders:
        with st.container():
            col1, col2, col3, col4 = st.columns([0.8, 4.5, 1.5, 0.8])
            
            with col1:
                if st.checkbox("✓", key=f"done_{r['id']}", value=r["done"]):
                    for rem in st.session_state.reminders:
                        if rem["id"] == r["id"]:
                            rem["done"] = True
                    save_reminders()
                    st.rerun()
            
            with col2:
                status = "✅ Выполнено" if r["done"] else "⏳ Ожидает"
                repeat_icon = {"daily": "🔄", "weekly": "📅", "none": "📌"}[r["repeat"]]
                st.markdown(f"""
                    <div style='padding: 1rem; border-left: 4px solid #949CFF; 
                                background: rgba(148, 156, 255, 0.1); 
                                border-radius: 8px;'>
                        <strong style='color: #F2749B;'>{status}</strong> 
                        <strong>{r['datetime']}</strong> {repeat_icon} 
                        <span style='color: #949CFF;'>[{r['category'].title()}]</span> 
                        {r['text']}
                    </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.caption(f"Повтор: {r['repeat']}")
            
            with col4:
                if st.button("🗑️", key=f"delete_{r['id']}"):
                    st.session_state.reminders = [rem for rem in st.session_state.reminders if rem["id"] != r["id"]]
                    save_reminders()
                    st.success("🗑️ Напоминание удалено!")
                    st.rerun()

# Статистика
st.sidebar.markdown("─" * 30)
st.sidebar.metric("Всего задач", len(st.session_state.reminders))
st.sidebar.metric("Активных", len([r for r in st.session_state.reminders if not r['done']]))
