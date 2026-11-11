# Data card

Everything about the files in `data/`, for when something looks odd. For where the data comes from and why it was changed, see [background.md](background.md)

## Files and fields

| File | Rows | Fields |
|---|---|---|
| `train.jsonl.gz` | 250653 | `id`, `query`, `code` |
| `dev_queries.jsonl` | 5000 | `query_id`, `pool`, `query` |
| `dev_candidates.jsonl` | 5000 | `candidate_id`, `pool`, `code` |
| `dev_answers.csv` | 5000 | `query_id`, `candidate_id`, `pool` |
| `test_queries.jsonl` | 5000 | `query_id`, `pool`, `query` |
| `test_candidates.jsonl` | 5000 | `candidate_id`, `pool`, `code` |

All files are UTF-8. The `.jsonl` files have one JSON object per line. `train.jsonl.gz` is gzip-compressed; read it with Python's `gzip.open(path, "rt")` or `pandas.read_json(path, lines=True)`

## What a positive pair means

A query and a candidate match when the query is **the docstring that was written for that function** in its original repository. That's the only relevance label. A different function that also fits the description well is still counted as wrong. Pairs like that were reduced by removing duplicates, but descriptions of very generic functions may still fit several candidates.

## Pools

- Dev and test each have 5 pools (`pool` = 0-4) of exactly 1000 queries and 1000 candidates.
- Every query has exactly one correct candidate, which is in its own pool.
- IDs are random: the number in a `query_id` says nothing about its `candidate_id`.

## Preprocessing applied

1. Docstrings and all `#` comments were removed from every function, train included. Blank lines were removed.
2. Queries are the original docstrings with whitespaces collapsed to single spaces. Nothing else was changed.
3. Metadata was removed: repository, file path, URL, commit and original name.
4. **Dev and test only** use the original AdvTest anonymisation: the function name became `Func`, and arguments and local variables became `arg_0`, `arg_1`, …
5. Functions with a structural duplicate, or a docstring shared with another function in dev, test or train, were removed. So were queries under 3 words and functions over 4000 characters.
6. Dev and test come from different repositories (703 and 262 respectively). Train comes from yet other repositories.

## Known quirks

- **`Func` replaces every occurrence of the function's own name**, even inside other calls. For example, a function originally called `show` may contain `plt.Func(...)` instead of `plt.show(...)`. About 14% of dev and test candidates contain the word `Func` more than once, and about 7% contain a call like `.Func(`.
- **Long queries.** About 26% of dev queries and 21% of test queries contain parameter or return sections (`:param`, `Args:`, `Returns:`). About 3-4% contain URLs.
- **Training code keeps real names and argument names.** You won't see these at test time.
- **Python 2 code.** Some functions won't parse with Python 3's `ast.parse`. Almost all of them use Python 2 syntax such as `print x` or `except A, e:`. If you parse code, catch `SyntaxError` and fall back to treating the function as text.
- **Noisy descriptions.** A small share of docstrings describe their function poorly. This applies to train, dev and test alike, so don't over-fit to individual failures.

## Licence

Derived from CodeSearchNet AdvTest (CodeXGLUE, Microsoft), built on the CodeSearchNet corpus, and distributed under the Computational Use of Data Agreement (C-UDA). The underlying code comes from open-source repositories with their own licences.
