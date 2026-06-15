# 🤝 Contributing To GhostIntel

<p align="center">
  <b>Hey! Thanks for taking the time to contribute to GhostIntel! 👋</b><br>
  <i>Anyone can contribute — even without writing a single line of code!</i>
</p>

<div align="center">

[![Contributions](https://img.shields.io/badge/Contributions-Welcome-brightgreen?style=for-the-badge)](https://github.com/ruyynn/GhostIntel)
[![PRs](https://img.shields.io/badge/PRs-Open-9b59b6?style=for-the-badge)](https://github.com/ruyynn/GhostIntel/pulls)
[![Issues](https://img.shields.io/badge/Issues-Report-ff6b6b?style=for-the-badge)](https://github.com/ruyynn/GhostIntel/issues)

</div>

---

## 📖 Table of Contents

- [Ground Rules](#-ground-rules)
- [Ways to Contribute](#-ways-to-contribute)
- [Setting Up Your Environment](#-setting-up-your-environment)
- [Step-by-Step Guide (with Code)](#-step-by-step-guide-with-code)
- [What Can I Work On?](#-what-can-i-work-on)
- [Code Style Guidelines](#-code-style-guidelines)
- [Commit Message Format](#-commit-message-format)
- [Pull Request Guide](#-pull-request-guide)
- [Reporting Bugs](#-reporting-bugs)
- [Suggesting Features](#-suggesting-features)
- [FAQ for Beginners](#-faq-for-beginners)
- [Contact](#-contact)

---

## 📋 Ground Rules

Before anything else, please read these rules:

- ❌ **Do not** remove or modify the copyright notice
- ❌ **Do not** redistribute this project commercially without written permission
- ❌ **Do not** submit code that is copied from other projects without proper credit
- ✅ **Do** fork, contribute, and open pull requests freely
- ✅ **Do** be respectful and constructive in all discussions
- ✅ **Do** test your changes before submitting
- ✅ **Do** write clear descriptions in your pull requests and issues

> All contributions are subject to the [MIT License](LICENSE).

---

## 🎯 Ways to Contribute

### 🟢 No Coding Required (Perfect for Beginners!)

You don't need to know how to code to help GhostIntel grow. Here are easy ways to contribute:

| Type | How To |
|------|--------|
| ⭐ **Star the repo** | Click the **Star** button at the top right of the repository page |
| 🐛 **Report a bug** | Open the **Issues** tab and describe what went wrong |
| 💡 **Suggest a feature** | Open the **Discussions** tab and share your idea |
| 📝 **Fix a typo** | Edit `README.md` or any `.md` file directly on GitHub |
| 📢 **Spread the word** | Share GhostIntel with friends, communities, or cybersecurity groups |
| 🧪 **Test the tool** | Run GhostIntel and report anything that feels broken or off |
| 📸 **Share screenshots** | Share your output screenshots (with targets you own/have permission for) |

### 🔵 With Coding (Beginner Friendly!)

| Difficulty | Contribution Idea | Target File |
|------------|-------------------|-------------|
| ⭐ Easy | Add a new phone provider prefix | `sources/phone_db.py` |
| ⭐ Easy | Add a new username platform | `sources/social_media.py` |
| ⭐ Easy | Fix a typo in code comments | Any file |
| ⭐⭐ Medium | Fix a small bug | `modules/*.py` |
| ⭐⭐ Medium | Improve error messages | `modules/*.py` or `core/engine.py` |
| ⭐⭐ Medium | Improve an existing module | `modules/*.py` |
| ⭐⭐⭐ Hard | Add a brand new module | `modules/` + `core/engine.py` |
| ⭐⭐⭐ Hard | Add a new country to phone OSINT | `modules/phone.py` + `sources/phone_db.py` |
| ⭐⭐⭐ Hard | Improve the HTML report template | `reports/html_template.py` |

> **Not sure where to start?** Look for issues labeled `good first issue` or `help wanted` in the [Issues tab](https://github.com/ruyynn/GhostIntel/issues).

---

## 🛠️ Setting Up Your Environment

Before you start coding, set up your local development environment by following these steps.

### Requirements

- **Python 3.8 or higher** — [Download here](https://python.org/downloads)
- **Git** — [Download here](https://git-scm.com/downloads)
- A code editor — [VS Code](https://code.visualstudio.com/) is recommended

### Check Your Versions

Open a terminal and run:

```bash
python --version    # Should be 3.8 or higher
git --version       # Any recent version is fine
```

### Fork & Clone the Repository

**Step 1 — Fork**

Go to [https://github.com/ruyynn/GhostIntel](https://github.com/ruyynn/GhostIntel) and click the **Fork** button at the top right. This creates your own copy of the repository under your GitHub account.

**Step 2 — Clone your fork**

```bash
git clone https://github.com/YOUR_USERNAME/GhostIntel.git
cd GhostIntel
```

> Replace `YOUR_USERNAME` with your actual GitHub username.

**Step 3 — Add the original repo as upstream**

This lets you pull in future updates from the original repository:

```bash
git remote add upstream https://github.com/ruyynn/GhostIntel.git
```

**Step 4 — Install dependencies**

```bash
# Recommended: use a virtual environment
python -m venv venv

source venv/bin/activate        # Linux / macOS
# venv\Scripts\activate         # Windows

pip install -r requirements.txt
```

**Step 5 — Verify everything works**

```bash
python ghostintel.py -h
```

If you see the help menu, you're all set! ✅

---

## 🚀 Step-by-Step Guide (with Code)

### 1️⃣ Make Sure Your Fork is Up to Date

Before starting any work, sync your fork with the latest changes from the original repo:

```bash
git checkout main
git fetch upstream
git merge upstream/main
```

### 2️⃣ Create a New Branch

**Always** create a new branch for your changes. Never work directly on `main`.

```bash
git checkout -b your-branch-name
```

**Branch naming conventions:**

| Type | Format | Example |
|------|--------|---------|
| New feature | `feat/description` | `feat/add-twitter-lookup` |
| Bug fix | `fix/description` | `fix/phone-parser-crash` |
| Documentation | `docs/description` | `docs/update-readme` |
| Code improvement | `refactor/description` | `refactor/clean-engine` |

### 3️⃣ Make Your Changes

Edit the relevant files. Here are some common contribution examples:

**Example A — Adding a new username platform** (`sources/social_media.py`):

```python
# Find the _load_platforms() method and add your platform to the list
{"name": "YourPlatform", "url": "https://yourplatform.com/{}", "category": "social"},
```

**Example B — Adding a phone provider prefix** (`sources/phone_db.py`):

```python
# Find the correct country section and add the prefix
'0812': 'Your Provider Name',
```

**Example C — Adding a new country to phone OSINT** (`modules/phone.py`):

```python
# Add country code to self.country_codes
self.country_codes = {
    'ID': 62, 'US': 1, 'GB': 44, 'MY': 60, 'IN': 91,
    'AU': 61  # ← your new country
}
```

### 4️⃣ Test Your Changes

Always test before submitting. Run GhostIntel and verify your changes work correctly:

```bash
python ghostintel.py -u testuser
python ghostintel.py -p 08123456789
python ghostintel.py -d example.com
python ghostintel.py -i 8.8.8.8
```

Make sure:
- The program runs without errors
- Your changes produce the expected output
- You haven't broken any existing functionality

### 5️⃣ Commit Your Changes

```bash
git add .
git commit -m "feat: add TikTok platform to username checker"
```

See [Commit Message Format](#-commit-message-format) below for proper conventions.

### 6️⃣ Push to Your Fork

```bash
git push origin your-branch-name
```

### 7️⃣ Open a Pull Request

1. Go to your fork on GitHub: `https://github.com/YOUR_USERNAME/GhostIntel`
2. You'll see a banner saying **"Compare & pull request"** — click it
3. Fill in the PR title and description using the [template below](#pull-request-template)
4. Click **Create pull request**

---

## 🔍 What Can I Work On?

### Adding a New Username Platform

File: `sources/social_media.py`

Each platform entry follows this format:

```python
{
    "name": "PlatformName",       # Display name
    "url": "https://example.com/{}",  # {} is replaced by the username
    "category": "social"          # Category: social, dev, gaming, music, video, forum, etc.
}
```

**Categories available:**

| Category | Examples |
|----------|---------|
| `social` | Facebook, Instagram, Twitter |
| `dev` | GitHub, GitLab, CodePen |
| `gaming` | Steam, Roblox, Chess.com |
| `music` | Spotify, SoundCloud |
| `video` | YouTube, Twitch, Vimeo |
| `forum` | Reddit, Quora |
| `professional` | LinkedIn, AngelList |
| `freelance` | Upwork, Fiverr |
| `blog` | Medium, Tumblr |
| `messaging` | Telegram |
| `funding` | Patreon, Ko-fi |

### Adding a Phone Provider Prefix

File: `sources/phone_db.py`

Find your country's section and add the prefix → provider mapping:

```python
'ID': {
    '0812': 'Telkomsel',
    '0856': 'Indosat',
    # Add your new prefix here:
    '0838': 'New Provider',
},
```

### Adding a New Country to Phone OSINT

This requires changes in two files:

1. **`modules/phone.py`** — Add to `self.country_codes` dict
2. **`sources/phone_db.py`** — Add a new country section with prefix data

Please open an [Issue](https://github.com/ruyynn/GhostIntel/issues) first to discuss the addition before starting.

### Fixing a Bug

1. First, check if the bug already has an open [Issue](https://github.com/ruyynn/GhostIntel/issues)
2. If not, create one to describe the bug
3. Comment on the issue saying you'll work on it
4. Then follow the contribution steps above

---

## ✏️ Code Style Guidelines

GhostIntel follows standard Python conventions. Please follow these rules when writing code:

### General

- Use **4 spaces** for indentation (no tabs)
- Keep line length under **100 characters**
- Add **docstrings** to all functions and classes
- Use **type hints** where possible

```python
# ✅ Good
async def scan(self, target: str) -> Dict:
    """Scan the given target and return results."""
    pass

# ❌ Bad
async def scan(self, target):
    pass
```

### Naming Conventions

| Type | Convention | Example |
|------|-----------|---------|
| Variables | `snake_case` | `phone_number` |
| Functions | `snake_case` | `def get_provider()` |
| Classes | `PascalCase` | `class PhoneModule` |
| Constants | `UPPER_SNAKE_CASE` | `MAX_THREADS = 20` |

### Error Handling

Always handle exceptions gracefully. Don't let the program crash silently:

```python
# ✅ Good
try:
    result = await self.session.get(url, timeout=5)
except asyncio.TimeoutError:
    pass  # or log it
except Exception as e:
    console.print(f"[red]Error: {str(e)}[/red]")

# ❌ Bad
result = await self.session.get(url)  # No error handling
```

### Comments

Write comments that explain **why**, not just **what**:

```python
# ✅ Good
# Skip private IPs — geolocation APIs don't support them
if ip_obj.is_private:
    return {}

# ❌ Bad
# Check if private
if ip_obj.is_private:
    return {}
```

---

## 📝 Commit Message Format

Use clear and consistent commit messages following this format:

```
type: short description (max 72 characters)

Optional longer description explaining WHY the change was made.
```

### Types

| Type | When to Use |
|------|-------------|
| `feat` | Adding a new feature |
| `fix` | Fixing a bug |
| `docs` | Documentation changes only |
| `refactor` | Code restructuring (no new features or bug fixes) |
| `style` | Formatting changes (spaces, indentation, etc.) |
| `test` | Adding or fixing tests |
| `chore` | Maintenance tasks (update deps, cleanup, etc.) |

### Examples

```bash
feat: add Discord platform to username checker
fix: handle timeout error in domain DNS lookup
docs: update README installation guide
refactor: simplify phone number normalization logic
style: fix indentation in email module
chore: update aiohttp to 3.9.1
```

---

## 🔃 Pull Request Guide

### Before Submitting

- [ ] My code follows the style guidelines above
- [ ] I tested my changes and everything works
- [ ] I haven't broken any existing features
- [ ] My commit messages follow the format above
- [ ] I've added comments to explain complex logic

### Pull Request Template

When you open a PR, fill in this template:

```markdown
## Description
What does this PR do? Why is it needed?

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Code refactor
- [ ] Other: ...

## Changes Made
- Added XYZ to file ABC
- Fixed bug where ...
- Updated ...

## How to Test
1. Run: `python ghostintel.py -u testuser`
2. Check that ...
3. Expected output: ...

## Screenshots (if applicable)
[Paste screenshots here]

## Checklist
- [ ] Tested locally
- [ ] No existing features broken
- [ ] Code is clean and commented
```

### What Happens After You Submit?

1. A maintainer will review your PR within **1–7 days**
2. They may request changes — that's completely normal!
3. Once approved, your PR will be merged into `main`
4. Your contribution will be live in the next release 🎉

---

## 🐛 Reporting Bugs

Found a bug? Please report it! Here's how to write a good bug report:

**Go to:** [Issues tab](https://github.com/ruyynn/GhostIntel/issues) → **New Issue**

### Bug Report Template

```markdown
## Bug Description
A clear description of what the bug is.

## Steps to Reproduce
1. Run: `python ghostintel.py -p 08123456789`
2. See error at step...

## Expected Behavior
What should have happened.

## Actual Behavior
What actually happened (include error messages).

## Environment
- OS: Windows 10 / Ubuntu 22.04 / macOS 13
- Python version: 3.10.x
- GhostIntel version: 2.0.0

## Error Output
```
Paste the full error traceback here
```

## Additional Notes
Any other context that might be helpful.
```

---

## 💡 Suggesting Features

Have an idea for a new feature? We'd love to hear it!

**Go to:** [Discussions tab](https://github.com/ruyynn/GhostIntel/discussions) → **New Discussion**

### Feature Request Template

```markdown
## Feature Summary
One sentence describing the feature.

## Problem It Solves
What problem does this feature address? Who benefits from it?

## Proposed Solution
How do you imagine this feature would work?

## Example Usage
ghostintel --new-flag target

## Alternatives Considered
Any other solutions you've thought about?

## Additional Context
Screenshots, references, or anything else relevant.
```

> **Note:** Complex features should be discussed in Discussions **before** you start coding. This avoids wasted effort if the feature doesn't align with the project direction.

---

## ❓ FAQ for Beginners

<details>
<summary><b>I've never contributed to open source before. Where do I start?</b></summary>
<br>
Start small! The easiest contributions are:

1. Star the repository ⭐
2. Report a bug you found
3. Fix a typo in the README or documentation
4. Add a new platform to `sources/social_media.py` — it's just adding one line to a list

Once you're comfortable, move on to bug fixes and features.
</details>

<details>
<summary><b>What is a Fork?</b></summary>
<br>
A fork is your own personal copy of the GhostIntel repository on your GitHub account. You can make any changes to your fork without affecting the original repository. When you're happy with your changes, you submit a Pull Request to propose merging them into the original.
</details>

<details>
<summary><b>What is a Pull Request (PR)?</b></summary>
<br>
A Pull Request is a way to say: "Hey, I made some changes in my fork — can you review and add them to the main project?" The maintainer reviews your code, may ask for changes, and then merges it if everything looks good.
</details>

<details>
<summary><b>What is a Branch?</b></summary>
<br>
A branch is an isolated copy of the code where you can make changes without affecting the main codebase. Think of it like a draft. You work on your draft, and when it's ready, you merge it back.

Always create a new branch for each contribution:
```bash
git checkout -b feat/my-new-feature
```
</details>

<details>
<summary><b>I made a mistake in my commit. Can I fix it?</b></summary>
<br>
Yes! If you haven't pushed yet:
```bash
git commit --amend -m "corrected commit message"
```

If you already pushed, just make another commit with the fix. Maintainers can help clean up history during the review process.
</details>

<details>
<summary><b>My PR has merge conflicts. What do I do?</b></summary>
<br>
This happens when the main branch changed after you created your branch. To fix it:

```bash
git fetch upstream
git checkout your-branch-name
git rebase upstream/main
```

Resolve any conflicts in the affected files, then:
```bash
git add .
git rebase --continue
git push origin your-branch-name --force
```
</details>

<details>
<summary><b>How long does a PR review take?</b></summary>
<br>
Usually between **1–7 days**, depending on the maintainer's availability and the complexity of the changes. Small, clean PRs are reviewed faster. Be patient — this is a volunteer-maintained project!
</details>

<details>
<summary><b>Can I contribute if I'm outside Indonesia?</b></summary>
<br>
Absolutely! GhostIntel welcomes contributors from anywhere in the world. Adding support for more countries (phone providers, local platforms, etc.) is especially appreciated.
</details>

<details>
<summary><b>What if my PR gets rejected?</b></summary>
<br>
Don't be discouraged! Rejections are usually accompanied by feedback explaining why. Read the feedback carefully, make the requested changes, and resubmit. Every contributor goes through this — it's part of the process.
</details>

---

## 📞 Contact

Have questions that aren't covered here? Reach out directly:

<p align="center">
  <a href="mailto:ruyynn25@gmail.com">
    <img src="https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white">
  </a>
  <a href="https://github.com/ruyynn">
    <img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white">
  </a>
  <a href="https://web.facebook.com/profile.php?id=61587795784907">
    <img src="https://img.shields.io/badge/Facebook-1877F2?style=for-the-badge&logo=facebook&logoColor=white">
  </a>
</p>

- 🐛 **Bug reports** → [GitHub Issues](https://github.com/ruyynn/GhostIntel/issues)
- 💡 **Feature ideas** → [GitHub Discussions](https://github.com/ruyynn/GhostIntel/discussions)
- ❓ **Quick questions** → DM on social media above
- 🤝 **Collaboration** → [Contact Me](mailto:ruyynn25@gmail.com)

---

## ⭐ Thank You!

<p align="center">
  <b>Thank you so much for contributing! 🙏</b><br>
  <i>Every contribution — no matter how small — makes GhostIntel better for everyone.</i>
</p>

<p align="center">
  <a href="https://github.com/ruyynn/GhostIntel">
    <img src="https://img.shields.io/github/stars/ruyynn/GhostIntel?style=for-the-badge&logo=github&color=gold&label=Star%20Repo">
  </a>
</p>

<p align="center">
  <b>© 2026 Ruyynn.</b>
</p>
