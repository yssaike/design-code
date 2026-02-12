# Setup Guide — Design Code

Follow these steps once to get everything running.

---

## 1. Move the folder to your Desktop

Move the entire `design-code` folder to your Desktop (or wherever you'd like it).

## 2. Create a GitHub repo

1. Go to https://github.com/new
2. Name it **design-code**
3. Set it to **Public** (so the commits show on your profile graph)
4. Do NOT add a README (we already have one)
5. Click **Create repository**

## 3. Initialize git and push

Open Terminal, then run:

```bash
cd ~/Desktop/design-code
git init
git add -A
git commit -m "initial commit — design token system"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/design-code.git
git push -u origin main
```

Replace `YOUR_USERNAME` with your actual GitHub username.

## 4. Daily usage

Every day (or whenever you want greener squares), open Terminal and run:

```bash
cd ~/Desktop/design-code
python3 commit.py
```

It will ask you how many commits to make, then push them all automatically.

---

## Tips

- **3–6 commits per day** looks natural and active.
- The script picks from 60+ unique design-themed messages, so your history will look varied and professional.
- Each commit modifies real JSON token files, so the diffs look legitimate if anyone checks.
- Your CHANGELOG.md will build up over time as a nice log of all changes.

That's it — enjoy your greener GitHub!
