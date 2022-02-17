import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from celery.result import AsyncResult

from .task import sample_task

def index(request):
    return render(request, 'index.html')

def ping(request):
    if request.method == 'GET':
        data = {'ping': 'pong!'}
        return JsonResponse(data)

@csrf_exempt
def create_task(request):
    if request.method == 'POST':
        payload = json.loads(request.body.decode('utf-8'))
        task_type = payload['type']
        task = sample_task.delay()
        return JsonResponse({ "taskType": task_type, "taskId": task.id }, status=202)

@csrf_exempt
def get_task_status(request, task_id):
    if request.method == 'GET':
        task_result = AsyncResult(task_id)
        result = {
            "task_id": task_id,
            "task_status": task_result.status,
            "task_result": task_result.result
        }
        return JsonResponse(result, status=200)
