from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from robots.models import Robot
from .models import Order


@login_required
@csrf_exempt
def create_order(request, robot_id):
    if request.method == 'POST':
        try:
            robot = Robot.objects.get(id=robot_id)
            quantity = int(request.POST.get('quantity', 1))

            if robot.available and robot.quantity >= quantity:
                # Получаем текущего пользователя и связываем его с заказом
                customer = request.user.customer
                order = Order(customer=customer, robot_serial=robot.serial, quantity=quantity)
                order.save()

                return JsonResponse({'message': 'Заказ успешно создан'}, status=200)
            else:
                return JsonResponse({'error': 'Робот недоступен или количество превышает наличие'}, status=400)

        except Robot.DoesNotExist:
            return JsonResponse({'error': 'Робот не найден'}, status=404)

    elif request.method == 'GET':
        return JsonResponse({'info': 'Используйте POST-запрос для создания заказа'}, status=200)
    else:
        return JsonResponse({'error': 'Метод не поддерживается'}, status=405)


def view_orders(request):
    orders = Order.objects.all()
    data = [{'id': order.id, 'robot_model': order.robot.model, 'quantity': order.quantity} for order in orders]
    return JsonResponse({'orders': data})
