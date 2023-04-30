import random
import uuid
from typing import Protocol, OrderedDict

from django.core.cache import cache
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt import tokens

from . import models, repos, tasks


class UserServicesInterface(Protocol):

    def create_user(self, data: OrderedDict) -> dict:
        ...

    def verify_user(self, data: OrderedDict) -> models.CustomUser | None:
        ...

    def create_token(self, data: OrderedDict) -> dict:
        ...

    def verify_token(self, data: OrderedDict) -> dict:
        ...


class UserServicesV1:
    user_repos: repos.UserReposInterface = repos.UserReposV1()

    def create_user(self, data: OrderedDict) -> dict:
        session_id = self._verify_email(data=data)

        return {
            'session_id': session_id,
        }

    def verify_user(self, data: OrderedDict) -> models.CustomUser | None:
        user_data = cache.get(data['session_id'])

        if not user_data:
            raise ValidationError

        if data['code'] != user_data['code']:
            raise ValidationError

        self.user_repos.create_user(data={
            'first_name': user_data['first_name'],
            'last_name': user_data['last_name'],
            'email': user_data['email'],
            'phone_number': user_data['phone_number'],
            'date_of_birth': user_data['date_of_birth']
        })

    def create_token(self, data: OrderedDict) -> dict:
        session_id = self._verify_email(data=data, is_exist=True)

        return {
            'session_id': session_id,
        }

    def verify_token(self, data: OrderedDict) -> dict:
        session = cache.get(data['session_id'])
        if not session:
            raise ValidationError

        if session['code'] != data['code']:
            raise ValidationError

        user = self.user_repos.get_user(data={'email': session['email']})
        access = tokens.AccessToken.for_user(user=user)
        refresh = tokens.RefreshToken.for_user(user=user)

        return {
            'access': str(access),
            'refresh': str(refresh),
        }

    def _verify_email(self, data: OrderedDict, is_exist: bool = False) -> str:
        email = data['email']
        if is_exist:
            user = self.user_repos.get_user(data)
            email = str(user.email)

        code = self._generate_code()
        session_id = self._generate_session_id()
        cache.set(session_id, {'email': email, 'code': code, **data}, timeout=300)

        tasks.send_code_to_email.delay(email=data['email'], code=code)

        return session_id

    @staticmethod
    def _generate_code(length: int = 4) -> str:
        numbers = [str(i) for i in range(10)]
        return ''.join(random.choices(numbers, k=length))

    @staticmethod
    def _generate_session_id() -> str:
        return str(uuid.uuid4())

