# Find the Function: a code search challenge

Starter kit for the code search challenge at **Golem Mini-Hackathon**, in partnership with JetBrains.

**The idea:** you get a plain-English description like *"Downloads Dailymotion videos by URL"* and 1000 Python functions. Rank them so the function that the query describes comes first. You're scored with MRR@100 on a hidden test set.

[//]: # (Everything about the task, the scoring and the rules is in the **[challenge PDF]&#40;docs/challenge_description.pdf&#41;**. Give it a read; it's not as long as it looks.)

## What's in here

```
├── notebook.ipynb            # start here
├── evaluate.py               # the scorer we use
├── requirements.txt
├── data/
│   ├── train.jsonl.gz          # 250653 matching (query, code) pairs
│   ├── dev_queries.jsonl       # 5000 queries      {query_id, pool, query}
│   ├── dev_candidates.jsonl    # 5000 functions    {candidate_id, pool, code}
│   ├── dev_answers.csv         # the right answer for each dev query
│   ├── test_queries.jsonl      # 5000 queries you're scored on
│   └── test_candidates.jsonl   # 5000 functions (answers stay with us)
├── submissions/
│   └── sample_submission_test.csv
└── docs/
    ├── challenge_description.pdf   # task, scoring, rules
    ├── data_card.md                # fields, stats, known quirks
    └── background.md               # the original benchmark and what we changed
```

## Quick start

**1.** Clone the repository
```bash
git clone https://github.com/majamuchowicz/golem-minihackathon.git
```
**2.** In your preferred coding tool open the **golem-minihackathon** folder and set up the virtual environment

**3.** Install the dependencies
```bash
pip install -r requirements.txt
```

[//]: # (## A few things that will save you time)

[//]: # ()
[//]: # (- **Every query has exactly one right answer, and it's in the query's own pool** &#40;`pool` 0-4, 1000 functions each&#41;. You never rank all 5000)

[//]: # (- **Dev and test code is anonymised**: every function is `Func`, and every variable is `arg_0`, `arg_1`, … Training code still has its real names, so watch out for that if you train a model)

[//]: # (- **Check every change on dev** with `evaluate.py`. If your score suddenly jumps way above the baseline, it's probably a bug, not genius. Look before you celebrate.)

[//]: # (- **Keep a short log in `METHOD.md`**: what you changed, the dev score, and whether it helped. You'll need it for the presentation anyway.)

## Submitting

A CSV file with a header and up to 100 rows per test query, best first:

```
query_id,candidate_id,rank
Tq00000,Tc00763,1
Tq00000,Tc00823,2
```

Use `evaluate.py` for development and checking the format of your submission:

```bash
python evaluate.py data/dev_answers.csv submissions/submission_dev.csv data/dev_candidates.jsonl
```

[//]: # (__!! dodać jak oddają submissions !!__)

[//]: # (czy oceniamy raz, tylko na końcu?)

[//]: # (Send your test file, code, model files and `METHOD.md` via **[form / e-mail / link]** before the deadline. The full list is in Section 7 of the PDF.)

## Where the data comes from

The data is adapted from CodeSearchNet AdvTest ([CodeXGLUE](https://github.com/microsoft/CodeXGLUE), Lu et al. 2021), built on the CodeSearchNet corpus (Husain et al. 2019), and distributed under the Computational Use of Data Agreement (C-UDA).
We changed a fair bit to make it fair and doable in a day; [docs/background.md](docs/background.md) has the details.

[//]: # (Found a bug in the kit, or something unclear? Reach out: **maja.muchowicz@jetbrains.com**)
