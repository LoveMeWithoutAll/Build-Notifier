import postMessage
import slumber
import simplejson as json
from apscheduler.jobstores.base import JobLookupError
from apscheduler.schedulers.background import BackgroundScheduler
import time

# http://clien.net/cs2/bbs/board.php?bo_table=lecture&wr_id=324116 import Scheduler
class Scheduler(object):
    
    def __init__(self):
        self.sched = BackgroundScheduler()
        self.sched.start()
        self.job_id = ''
    
    def __del__(self):
        self.shutdown()
    
    def shutdown(self):
        self.sched.shutdown()
        
    def kill_scheduler(self, job_id):
        try:
            self.sched.remove_job(job_id)
        except JobLookupError as err:
            print "fail to stop scheduler: %s" % err
            return
        
    def hello(self, type, job_id):
        print("%s scheduler process_id[%s] : %d") % (type, job_id, time.localtime().tm_sec)
        
    def scheduler(self, type, job_id):
        print "%s Scheduler Start" % type
        if type == 'interval':
            self.sched.add_job(self.hello, type, seconds=10, id=job_id, args=(type, job_id))
        elif type == 'cron':
            self.sched.add_job(self.hello, type, day_of_week='mon-fri', hour='0-23', second='*/2', id=job_id, args=(type, job_id))
            
if __name__ == '__main__':
    scheduler = Scheduler()
    scheduler.scheduler('interval', "1")
    
    lastBuildDate = ''
    recentBuildTime = ''
    
    count = 0
    while True:
        print "Running main process............."
        time.sleep(30)
        count += 1
        
        api = slumber.API(base_url='http://readthedocs.org/api/v1')
        val = api.project.get(slug='put your docs name')
        #val = api.project.get(slug='python-guide-kr') #https://readthedocs.org/projects/python-guide-kr/
        recentBuildTime = val["objects"][0]["modified_date"]
        
        print 'last buld date : ' + lastBuildDate
        print 'recent build time : ' + recentBuildTime
        
        if lastBuildDate != recentBuildTime:
            lastBuildDate = recentBuildTime
            postMessage.post('build success!!')
        else:
            postMessage.post('no change')
        
        if count == 10:
            scheduler.kill_scheduler("1")
            print "###### kill interval schedule ######"