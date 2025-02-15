import json
import os
import random

random.seed(42)
def get_my_text(subf):
    json_strings = []
    subfolder_path="../dbba_txt" + '/'+subf
    txt_files = os.listdir(subfolder_path)
    selected_files = random.sample(txt_files, min(10, len(txt_files)))  # 随机选择10个文件
    for file_name in selected_files:
        # 读取文件内容
        with open(os.path.join(subfolder_path, file_name), 'r', encoding='utf-8') as file:
            content = file.read()
            # 去除文件名中的《》
            standard_name = file_name.replace("《", "").replace("》", "")
            # 如果内容超过6k就跳过这个文档
            if len(content) > 6000:
                print("!!跳过一个文件!!当前文件名字是",standard_name,"字数是",len(content))
                continue
            json_data = {
                "instruction": "你是一个特色农产品标准化文件制定助手。请根据用户输入，输出相应回答，用户输入：",
                "input": f"初步起草一份《{standard_name}》的标准化稿件。",
                "output": content
            }
            json_strings.append(json_data)
    return json_strings
if __name__ == '__main__':
    folder_path = "../dbba_pdf"
    # 获取所有子文件夹，只获取文件夹
    subfolders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]
    subfolders.remove("脐橙")
    # print(subfolders)
    json_data_list=[]
    for subf in subfolders:
        json_strings=get_my_text(subf)
        json_data_list.extend(json_strings)
    with open('output_dataset.json', 'a', encoding='utf-8') as json_file:
        for json_data in json_data_list:
            json.dump(json_data, json_file, ensure_ascii=False)
            json_file.write('\n')  # 每个JSON对象换行