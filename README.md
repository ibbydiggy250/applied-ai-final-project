# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

# Smarter Scheduling

    We implemented some algorithms in this project to make it smarter. One thing was sorting and filtering by time, pet name, and completion. This was to allow better viewing experience and more ordered tasks. Another was automating recurring tasks. If a task is daily, and you mark it complete, it will create a new task for tomorrow. If a task is weekly, and you mark it complete, it will be due in 7 days. This is to automate things better for the user, ensuring them putting daily or weekly actually reflects onto the app. Finally, we used conflict detection to ensure the user is not putting two tasks at the same time.

# Testing PawPal+
To run: python -m pytest

I have 9 tests running to ensure system reliability. These tests cover ensuring completed actually gets marked, tasks are added to the list, out-of-order tasks become sorted, conflict detection is ensured, making sure an empty schedule does not crash, a task on pet a blocks pet b at the same time, a completed task still blocks a new task at the same time, and with two pets and mixed completion only the completed pets task is returned.

I would give my reliability a 4/5, since these tests cover both happy path and edge cases, which is important to ensure user experience is not deterred.

# Features
Task Filtering:
Filter the task table by pet name, completion status, or both simultaneously. Built as a single-pass list comprehension using None as a sentinel — only active filters are evaluated, so no separate methods are needed for each combination.

Sort by Time:
Sort all tasks chronologically by their scheduled time. Because all times follow HH:MM format, Python's built-in sorted() with a string key works correctly without any datetime parsing — lexicographic order matches chronological order.

Recurring Tasks:
Mark a daily or weekly task complete and a new instance is automatically created for the next occurrence — tomorrow for daily, 7 days later for weekly. The original task is preserved as completed; timedelta arithmetic advances the due date on the new task.

Conflict Detection:
Before any task is added, the scheduler checks all existing tasks across every pet for a matching time slot. If a conflict is found, the user sees a warning naming the clashing task — and the new task is blocked from being added without crashing the app.

# Demo

<a href="/course_images/ai110/demo.png" target="_blank"><img src='/course_images/ai110/demo.png' title='PawPal App' width='' alt='PawPal App' class='center-block' /></a>

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.
