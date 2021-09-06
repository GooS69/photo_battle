from celery import shared_task

@shared_task
def add(x, y):
    with open(r'D:\Programms\PyCharm\photo_battle\post\out', 'w') as out:
        print(x+y, file=out)
