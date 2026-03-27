from pawpal_system import Owner, Pet, Scheduler

# --- Setup ---
owner = Owner(name="Alex", email="alex@email.com")
owner.scheduler = Scheduler(owner=owner)

# --- Pets ---
buddy = Pet(name="Buddy", species="Dog", breed="Labrador", age=3)
whiskers = Pet(name="Whiskers", species="Cat", breed="Siamese", age=5)

owner.register_pet(buddy)
owner.register_pet(whiskers)

# --- Tasks for Buddy ---
buddy.assign_task(owner.create_task("Morning Walk",     duration=30, priority=3, description="Walk around the block"))
buddy.assign_task(owner.create_task("Feeding",          duration=10, priority=5, description="Dry food, 1 cup"))
buddy.assign_task(owner.create_task("Grooming",         duration=20, priority=1, description="Brush coat"))

# --- Tasks for Whiskers ---
whiskers.assign_task(owner.create_task("Feeding",       duration=10, priority=5, description="Wet food, half can"))
whiskers.assign_task(owner.create_task("Playtime",      duration=15, priority=2, description="Feather toy session"))
whiskers.assign_task(owner.create_task("Litter Box",    duration=5,  priority=4, description="Clean and refill"))

# --- Today's Schedule ---
plan = owner.scheduler.generate_plan()

print("=" * 40)
print("        TODAY'S SCHEDULE")
print("=" * 40)

for i, task in enumerate(plan, start=1):
    status = "Done" if task.completed else "Pending"
    print(f"{i}. [{task.priority}] {task.name:<15} {task.duration} min  |  {status}")
    print(f"   {task.description}")
    print()

print("=" * 40)
print(f"Total tasks: {len(plan)}")
print(f"Total time:  {sum(t.duration for t in plan)} min")
print("=" * 40)
