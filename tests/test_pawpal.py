from datetime import date, timedelta
from pawpal_system import Task, Pet, Scheduler, Owner, PawAgent


def test_mark_complete_sets_completed_true():
    task = Task(name="Walk", time="07:00", priority=3, description="Morning walk")
    task.mark_complete()
    assert task.completed is True


def test_assign_task_increases_pet_task_count():
    pet = Pet(name="Buddy", species="Dog", breed="Labrador", age=3)
    task = Task(name="Feeding", time="08:00", priority=1, description="Dry food")
    pet.assign_task(task)
    assert len(pet.tasks) == 1


# Required: sort_by_time returns tasks in chronological order
def test_sort_by_time_returns_chronological_order():
    owner = Owner(name="Alex", email="alex@example.com")
    pet = Pet(name="Buddy", species="Dog", breed="Labrador", age=3)
    owner.register_pet(pet)
    owner.scheduler = Scheduler(owner=owner)

    pet.assign_task(Task(name="Grooming", time="14:00", priority=2, description="Brush coat"))
    pet.assign_task(Task(name="Feeding", time="08:00", priority=1, description="Dry food"))
    pet.assign_task(Task(name="Walk", time="07:00", priority=3, description="Morning walk"))

    sorted_tasks = owner.scheduler.sort_by_time()
    times = [t.time for t in sorted_tasks]
    assert times == ["07:00", "08:00", "14:00"]


# Required: marking a daily task complete creates a new task for the following day
def test_marking_daily_complete_creates_next_day_task():
    base = date(2026, 3, 28)
    task = Task(name="Feeding", time="08:00", priority=1, description="Dry food", frequency="daily", due_date=base)
    task.mark_complete()
    renewed = task.renew()
    assert task.completed is True
    assert renewed.completed is False
    assert renewed.due_date == base + timedelta(days=1)


# Required: Scheduler flags duplicate times as conflicts
def test_scheduler_flags_duplicate_times():
    owner = Owner(name="Alex", email="alex@example.com")
    pet = Pet(name="Buddy", species="Dog", breed="Labrador", age=3)
    owner.register_pet(pet)
    owner.scheduler = Scheduler(owner=owner)

    pet.assign_task(Task(name="Feeding", time="08:00", priority=1, description="Dry food"))
    candidate = Task(name="Meds", time="08:00", priority=2, description="Pills")

    conflicts = owner.scheduler.detect_conflicts(candidate)
    assert len(conflicts) == 1
    assert conflicts[0].name == "Feeding"


# Edge case: first task can always be added to an empty schedule
def test_detect_conflicts_returns_empty_on_empty_schedule():
    owner = Owner(name="Alex", email="alex@example.com")
    owner.scheduler = Scheduler(owner=owner)

    candidate = Task(name="Feeding", time="08:00", priority=1, description="Dry food")
    assert owner.scheduler.detect_conflicts(candidate) == []


# Edge case: completed tasks still occupy their time slot and block new tasks
def test_detect_conflicts_includes_completed_tasks():
    owner = Owner(name="Alex", email="alex@example.com")
    pet = Pet(name="Buddy", species="Dog", breed="Labrador", age=3)
    owner.register_pet(pet)
    owner.scheduler = Scheduler(owner=owner)

    done = Task(name="Feeding", time="08:00", priority=1, description="Dry food")
    done.mark_complete()
    pet.assign_task(done)

    candidate = Task(name="Meds", time="08:00", priority=2, description="Pills")
    assert len(owner.scheduler.detect_conflicts(candidate)) == 1


# filter_tasks: both filters active returns only matching pet's incomplete tasks
def test_filter_tasks_by_pet_name_and_completed_status():
    owner = Owner(name="Alex", email="alex@example.com")
    buddy = Pet(name="Buddy", species="Dog", breed="Labrador", age=3)
    whiskers = Pet(name="Whiskers", species="Cat", breed="Tabby", age=2)
    owner.register_pet(buddy)
    owner.register_pet(whiskers)
    owner.scheduler = Scheduler(owner=owner)

    done = Task(name="Walk", time="07:00", priority=3, description="Morning walk")
    done.mark_complete()
    buddy.assign_task(done)
    buddy.assign_task(Task(name="Feeding", time="08:00", priority=1, description="Dry food"))
    whiskers.assign_task(Task(name="Brushing", time="09:00", priority=2, description="Fur brush"))

    result = owner.scheduler.filter_tasks(pet_name="Buddy", completed=False)
    assert len(result) == 1
    assert result[0].name == "Feeding"


# Multi-pet: conflict detection spans all pets, not just one
def test_conflict_detection_across_multiple_pets():
    owner = Owner(name="Alex", email="alex@example.com")
    buddy = Pet(name="Buddy", species="Dog", breed="Labrador", age=3)
    whiskers = Pet(name="Whiskers", species="Cat", breed="Tabby", age=2)
    owner.register_pet(buddy)
    owner.register_pet(whiskers)
    owner.scheduler = Scheduler(owner=owner)

    buddy.assign_task(Task(name="Feeding", time="08:00", priority=1, description="Dry food"))
    candidate = Task(name="Brushing", time="08:00", priority=2, description="Fur brush")

    conflicts = owner.scheduler.detect_conflicts(candidate)
    assert len(conflicts) == 1
    assert conflicts[0].name == "Feeding"
    
    
## AGENTIC TEST CASES 


# --- Profile Rule ---

