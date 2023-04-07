import csv
import os

directory = '/Users/shuhrat/tmp'
csv_path = 'blanks.csv'
csv_file = open(csv_path, 'r')
csv_reader = csv.DictReader(csv_file)
os.chdir(directory)
main_dict = {}
for row in csv_reader:
    main_dict[row['blank_id']] = row['id']

print(main_dict)

for file in os.listdir(os.curdir):
    name = file.split('.')[0]
    extension = file.split('.')[-1]
    if not os.path.isdir(file) and name in main_dict:
        os.rename(file, '.'.join([main_dict[name], extension]))
