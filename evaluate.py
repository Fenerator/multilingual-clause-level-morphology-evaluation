#!/usr/bin/env python

# from Levenshtein import distance as lev  # TODO
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


def calculate_levensthein(gold, prediction):
    try:
        dist = lev(gold, prediction)
        return dist
    except Exception as e:
        # print e, "gold:", gold, "prediction:", prediction
        return 300  # TODO


def main():
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    # input_dir = '/home/dug/Py/mrl_2022_shared_task_evaluation'
    # output_dir = '/home/dug/Py/mrl_2022_shared_task_evaluation'

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

                print gold[0]
                print predictions[0]

                assert len(gold) == len(
                    predictions), 'Len of predictions is not the same as  len of reference'

                accuracy, _, edit_distances, mean_edit_distance = calculate_matching(
                    gold, predictions)

                submission_accuracies.append(accuracy)
                submission_distances.append(mean_edit_distance)

                print 'Matching Predictions:', accuracy
                print 'Edit Distance:', mean_edit_distance

        submission_accuracy = get_list_average(submission_accuracies)
        submission_distance = get_list_average(submission_distances)

        print '======== Average over all files ========'
        print 'Average Accuracy:', submission_accuracy, submission_accuracies
        print 'Average Edit Distance:', submission_distance, submission_distances

        output_file.write("Difference: %f" % submission_accuracy)
        output_file.close()


if __name__ == "__main__":
    main()


'''
NOTES:
lines cannot be empty
Input:
I will give him to her
Ich werde ihn ihr geben

Gold
I will give him to her
Ich werde ihn ihr geben

Calculate exact match accuracy ratings (proportion of correctly predicted lemma and features)
using ==
Calcultate Edit Distance (Levenstein distance, averaged over all predictions)
using levenstein

both can be used for all subtasks
average over languages as well, or is test set mixed?
'''
