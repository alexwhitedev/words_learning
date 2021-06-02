from celery import shared_task, Task
from django.core.mail import EmailMessage


class CallbackTask(Task):
    def run(self, *args, **kwargs):
        pass

    def on_success(self, retval, task_id, args, kwargs):
        print("TaskID=%s, ARGS=%s, kwargs=%s, Result is %s" % (task_id, args, kwargs, retval))

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        pass


@shared_task(name="sum_two_numbers", base=CallbackTask)
def add(x, y):
    return x + y


@shared_task(name="multiply_two_numbers", base=CallbackTask)
def mul(x, y):
    total = x * y
    return total


@shared_task(name="send_email_tasks", base=CallbackTask)
def send_email(emails: list):
    message_content = "Test message"
    msg = EmailMessage("lab3", message_content, 'wordslearning.notificator@gmail.com', emails)
    msg.send()
    return "successful"