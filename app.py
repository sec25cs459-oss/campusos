import streamlit as st
import requests
from textwrap import dedent

# ============================================================
# CONFIG
# ============================================================
def ask_ollama(prompt):
    try:
        response = requests.post(
            "http://localhost:11434/api/chat",
            json={
                "model": "qwen3:4b",

                "messages": [
                    {
                        "role": "system",
                        "content": """You are CAMPUSOS AI.

Help students with assignments, exams, classes, deadlines, priorities and study plans.

Give a direct, practical answer.
Do not show reasoning.
Do not explain your thought process.
Keep answers concise.

For study plans:
- Respect the available time.
- Prioritize the most urgent task.
- Use realistic time blocks.
- Include short breaks.
- Give the final plan directly.
"""
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],

                "stream": False,
                "think": False,

                "options": {
                    "temperature": 0.3,
                    "num_predict": 250
                }
            },

            timeout=300
        )

        response.raise_for_status()

        

        data = response.json()

        message = data.get("message", {})

# Use only the final answer
        answer = message.get("content", "").strip()

# Safety fallback if Qwen puts thinking in the response
        if not answer:
            answer = message.get("thinking", "").strip()

        return answer

    except requests.exceptions.Timeout:
        return "⏳ CAMPUSOS AI is taking too long to respond. Please try again."

    except requests.exceptions.ConnectionError:
        return "❌ Ollama is not running. Please start Ollama first."

    except Exception as e:
        return f"❌ AI connection error: {e}"

st.set_page_config(
    page_title="CAMPUSOS",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)
# ==============================
# STUDENT PROFILE
# ==============================

if "student_data" not in st.session_state:
    st.session_state.student_data = {
        "name": "",
        "classes": "",
        "assignments": "",
        "exams": "",
        "study_time": "",
        "constraints": ""
    }


# ============================================================
# HTML HELPER
# ============================================================

def html(content):
    st.html(dedent(content))

# ============================================================
# CSS
# ============================================================

html("""
<style>

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

.stApp {
    background: #F6F7FB;
    color: #172033;
}

.block-container {
    max-width: 1500px;
    padding: 38px 48px 70px;
}

/* ================= SIDEBAR ================= */

section[data-testid="stSidebar"] {
    background: #101827;
    border-right: 0;
}

section[data-testid="stSidebar"] * {
    color: #E7EAF0;
}

.brand {
    font-size: 23px;
    font-weight: 850;
    color: white;
    letter-spacing: -0.7px;
}

.brand-sub {
    color: #8D97AA;
    font-size: 10px;
    margin-top: 5px;
    margin-bottom: 28px;
}

.nav-title {
    color: #68748A;
    font-size: 9px;
    font-weight: 800;
    letter-spacing: 1.5px;
    margin: 18px 7px 8px;
}

.sidebar-user {
    margin-top: 35px;
    padding: 14px;
    border-radius: 14px;
    background: #1B2537;
    border: 1px solid #29344A;
}

.sidebar-user-name {
    color: white;
    font-size: 12px;
    font-weight: 800;
}

.sidebar-user-info {
    color: #8D97AA;
    font-size: 9px;
    margin-top: 4px;
}

/* ================= HEADINGS ================= */

.page-title {
    font-size: 32px;
    font-weight: 850;
    letter-spacing: -1.2px;
    color: #131A2A;
}

.page-subtitle {
    color: #788294;
    font-size: 13px;
    margin-top: 5px;
    margin-bottom: 26px;
}

.section-title {
    font-size: 17px;
    font-weight: 800;
    color: #172033;
    margin-top: 27px;
    margin-bottom: 12px;
}

/* ================= TILES ================= */

.tile {
    border-radius: 18px;
    padding: 20px;
    min-height: 128px;
    border: 1px solid rgba(0,0,0,.035);
    box-shadow: 0 4px 14px rgba(15,23,42,.035);
}

.purple {
    background: linear-gradient(135deg,#EEE9FF,#DDD6FE);
}

.blue {
    background: linear-gradient(135deg,#E0F2FE,#BFDBFE);
}

.green {
    background: linear-gradient(135deg,#DCFCE7,#BBF7D0);
}

.orange {
    background: linear-gradient(135deg,#FFEDD5,#FED7AA);
}

.pink {
    background: linear-gradient(135deg,#FCE7F3,#FBCFE8);
}

.yellow {
    background: linear-gradient(135deg,#FEF9C3,#FEF08A);
}

.cyan {
    background: linear-gradient(135deg,#CFFAFE,#A5F3FC);
}

.tile-icon {
    font-size: 23px;
}

.tile-label {
    font-size: 10px;
    font-weight: 750;
    color: #687387;
    margin-top: 12px;
}

.tile-number {
    font-size: 29px;
    font-weight: 850;
    color: #151B2B;
    margin-top: 3px;
}

.tile-info {
    color: #778195;
    font-size: 10px;
    margin-top: 2px;
}

/* ================= CARDS ================= */

.card {
    background: white;
    border: 1px solid #E5E8EF;
    border-radius: 16px;
    padding: 17px 18px;
    margin-bottom: 10px;
    box-shadow: 0 3px 12px rgba(15,23,42,.035);
}

.card-title {
    font-size: 13px;
    font-weight: 800;
    color: #172033;
}

.card-text {
    font-size: 10px;
    color: #7C8596;
    margin-top: 5px;
}

.card-small {
    font-size: 9px;
    color: #929AAA;
    text-transform: uppercase;
    letter-spacing: .8px;
    font-weight: 800;
}

/* ================= TASK ================= */

.task {
    background: white;
    border: 1px solid #E5E8EF;
    border-radius: 15px;
    padding: 16px 18px;
    margin-bottom: 9px;
}

.task-time {
    float: right;
    color: #778195;
    font-size: 10px;
    font-weight: 750;
}

.task-name {
    font-size: 13px;
    font-weight: 800;
    color: #172033;
}

.task-info {
    font-size: 10px;
    color: #7C8596;
    margin-top: 4px;
}

.red {
    color: #EF4444;
}

.gold {
    color: #F59E0B;
}

.green-dot {
    color: #22C55E;
}

.blue-dot {
    color: #3B82F6;
}

/* ================= AI ================= */

.ai-box {
    background: linear-gradient(135deg,#21154D,#41318C,#6258D7);
    border-radius: 22px;
    padding: 29px;
    margin-top: 28px;
    color: white;
    box-shadow: 0 15px 35px rgba(63,45,140,.20);
}

.ai-badge {
    display: inline-block;
    padding: 6px 10px;
    border-radius: 20px;
    background: rgba(255,255,255,.13);
    color: #E8E5FF;
    font-size: 9px;
    font-weight: 800;
    letter-spacing: .8px;
}

.ai-title {
    font-size: 23px;
    font-weight: 850;
    margin-top: 13px;
}

.ai-text {
    color: #D5D0EF;
    font-size: 12px;
    margin-top: 5px;
}

/* ================= BLOCKED ================= */

.blocked {
    background: #FFF1F2;
    border: 1px solid #FECDD3;
    border-radius: 16px;
    padding: 17px;
}

.blocked-title {
    color: #9F1239;
    font-size: 13px;
    font-weight: 800;
}

.blocked-text {
    color: #BE4B6A;
    font-size: 10px;
    margin-top: 5px;
}

/* ================= NOTICE ================= */

.notice {
    background: #FFF7ED;
    border: 1px solid #FED7AA;
    border-radius: 15px;
    padding: 15px;
    margin-bottom: 9px;
}

.notice-title {
    color: #7C3D12;
    font-size: 12px;
    font-weight: 800;
}

.notice-text {
    color: #9A5B28;
    font-size: 10px;
    margin-top: 4px;
}

/* ================= QUICK TILE ================= */

.quick {
    background: white;
    border: 1px solid #E5E8EF;
    border-radius: 17px;
    padding: 18px 10px;
    text-align: center;
    min-height: 105px;
    box-shadow: 0 3px 12px rgba(15,23,42,.035);
}

.quick-icon {
    font-size: 24px;
}

.quick-title {
    color: #172033;
    font-size: 11px;
    font-weight: 800;
    margin-top: 7px;
}

.quick-text {
    color: #8992A2;
    font-size: 9px;
    margin-top: 3px;
}

/* ================= PROGRESS ================= */

.progress-bg {
    background: #ECEEF4;
    height: 8px;
    border-radius: 20px;
    overflow: hidden;
    margin-top: 10px;
}

.progress-purple {
    background: #6366F1;
    width: 72%;
    height: 100%;
}

.progress-blue {
    background: #3B82F6;
    width: 55%;
    height: 100%;
}

.progress-green {
    background: #22C55E;
    width: 84%;
    height: 100%;
}

/* ================= INPUT ================= */

.stTextInput input,
.stTextArea textarea {
    background: white !important;
    color: #172033 !important;
    border: 1px solid #DDE2EA !important;
    border-radius: 13px !important;
}

.stTextInput input:focus,
.stTextArea textarea:focus {
    border-color: #6366F1 !important;
    box-shadow: 0 0 0 2px rgba(99,102,241,.10) !important;
}

/* ================= BUTTONS ================= */

.stButton > button {
    border-radius: 10px !important;
    font-weight: 700 !important;
    font-size: 11px !important;
}

/* ================= FILE UPLOAD ================= */

[data-testid="stFileUploader"] {
    background: white;
    border: 1px solid #E4E7ED;
    border-radius: 15px;
}

/* ================= MOBILE ================= */

@media (max-width: 900px) {
    .block-container {
        padding: 25px 18px;
    }
}

</style>
""")


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    html("""
    <div class="brand">🎓 CAMPUSOS</div>
    <div class="brand-sub">
        AI operating system for college life
    </div>
    """)

    html('<div class="nav-title">OVERVIEW</div>')

    page = st.radio(
        "Navigation",
        [
            "🧠 Setup",
            "🏠 Dashboard",
            "✓ My Tasks",
            "📅 Schedule",
            "🎓 Campus",
            "📝 Assignments",
            "🧪 Exams",
            "🧠 AI Copilot",
            "📄 Documents",
            "⚙️ Profile"
        ],
        label_visibility="collapsed"
    )

    html('<div class="nav-title">QUICK ACTIONS</div>')

    st.button("＋ Add Task", use_container_width=True)
    st.button("✦ Ask CAMPUSOS", use_container_width=True)

    html("""
    <div class="sidebar-user">
        <div class="sidebar-user-name">👤 Student</div>
        <div class="sidebar-user-info">
            Computer Science • 3rd Year
        </div>
    </div>
    """)


# ============================================================
# DASHBOARD
# ============================================================

if page == "🏠 Dashboard":

    html("""
    <div class="page-title">Good afternoon 👋</div>
    <div class="page-subtitle">
        Here's everything that needs your attention today.
    </div>
    """)

    # STAT TILES

    c1, c2, c3, c4 = st.columns(4)

    tiles = [
        ("purple", "✓", "PENDING TASKS", "03", "2 due soon"),
        ("blue", "📚", "CLASSES TODAY", "04", "Next at 2:00 PM"),
        ("orange", "🧪", "UPCOMING EXAMS", "02", "Next in 4 days"),
        ("pink", "⚠️", "NEEDS ATTENTION", "01", "Blocked task")
    ]

    for col, data in zip([c1,c2,c3,c4], tiles):

        color, icon, label, number, info = data

        with col:
            html(f"""
            <div class="tile {color}">
                <div class="tile-icon">{icon}</div>
                <div class="tile-label">{label}</div>
                <div class="tile-number">{number}</div>
                <div class="tile-info">{info}</div>
            </div>
            """)

    # MAIN COLUMNS

    left, right = st.columns([1.55,1])

    with left:

        html('<div class="section-title">📅 Today\'s plan</div>')

        html("""
        <div class="task">
            <span class="task-time">6:00 PM</span>
            <span class="red">●</span>
            <span class="task-name"> AI Assignment</span>
            <div class="task-info">
                Due Wednesday • High priority
            </div>
        </div>

        <div class="task">
            <span class="task-time">7:00 PM</span>
            <span class="gold">●</span>
            <span class="task-name"> Database Lab Revision</span>
            <div class="task-info">
                Exam Friday • 3 units remaining
            </div>
        </div>

        <div class="task">
            <span class="task-time">8:00 PM</span>
            <span class="green-dot">●</span>
            <span class="task-name"> Project Meeting</span>
            <div class="task-info">
                Team discussion • 45 minutes
            </div>
        </div>
        """)

        html("""
        <div class="section-title">⚠️ Needs attention</div>

        <div class="blocked">
            <div class="blocked-title">
                AI Assignment is blocked
            </div>

            <div class="blocked-text">
                Waiting for Rahul's dataset before analysis can begin.
                CAMPUSOS can automatically re-plan when the dependency is resolved.
            </div>
        </div>
        """)

    with right:

        html('<div class="section-title">📌 Upcoming</div>')

        html("""
        <div class="card">
            <div class="card-small">FRIDAY • SEP 11</div>
            <div class="card-title">🧪 Database Lab Exam</div>
            <div class="card-text">3 units to revise</div>
        </div>

        <div class="card">
            <div class="card-small">MONDAY • SEP 14</div>
            <div class="card-title">🤖 AI Project Submission</div>
            <div class="card-text">Report + presentation</div>
        </div>

        <div class="card">
            <div class="card-small">WEDNESDAY • SEP 16</div>
            <div class="card-title">📝 Internal Assessment</div>
            <div class="card-text">Academic block examination</div>
        </div>
        """)

        html('<div class="section-title">📢 Campus Pulse</div>')

        html("""
        <div class="notice">
            <div class="notice-title">
                📣 Internal assessment schedule updated
            </div>
            <div class="notice-text">
                Academic office • 2 hours ago
            </div>
        </div>

        <div class="notice">
            <div class="notice-title">
                🚀 Hackathon registration closes Friday
            </div>
            <div class="notice-text">
                Student affairs • Today
            </div>
        </div>
        """)

    # AI

    html("""
    <div class="ai-box">
        <span class="ai-badge">✦ CAMPUSOS AI</span>

        <div class="ai-title">
            What do you need to figure out?
        </div>

        <div class="ai-text">
            Tell CAMPUSOS what is happening. It will understand your
            tasks, deadlines and campus information and help decide
            what you should do next.
        </div>
    </div>
    """)

    ai_input = st.text_input(
        "AI",
        placeholder='Try: "I only have 2 hours tonight. What should I focus on?"',
        label_visibility="collapsed"
    )

    if ai_input:

        html(f"""
        <div class="card">
            <div class="card-title">🧠 Your request</div>
            <div class="card-text">{ai_input}</div>
        </div>
        """)

    # QUICK ACCESS

    html('<div class="section-title">⚡ Quick access</div>')

    q1,q2,q3,q4,q5 = st.columns(5)

    quick = [
        ("📚","Study","Start session"),
        ("📝","Assignments","3 pending"),
        ("🧪","Exams","2 upcoming"),
        ("📄","Documents","12 files"),
        ("🎓","Campus","Ask anything")
    ]

    for col,(icon,title,text) in zip(
        [q1,q2,q3,q4,q5],
        quick
    ):

        with col:

            html(f"""
            <div class="quick">
                <div class="quick-icon">{icon}</div>
                <div class="quick-title">{title}</div>
                <div class="quick-text">{text}</div>
            </div>
            """)


# ============================================================
# TASKS
# ============================================================

elif page == "✓ My Tasks":

    html("""
    <div class="page-title">My Tasks ✓</div>
    <div class="page-subtitle">
        Everything you need to get done, organized around priority.
    </div>
    """)

    c1,c2,c3 = st.columns(3)

    task_tiles = [
        ("pink","🔴","HIGH PRIORITY","2","Need attention"),
        ("yellow","⏳","IN PROGRESS","3","Currently working"),
        ("green","✓","COMPLETED","12","This semester")
    ]

    for col,data in zip([c1,c2,c3],task_tiles):

        color,icon,label,num,info = data

        with col:

            html(f"""
            <div class="tile {color}">
                <div class="tile-icon">{icon}</div>
                <div class="tile-label">{label}</div>
                <div class="tile-number">{num}</div>
                <div class="tile-info">{info}</div>
            </div>
            """)

    html('<div class="section-title">All tasks</div>')

    tasks = [
        ("🔴","Complete AI Assignment","Due Wednesday","HIGH"),
        ("🟡","Prepare Database Lab","Exam Friday","MEDIUM"),
        ("🟢","Finish project documentation","Due Monday","LOW"),
        ("🔵","Read Unit 4 notes","No deadline","LOW"),
        ("🟣","Prepare presentation slides","Next Monday","MEDIUM")
    ]

    for icon,title,info,priority in tasks:

        html(f"""
        <div class="card">

            <span style="
                float:right;
                font-size:9px;
                font-weight:800;
                color:#7C8596;
            ">
                {priority}
            </span>

            <div class="card-title">
                {icon} {title}
            </div>

            <div class="card-text">
                {info}
            </div>

        </div>
        """)


# ============================================================
# SCHEDULE
# ============================================================

elif page == "📅 Schedule":

    html("""
    <div class="page-title">Schedule 📅</div>
    <div class="page-subtitle">
        Classes, meetings and planned study sessions.
    </div>
    """)

    tabs = st.tabs(["MON","TUE","WED","THU","FRI"])

    schedule = [
        ("09:00","📚","Data Structures","Room 302"),
        ("11:00","💻","Operating Systems","Room 204"),
        ("02:00","🧪","Database Systems","Lab 3"),
        ("04:00","🚀","Project Work","Library"),
        ("06:00","📝","AI Assignment","Personal")
    ]

    for tab in tabs:

        with tab:

            for time,icon,name,room in schedule:

                html(f"""
                <div class="card">

                    <span style="
                        float:right;
                        font-size:10px;
                        font-weight:800;
                        color:#687387;
                    ">
                        {time}
                    </span>

                    <div class="card-title">
                        {icon} {name}
                    </div>

                    <div class="card-text">
                        📍 {room}
                    </div>

                </div>
                """)


# ============================================================
# CAMPUS
# ============================================================

elif page == "🎓 Campus":

    html("""
    <div class="page-title">Campus 🎓</div>
    <div class="page-subtitle">
        Your college information, understood by AI.
    </div>
    """)

    c1,c2,c3 = st.columns(3)

    campus = [
        ("purple","📚","COURSES","8","Current semester"),
        ("blue","📢","NOTICES","14","Important updates"),
        ("orange","📅","EVENTS","5","This month")
    ]

    for col,data in zip([c1,c2,c3],campus):

        color,icon,label,num,info = data

        with col:

            html(f"""
            <div class="tile {color}">
                <div class="tile-icon">{icon}</div>
                <div class="tile-label">{label}</div>
                <div class="tile-number">{num}</div>
                <div class="tile-info">{info}</div>
            </div>
            """)

    html('<div class="section-title">🎓 Campus Brain</div>')

    uploaded = st.file_uploader(
        "Upload timetable, syllabus, notices, regulations or exam schedules",
        type=["pdf","txt"],
        accept_multiple_files=True
    )

    if uploaded:
        st.success(f"✓ {len(uploaded)} document(s) uploaded.")

    question = st.text_input(
        "Ask your campus",
        placeholder="When is my next lab exam?"
    )

    if question:

        html(f"""
        <div class="card">
            <div class="card-title">🔍 Campus question</div>
            <div class="card-text">{question}</div>
        </div>
        """)


# ============================================================
# ASSIGNMENTS
# ============================================================

elif page == "📝 Assignments":

    html("""
    <div class="page-title">Assignments 📝</div>
    <div class="page-subtitle">
        Never lose track of another submission.
    </div>
    """)

    a1,a2,a3,a4 = st.columns(4)

    stats = [
        ("pink","🔴","PENDING","3"),
        ("yellow","⏳","IN PROGRESS","2"),
        ("green","✓","COMPLETED","7"),
        ("blue","⚠️","OVERDUE","0")
    ]

    for col,data in zip([a1,a2,a3,a4],stats):

        color,icon,label,num = data

        with col:

            html(f"""
            <div class="tile {color}">
                <div class="tile-icon">{icon}</div>
                <div class="tile-label">{label}</div>
                <div class="tile-number">{num}</div>
            </div>
            """)

    html('<div class="section-title">Upcoming assignments</div>')

    # ==============================
    # STUDENT ASSIGNMENTS
    # ==============================

    if "assignment_items" not in st.session_state:
        st.session_state.assignment_items = []


    with st.expander("➕ Add a new assignment", expanded=True):

        assignment_subject = st.text_input(
            "Subject",
            placeholder="Example: Data Structures"
        )

        assignment_name = st.text_input(
            "Assignment",
            placeholder="Example: Lab Record"
        )

        assignment_deadline = st.text_input(
            "Deadline",
            placeholder="Example: September 10"
        )

        assignment_progress = st.slider(
            "Progress",
            0,
            100,
            0
        )

        if st.button("➕ Add Assignment", use_container_width=True):

            if assignment_subject and assignment_name and assignment_deadline:

                st.session_state.assignment_items.append(
                    (
                        "📝",
                        assignment_subject,
                        assignment_name,
                        assignment_deadline,
                        assignment_progress
                    )
                )

                # Sync with CAMPUSOS AI
                st.session_state.student_data["assignments"] = "\n".join(
                    [
                        f"{item[2]} ({item[1]}) - due {item[3]}"
                        for item in st.session_state.assignment_items
                    ]
                )

                st.success("✅ Assignment added to CAMPUSOS Brain!")

            else:
                st.warning("Please fill in Subject, Assignment and Deadline.")


    assignments = st.session_state.assignment_items

    for icon,subject,name,date,progress in assignments:

        html(f"""
        <div class="card">

            <div class="card-small">
                {subject}
            </div>

            <div class="card-title">
                {icon} {name}
            </div>

            <div class="card-text">
                Deadline: {date}
            </div>

            <div class="progress-bg">
                <div style="
                    width:{progress}%;
                    height:100%;
                    background:#6366F1;
                    border-radius:20px;
                "></div>
            </div>

            <div class="card-text">
                {progress}% complete
            </div>

        </div>
        """)


# ============================================================
# EXAMS
# ============================================================

elif page == "🧪 Exams":

    html("""
    <div class="page-title">Exams 🧪</div>
    <div class="page-subtitle">
        Know what is coming before it becomes urgent.
    </div>
    """)

    e1,e2,e3 = st.columns(3)

        # ==============================
    # STUDENT EXAMS
    # ==============================

    if "exam_items" not in st.session_state:
        st.session_state.exam_items = []


    with st.expander("➕ Add a new exam", expanded=True):

        exam_subject = st.text_input(
            "Exam subject",
            placeholder="Example: Database Systems"
        )

        exam_date = st.text_input(
            "Exam date",
            placeholder="Example: September 18"
        )

        exam_venue = st.text_input(
            "Venue",
            placeholder="Example: Hall A"
        )

        if st.button("➕ Add Exam", use_container_width=True):

            if exam_subject and exam_date:

                st.session_state.exam_items.append(
                    (
                        exam_date,
                        exam_subject,
                        exam_venue
                    )
                )

                # Sync exams with CAMPUSOS Brain
                st.session_state.student_data["exams"] = "\n".join(
                    [
                        f"{item[1]} - {item[0]} - {item[2]}"
                        for item in st.session_state.exam_items
                    ]
                )

                st.success("✅ Exam added to CAMPUSOS Brain!")

            else:
                st.warning("Please enter the exam subject and date.")


    exam_list = st.session_state.exam_items

    html('<div class="section-title">Exam schedule</div>')

    exam_list = [
        ("Sep 11","Database Systems Lab","Lab 3"),
        ("Sep 18","Artificial Intelligence","Hall A"),
        ("Sep 25","Operating Systems","Hall B"),
        ("Oct 02","Software Engineering","Hall C")
    ]

    for date,name,venue in exam_list:

        html(f"""
        <div class="card">

            <span style="
                float:right;
                background:#EEF2FF;
                color:#4F46E5;
                padding:5px 9px;
                border-radius:20px;
                font-size:9px;
                font-weight:800;
            ">
                {date}
            </span>

            <div class="card-title">
                🧪 {name}
            </div>

            <div class="card-text">
                📍 {venue}
            </div>

        </div>
        """)


# ============================================================
# AI COPILOT
# ============================================================
elif page == "🧠 Setup":

    html("""
    <div class="page-title">🧠 Setup CAMPUSOS</div>
    <div class="page-subtitle">
        Tell CAMPUSOS about yourself so your AI can understand your college life.
    </div>
    """)

    st.markdown("### 👋 Let's get you set up")

    name = st.text_input(
        "1. What's your name?",
        value=st.session_state.student_data["name"],
        placeholder="Example: Abraar"
    )

    classes = st.text_area(
        "2. What classes/subjects do you have?",
        value=st.session_state.student_data["classes"],
        placeholder="""Example:
Data Structures
Operating Systems
Database Management
AI & ML""",
        height=120
    )

    assignments = st.text_area(
        "3. What assignments or tasks do you have?",
        value=st.session_state.student_data["assignments"],
        placeholder="""Example:
DS Lab Record - due tomorrow
DBMS Assignment - due Wednesday
AI Project - due next Monday""",
        height=150
    )

    exams = st.text_area(
        "4. What exams are coming up?",
        value=st.session_state.student_data["exams"],
        placeholder="""Example:
AI & ML - Friday
DBMS - next Tuesday""",
        height=120
    )

    study_time = st.text_input(
        "5. How much time can you study/work each day?",
        value=st.session_state.student_data["study_time"],
        placeholder="Example: 2 hours on weekdays, 4 hours on weekends"
    )

    constraints = st.text_area(
        "6. Anything CAMPUSOS should know?",
        value=st.session_state.student_data["constraints"],
        placeholder="Example: I have classes until 4 PM and travel for 1 hour.",
        height=100
    )

    if st.button("🚀 Save My CAMPUSOS Profile", use_container_width=True):

        st.session_state.student_data = {
            "name": name,
            "classes": classes,
            "assignments": assignments,
            "exams": exams,
            "study_time": study_time,
            "constraints": constraints
        }

        st.success("✅ CAMPUSOS now knows your academic context!")



elif page == "🧠 AI Copilot":

    html("""
    <div class="page-title">AI Copilot 🧠</div>
    <div class="page-subtitle">
        Your personal AI for planning, campus knowledge and priorities.
    </div>
    """)

    html("""
    <div class="ai-box">

        <span class="ai-badge">
            ✦ CAMPUSOS BRAIN
        </span>

        <div class="ai-title">
            Tell me what's happening.
        </div>

        <div class="ai-text">
            I can understand your deadlines, tasks, documents,
            schedule and dependencies.
        </div>

    </div>
    """)

    question = st.text_area(
        "Message",
        placeholder="""Example:

I have an exam Friday,
an assignment due Wednesday,
and only two hours tonight.

What should I do?""",
        height=150,
        label_visibility="collapsed"
    )
        # ==============================
    # CAMPUSOS AI RESPONSE
    # ==============================

    if st.button("✨ Ask CAMPUSOS AI", use_container_width=True):

                if question.strip():

                    student = st.session_state.student_data

                    student_context = f"""
        Student name:
        {student["name"]}

        Classes:
        {student["classes"]}

        Assignments:
        {student["assignments"]}

        Exams:
        {student["exams"]}

        Available study time:
        {student["study_time"]}

        Other constraints:
        {student["constraints"]}
        """

                    with st.spinner("🧠 CAMPUSOS AI is thinking..."):

                        answer = ask_ollama(
                            f"""
        Here is the student's CAMPUSOS profile:

        {student_context}

        Student request:
        {question}

        Use the student's information to give a personalized answer.

        Give ONLY the final answer.
        Do not show reasoning.
        """
                        )

                    html(f"""
                    <div class="card">
                        <div class="card-title">🧠 CAMPUSOS AI</div>
                        <div class="card-text">{answer}</div>
                    </div>
                    """)

                else:
                    st.warning("Please enter a message first.")


    

    b1,b2,b3 = st.columns(3)

    with b1:
        if st.button("🗓️ Make a plan", use_container_width=True):
            if question.strip():

                student = st.session_state.student_data

                student_context = f"""
    Student name: {student["name"]}

    Classes:
    {student["classes"]}

    Assignments:
    {student["assignments"]}

    Exams:
    {student["exams"]}

    Available study time:
    {student["study_time"]}

    Other constraints:
    {student["constraints"]}
    """

                with st.spinner("🧠 Building your plan..."):

                    answer = ask_ollama(
                        f"""
    Create a realistic plan for this student.

    STUDENT INFORMATION:
    {student_context}

    STUDENT REQUEST:
    {question}

    Use the student's actual assignments, exams, available time and constraints.
    Prioritize urgent deadlines.
    Give ONLY the final plan.
    """
                    )

                st.success("Your plan is ready!")
                st.write(answer)

    with b2:
        if st.button("🎯 Prioritize", use_container_width=True):
            if question.strip():

                student = st.session_state.student_data

                with st.spinner("🎯 Finding priorities..."):

                    answer = ask_ollama(
                        f"""
    Here is the student's CAMPUSOS information:

    {student}

    Student request:
    {question}

    Analyze all tasks, assignments and exams.
    Rank them from highest to lowest priority based on urgency and deadlines.

    Give ONLY the final prioritized list.
    """
                    )

                st.success("Priorities identified!")
                st.write(answer)

    with b3:
        if st.button("🔍 Find deadlines", use_container_width=True):
            if question.strip():

                student = st.session_state.student_data

                with st.spinner("🔍 Analyzing deadlines..."):

                    answer = ask_ollama(
                        f"""
    Here is the student's CAMPUSOS information:

    {student}

    Student request:
    {question}

    Find all assignments, exams and deadlines.
    Organize them clearly by urgency.

    Give ONLY the final answer.
    """
                    )

                st.success("Deadlines found!")
                st.write(answer)

        html('<div class="section-title">💬 Try asking</div>')

        examples = [
            "What should I focus on tonight?",
            "When is my next exam?",
            "What assignments are due this week?",
            "What is blocking my project?",
            "Make me a study plan."
        ]

        for example in examples:

            html(f"""
            <div class="card">
                <div class="card-title">
                    💬 {example}
                </div>
            </div>
            """)

        if question:

            html(f"""
            <div class="card">
                <div class="card-title">
                    🧠 CAMPUSOS received your request
                </div>

                <div class="card-text">
                    {question}
                </div>
            </div>
            """)


# ============================================================
# DOCUMENTS
# ============================================================

elif page == "📄 Documents":

    html("""
    <div class="page-title">Documents 📄</div>
    <div class="page-subtitle">
        Upload information and let CAMPUSOS turn it into knowledge.
    </div>
    """)

    c1,c2,c3 = st.columns(3)

    docs_tiles = [
        ("purple","📚","SYLLABUS","8","courses"),
        ("blue","📅","TIMETABLE","1","weekly schedule"),
        ("orange","📢","NOTICES","14","campus updates")
    ]

    for col,data in zip([c1,c2,c3],docs_tiles):

        color,icon,label,num,info = data

        with col:

            html(f"""
            <div class="tile {color}">
                <div class="tile-icon">{icon}</div>
                <div class="tile-label">{label}</div>
                <div class="tile-number">{num}</div>
                <div class="tile-info">{info}</div>
            </div>
            """)

    html('<div class="section-title">Upload documents</div>')

    uploaded = st.file_uploader(
        "Drop your college PDFs here",
        type=["pdf","txt","csv"],
        accept_multiple_files=True
    )

    if uploaded:

        for file in uploaded:

            html(f"""
            <div class="card">
                <div class="card-title">
                    📄 {file.name}
                </div>
                <div class="card-text">
                    Ready for CAMPUSOS AI processing
                </div>
            </div>
            """)

        st.success(
            f"✓ {len(uploaded)} document(s) uploaded."
        )

    html('<div class="section-title">Recommended documents</div>')

    recommended = [
        ("📅","Timetable","Weekly class schedule"),
        ("📚","Syllabus","Course topics and structure"),
        ("🧪","Exam Schedule","Upcoming examinations"),
        ("📢","College Notices","Important announcements"),
        ("📜","Regulations","Academic rules")
    ]

    for icon,name,description in recommended:

        html(f"""
        <div class="card">
            <div class="card-title">
                {icon} {name}
            </div>

            <div class="card-text">
                {description}
            </div>
        </div>
        """)


# ============================================================
# PROFILE
# ============================================================

elif page == "⚙️ Profile":

    html("""
    <div class="page-title">Profile ⚙️</div>
    <div class="page-subtitle">
        Tell CAMPUSOS how you work and study.
    </div>
    """)

    left,right = st.columns([1,2])

    with left:

        html("""
        <div class="tile purple" style="text-align:center;">

            <div style="font-size:60px;">
                👤
            </div>

            <div class="tile-number">
                Student
            </div>

            <div class="tile-info">
                Computer Science • 3rd Year
            </div>

        </div>
        """)

    with right:

        html('<div class="section-title">Student information</div>')

        st.text_input("Name", value="Student")

        st.text_input(
            "Course",
            value="Computer Science"
        )

        st.text_input(
            "Year",
            value="3rd Year"
        )

        st.selectbox(
            "Planning style",
            [
                "Balanced",
                "Deadline focused",
                "Study focused",
                "Minimal schedule"
            ]
        )

        st.button(
            "Save Profile",
            use_container_width=True
        )
