# MRL 2022 Shared Task Evaluation

## CodaLab Competitions

- Task 1: Inflection: [URL](https://codalab.lisn.upsaclay.fr/competitions/6823?secret_key=168d2627-00fa-4d2b-abca-0982726c280c)
(leaderboard score is edit distance)
- Task 2: Reinflection: [URL](https://codalab.lisn.upsaclay.fr/competitions/6824?secret_key=aa6c5a3f-f261-44bf-bffd-c0698f022358)
(leaderboard score is edit distance)
- Task 3: Analysis: [URL](https://codalab.lisn.upsaclay.fr/competitions/6830?secret_key=44e813c2-96c8-4889-b0fc-24dbe83ad2c6)
(leaderboard score is F1-score)

## To Run the Script Locally

```bash
/bin/python2 evaluate.py <input directory> <output directory> <enable F1>
```

e.g.:

```bash
/bin/python2 evaluate.py ~/Desktop/eval ~/Desktop/eval False
```

This script assumes that there is a folder `res` and `ref` in the `<input directory>`. Files containing the gold reference are stored in `ref` and the submitted files in `res`. Set flag `enable F1` to `True` if you are evaluating task 3, otherwise use `False`.

## CodaLab Submission Requirements

A submission uploaded to CodaLab must be of the following format:

```
.
├── <Name of submission>.zip                   
│   ├── deu.dev
│   ├── eng.dev
│   ├── fra.dev
│   ├── heb.dev
│   ├── heb_unvoc.dev
│   ├── rus.dev
│   ├── tur.dev
```

Make sure the outermost folder does not include anything but the text files themselves. To achive that zip the folder containing the text files (here named submission) as follows:

```bash
zip -j submission.zip submission/*
```

## Evaluation

The script compares each gold file to the corresponding submission and calculates for each prediction:

- exact match accuracy ratings (proportion of correctly predicted lemma and features)
- Levenshtein Distance based on [this](https://python-course.eu/applications-python/levenshtein-distance.php) implementation. Costs are assumed to be 1 for each operation.

These scores are then averaged for each language. In the end, average scores are calculated over all languages. All results can be found in the `scoring output log` next to the submission.
