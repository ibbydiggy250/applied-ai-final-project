import streamlit as st
from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Register Pet"):
    pet = Pet(name=pet_name, species=species, breed="", age=0)
    st.session_state.owner.name = owner_name
    st.session_state.owner.register_pet(pet)
    st.session_state.pets.append(pet)

if st.session_state.get("pets"):
    st.write("Registered pets:", [p.name for p in st.session_state.pets])

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="", email="")
if "tasks" not in st.session_state:
    st.session_state.tasks = []
if "pets" not in st.session_state:
    st.session_state.pets = []
if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler(owner=st.session_state.owner)

col1, col2, col3, col4 = st.columns(4)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", [1, 2, 3, 4, 5], index=2)
with col4:
    frequency = st.selectbox("Frequency", ["once", "daily", "weekly", "monthly", "custom"])

if st.session_state.pets:
    selected_pet_name = st.selectbox("Assign to pet", [p.name for p in st.session_state.pets])
    selected_pet = next(p for p in st.session_state.pets if p.name == selected_pet_name)

    if st.button("Add task"):
        task = st.session_state.owner.create_task(
            name=task_title, duration=int(duration), priority=priority, description="", frequency=frequency
        )
        selected_pet.assign_task(task)
        st.session_state.tasks.append((task, selected_pet.name))
else:
    st.info("Register a pet first before adding tasks.")

if st.session_state.tasks:
    st.write("Current tasks:")
    col1, col2, col3, col4, col5, col6 = st.columns([1, 2, 3, 2, 2, 2])
    col1.markdown("**Done**")
    col2.markdown("**Pet**")
    col3.markdown("**Task**")
    col4.markdown("**Duration**")
    col5.markdown("**Priority**")
    col6.markdown("**Frequency**")
    st.divider()
    for task, pet_name in st.session_state.tasks:
        col1, col2, col3, col4, col5, col6 = st.columns([1, 2, 3, 2, 2, 2])
        checked = col1.checkbox("", value=task.completed, key=task.name)
        if checked and not task.completed:
            task.mark_complete()
        label = f"~~{task.name}~~" if task.completed else task.name
        col2.markdown(pet_name)
        col3.markdown(label)
        col4.markdown(f"{task.duration} min")
        col5.markdown(str(task.priority))
        col6.markdown(task.frequency)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button should call your scheduling logic once you implement it.")

if st.button("Generate schedule"):
    plan = st.session_state.scheduler.generate_plan()
    if plan:
        st.write("Today's Schedule:")
        for i, task in enumerate(plan, start=1):
            st.markdown(f"**{i}. [{task.priority}] {task.name}** — {task.duration} min")
    else:
        st.info("No tasks found. Register a pet and add tasks first.")
'''     
Suggested approach:
1. Design your UML (draft).
2. Create class stubs (no logic).
3. Implement scheduling behavior.
4. Connect your scheduler here and display results.
"""
    )
'''