import os
import time

def start_rename():
    # 提示用户输入文件夹路径
    folder_path = input("请输入文件夹路径: ").strip()

    # 检查路径是否存在
    if not os.path.exists(folder_path):
        print("路径不存在，请检查后重试。")
        return

    # 获取路径下的所有文件
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

    # 遍历文件并重命名
    for file in files:
        old_path = os.path.join(folder_path, file)
        file_extension = os.path.splitext(file)[1]  # 获取文件扩展名
        creation_time = time.strftime("%Y%m%d_%H%M%S", time.localtime(os.path.getctime(old_path)))  # 格式化创建时间

        # 初始文件名
        new_name = f"{creation_time}{file_extension}"
        new_path = os.path.join(folder_path, new_name)

        # 如果文件名已存在，添加递增的数字后缀
        counter = 1
        while os.path.exists(new_path):
            new_name = f"{creation_time}_{counter}{file_extension}"
            new_path = os.path.join(folder_path, new_name)
            counter += 1

        # 重命名文件
        os.rename(old_path, new_path)
        print(f"已重命名: {file} -> {new_name}")

if __name__ == "__main__":
    start_rename()