import os


def copy(path_1, path_2):
    """
    将 path_1 下的所有目录及文件复制到 path_2 下

    path_1: 待复制的目录或者文件路径
    path_2: 目标路径
    """
    if os.path.isdir(path_1):  # path_1是目录

        list_1 = os.listdir(path_1)
        if not list_1:  # 复制目录，仅仅是复制空目录
            os.mkdir(path_2)
        else:
            os.mkdir(path_2)  # 先复制最上层空目录
            for i in list_1:
                path_r = os.path.join(path_1, i)  # 下层目录或文件的绝对路径
                path_w = os.path.join(path_2, i)  # 目标目录或文件的绝对路径
                if os.path.isfile(path_r):  # 是文件则直接进行复制
                    with open(path_r, 'rb') as rstream:
                        container = rstream.read()
                        with open(path_w, 'wb') as wstream:
                            wstream.write(container)
                else:  # 是目录则调用本函数
                    copy(path_r, path_w)

    else:  # path_1是文件
        with open(path_1, 'rb') as rstream:  # 是文件直接复制文件
            container = rstream.read()
            file_name = os.path.basename(path_1)
            path_2 = os.path.join(path_2, file_name)
            with open(path_2, 'wb') as wstream:
                wstream.write(container)


def delete(path):
    """
    删除 p 下的所有目录及文件
    p: 待删除目录或文件的路径
    """
    if os.path.exists(path) is False:
        return
    if os.path.isdir(path):  # path_3是目录
        list_1 = os.listdir(path)
        if not list_1:
            os.rmdir(path)  # 空目录直接删除
        else:  # 非空目录
            for index, i in enumerate(list_1):
                # 获得目录下所有目录及文件的绝对路径
                list_1[index] = os.path.join(path, i)

            for i in list_1:
                if os.path.isfile(i):  # 是文件直接删除
                    os.remove(i)
                else:  # 是目录循环继续执行本函数
                    delete(i)
            os.rmdir(path)
    else:  # path是文件
        os.remove(path)


if __name__ == "__main__":
    script_path = os.getcwd()
    dist = script_path + "\\dist"
    img = script_path + "\\img"
    mumuyys = dist + "\\mumuyys"
    archive = dist + "\\mumuyys.7z"

    os.system("pyinstaller -F main.py")  # 打包app

    # 重建软件文件夹
    delete(mumuyys)
    os.mkdir(mumuyys)
    # 复制文件
    copy(dist + "\\main.exe", mumuyys)
    copy(img, mumuyys + "\\img")
    # bandizip 压缩 -l:9 最大效率
    os.system("bz c -l:9 %s %s" % (archive, mumuyys))
    # 打开文件夹
    os.system("start %s" % dist)
