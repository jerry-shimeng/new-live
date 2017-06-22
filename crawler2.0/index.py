# from douban.douban import DoubanContentParser
#
# if __name__ =="__main__":
# 	DoubanContentParser.parse("hello,树先生")
# 	pass

from apscheduler.schedulers.blocking import BlockingScheduler

from douban.douban import DoubanContentParser
from lbl.lbl import LblContentParser


def my_job():
	print("hello")


if __name__ == "__main__":
	# sched = BlockingScheduler()
	# sched.add_job(my_job, 'interval', seconds=5)
	# sched.start()
	# LblContentParser.run()
	DoubanContentParser.run(10)