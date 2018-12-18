# coding:utf-8
import os
import shutil
rootPath = os.path.abspath('.')

# 使用前需设置要收集的扩展名和 保存目录
extnameContainer ={
    '.7z':[],
    # '.exe':[]
    }
targetDirectory={
    # '.go':os.path.join(rootPath,'go'),
    # '.exe':os.path.join(rootPath,'exe'),
    '.7z':os.path.join(rootPath,'7z2'),
}

def collect(path,extnameContainer):
    for x in os.listdir(path):
        nextpath = path+'\\'+x
        if(os.path.isdir(nextpath)):
            collect(nextpath,extnameContainer)
        else:
            derectory,extname = os.path.splitext(nextpath)
            # print(extname)
            if extname in extnameContainer:
                extnameContainer[extname].append(nextpath)

def copyAlist(filelist):
    print('该文件列表的文件总数为:'+str(len(filelist)))
    for index,i in enumerate(filelist):
        extname = os.path.splitext(i)[1]
        copyFile(i,targetDirectory[extname])
        print('正在拷贝第'+str(index)+'个文件'+i+'到'+targetDirectory[extname])

def copyFile(sourcePath,targetPath):
    if not os.path.exists(targetPath):
        print('目标路径不存在，创建目标路径: '+targetPath)
        os.mkdir(targetPath)
    basename = os.path.basename(sourcePath)
    with open(sourcePath,'rb') as f:
        with open(targetPath+'\\'+basename,'ab+') as fw:
            # 处理大文件的时候，一点一点读
            for line in f:
                fw.write(line)
        fw.close()
    f.close()

# # 调用系统shell兼容性不佳，只适用于windows系统
# def moveFile(sourcePath,targetPath):
#     if not os.path.exists(targetPath):
#         print('目标路径不存在，创建目标路径: '+ targetPath)
#         os.mkdir(targetPath)
#     # 拼接批处理命令，move的文件名中可能会有空格，目录名要用双引号括起来
#     command = 'move "'+sourcePath+'" "'+targetPath+'"'
#     print(command)
#     status = os.system(command)
#     # print('正在移文件'+sourcePath+'到'+targetPath)
#     print(status)

def moveAlist(filelist):
    print('该文件列表的文件总数为:'+str(len(filelist)))
    for index,i in enumerate(filelist):
        # 使用enumerate可以返回下标
        extname = os.path.splitext(i)[1]
        print('正在移动第'+str(index)+'个文件'+i+'到'+targetDirectory[extname])
        # shutil模块中有shutil.copyfile和shutilmove等方法
        shutil.move(i,targetDirectory[extname])
        # moveFile(i,targetDirectory[extname])



if __name__ == "__main__":
    collect(rootPath,extnameContainer)
    # print(extnameContainer)
    for key in extnameContainer:
        print('当前处理的文件类型'+key)
        moveAlist(extnameContainer[key])
        
# go语言build默认是在当前目录生成exe，而且一个目录作为一个项目只能有一个main
# 每次打开都隔着一层目录，这样不利于学习阶段代码片段的查看
# 所以写了这个collectGo脚本，把一个目录中所有go程序和exe程序分别收集起来
# 放到脚本运行目录下的go和exe文件夹中
