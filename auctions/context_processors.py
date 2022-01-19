from .models import *


def add_variable_to_context(request):
    notifmessages = Messages.objects.filter(receiver=request.user.username, read=False)
    overallnotifs = Notifications.objects.filter(user=request.user.username, read=False)

    if request.user.is_authenticated:
        currentmode = Mode.objects.get(user=request.user.username)

    else:
        currentmode = "none"
    return {
        'testme': notifmessages,
        'metoo': overallnotifs,
        'currentmode': currentmode

    }