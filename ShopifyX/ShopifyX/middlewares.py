
from django.utils import timezone
from django.contrib.auth.models import User
from Profile.models import UserProfile  # Замените 'Profile' на имя вашего приложения

class UserVisitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Проверка, что пользователь аутентифицирован
        if request.user.is_authenticated:
            # Попытка получить профиль пользователя
            try:
                user_profile = UserProfile.objects.get(user=request.user)
            except UserProfile.DoesNotExist:
                # Если профиля нет, создаем его
                user_profile = UserProfile.objects.create(user=request.user)

            # Обновление данных профиля
            user_profile.last_visit = timezone.now()
            user_profile.visit_count += 1
            user_profile.save()

        return response