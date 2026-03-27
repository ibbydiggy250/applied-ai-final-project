from pawpal_system import Task, Pet


def test_mark_complete_sets_completed_true():
    task = Task(name="Walk", duration=30, priority=3, description="Morning walk")
    task.mark_complete()
    assert task.completed is True


def test_assign_task_increases_pet_task_count():
    pet = Pet(name="Buddy", species="Dog", breed="Labrador", age=3)
    task = Task(name="Feeding", duration=10, priority=5, description="Dry food")
    pet.assign_task(task)
    assert len(pet.tasks) == 1
