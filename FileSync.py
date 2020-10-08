import os
import shutil
import time
import schedule
import logging


def startsync(timing):
    schedule.every().day.at(timing).do(main)
    while True:
        schedule.run_pending()
        time.sleep(300)


def main():
    srcdir = "sourcedir"
    desdir = "destinationdir"
    sync = SyncFile(srcdir, desdir)
    sync.syncdir()


class SyncFile:
    def __init__(self, fromdir, todir):
        self.fromdir = fromdir
        self.todir = todir


    def syncdir(self):
        print("Start synchronize files from %s to %s at %s" % (self.fromdir, self.todir, self._localtime()))
        self._copydir(self.fromdir, self.todir)
        print("Today's synchronization has been finished!")

    def _localtime(self):
        localtime = time.asctime(time.localtime(time.time()))
        return localtime

    def _copydir(self, fromdir, todir):
        self._mkdir(todir)

        for filename in os.listdir(fromdir):
            if filename.startswith('.'):
                continue
            elif filename.startswith('FileSync'):
                continue
            elif filename.startswith('venv'):
                continue
            elif filename.startswith("All Users"):
                continue
            fromfile = fromdir + os.sep + filename
            tofile = todir + os.sep + filename
            if os.path.isdir(fromfile):
                self._copydir(fromfile, tofile)
            else:
                self._copyfile(fromfile, tofile)

    def _copyfile(self, fromfile, tofile):
        if not os.path.exists(tofile):
            try:
                shutil.copy2(fromfile, tofile)
                logging.info("新增文件%s ==> %s at %s" % (fromfile, tofile, self._localtime()))
            except PermissionError:
                logging.info("文件%s 权限不够" % fromfile)
        fromstat = os.stat(fromfile)
        tostat = os.stat(tofile)
        if fromstat.st_ctime > tostat.st_ctime:
            try:
                shutil.copy2(fromfile, tofile)
                logging.info("更新文件%s ==> %s at %s" % (fromfile, tofile, self._localtime()))
            except PermissionError:
                logging.info("文件%s 权限不够" % fromfile)

    def _mkdir(self, path):
        path = path.strip()
        path = path.rstrip(os.sep)
        isExists = os.path.exists(path)
        if not isExists:
            os.makedirs(path)
            logging.info(path + ' 目录创建成功 at %s' % self._localtime())


if __name__ == '__main__':
    logging.basicConfig(filename="FileSyncLog.log", level=logging.INFO)
    startsync("05:00")
