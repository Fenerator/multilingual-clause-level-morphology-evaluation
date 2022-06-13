#!/usr/bin/env python
import sys
import os
import os.path


def read_file(file):
    with open(file, 'r') as infile:  # , encoding='utf-8'
        # or without \n lines = [line.rstrip('\n') for line in infile]
        lines = infile.readlines()

        # keep only the last part of the line after '\t'
        content = [line.rstrip().split('\t')[-1] for line in lines]

    return content


def get_list_average(list):
    print float(sum(list))
    print float(len(list))
    return float(sum(list))/float(len(list))


def calculate_matching(gold, predictions):
    """
    Args:
        gold (list of str)
        predictions (list of str)

    Returns:
        (float, list): proportion of matching predictions, position of matching predictions
    """
    matching = []  # denotes whether predictions at the position are matching
    lev_distances = []  # stores edit distances per sentence

    for i, j in zip(gold, predictions):
        if i == j:
            matching.append(1)
        else:
            matching.append(0)

        lev_distances.append(calculate_levensthein(i, j))

    accuracy = float(sum(matching))/float(len(matching))
    mean_distance = get_list_average(lev_distances)

    return accuracy, matching, lev_distances, mean_distance


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
        # print e, "gold:", gold, "prediction:", prediction
        return 300  # TODO


def main():
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]

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

        for file in gold_files:
            gold_file = os.path.join(truth_dir, file)
            corresponding_submission_file = os.path.join(submit_dir, file)
            if os.path.exists(corresponding_submission_file):
                print '-------- Evaluating', corresponding_submission_file, '--------'

                gold = read_file(gold_file)
                predictions = read_file(corresponding_submission_file)

                assert len(gold) == len(
                    predictions), 'Len of predictions is not the same as  len of reference'

                accuracy, _, edit_distances, mean_edit_distance = calculate_matching(
                    gold, predictions)

                submission_accuracies.append(accuracy)
                submission_distances.append(mean_edit_distance)

                print 'Matching Predictions:', accuracy
                print 'Edit Distance:', mean_edit_distance

            else:
                print 'no corresponding submission file found for', file
                exit()

        submission_accuracy = get_list_average(submission_accuracies)
        submission_distance = get_list_average(submission_distances)

        print '======== Average over all files ========'
        print 'Average Accuracy:', submission_accuracy, submission_accuracies
        print 'Average Edit Distance:', submission_distance, submission_distances

        output_file.write("Difference: %f" % submission_accuracy)
        output_file.close()


if __name__ == "__main__":
    main()
