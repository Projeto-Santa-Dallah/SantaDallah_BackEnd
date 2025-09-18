from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from drf_spectacular.extensions import OpenApiAuthenticationExtension
from drf_spectacular.plumbing import build_bearer_security_scheme_object
from passageidentity import Passage, PassageError
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import Group

from core.models import User  # seu modelo custom

PASSAGE_APP_ID = settings.PASSAGE_APP_ID
PASSAGE_API_KEY = settings.PASSAGE_API_KEY
psg = Passage(PASSAGE_APP_ID, PASSAGE_API_KEY)


class TokenAuthenticationScheme(OpenApiAuthenticationExtension):
    target_class = "core.authentication.TokenAuthentication"
    name = "tokenAuth"
    match_subclasses = True
    priority = -1

    def get_security_definition(self, auto_schema):
        return build_bearer_security_scheme_object(
            header_name="Authorization",
            token_prefix="Bearer",
        )


class TokenAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request) -> tuple[User, None]:
        if not request.headers.get("Authorization"):
            return None

        token = request.headers.get("Authorization").split()[1]
        psg_user_id: str = self._get_user_id(token)
        user: User = self._get_or_create_user(psg_user_id)

        return (user, None)

    def _get_or_create_user(self, psg_user_id) -> User:
        try:
            user: User = User.objects.get(passage_id=psg_user_id)
            psg_user = psg.user.get(psg_user_id)  # já retorna dict/objeto
        except ObjectDoesNotExist:
            try:
                psg_user = psg.user.get(psg_user_id)
                user: User = User.objects.create_user(
                passage_id=psg_user.id,
                email=psg_user.email,
                name=psg_user.email.split("@")[0]
            )
            except PassageError as e:
                raise AuthenticationFailed("Erro ao obter informações do usuário do Passage.") from e

        self._promote_if_admin(user)
        return user

    def _promote_if_admin(self, user: User) -> None:
        if user.email in settings.ADMIN_EMAILS:
            group, _ = Group.objects.get_or_create(name=settings.ADMIN_GROUP_NAME)
            user.groups.add(group)
            user.is_staff = True
            user.is_superuser = True
            user.save()
        else:
            group, _ = Group.objects.get_or_create(name=settings.CLIENTE_GROUP_NAME)
            user.groups.add(group)
            user.is_staff = False
            user.is_superuser = False
            user.save()

    def _get_user_id(self, token) -> str:
        try:
            return psg.auth.validate_jwt(token)
        except PassageError as e:
            raise AuthenticationFailed("Falha na autenticação do token.") from e
