from django.contrib.auth.models import Group, Permission, User
import os

def run():
    try:
        admin_user = User.objects.get(username=os.environ["DJANGO_ADMIN_USER"])
    except User.DoesNotExist:
        admin_user = User.objects.create_superuser(
            os.environ['DJANGO_ADMIN_USER'],
            os.environ['DJANGO_ADMIN_MAIL'],
            os.environ['DJANGO_ADMIN_PASSWORD'],
        )

    try:
        admin_dra_user = User.objects.get(username=os.environ["DJANGO_ADMIN_DRA_USER"])
    except User.DoesNotExist:
        admin_dra_user = User.objects.create_user(
            os.environ["DJANGO_ADMIN_DRA_USER"], 
            email = os.environ["DJANGO_ADMIN_DRA_MAIL"],
            password = os.environ["DJANGO_ADMIN_DRA_PASSWORD"],
            is_staff=True,
        )

    try:
        usuario_dra_user = User.objects.get(username=os.environ["DJANGO_USUARIO_DRA_USER"])
    except User.DoesNotExist:
        usuario_dra_user = User.objects.create_user(
            os.environ["DJANGO_USUARIO_DRA_USER"], 
            email = os.environ["DJANGO_USUARIO_DRA_MAIL"],
            password = os.environ["DJANGO_USUARIO_DRA_PASSWORD"],
            is_staff=True,
        )

    try:
        admin_der_user = User.objects.get(username=os.environ["DJANGO_ADMIN_DER_USER"])
    except User.DoesNotExist:
        admin_der_user = User.objects.create_user(
            os.environ["DJANGO_ADMIN_DER_USER"], 
            email = os.environ["DJANGO_ADMIN_DER_MAIL"],
            password = os.environ["DJANGO_ADMIN_DER_PASSWORD"],
            is_staff=True,
        )

    try:
        usuario_der_user = User.objects.get(username=os.environ["DJANGO_USUARIO_DER_USER"])
    except User.DoesNotExist:
        usuario_der_user = User.objects.create_user(
            os.environ["DJANGO_USUARIO_DER_USER"], 
            email = os.environ["DJANGO_USUARIO_DER_MAIL"],
            password = os.environ["DJANGO_USUARIO_DER_PASSWORD"],
            is_staff=True,
        )


    admin_dra_group, admin_dra_created = Group.objects.get_or_create(name="admin-dra-grupo")
    usuario_dra_group, usuario_dra_created = Group.objects.get_or_create(name="usuario-dra-grupo")
    admin_der_group, admin_der_created = Group.objects.get_or_create(name="admin-der-grupo")
    usuario_der_group, usuario_der_created = Group.objects.get_or_create(name="usuario-der-grupo")

    dra_model_codes = ["sarh","tecnicaldatasub","tecnicaldatasub","epsa","supplyarea"]

    for i, group, created in zip(range(2), [admin_dra_group,usuario_dra_group],[admin_dra_created,usuario_dra_created]):
        for model_code in dra_model_codes:
            actions = ["add","change","delete","view"] if i == 0 else ["view"]
            for action in actions:
                permission = Permission.objects.get(codename=f"{action}_{model_code}")
                if created:
                    group.permissions.add(permission)

    der_model_codes = ["epsa","supplyarea","variable","indicator","variablereport","indicatormeasurement","coopexpense","muniexpense","plan","plangoal","poa",]

    for i, group, created in zip(range(2),[admin_der_group,usuario_der_group],[admin_der_created,usuario_der_created]):
        for model_code in der_model_codes:
            actions = ["add","change","delete","view"] if i == 0 else ["view"]
            for action in actions:
                permission = Permission.objects.get(codename=f"{action}_{model_code}")
                if created:
                    group.permissions.add(permission)

    admin_dra_group.user_set.add(admin_dra_user)
    usuario_dra_group.user_set.add(usuario_dra_user)
    admin_der_group.user_set.add(admin_der_user)
    usuario_der_group.user_set.add(usuario_der_user)
