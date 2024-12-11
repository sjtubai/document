import shutil
import re
import os

path = input("置換対象が格納されているディレクトリを指定してください（例：20241210171747）：")
path_old = path + "\\Blue"
path_new = path + "\\PCS"

shutil.copytree(path_old, path_new)

target_dir_path = path_new

def replaceText(target_dir_path):
   for current_dir, sub_dirs, files_list in os.walk(target_dir_path):
       for file_name in files_list:
           print(os.path.join(current_dir,file_name))
           with open(os.path.join(current_dir,file_name),encoding="utf-8") as reader:
               data_lines = reader.read()
               
               # 文字列置換
               data_lines = re.sub("/blue", "/pcs", data_lines)
               data_lines = re.sub("-qa", "-pcs", data_lines)

           # 同じファイル名で保存
           with open(os.path.join(current_dir,file_name),mode="w") as writer:
               writer.write(data_lines)

replaceText(target_dir_path)

