# PawPal+ Project Reflection

## 1. System Design
Actions:
Add/remove tasks
Register pets
View and order tasks(Schedule building)

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

The classes I chose were Owner, Pet, Schedule, and Task. My UML was as follows: An owner owns a pet, creates a schedule and creates a task. The pet has a schedule and is assigned a task. A schedule contains a task. The owner could register a pet, create a task and a schedule. Pets could be assigned tasks,schedules, and can generate summaries. Schedules can add and remove tasks, as well as generate a plan based on priority. A task is lowest on the UML diagram, being able to be edited and marked complete.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Yes, it did change. Originally, both the schedule and the pet had tasks as attributes. The issue was that they were both pointing to the same tasks in two different methods, which would cause issues with updating one another. Because of this, we changed the task list from pet to a derived property from the schedule tasks.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

The scheduler considers priority as a constraint. Tasks are given priority, and based on that are ordered. This mattered the most because an owner would like to priortize different things, like walking before cleaning, or eating before walking, so this just made those priorities clearer, which is why I picked this as my contraint

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

One tradeoff I made was that when generating a plan, the scheduler sorts purely based on priority, ignoring time. However, I found this tradeoff reasonable because inherintely, priority comes with an ordered timing, and some things may need to happen no matter of the time. Priority makes more sense to order than duration. Also, detect conflicts only relies on if the HH:MM matches. For example, you could have one thing at 08:00 and another at 08:10. Even if the activities overlap, you are able to put them both because the times are different. This is reasonable for now because it is for simplicity, but overlaps can happen.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

One example is when I asked it to look at the renew function, and see if I could simplify it. However, it told me to swap the if else statements with a dictionary lookup. While this was technically a more efficient and pythonic way of doing things, I figured it was harder to follow what it was doing. Thus, I kept the if else statements in order to make it human readable.
---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
