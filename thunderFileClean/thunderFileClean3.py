# coding:utf-8
import os
import re
print('='*30)
print('迅雷文件清理程序')
print('='*30)
print("本程序主要作用为，清理迅雷种子文件，以及重命名下载到99%的迅雷下载文件，对于空文件夹，暂不处理")
cleaned=[]
rootpath = os.path.abspath('.')
# rootpath = 'G:\\'
# systemDir=[rootpath+'System Volume Information']
def clean(path,cleaned):
    for x in os.listdir(path):
        # print(x)
        # 文件名不能以\结尾，所以这个判断无用
        if(path[-1:]=='\\'):
            nextpath=path+x
        else:
            nextpath=path+'\\'+x
        # nextpath=nextpath+r'\'+x
        # print('遍历路径：'+nextpath)
        if os.path.isdir(nextpath):
            # 判断为文件夹，递归查找
            # print('ok')
            try:
                if(os.listdir(nextpath)):
                    clean(nextpath,cleaned)
                else:
                    print('发现空文件夹，暂不处理'+nextpath)
                    cleaned.append(nextpath)
                    # confirm = input('发现空文件夹，是否清除,输入1清除，0或其他键跳过：'+nextpath);
                    # if confirm =='1':
                    #      os.rmdir(nextpath)
                    #      print('已清除空文件夹'+nextpath)
                    #      cleaned.append(nextpath)
                    #
                    # else:
                    #     pass
            except PermissionError as e:
                print('捕捉到异常：')
                print(e)
        else:
            # 判断为文件，清除torrent种子文件，重命名迅雷下载文件
            # 如3.wmv.bt.xltd
            # filepath,filename=os.path.split(nextpath)
            # print('ok')
            if re.match(r'.*\.torrent$',nextpath):
                try:
                    os.remove(nextpath)
                except Exception as e:
                    print(e)
                finally:
                    print('路径名过长,暂时无法删除:'+nextpath)
                print('已清除种子文件'+nextpath)
                cleaned.append(nextpath)
            elif re.match(r'.*\.bt\.xltd$',nextpath):
                try:
                    os.rename(nextpath,nextpath[:-8])
                except Exception as e:
                    print(e)
                finally:
                    print('重命名失败')
                print('重命名'+nextpath+'为'+nextpath[:-8])
                cleaned.append(nextpath)

# try:
#     clean(rootpath,cleaned)
#
# except :
#     pass
clean(rootpath,cleaned)
# print('共清理种子'+len(cleanedBt)）)
print('清理完成，共清理'+str(len(cleaned))+'项')
os.system('pause')



