import streamlit as st
import json
import os
from datetime import datetime, timedelta
import calendar
import random

st.set_page_config(page_title="TimeStudent", layout="wide")
st.title("📚 TimeStudent")
st.markdown("---")

DATA_FILE = "reminders.json"

# Приоритеты с цветами
PRIORITY_COLORS = {
    "низкий": "🟢",
    "средний": "🟡", 
    "высокий": "🔴",
    "критический": "🔴🔴"
}

PRIORITY_OPTIONS = list(PRIORITY_COLORS.keys())

# Русские названия месяцев
RUSSIAN_MONTHS = [
    "", "Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
    "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"
]

# Русские названия дней недели (сокращенные)
RUSSIAN_WEEKDAYS = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]

if 'reminders' not in st.session_state:
    st.session_state.reminders = []
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                st.session_state.reminders = json.load(f)
        except:
            pass

# Статистика выполнения
if 'completed_count' not in st.session_state:
    st.session_state.completed_count = 0
    st.session_state.total_tasks = len(st.session_state.reminders)

def save_reminders():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(st.session_state.reminders, f, ensure_ascii=False, indent=2)

def get_completion_stats():
    total = len(st.session_state.reminders)
    completed = len([r for r in st.session_state.reminders if r['done']])
    if total > 0:
        percentage = (completed / total) * 100
    else:
        percentage = 0
    return total, completed, percentage

def show_celebration():
    celebrations = [
        "🎉 Отличная работа!",
        "🎊 Молодец!",
        "🌟 Продолжай в том же духе!",
        "👏 Ты супер!",
        "🏆 Победа!"
    ]
    st.balloons()
    st.success(random.choice(celebrations))

def generate_russian_calendar(year, month):
    """Генерирует календарь на русском языке"""
    cal = calendar.monthcalendar(year, month)
    
    # Заголовок с названием месяца
    header = f"**{RUSSIAN_MONTHS[month]} {year}**\n\n"
    
    # Дни недели
    weekdays = " ".join([f"{day:>2}" for day in RUSSIAN_WEEKDAYS])
    calendar_text = header + weekdays + "\n"
    
    # Дни месяца
    for week in cal:
        week_str = ""
        for day in week:
            if day == 0:
                week_str += "   "
            else:
                # Проверяем, есть ли задачи на этот день
                day_str = f"{day:>2}"
                week_str += f"{day_str} "
        calendar_text += week_str + "\n"
    
    return calendar_text

CATEGORIES = ["учёба", "экзамены", "личное", "прочее"]

# Sidebar: filter + stats
st.sidebar.header("🔍 Фильтр")
filter_cat = st.sidebar.selectbox("Категория:", ["Все"] + CATEGORIES)
filter_priority = st.sidebar.selectbox("Приоритет:", ["Все"] + PRIORITY_OPTIONS)

# Статистика
st.sidebar.markdown("---")
st.sidebar.header("📊 Статистика")
total, completed, percentage = get_completion_stats()
st.sidebar.metric("Всего задач", total)
st.sidebar.metric("Выполнено", completed)
st.sidebar.metric("Прогресс", f"{percentage:.1f}%")

# Прогресс-бар
st.sidebar.progress(percentage / 100)
if percentage == 100 and total > 0:
    show_celebration()

# Календарь на русском
st.sidebar.markdown("---")
st.sidebar.header("📅 Календарь")
current_date = datetime.now()
year = current_date.year
month = current_date.month

# Создание календаря на русском
russian_calendar = generate_russian_calendar(year, month)
st.sidebar.markdown(russian_calendar)

# Add reminder form
st.header("➕ Добавить напоминание")

col1, col2 = st.columns(2)
with col1:
    text = st.text_input("Задача:", placeholder="Например: Выучить HSK 4")
with col2:
    date_str = st.text_input("Дата/время:", datetime.now().strftime("%Y-%m-%d %H:%M"))

col3, col4, col5, col6 = st.columns(4)
with col3:
    category = st.selectbox("Категория:", CATEGORIES)
with col4:
    repeat = st.selectbox("Повтор:", ["-", "ежедневно", "еженедельно"])
with col5:
    priority = st.selectbox("Приоритет:", PRIORITY_OPTIONS)
with col6:
    progress = st.slider("Прогресс (%)", 0, 100, 0)

