# Model Card — PawPal+ / PawAgent

## Reflection

**What are the limitations or biases in your system?**

Because this AI is hardcoded, it has a few limitations. The main limitation is the knowledge-base. Since I don't have an LLM connected, the PawAgent is following a hardcoded set of rules rather than making its own decisions based on the current context. A bias that exists in my code are the tasks that I believe to be best for each species, or what breeds I consider to be high energy. A person may have an animal that is high energy but their breed is considered low-energy in my code. However, this bias is mitigated by the fact that the user can input their own tasks too. This makes sure that if the PawAgent misses or adds something, the user can remove or add more to it.

---

**Could your AI be misused, and how would you prevent that?**

The agent can generate an inappropriate task list if the user doesn't add the right parameters. For example, if a person has a bunny but they register it as a dog, the PawAgent would generate a full dog schedule, which wouldn't be appropriate for the user's pet. Because the PawAgent acts autonomously without confirmation, wrong inputs directly lead to wrong outputs. The main preventions of this are the guardrails in place and the flexibility the agent provides. If the schedule is not what the user expected, they can add their own tasks and update the schedule. On top of this, the PawAgent gives visible reasonings for each decision it makes, so the user can pick up quickly where the AI went wrong.

---

**What surprised you while testing your AI's reliability?**

I was surprised about how important the guardrails I implemented were, and how the order of the agent rules matter a lot. For example, without the idempotency guardrail, you could run the agent multiple times, generating duplicate tasks, effectively breaking the use. On top of this, the order that the rules fire in matter. The Conflict Rule has to run last, otherwise the Coverage and Species Rules can create new conflicts after conflicts have already been resolved.

---

**Describe your collaboration with AI during this project. Identify one instance when the AI gave a helpful suggestion and one instance where its suggestion was flawed or incorrect.**

In this project, I acted mostly as the brain, while AI made the small feature requests I wanted. I implemented the idea of the PawAgent, created the different rules it had to follow, and the guardrails that went with it. I went feature by feature, making sure each thing worked before I moved on. Not only did I create tests for my features, I also went into the Streamlit and tested custom edge cases. The most helpful suggestion the AI gave was the idea of the idempotency rule. I had not thought of this one, and while implementing the guardrails, Claude recommended adding a guardrail to ensure no duplicate tasks from the agent. One time when it was flawed was when I asked it how to test for the urgency rule. It told me to set the due attribute for the past. However, at that point, I did not have a "due in" attribute, so Claude gave me a false test case. I did implement a due date attribute later on, since it seemed useful to add.
