# MRL 2022 Shared Task Evaluation

## CodaLab Competitions

- Task 1: Inflection: [Secret URL](https://codalab.lisn.upsaclay.fr/competitions/5358?secret_key=c59d2248-110d-4485-b33b-1f86e9687901)
(leaderboard score is edit distance)
- Task 2: Reinflection: [Secret URL](https://codalab.lisn.upsaclay.fr/competitions/5317?secret_key=38dcc82a-12c2-4faa-8204-4577884283ed)
(leaderboard score is edit distance)
- Task 3: Analysis: [Secret URL](https://codalab.lisn.upsaclay.fr/competitions/5318?secret_key=c1e9f2c0-339c-4876-92d2-11b67c6170d5)
(leaderboard score is exact match accuracy)

## To Run the Script Locally

```bash
/bin/python2 evaluate.py <input directory> <output directory>
```

This script assumes that there is a folder `res` and `ref` in the `<input directory>`. Files containing the gold reference are stored in `ref` and the submitted files in `res`.

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
