#coding:utf-8
import urllib2
import ssl
from time import sleep
from Queue import Queue
import threading
# 使用方法，修改bookUrl和pageNum和fileName即可
class ThreadCrawl(threading.Thread):
    def __init__(self,threadName,pageQueue,dataQueue):
        #调用父类初始化方法
        super(ThreadCrawl,self).__init__()
        self.threadName = threadName
        self.pageQueue = pageQueue
        self.dataQueue = dataQueue
        self.head = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.52 Safari/537.36" }
        self.context = ssl._create_unverified_context()

    def LoopRequest(self,getUrl,num):
        request = urllib2.Request(getUrl, headers=self.head)
        try:
            response = urllib2.urlopen(request, context=self.context)
        except:
            print("内容获取失败，休息5秒，重新执行")
            sleep(5)
            response = self.LoopRequest(getUrl,num)
        print("成功获取第"+str(num)+"篇")
        return response

    def pageQueueEmpty(self):
        if (self.pageQueue.empty()):
            global CRAWL_EXIT
            CRAWL_EXIT = True
            print("页面队列为空")
    def run(self):
        print "启动" + self.threadName
        while not CRAWL_EXIT:

            try:
                # block参数，为true，则当队列为空自动进入阻塞状态，等待队列有新的数据，为false，则当队列为空，抛出一个异常
                pageList = self.pageQueue.get(False)
            except:
                pass
            getUrl = pageList[1]
            num = pageList[0]
            request = urllib2.Request(getUrl, headers=self.head)
            # try:
            #     response = urllib2.urlopen(request, context=self.context)
            # except:
            #     print("内容获取失败，休息10秒，重新执行")
            #     sleep(10)
            #     response = urllib2.urlopen(request, context=self.context)
            response = self.LoopRequest(getUrl,num)
            text = response.read()
            self.dataQueue.put([num,text])
            self.pageQueueEmpty()
        print "结束" + self.threadName

# class ThreadParse(threading.Thread):
#     def __init__(self, threadName, dataQueue,filename):
#         # 调用父类初始化方法
#         super(ThreadCrawl, self).__init__()
#         self.threadName = threadName
#         self.dataQueue = dataQueue
#         self.filename = filename
#     def run(self):
#         while not Parse_EXIT:
#             try:
#                 self.dataQueue.get(False)
#             except:
#                 print("写入出现异常")


CRAWL_EXIT= False
# Parse_EXIT= False
def main():
    booksnum=raw_input("请输入下载页书籍的编号:")
    pageNum = int(raw_input("请输入下载书籍的章数:"))
    # bookUrl = "https://ncode.syosetu.com/txtdownload/dlstart/ncode/1179366/"
    bookUrl = "https://ncode.syosetu.com/txtdownload/dlstart/ncode/"+booksnum+"/"
    # pageNum = 54
    #fileName = raw_input("请输入下载书籍的名字") + ".txt"
    fileName = "1217838.txt"
    pageQueue = Queue()
    dataQueue = Queue()
    for num in range(1, pageNum + 1):
        # bookList.num=bookUrl+str(num)+r'/'
        getUrl = bookUrl + "?no=" + str(num) + "&hankaku=0&code=utf-8&kaigyo=crlf"
        pageQueue.put([num, getUrl])

    # crawlLiat=["01","02","03"]
    crawlLiat = ["01"]
    threadcrawl = []
    for threadName in crawlLiat:
        thread = ThreadCrawl(threadName, pageQueue, dataQueue)
        thread.start()
        threadcrawl.append(thread)
    # parselLiat = ["p01", "p02", "p03"]
    # threadparse=[]
    # for threadName in parselLiat:
    #     thread = ThreadParse(threadName,dataQueue,filename)
    #     thread.start()
    #     threadparse.append(threadName)

    f = open(fileName, "a")
    for temp in range(1,pageNum+1):
        pageList = dataQueue.get(True)
        text = pageList[1]
        num = pageList[0]
        try:
            f.write(text)
            f.write("\n")
            print "已写入第"+ str(num)+"篇"
        except:
            print("写入出错")
            f.write(text)

    f.close()
    print("已完成这篇小说的下载")
    for thread in threadcrawl:
        thread.join()

main()