# Центрированная кнопка под блоками
cols = st.columns(11)
with cols[5]:
    if st.button("➕ Добавить"):
        if text and date_str:
            try:
                dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
                reminder = {
                    "id": len(st.session_state.reminders) + 1,
                    "text": text,
                    "datetime": dt.strftime("%Y-%m-%d %H:%M"),
                    "category": category,
                    "repeat": repeat,
                    "priority": priority,
                    "progress": progress,
                    "done": progress == 100
                }
                st.session_state.reminders.append(reminder)
                save_reminders()
                st.success("✅ Добавлено!")
                st.rerun()
            except ValueError:
                st.error("❌ Формат: ГГГГ-ММ-ДД ЧЧ:ММ")
        else:
            st.warning("⚠️ Заполните все поля!")

# Reminders list
st.header("📋 Напоминания")
filtered_reminders = [r for r in st.session_state.reminders 
                     if (filter_cat == "Все" or r["category"] == filter_cat) and
                        (filter_priority == "Все" or r["priority"] == filter_priority)]

if not filtered_reminders:
    st.info("😊 Нет напоминаний")
else:
    filtered_reminders.sort(key=lambda x: (x["priority"], x["datetime"]))
    
    for r in filtered_reminders:
        # Цветовая идентификация по приоритету
        priority_color = PRIORITY_COLORS.get(r["priority"], "⚪")
        
        col1, col2, col3, col4, col5 = st.columns([1, 3, 2, 2, 1])
        
        with col1:
            if st.checkbox("✓", key=f"done_{r['id']}", value=r["done"]):
                for rem in st.session_state.reminders:
                    if rem["id"] == r["id"]:
                        rem["done"] = True
                        rem["progress"] = 100
                save_reminders()
                # Проверка на достижение 100%
                total_tasks, completed_tasks, new_percentage = get_completion_stats()
                if new_percentage == 100 and total_tasks > 0:
                    show_celebration()
                st.rerun()
        
        with col2:
            status = "✅" if r["done"] else "⏳"
            repeat_icon = {"ежедневно": "🔄", "еженедельно": "📅", "-": ""}[r["repeat"]]
            priority_text = f"{priority_color} [{r['priority']}]"
            st.write(f"{status} **{r['datetime']}** {repeat_icon} **[{r['category']}]** {priority_text} {r['text']}")
        
        with col3:
            # Прогресс выполнения
            progress_value = r["progress"] if not r["done"] else 100
            st.progress(progress_value / 100)
            st.caption(f"Прогресс: {progress_value}%")
        
        with col4:
            # Редактирование прогресса
            new_progress = st.slider("Изменить прогресс", 0, 100, progress_value, key=f"progress_{r['id']}")
            if new_progress != progress_value:
                for rem in st.session_state.reminders:
                    if rem["id"] == r["id"]:
                        rem["progress"] = new_progress
                        rem["done"] = new_progress == 100
                save_reminders()
                st.rerun()
        
        with col5:
            if st.button("🗑️", key=f"delete_{r['id']}"):
                st.session_state.reminders = [rem for rem in st.session_state.reminders if rem["id"] != r["id"]]
                save_reminders()
                st.rerun()

# Анимация для новых задач
st.markdown("""
<style>
@keyframes fadeIn {
    from {opacity: 0;}
    to {opacity: 1;}
}
.fade-in {
    animation: fadeIn 1s;
}
</style>
""", unsafe_allow_html=True)

# Дополнительная статистика
st.markdown("---")
st.header("📈 Детальная статистика")

if st.session_state.reminders:
    # Распределение по приоритетам
    priority_stats = {}
    for priority in PRIORITY_OPTIONS:
        priority_stats[priority] = len([r for r in st.session_state.reminders if r['priority'] == priority])
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("По приоритетам")
        for priority, count in priority_stats.items():
            color = PRIORITY_COLORS[priority]
            st.write(f"{color} {priority}: {count}")
    
    with col2:
        st.subheader("По категориям")
        for category in CATEGORIES:
            count = len([r for r in st.session_state.reminders if r['category'] == category])
            st.write(f"📁 {category}: {count}")
    
    with col3:
        st.subheader("По статусу")
        active = len([r for r in st.session_state.reminders if not r['done']])
        completed = len([r for r in st.session_state.reminders if r['done']])
        st.write(f"⏳ Активные: {active}")
        st.write(f"✅ Выполненные: {completed}")
