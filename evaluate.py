#!/usr/bin/env python
import sys
import os
import os.path
import re


def read_file(file):
    with open(file, 'r') as infile:  # , encoding='utf-8'
        # or without \n lines = [line.rstrip('\n') for line in infile]
        lines = infile.readlines()

        # keep only the last part of the line after '\t'
        content = [line.rstrip().split('\t')[-1] for line in lines]

    return content


def get_list_average(list):
    return float(sum(list))/float(len(list))


def deconstruction(pred):
    pred = pred.replace(';', ' ').split()
    lemma = pred.pop(0)
    features = []

    for el in pred:
        if '(' in el:
            main_feature = re.search(r'(.*?)\(', el).group(1)
            in_bracket = re.search(r'\((.*?)\)', el).group(1).split(',')

            for sub_feature in in_bracket:
                x = main_feature + '-' + sub_feature
                features.append(x)

        else:
            features.append(el)

    return features, lemma


def calculate_f1(gold, prediction):
    # deconstruction
    gold_f, gold_lemma = deconstruction(gold)
    prediction_f, prediction_lemma = deconstruction(prediction)

    # consider correct lemma in f1 score
    weight_lemma = 3.0
    if gold_lemma == prediction_lemma:
        lemma = weight_lemma
    else:
        lemma = 0.0

    overlapping = float(len(list(set(gold_f) & set(prediction_f)))) + lemma
    num_pred = float(len(prediction_f))
    num_gold = float(len(gold_f))

    precision = overlapping / (num_pred + weight_lemma)
    recall = overlapping / (num_gold + weight_lemma)
    f1 = (2 * precision * recall) / (precision + recall)

    return f1


def calculate_metrics(gold, predictions, f1_enabled):
    matching = []  # denotes whether predictions at the position are matching
    lev_distances = []  # stores edit distances per sentence
    f1_scores = []

    for i, j in zip(gold, predictions):
        if i == j:
            matching.append(1)
        else:
            matching.append(0)

        lev_distances.append(calculate_levensthein(i, j))

        if f1_enabled == 'True':
            f1_scores.append(calculate_f1(i, j))
        else:
            f1_scores.append(0.0)

    accuracy = float(sum(matching))/float(len(matching))
    mean_distance = get_list_average(lev_distances)

    mean_f1 = get_list_average(f1_scores)

    return accuracy, matching, lev_distances, mean_distance, mean_f1


def _calculate_levenshtein(s, t, costs=(1, 1, 1)):
    """
        Source: https://www.python-course.eu/levenshtein_distance.php 
    """
    rows = len(s) + 1
    cols = len(t) + 1
    deletes, inserts, substitutes = costs

    dist = [[0 for x in range(cols)] for x in range(rows)]

    # source prefixes can be transformed into empty strings
    # by deletions:
    for row in range(1, rows):
        dist[row][0] = row * deletes

    # target prefixes can be created from an empty source string
    # by inserting the characters
    for col in range(1, cols):
        dist[0][col] = col * inserts

    for col in range(1, cols):
        for row in range(1, rows):
            if s[row - 1] == t[col - 1]:
                cost = 0
            else:
                cost = substitutes
            dist[row][col] = min(dist[row - 1][col] + deletes,
                                 dist[row][col - 1] + inserts,
                                 dist[row - 1][col - 1] + cost)  # substitution

    return dist[row][col]


def calculate_levensthein(gold, prediction):
    try:
        #dist = lev(gold, prediction)
        dist_iterative = _calculate_levenshtein(gold, prediction)
        return dist_iterative
    except Exception as e:
        print 'Exception during edit distance calculation of', prediction, e
        exit()


def main():
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    f1_enabled = sys.argv[3]

    submit_dir = os.path.join(input_dir, 'res')  # submission
    truth_dir = os.path.join(input_dir, 'ref')  # gold

    if not os.path.isdir(submit_dir):
        print "%s doesn't exist" % submit_dir

    if os.path.isdir(submit_dir) and os.path.isdir(truth_dir):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        output_filename = os.path.join(output_dir, 'scores.txt')
        output_file = open(output_filename, 'wb')

        gold_files = os.listdir(truth_dir)

        submission_accuracies = []
        submission_distances = []
        submission_f1s = []

        for file in gold_files:
            gold_file = os.path.join(truth_dir, file)
            corresponding_submission_file = os.path.join(submit_dir, file)
            if os.path.exists(corresponding_submission_file):
                print '-------- Evaluating', corresponding_submission_file, '--------'

                gold = read_file(gold_file)
                predictions = read_file(corresponding_submission_file)

                assert len(gold) == len(
                    predictions), 'Len of predictions is not the same as  len of reference'

                accuracy, _, edit_distances, mean_edit_distance, mean_f1 = calculate_metrics(
                    gold, predictions, f1_enabled)

                submission_accuracies.append(accuracy)
                submission_distances.append(mean_edit_distance)
                submission_f1s.append(mean_f1)

                print 'Matching Predictions:', accuracy
                print 'Edit Distance:', mean_edit_distance
                print 'F1:', mean_f1

            else:
                print 'no corresponding submission file found for', file
                exit()

        submission_accuracy = get_list_average(submission_accuracies)
        submission_distance = get_list_average(submission_distances)
        submission_f1 = get_list_average(submission_f1s)

        print '======== Average over all files ========'
        print 'Average Accuracy (on string level):', submission_accuracy, submission_accuracies
        print 'Average Edit Distance:', submission_distance, submission_distances
        print 'Average F1:', submission_f1, submission_f1s

        output_file.write("Difference: %f" % submission_f1)
        output_file.close()


if __name__ == "__main__":
    main()
