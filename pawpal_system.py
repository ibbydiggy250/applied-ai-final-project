from dataclasses import dataclass, field
from datetime import date, timedelta

SPECIES_TEMPLATES: dict[str, list[dict]] = {
    "dog": [
        {"name": "Morning walk",  "time": "07:00", "priority": 2, "frequency": "daily"},
        {"name": "Feeding",       "time": "08:00", "priority": 1, "frequency": "daily"},
        {"name": "Evening walk",  "time": "18:00", "priority": 2, "frequency": "daily"},
        {"name": "Dinner",        "time": "18:30", "priority": 1, "frequency": "daily"},
        {"name": "Grooming",      "time": "10:00", "priority": 3, "frequency": "weekly"},
    ],
    "cat": [
        {"name": "Feeding",             "time": "08:00", "priority": 1, "frequency": "daily"},
        {"name": "Litter box cleaning", "time": "09:00", "priority": 2, "frequency": "daily"},
        {"name": "Dinner",              "time": "18:00", "priority": 1, "frequency": "daily"},
        {"name": "Playtime",            "time": "19:00", "priority": 3, "frequency": "daily"},
    ],
    "other": [
        {"name": "Feeding",          "time": "08:00", "priority": 1, "frequency": "daily"},
        {"name": "Habitat cleaning", "time": "10:00", "priority": 2, "frequency": "weekly"},
    ],
}

HIGH_ENERGY_BREEDS: set[str] = {
    "husky", "siberian husky", "border collie", "australian shepherd",
    "labrador", "golden retriever", "jack russell", "dalmatian",
    "vizsla", "weimaraner",
}


@dataclass
class Task:
    name: str
    time: str
    priority: int
    description: str
    frequency: str = "once"
    completed: bool = False
    due_date: date = field(default_factory=date.today)
    agent_created: bool = False

    def edit(self, name: str, time: str, priority: int, description: str, frequency: str) -> None:
        # Overwrites the task's attributes with the provided values.
        self.name = name
        self.time = time
        self.priority = priority
        self.description = description
        self.frequency = frequency

    def mark_complete(self) -> None:
        # Sets the task as completed.
        self.completed = True

    def renew(self) -> "Task":
        # Recurring Task Algorithm: Instead of mutating the completed task, this creates a brand
        # new Task instance with an advanced due_date using timedelta arithmetic. This preserves
        # the history of the completed task while automatically queuing the next occurrence,
        # eliminating the need for manual re-entry of repeating care tasks.
        if self.frequency == "daily":
            next_due = self.due_date + timedelta(days=1)
        elif self.frequency == "weekly":
            next_due = self.due_date + timedelta(days=7)
        else:
            next_due = self.due_date
        return Task(
            name=self.name,
            time=self.time,
            priority=self.priority,
            description=self.description,
            frequency=self.frequency,
            due_date=next_due,
        )

    @property
    def due_in(self) -> str:
        # Returns a human-readable string of how many days until the task is due.
        days = (self.due_date - date.today()).days
        if days == 0:
            return "Due today"
        elif days == 1:
            return "Due tomorrow"
        else:
            return f"Due in {days} days"


@dataclass
class AgentDecision:
    rule: str
    action: str
    reasoning: str
    target: str


@dataclass
class Pet:
    name: str
    species: str
    breed: str
    age: int
    tasks: list[Task] = field(default_factory=list)

    def assign_task(self, task: Task) -> None:
        # Adds a task to the pet's task list.
        self.tasks.append(task)

    def get_summary(self) -> str:
        # Returns a formatted string of the pet's details and assigned task names.
        task_names = ", ".join(t.name for t in self.tasks) if self.tasks else "None"
        return f"{self.name} ({self.species}, {self.breed}, age {self.age}) | Tasks: {task_names}"


@dataclass
class Scheduler:
    owner: "Owner"

    def get_all_tasks(self) -> list[Task]:
        # Collects and returns all tasks from every pet owned by the owner.
        return [task for pet in self.owner.pets for task in pet.tasks]

    def generate_plan(self) -> list[Task]:
        # Returns all tasks sorted by priority, lowest number first (1 = highest priority).
        return sorted(self.get_all_tasks(), key=lambda t: t.priority)
    def filter_tasks(self, pet_name: str | None = None, completed: bool | None = None) -> list[Task]:
        # Filter Algorithm: Iterates all tasks once and applies up to two conditions (pet name,
        # completion status) in a single pass using a list comprehension. Using None as a sentinel
        # value makes each filter optional — only active filters are evaluated, avoiding separate
        # methods for every filter combination.
        return [
            task
            for pet in self.owner.pets
            for task in pet.tasks
            if (pet_name is None or pet.name == pet_name)
            and (completed is None or task.completed == completed)
        ]

    def detect_conflicts(self, candidate: Task) -> list[Task]:
        # Conflict Detection Algorithm: Before a task is added, this scans all existing tasks
        # across every pet for a matching time value. Because HH:MM strings compare correctly
        # as plain strings, no time parsing is needed. Returning a list (rather than a bool)
        # lets the UI name the specific conflicting tasks in the warning message.
        return [task for task in self.get_all_tasks() if task.time == candidate.time]

    def sort_by_time(self) -> list[Task]:
        # Sort Algorithm: Uses Python's built-in sorted() with a lambda key that extracts the
        # HH:MM string from each task. Because all times share the same fixed format, lexicographic
        # string comparison is equivalent to chronological order — no datetime parsing required,
        # keeping the sort lightweight and readable.
        return sorted(self.get_all_tasks(), key=lambda t: t.time)


@dataclass
class Owner:
    name: str
    email: str
    pets: list[Pet] = field(default_factory=list)
    scheduler: Scheduler = None

    def register_pet(self, pet: Pet) -> None:
        # Adds a pet to the owner's pet list.
        self.pets.append(pet)

    def create_task(self, name: str, time: str, priority: int, description: str, frequency: str = "daily") -> Task:
        # Instantiates and returns a new Task with the given attributes.
        return Task(name=name, time=time, priority=priority, description=description, frequency=frequency)


@dataclass
class PawAgent:
    owner: Owner
    decisions: list[AgentDecision] = field(default_factory=list)

    def run(self) -> list[AgentDecision]:
        self.decisions = []
        self._profile_rule()
        return self.decisions

    def _profile_rule(self) -> None:
        # For every pet with no tasks, generate a full schedule from SPECIES_TEMPLATES.
        for pet in self.owner.pets:
            if pet.tasks:
                continue
            templates = SPECIES_TEMPLATES.get(pet.species, SPECIES_TEMPLATES["other"])
            for t in templates:
                task = Task(
                    name=t["name"],
                    time=t["time"],
                    priority=t["priority"],
                    description=f"Auto-generated for {pet.name}",
                    frequency=t["frequency"],
                    agent_created=True,
                )
                pet.assign_task(task)
                self.decisions.append(AgentDecision(
                    rule="ProfileRule",
                    action=f"Added '{t['name']}' to {pet.name}",
                    reasoning=f"{pet.name} had no tasks; generated default {pet.species} schedule",
                    target=pet.name,
                ))
