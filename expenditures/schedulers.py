import time
from functools import partial

from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job

from django.db import models

from expenditures.tasks import NotificationTask, RecommendTask

scheduler = None

def start():
    scheduler = BackgroundScheduler(timezone='Asia/Seoul')  # 시간대 설정
    # DjangoJobStore : django 데이터베이스를 사용하여 스케쥴링 작업 저장 및 관리
    scheduler.add_jobstore(DjangoJobStore(), 'djangojobstore')
    register_events(scheduler)
    # 이전 스케줄이 완료될 때까지 대기할 시간(초) 설정
    wait_time = 1000
    job1 = partial(RecommendTask.mainjob(), RecommendTask())
    job2 = partial(NotificationTask.mainjob(), NotificationTask())
    
    scheduler.add_job(job1, 'cron', hour=8, misfire_grace_time=wait_time)  # 오전8시 실행(default)
    
    scheduler.add_job(job2, 'cron', hour=22, misfire_grace_time=wait_time)  # 오후10시 실행(default)
    
    # scheduler1.add_job(job1, 'cron', minute='*',misfire_grace_time=wait_time) #!매분 실행으로 테스트
    scheduler.start()

