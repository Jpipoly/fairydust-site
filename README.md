# Fairydust Ventures website

Static redesign of fairydust.vc. No build step.

- `index.html` — home (value prop, how it works, the boring work, team, paths)
- `investors.html` — For Investors (SPV model + deals list)
- `founders.html` — For Founders (pitch form)

## Run locally

```bash
python3 serve.py 8080
```
Open http://localhost:8080. `serve.py` mimics Vercel clean URLs.

## Forms
Forms currently open a pre-filled email to ohhey@fairydust.vc. Swap in Formspree, Tally, or a Vercel function for real submissions.

## Deploy
Import this repo in Vercel (framework preset: Other). `vercel.json` enables clean URLs.
