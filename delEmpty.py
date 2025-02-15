import os

def delete_zero_kb_pdfs(directory):
    deleted_files = []
    for filename in os.listdir(directory):
        if filename.endswith(".pdf"):
            file_path = os.path.join(directory, filename)
            if os.path.getsize(file_path) == 0:
                os.remove(file_path)
                deleted_files.append(filename)
    print("当前目录是",directory)
    print(f"Deleted {len(deleted_files)} file(s):")
    for file in deleted_files:
        print(file)

name_list=[
    "脐橙", "柚", "猕猴桃", "李",
    "草莓", "香蕉", "西瓜", "葡萄", "菠萝", "芒果", "梨", "油桃", "蓝莓", "柠檬", "柑橘",
    "辣椒", "番茄", "黄瓜", "马铃薯", "姜", "茄子", "菠菜", "大葱", "蒜", "红薯", "豌豆",
    "红茶", "绿茶", "白茶", "南瓜"
]

for i in name_list:
    delete_zero_kb_pdfs(i)
