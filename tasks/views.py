from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from users.models import UserProfile
from tasks.models import Task, TaskManager
from tasks.forms import AddTaskForm,  AddTaskManagerForm, UpdateTaskForm, AddSingleTaskManagerForm, UpdateTaskStatusForm
from units.models import Unit
# from django.contrib.auth.models import User
from django.http.response import Http404, JsonResponse
from django.http import HttpResponseForbidden


@login_required(login_url='login')
def allTasks(request):
    user = request.user
    # print("user: ", user)
    userProfile = UserProfile.objects.get(user=user)
    company = userProfile.company

    tasks = Task.objects.filter(company=company).order_by('-date_created')

    context = {
        "userProfile": userProfile,
        "tasks": tasks,
    }

    return render(request, 'tasks/all_tasks.html', context)


@login_required(login_url='login')
def addTask(request):
    user = request.user
    userProfile = UserProfile.objects.get(user=user)
    company = userProfile.company

    unitId = request.GET.get('unit')
    if unitId:
        unitId = unitId.split('/')[0]
        unit = Unit.objects.get(id=unitId)

    if request.method == 'POST':

        taskForm = AddTaskForm(company, unit, request.POST)
        assignedToIds = request.POST.getlist('assigned_to')
        print("assignedToIds: ", assignedToIds)
        if taskForm.is_valid():
            # print("task form valid")
            newTaskObj = taskForm.save(commit=False)
            newTaskObj.company = company
            newTaskObj.created_by = user
            newTaskObj.save()

            for userId in assignedToIds:
                assignedUser = UserProfile.objects.get(id=userId)
                # print("assignedUser: ", assignedUser.user.first_name)
                TaskManager.objects.create(
                    task=newTaskObj,
                    assigned_to=assignedUser,
                    created_by=user
                )

            return redirect('get_all_task')

    else:
        if unitId:
            # If there's any unit request then filter booking accornding to unit
            form = AddTaskForm(
                initial={"unit": unit}, company=company, unit=unit)
            form2 = AddTaskManagerForm(company=company)
        else:
            form = AddTaskForm(company=company)
            form2 = AddTaskManagerForm(company=company)
        context = {
            "form": form,
            "form2": form2,
            "userProfile": userProfile,
        }
        return render(request, 'tasks/add_task.html', context)


@ login_required(login_url='login')
def taskDetails(request, task_id):
    user = request.user
    # print("user: ", user)
    userProfile = UserProfile.objects.get(user=user)
    company = userProfile.company
    context = {}
    try:
        task = Task.objects.get(id=task_id, is_deleted=False)
    except Task.DoesNotExist:
        raise Http404()

    taskManagers = TaskManager.objects.filter(
        task=task).order_by('-date_created')
    updateTaskForm = UpdateTaskForm(instance=task)
    addTaskManagerForm = AddSingleTaskManagerForm(company=company)

    updateTaskStatusForm = UpdateTaskStatusForm(instance=task)

    context = {
        "userProfile": userProfile,
        "task": task,
        "taskManagers": taskManagers,
        "form": updateTaskForm,
        "addTaskManagerForm": addTaskManagerForm,
        "updateTaskStatusForm": updateTaskStatusForm
    }

    if request.method == 'POST':
        updateTaskForm = UpdateTaskForm(request.POST, instance=task)
        if updateTaskForm.is_valid():
            print("Form is Valid")
            updateTaskForm.save()

            return redirect('task_details', task_id=task_id)

    return render(request, 'tasks/task_details.html', context)


@ login_required(login_url='login')
def updateTaskStatus(request, task_id):
    if request.method == 'POST':
        try:
            task = Task.objects.get(id=task_id, is_deleted=False)
            newTaskStatus = request.POST['task_status']
            task.task_status = newTaskStatus
            task.save()
            return redirect('task_details', task_id=task_id)
        except Task.DoesNotExist:
            raise Http404()


@ login_required(login_url='login')
def addTaskManager(request, task_id):
    if request.method == 'POST':
        userProfile = UserProfile.objects.get(user=request.user)
        company = userProfile.company
        task = Task.objects.get(id=task_id)
        taskManagerForm = AddSingleTaskManagerForm(company, request.POST)
        if taskManagerForm.is_valid():
            print("form valid")
            newTaskManagerObj = taskManagerForm.save(commit=False)
            newTaskManagerObj.task = task
            newTaskManagerObj.created_by = request.user
            newTaskManagerObj.save()
        return redirect('task_details', task_id=task_id)


@ login_required(login_url='login')
def removeTaskManager(request, task_manager_id):
    if request.method == 'POST':
        taskManager = TaskManager.objects.get(id=task_manager_id)
        task_id = taskManager.task.id
        taskManager.delete()
        return redirect('task_details', task_id=task_id)


@ login_required(login_url='login')
def updateTaskManagerStatus(request, task_manager_id):
    if request.method == 'POST':
        taskManager = TaskManager.objects.get(id=task_manager_id)
        task = taskManager.task
        isLead = request.POST.get('is_lead_manager')

        if isLead == 'on':
            isLeadValue = True
        else:
            isLeadValue = False

        # print("isLead: ", isLeadValue)
        taskManagers = TaskManager.objects.filter(task=task)
        for item in taskManagers:
            if item.id == task_manager_id:
                # print(task_manager_id, " : ", item.id)
                item.is_lead_manager = isLeadValue
            else:
                item.is_lead_manager = False
            item.save()
        # taskManager.is_lead_manager = isLead
        # taskManager.save()

        return redirect('task_details', task_id=task.id)
