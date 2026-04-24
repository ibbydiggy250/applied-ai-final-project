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
breed = st.text_input("Breed", value="")
age = st.number_input("Age (years)", min_value=0, max_value=30, value=0, step=1)

if st.button("Register Pet"):
    pet = Pet(name=pet_name, species=species, breed=breed, age=int(age))
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
    time = st.text_input("Time (HH:MM)", value="08:00")
with col3:
    priority = st.selectbox("Priority", [1, 2, 3, 4, 5], index=2)
with col4:
    frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])

if st.session_state.pets:
    selected_pet_name = st.selectbox("Assign to pet", [p.name for p in st.session_state.pets])
    selected_pet = next(p for p in st.session_state.pets if p.name == selected_pet_name)

    if st.button("Add task"):
        candidate = st.session_state.owner.create_task(
            name=task_title, time=time, priority=priority, description="", frequency=frequency
        )
        conflicts = st.session_state.scheduler.detect_conflicts(candidate)
        if conflicts:
            conflict_names = ", ".join(f"'{t.name}'" for t in conflicts)
            st.warning(f"Time conflict at {time}: {conflict_names} is already scheduled at this time. Choose a different time.")
        else:
            selected_pet.assign_task(candidate)
            st.session_state.tasks.append((candidate, selected_pet.name))
else:
    st.info("Register a pet first before adding tasks.")

if st.session_state.tasks:
    st.write("Current tasks:")

    filter_col1, filter_col2, filter_col3 = st.columns(3)
    with filter_col1:
        pet_options = ["All"] + [p.name for p in st.session_state.pets]
        pet_filter = st.selectbox("Filter by pet", pet_options)
    with filter_col2:
        status_filter = st.selectbox("Filter by status", ["All", "Pending", "Completed"])
    with filter_col3:
        sort_by = st.selectbox("Sort by", ["Default", "Time"])

    pet_arg = None if pet_filter == "All" else pet_filter
    completed_arg = None if status_filter == "All" else (status_filter == "Completed")

    filtered = st.session_state.scheduler.filter_tasks(pet_name=pet_arg, completed=completed_arg)
    if sort_by == "Time":
        filtered = sorted(filtered, key=lambda t: t.time)

    pet_lookup = {p.name: p for p in st.session_state.pets}
    task_to_pet = {
        id(task): pet.name
        for pet in st.session_state.pets
        for task in pet.tasks
    }

    col1, col2, col3, col4, col5, col6, col7 = st.columns([1, 2, 3, 2, 2, 2, 2])
    col1.markdown("**Done**")
    col2.markdown("**Pet**")
    col3.markdown("**Task**")
    col4.markdown("**Time**")
    col5.markdown("**Priority**")
    col6.markdown("**Frequency**")
    col7.markdown("**Due**")
    st.divider()
    for task in filtered:
        col1, col2, col3, col4, col5, col6, col7 = st.columns([1, 2, 3, 2, 2, 2, 2])
        checked = col1.checkbox("", value=task.completed, key=id(task))
        if checked and not task.completed:
            task.mark_complete()
            if task.frequency in ("daily", "weekly"):
                new_task = task.renew()
                pet_name_for_task = task_to_pet.get(id(task), "")
                pet_for_task = next((p for p in st.session_state.pets if p.name == pet_name_for_task), None)
                if pet_for_task:
                    pet_for_task.assign_task(new_task)
                    st.session_state.tasks.append((new_task, pet_name_for_task))
                st.rerun()
        label = f"~~{task.name}~~" if task.completed else task.name
        col2.markdown(task_to_pet.get(id(task), ""))
        col3.markdown(label)
        col4.markdown(task.time)
        col5.markdown(str(task.priority))
        col6.markdown(task.frequency)
        col7.markdown(task.due_in)
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
            st.markdown(f"**{i}. [{task.priority}] {task.name}** — {task.time}")
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