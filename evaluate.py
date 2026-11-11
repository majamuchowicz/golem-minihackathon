"""Official scorer for the Code Search Challenge.

Metric: MRR@100 (Mean Reciprocal Rank, cut off at rank 100).
For every query we look up the rank of its single correct candidate in your submission:
    score = 1 / rank   if the correct candidate is in your top 100,
    score = 0          otherwise (or if the query is missing from your file).
MRR@100 is the average of these scores over ALL queries. Higher is better; 1.0 is perfect.
Recall@1 and Recall@10 are reported for information (Recall@1 is the first tie-breaker).

Usage:
    python evaluate.py data/dev_answers.csv submission_dev.csv
"""
import csv
import sys
from collections import defaultdict

MAX_RANK = 100


class InvalidSubmission(Exception):
    pass


def load_answers(path):
    with open(path, newline="") as f:
        return {r["query_id"]: (r["candidate_id"], int(r["pool"])) for r in csv.DictReader(f)}


def load_submission(path, answers, candidate_pool=None):
    """Read and validate a submission. Raises InvalidSubmission with a readable message."""
    ranks = defaultdict(dict)        # query_id -> {candidate_id: rank}
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != ["query_id", "candidate_id", "rank"]:
            raise InvalidSubmission(f"header must be 'query_id,candidate_id,rank', got {reader.fieldnames}")
        for line_no, row in enumerate(reader, start=2):
            q, c = row["query_id"], row["candidate_id"]
            if q not in answers:
                raise InvalidSubmission(f"line {line_no}: unknown query_id {q!r}")
            try:
                r = int(row["rank"])
            except ValueError:
                raise InvalidSubmission(f"line {line_no}: rank is not an integer: {row['rank']!r}")
            if not 1 <= r <= MAX_RANK:
                raise InvalidSubmission(f"line {line_no}: rank must be 1..{MAX_RANK}, got {r}")
            if r in ranks[q].values():
                raise InvalidSubmission(f"line {line_no}: query {q} uses rank {r} twice")
            if c in ranks[q]:
                raise InvalidSubmission(f"line {line_no}: query {q} lists candidate {c} twice")
            if candidate_pool is not None and candidate_pool.get(c) != answers[q][1]:
                raise InvalidSubmission(f"line {line_no}: candidate {c} is not in the pool of query {q}")
            ranks[q][c] = r
    return ranks


def score(answers_path, submission_path, candidates_path=None):
    answers = load_answers(answers_path)
    pool_of = None
    if candidates_path:
        import json
        with open(candidates_path) as f:
            pool_of = {d["candidate_id"]: d["pool"] for d in map(json.loads, f)}
    ranks = load_submission(submission_path, answers, pool_of)
    rr, hit1, hit10 = 0.0, 0, 0
    for q, (gold, _) in answers.items():
        r = ranks.get(q, {}).get(gold)
        if r:
            rr += 1.0 / r
            hit1 += r == 1
            hit10 += r <= 10
    n = len(answers)
    return {"MRR@100": rr / n, "Recall@1": hit1 / n, "Recall@10": hit10 / n,
            "queries": n, "queries_answered": len(ranks)}


if __name__ == "__main__":
    if len(sys.argv) not in (3, 4):
        sys.exit("usage: python evaluate.py ANSWERS.csv SUBMISSION.csv [CANDIDATES.jsonl]")
    try:
        result = score(*sys.argv[1:])
    except InvalidSubmission as e:
        sys.exit(f"INVALID SUBMISSION: {e}")
    print("  ".join(f"{k}={v:.4f}" if isinstance(v, float) else f"{k}={v}" for k, v in result.items()))
