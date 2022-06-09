# MRL 2022 Shared Task Evaluation

## CodaLab Competitions

- Task 1: Inflection: [Secret URL](https://codalab.lisn.upsaclay.fr/competitions/5300?secret_key=b3f74db4-c45b-4885-a7cd-fe951aa1deec)
(leaderboard score is edit distance)
- Task 2: Reinflection: [Secret URL](https://codalab.lisn.upsaclay.fr/competitions/5301?secret_key=b2501f67-66e1-4149-8f16-55695646b378)
(leaderboard score is edit distance)
- Task 3: Analysis: [Secret URL](https://codalab.lisn.upsaclay.fr/competitions/5302?secret_key=be490d46-f7b1-4b8b-be25-996e4feb9749)
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

## Evaluation

The script compares each gold file to the corresponding submission and calculates for each prediction:

- exact match accuracy ratings (proportion of correctly predicted lemma and features)
- Levenshtein Distance based on [this](https://python-course.eu/applications-python/levenshtein-distance.php) implementation. Costs are assumed to be 1 for each operation.

These scores are then averaged for each language. In the end, average scores are calculated over all languages. All results can be found in the `scoring output log` next to the submission.
