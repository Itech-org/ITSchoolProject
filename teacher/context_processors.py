from manager_school.models import *

def get_groups(request):
    groups = GroupModel.objects.filter(teacher__id=request.user.id)
    return {'groups':groups}