def test_profile_rule_fills_empty_pet():
    owner = Owner(name="Alex", email="alex@example.com")
    pet = Pet(name="Buddy", species="dog", breed="Labrador", age=3)
    owner.register_pet(pet)
    PawAgent(owner=owner).run()
    assert len(pet.tasks) > 0


def test_profile_rule_marks_tasks_agent_created():
    owner = Owner(name="Alex", email="alex@example.com")
    pet = Pet(name="Buddy", species="dog", breed="Labrador", age=3)
    owner.register_pet(pet)
    PawAgent(owner=owner).run()
    assert all(t.agent_created for t in pet.tasks)


def test_profile_rule_skips_pet_with_existing_tasks():
    owner = Owner(name="Alex", email="alex@example.com")
    pet = Pet(name="Buddy", species="dog", breed="Labrador", age=3)
    pet.assign_task(Task(name="Walk", time="07:00", priority=2, description=""))
    owner.register_pet(pet)
    decisions = PawAgent(owner=owner).run()
    profile_decisions = [d for d in decisions if d.rule == "ProfileRule"]
    assert len(profile_decisions) == 0


# --- Urgency Rule ---

def test_urgency_rule_escalates_overdue_task():
    owner = Owner(name="Alex", email="alex@example.com")
    pet = Pet(name="Buddy", species="dog", breed="Labrador", age=3)
    task = Task(name="Walk", time="07:00", priority=4, description="",
                due_date=date.today() - timedelta(days=4))
    pet.assign_task(task)
    owner.register_pet(pet)
    PawAgent(owner=owner).run()
    assert task.priority < 4


def test_urgency_rule_skips_completed_tasks():
    owner = Owner(name="Alex", email="alex@example.com")
    pet = Pet(name="Buddy", species="dog", breed="Labrador", age=3)
    task = Task(name="Walk", time="07:00", priority=4, description="",
                due_date=date.today() - timedelta(days=4))
    task.mark_complete()
    pet.assign_task(task)
    owner.register_pet(pet)
    PawAgent(owner=owner).run()
    assert task.priority == 4


# --- Coverage Rule ---

def test_coverage_rule_adds_missing_feeding():
    owner = Owner(name="Alex", email="alex@example.com")
    pet = Pet(name="Buddy", species="dog", breed="Labrador", age=3)
    pet.assign_task(Task(name="Morning walk", time="07:00", priority=2, description=""))
    owner.register_pet(pet)
    PawAgent(owner=owner).run()
    names = [t.name.lower() for t in pet.tasks]
    assert any("feed" in n or "dinner" in n for n in names)


def test_coverage_rule_skips_fully_covered_pet():
    owner = Owner(name="Alex", email="alex@example.com")
    pet = Pet(name="Buddy", species="dog", breed="Labrador", age=3)
    pet.assign_task(Task(name="Feeding",      time="08:00", priority=1, description=""))
    pet.assign_task(Task(name="Morning walk", time="07:00", priority=2, description=""))
    pet.assign_task(Task(name="Grooming",     time="10:00", priority=3, description=""))
    owner.register_pet(pet)
    decisions = PawAgent(owner=owner).run()
    assert not any(d.rule == "CoverageRule" for d in decisions)


# --- Species Rule ---

def test_species_rule_adds_vet_check_for_senior_dog():
    owner = Owner(name="Alex", email="alex@example.com")
    pet = Pet(name="Buddy", species="dog", breed="Labrador", age=8)
    pet.assign_task(Task(name="Walk", time="07:00", priority=2, description=""))
    owner.register_pet(pet)
    PawAgent(owner=owner).run()
    assert any(t.name.lower() == "vet check" for t in pet.tasks)


def test_species_rule_no_vet_check_for_young_dog():
    owner = Owner(name="Alex", email="alex@example.com")
    pet = Pet(name="Buddy", species="dog", breed="Labrador", age=3)
    pet.assign_task(Task(name="Walk", time="07:00", priority=2, description=""))
    owner.register_pet(pet)
    PawAgent(owner=owner).run()
    assert not any(t.name.lower() == "vet check" for t in pet.tasks)


def test_species_rule_adds_midday_walk_for_high_energy_breed():
    owner = Owner(name="Alex", email="alex@example.com")
    pet = Pet(name="Max", species="dog", breed="husky", age=3)
    pet.assign_task(Task(name="Walk", time="07:00", priority=2, description=""))
    owner.register_pet(pet)
    PawAgent(owner=owner).run()
    assert any(t.name.lower() == "midday walk" for t in pet.tasks)


def test_species_rule_adds_litter_for_cat():
    owner = Owner(name="Alex", email="alex@example.com")
    pet = Pet(name="Luna", species="cat", breed="Persian", age=2)
    pet.assign_task(Task(name="Playtime", time="19:00", priority=3, description=""))
    owner.register_pet(pet)
    PawAgent(owner=owner).run()
    assert any(t.name.lower() == "litter box cleaning" for t in pet.tasks)


def test_species_rule_no_duplicate_litter_if_already_present():
    owner = Owner(name="Alex", email="alex@example.com")
    pet = Pet(name="Luna", species="cat", breed="Persian", age=2)
    pet.assign_task(Task(name="Litter box cleaning", time="09:00", priority=2, description=""))
    owner.register_pet(pet)
    PawAgent(owner=owner).run()
    count = sum(1 for t in pet.tasks if t.name.lower() == "litter box cleaning")
    assert count == 1

