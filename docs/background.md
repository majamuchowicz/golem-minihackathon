# Background: where the data comes from and what we changed

Optional reading, for the curious: the research benchmark this challenge comes from, what we changed, and why.
The actual rules are in [challenge_description.pdf](challenge_description.pdf)

## 1. CodeSearchNet (2019)

[CodeSearchNet](https://arxiv.org/abs/1909.09436) was released by GitHub and Microsoft Research to measure progress in semantic code search: finding code from a natural-language description.

- **Data:** about 6.4 million functions from open-source GitHub projects in six languages (Go, Java, JavaScript, PHP, Python, Ruby). About 2.3 million of them have documentation, and those function-documentation pairs are used for training and evaluation. The data is split 80 / 10 / 10 into train, validation and test.
- **Cleaning:** documentation is cut to its first paragraph. The authors removed pairs whose documentation is shorter than 3 tokens, functions shorter than 3 lines, test functions, constructors and standard methods such as `__str__`, and near-duplicates.
- **Evaluation:** the documentation serves as the query. Each query is ranked against its correct function plus **999 distractors**, and the result is scored with **Mean Reciprocal Rank**.
- **The CodeSearchNet Challenge:** a separate set of 99 real search queries with 4026 relevance ratings from experts, scored with NDCG. We don't use it here.

## 2. AdvTest, part of CodeXGLUE (2021)

[CodeXGLUE](https://arxiv.org/abs/2102.04664) is Microsoft's collection of benchmarks for code models. Its *NL-code-search-Adv* task, usually called **AdvTest**, is built from the Python part of CodeSearchNet:

- Low-quality examples are filtered out, for example code that doesn't parse and very short or very long documentation.
- Splits: 251820 train / 9604 validation / 19210 test.
- In validation and test, **function and variable names are normalised** to `Func` and `arg_0`, `arg_1`, … This is the "adversarial" part. Models that relied on matching query words to function names drop sharply, so the benchmark tests whether a model understands the function body.
- Each query is ranked against **all 19210 test functions**, and scored with MRR.

### Published results on AdvTest

These are fine-tuned research models, mostly trained on GPUs, ranked against the full 19210-function test pool ([UniXcoder paper](https://arxiv.org/abs/2203.03850), Table 1):

| Model | MRR (full pool) |
|---|---|
| RoBERTa | 0.183 |
| CodeBERT | 0.272 |
| UniXcoder | 0.413 |

**These numbers are not comparable with your scores.** They use a pool 19 times larger, the original split, and the original preprocessing.

## 3. What we changed for this challenge
1. Docstrings and comments stripped from all code 
2. Metadata removed (URL, repository, file path, original function name, commit) 
3. Dev and test rebuilt with no shared repositories 
4. Functions removed if they have a structural duplicate, share their exact docstring with another function, or overlap with train
5. Queries shorter than 3 words and functions longer than 4000 characters removed 
6. Pools of 1000 instead of the full 19210 
7. MRR@100 instead of full-ranking MRR, so that submission files stay small
8. 5000 dev and 5000 test queries to fit a one-day event

What we kept: the queries, the code, the anonymisation of evaluation code, the training pairs (with real names), and MRR as the metric.

## 4. Things we left as they are, on purpose

- **Long queries.** Unlike CodeSearchNet, AdvTest keeps the whole docstring. About a quarter of dev queries include parameter descriptions (`:param`, `Args:`, `Returns:`).
- **Noisy pairs.** Some docstrings are poor descriptions of their function ("TODO", copied text, very generic wording). These are present in train, dev and test alike.
- **Train vs test mismatch.** Training code has real names and test code doesn't. This mirrors the benchmark, and handling it is part of the challenge.

## References

- Husain et al., *CodeSearchNet Challenge: Evaluating the State of Semantic Code Search*, 2019. <https://arxiv.org/abs/1909.09436>
- Lu et al., *CodeXGLUE: A Machine Learning Benchmark Dataset for Code Understanding and Generation*, 2021. <https://arxiv.org/abs/2102.04664>, code and data: <https://github.com/microsoft/CodeXGLUE>
- Guo et al., *UniXcoder: Unified Cross-Modal Pre-training for Code Representation*, 2022. <https://arxiv.org/abs/2203.03850>
