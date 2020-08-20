from django.shortcuts import get_object_or_404
from manager_school.models import *


def group_filter(request):
    group = request.GET.get('group', '')
    groups = request.user.groupmodel_set.all()
    if group == '':
        current_group = groups[0]
    else:
        group_id = int(group)
        current_group = get_object_or_404(GroupModel, id=group_id)
    return groups, current_group


def save_picture(request, payment_stages, picture):
    paid_stages, unpaid_stages, stage_wo_check = stage_checker(payment_stages)
    stage = PaymentStage.objects.get(id=request.POST.get('id'))
    first_stage_wo_check = stage_wo_check[0]
    first_unpaid_stage = unpaid_stages[0]
    if stage.id == first_unpaid_stage.id:
        if stage.id == first_stage_wo_check.id:
            stage.picture = picture
            stage.save()


def stage_checker(payment_stages):
    paid_stages = []
    unpaid_stages = []
    stage_wo_check = []
    for stage in payment_stages:
        if stage.picture:
            if stage.is_confirmed == True:
                paid_stages.append(stage)
            else:
                unpaid_stages.append(stage)
        else:
            stage_wo_check.append(stage)
            unpaid_stages.append(stage)
    return paid_stages, unpaid_stages, stage_wo_check


def get_user_payment(request, current_group):
    user_payment = UserPayment.objects.filter(contract__group__id=current_group.id).get(
        contract__account__id=request.user.id)
    return user_payment


def get_payment_stages(request, current_group):
    payment_stages = PaymentStage.objects.filter(payment__contract__group__id=current_group.id).filter(
        payment__contract__account__id=request.user.id)
    return payment_stages


def get_paid_percent(payment_stages):
    stages_amount = int(payment_stages.count())
    stages_paid_list = []
    for stage in payment_stages:
        if stage.is_confirmed:
            stages_paid_list.append(stage)
    paid_amount = int(len(stages_paid_list))
    percentage = (paid_amount * 100) / stages_amount
    return percentage, paid_amount, stages_amount


def get_alert(request, payment_stages):
    stage = PaymentStage.objects.get(id=request.POST.get('id'))
    paid_stages, unpaid_stages, stage_wo_check = stage_checker(payment_stages)
    first_unpaid_stage = unpaid_stages[0]
    first_stage_wo_check = stage_wo_check[0]
    if stage.id == first_stage_wo_check.id:
        if stage.id != first_unpaid_stage.id:
            alert = 'Wait for manager'
        else:
            alert = 'Success'
    else:
        if stage.id == first_unpaid_stage.id:
            alert = 'Already paid'
        else:
            alert = 'No check'
    return alert
