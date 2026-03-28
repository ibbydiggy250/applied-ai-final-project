from dataclasses import dataclass, field


@dataclass
class Task:
    name: str
    duration: int
    priority: int
    description: str
    frequency: str = "once"
    completed: bool = False

    def edit(self, name: str, duration: int, priority: int, description: str, frequency: str) -> None:
        # Overwrites the task's attributes with the provided values.
        self.name = name
        self.duration = duration
        self.priority = priority
        self.description = description
        self.frequency = frequency

    def mark_complete(self) -> None:
        # Sets the task as completed.
        self.completed = True


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


@dataclass
class Owner:
    name: str
    email: str
    pets: list[Pet] = field(default_factory=list)
    scheduler: Scheduler = None

    def register_pet(self, pet: Pet) -> None:
        # Adds a pet to the owner's pet list.
        self.pets.append(pet)

    def create_task(self, name: str, duration: int, priority: int, description: str, frequency: str = "daily") -> Task:
        # Instantiates and returns a new Task with the given attributes.
        return Task(name=name, duration=duration, priority=priority, description=description, frequency=frequency)
