# mom

**Your code’s mom.** She’s watching. And judging.

`mom` is a CLI tool that takes care of your codebase like a loving, slightly disappointed parent.  
It nudges you to commit, reminds you of your goals, nags you if you slack off, wraps best practices into a delightful package, and is now available via `pip install mom-cli`.

---

## ✨ Features

- 🧼 Checks for uncommitted changes and recent commits
- 🧹 Applies `ruff`, `black`, and `isort` to tidy up your code
- ☂️ Analyzes test coverage and points out weak spots
- 🧠 Lets you define your current dev goal (`plan`) and stay focused on it
- 💬 Suggests what to do next with a lovingly sarcastic tone

---

## 📦 Installation

You can install `mom` directly from PyPI:

```bash
pip install mom-cli
```

---

## 🚀 Available commands

| Command         | Description                                   |
|-----------------|-----------------------------------------------|
| `mom status`    | Checks for uncommitted changes and last commit |
| `mom tidy`      | Runs `black`, `ruff`, `isort` if available     |
| `mom cover`     | Runs tests with coverage and shows gaps        |
| `mom nag`       | Shames you for forgetting to commit            |
| `mom plan`      | Saves your current dev goal and focus area     |
| `mom focus`     | Reminds you what you were working on           |
| `mom suggest`   | Evaluates the state of your codebase and scolds you helpfully |

---

## 🖼️ Sample output

```bash
$ mom suggest

mom is thinking... 🧠

🧼 You have uncommitted changes.
You should commit, genius. That’s what Git is for.

☂️ Some files are poorly tested:
✗ app/core.py → 67.5%

🧹 Code could use a cleanup.
• ruff returned issues.

🧠 No current plan found.
Did you even tell me what you’re working on today?

📋 Summary:
✗ Commit state
✗ Test coverage
✗ Code style
✗ Active plan

✅ mom suggest completed. Whether you listen is another matter.
```

---

## ❤️ Philosophy

Your mom doesn’t fix your bugs.
But she does keep your space clean, your goals in sight, and your guilt levels high.

---
