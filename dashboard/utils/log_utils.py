from dashboard.models import ActivityLog

def add_log(user, action):
    ActivityLog.objects.create(user=user, action=action)
