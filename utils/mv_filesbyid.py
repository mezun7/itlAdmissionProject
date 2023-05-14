import os

id_starts = -3
cur_dir = r'E:\output'
result_dir = r'E:\results2tour'
os.chdir(cur_dir)
for file in os.listdir(os.curdir):
    if os.path.isdir(file):
        folder_id = str(int(file[id_starts:]))
        from_file = os.path.join(os.curdir, file)
        to_dir = os.path.join(result_dir, folder_id)
        if not os.path.exists(to_dir):
            os.mkdir(to_dir)
        to_file = os.path.join(to_dir, file)
        os.replace(from_file, to_file)
