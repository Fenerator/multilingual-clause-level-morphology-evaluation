# MRL 2022 Shared Task Evaluation

## CodaLab Competitions

- Task 1: Inflection: [URL](https://codalab.lisn.upsaclay.fr/competitions/5549?secret_key=77e09d5c-26ac-4dd2-898e-d2d7be80198f)
(leaderboard score is edit distance)
- Task 2: Reinflection: [URL](https://codalab.lisn.upsaclay.fr/competitions/5550?secret_key=4512af71-8e9a-4def-b3a6-fb747d626901)
(leaderboard score is edit distance)
- Task 3: Analysis: [URL](https://codalab.lisn.upsaclay.fr/competitions/5551?secret_key=cdeef5ac-2234-4a97-9498-e9d4b3a2e6a4)
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
