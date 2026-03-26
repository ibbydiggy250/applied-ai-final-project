from dataclasses import dataclass, field
from datetime import date


@dataclass
class Task:
    name: str
    duration: int
    priority: int
    description: str
    completed: bool = False

    def edit(self, name: str, duration: int, priority: int, description: str) -> None:
        pass

    def mark_complete(self) -> None:
        pass


@dataclass
class Schedule:
    date: date
    tasks: list[Task] = field(default_factory=list)
    pet: "Pet" = None

    @property
    def num_tasks(self) -> int:
        pass

    def add_task(self, task: Task) -> None:
        pass

    def remove_task(self, task: Task) -> None:
        pass

    def generate_plan(self) -> list[Task]:
        pass


@dataclass
class Pet:
    name: str
    species: str
    breed: str
    age: int
    schedule: Schedule = None

    @property
    def tasks(self) -> list[Task]:
        pass

    def assign_task(self, task: Task) -> None:
        pass

    def assign_schedule(self, schedule: Schedule) -> None:
        pass

    def get_summary(self) -> str:
        pass


@dataclass
class Owner:
    name: str
    email: str
    pets: list[Pet] = field(default_factory=list)

    def register_pet(self, pet: Pet) -> None:
        pass

    def create_task(self, name: str, duration: int, priority: int, description: str) -> Task:
        pass

    def create_schedule(self, pet: Pet, date: date) -> Schedule:
        pass
