# PawPal+

## Original Project

PawPal+ started as a Streamlit app for pet owners to manually track and schedule care tasks for their pets. Owners could register pets, assign tasks with a time, priority, and frequency, and the scheduler would sort tasks by priority and detect time conflicts. The system was entirely passive, the user was responsible for creating every task and resolving every issue.

---

## Title and Summary

This project is called PawPal+, an app to put all your pets needs in one place.  You can register a pet with attributes such as species, breed, age, etc. From here, you can assign tasks to these pets at different times, priorities, along with due dates. If you have a recurring task, once you complete it, it will automatically create another task for the next due date. If two events overlap, the system will warn you, since a pet can’t do two things at once. However, sometimes an owner has trouble figuring out what tasks are best for their pet. Many pets have different needs based on their species, breed, or their age. They also may have trouble assigning the correct attributes to each task.

This is where **PawAgent** comes in. PawAgent is a built-in AI that can create tasks for your pet based on the attributes you assigned to it. Whether it's creating a completely new set of tasks, building on tasks you’ve already listed, or just resolving conflicts, PawAgent allows you to see the best tasks for your pet, without you having to create your own tasks. PawAgent pulls from different data, such as what the species of the animal is and the specific breed. On top of this, after creating your tasks, PawAgent can generate a schedule so that you can plan your day.


---

## Architecture Overview

This system is broken into 4 parts. First, the user inputs the pet info, as well as any tasks if required. Then, there are 4 data models made: The owner, which has a scheduler and their pets. The pets then have their tasks. From these data models, the user can run PawAgent. PawAgent populates the tasks using a set of rules that gives instructions as to how and when to populate the tasks for different animals. These also have guardrails to enforce task caps, time ceilings, and idempotency. Finally, each rule produces an AgentDecision that shows up on the UI as a step-by-step reason for each task, as well as an updated schedule.

---

## Setup Instructions

### Prerequisites
- Python 3.10 or higher

### Installation

1. Clone the repository
2. Create a virtual environment:
   ```
   python -m venv .venv
   ```
3. Activate the virtual environment:
   - Windows: `.venv\Scripts\activate`
   - Mac/Linux: `source .venv/bin/activate`
4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

### Running the App
```
streamlit run app.py
```

### Running Tests
```
python -m pytest
```

---

## Sample Interactions

### Input 1 — Buddy (Dog, Labrador, Age 3) — No tasks
Buddy is registered with no tasks. PawAgent runs the Profile Rule and generates a full dog schedule from scratch. Because Labrador is a high-energy breed, the Species Rule also adds a Midday walk.

**Resulting schedule:**

![alt text](ex1.png)
---

### Input 2 — Mochi (Dog, Bulldog, Age 2) — Morning walk manually added at 08:00
Mochi already has one task. The Coverage Rule fills in the rest of the recommended dog schedule. Because Morning walk was added at 08:00 — the same time Feeding was going to be placed — the Conflict Rule moves Morning walk to 08:30. No Midday walk is added since Bulldog is not a high-energy breed.

**Resulting schedule:**

![alt text](ex2.png)

---

### Input 3 — Mochi (Cat, Abyssinian, Age 10) — No tasks
Mochi is a senior cat with no tasks. The Profile Rule generates a full cat schedule from scratch. The Species Rule then adds a weekly Vet check because Mochi is age 10 (≥ 7).

**Resulting schedule:**

![alt text](ex3.png)

## Design Decisions

**Rule-based AI instead of an LLM** — I used a rule based AI instead of an LLM because there were no APIs called, it was fully deterministic, and every decision is backed by logic. The trade-off is the knowledge. Because it is rule-based, the algorithm is very hardcoded.

**Agent is additive only** —  I also made the agent additive. It allows the user to input their own tasks, and only allows the agent to act if the user wants it to. The agent never removes user input, so it preserves intent while adding autonomously.

**Coverage rule aligned to the full template** — Originally, the Coverage Rule only filled missing categories (feeding, activity, hygiene), which meant a pet with one task got a worse schedule than a pet with no tasks. Aligning it to the full species template made behavior consistent regardless of starting state.

---

## Testing Summary

29 tests cover both the original scheduling system and the new PawAgent rules. All 29 passed. Tests cover the full agent pipeline: Profile Rule generating tasks for empty pets, Coverage Rule filling gaps, Species Rule adding breed- and age-specific tasks, Urgency Rule escalating overdue priorities, Conflict Rule retiming clashing slots, and all four guardrails (task cap, time ceiling, idempotency, priority clamp). The original 9 scheduler tests were preserved to confirm no regressions.

---

## Reflection

Building PawAgent taught me that rule-based AI requires hardcoding the AI logic explicitly. I have to make sure that every decision the agent needs to make is deliberately designed and written. Unlike an LLM that generalizes from training data, a rule-based agent only knows what you tell it. This made the system predictable and debuggable, but also highlighted the trade-off. Adding support for more species or breeds required more coding, rather than feeding data. The most valuable insight was that making an AI feel intelligent is less about the complexity of the algorithm and more about the quality of the reasoning it surfaces to the user. If the user can follow what the AI is doing, they can understand the thought process and logic behind it. 

## Demo Video:

Through Loom: https://www.loom.com/share/63959c622bb944a690a3ef0e38d8fffe

This video covers the examples shown in the sample interactions. It is a live demo of the end to end app run, showing pet generation, task addition, Agent features, and Schedule generation.
