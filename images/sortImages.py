import csv


'''This code runs through a list of human-annotated images and 
filters out the ones with low annotation confidence'''

with open('annotations-human.csv', 'rb') as csvfile:
    annotation_reader = csv.reader(csvfile, delimiter=',')

    annotations = []

    for row in annotation_reader:
        if row[3] == '1':
            annotations.append(row)

    with open('confident-annotations.csv', 'w') as confident_annotations:
        annotation_writer = csv.writer(confident_annotations)

        for row in annotations:
            annotation_writer.writerow(row)
