import schedule
import time

from douban.douban import DoubanContentParser
from lbl.lbl import LblContentParser


def lbl_job():
	print('lbl job is running')
	LblContentParser.run()
	print('lbl job end')


def douban_job():
	print('douban job is running')
	DoubanContentParser.run()
	print('douban job end')


def test_jon():
	print(time.time())


#
schedule.every(10).minutes.do(lbl_job)
schedule.every(10).minutes.do(douban_job)
# schedule.every(10).seconds.do(test_jon)

# schedule.every().hour.do(job)
# schedule.every().day.at("10:30").do(job)
# schedule.every().monday.do(job)
# schedule.every().wednesday.at("13:15").do(job)


if __name__ == "__main__":
	lbl_job()
	# while True:
	# 	schedule.run_pending()
	# 	time.sleep(60)
