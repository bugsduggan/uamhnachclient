import argparse
import json
import os

from uamhnachclient.exc import ClientException
from uamhnachclient.client import Client


def get_client(*args, **kwargs):
    host = kwargs.pop('host')
    email = kwargs.pop('email')
    password = kwargs.pop('password')

    return Client(api_host=host, email=email, password=password)


def user_list(*args, **kwargs):
    client = get_client(**kwargs)
    return client.users()


def user_create(*args, **kwargs):
    client = get_client(**kwargs)
    name = kwargs.pop('user_name')
    email = kwargs.pop('user_email')
    password = kwargs.pop('user_password')
    create_group = kwargs.pop('create_group')

    u_resp = client.create_user(name=name, email=email, password=password)
    if create_group:
        g_resp = client.create_group(name)
        client.add_to_group(g_resp['id'], u_resp['id'])
    return client.user(u_resp['id'])


def user_show(*args, **kwargs):
    client = get_client(**kwargs)
    user_id = kwargs.pop('user_id')
    return client.user(int(user_id))


def user_update(*args, **kwargs):
    client = get_client(**kwargs)
    user_id = kwargs.pop('user_id')
    name = kwargs.pop('user_name')
    email = kwargs.pop('user_email')
    password = kwargs.pop('user_password')
    return client.update_user(int(user_id), name=name, email=email,
                              password=password)


def user_delete(*args, **kwargs):
    client = get_client(**kwargs)
    user_id = kwargs.pop('user_id')
    client.delete_user(int(user_id))


def group_list(*args, **kwargs):
    client = get_client(**kwargs)
    return client.groups()


def group_create(*args, **kwargs):
    client = get_client(**kwargs)
    group_name = kwargs.pop('group_name')
    return client.create_group(group_name)


def group_show(*args, **kwargs):
    client = get_client(**kwargs)
    group_id = kwargs.pop('group_id')
    return client.group(int(group_id))


def group_add_user(*args, **kwargs):
    client = get_client(**kwargs)
    group_id = kwargs.pop('group_id')
    user_id = kwargs.pop('user_id')
    return client.add_to_group(int(group_id), int(user_id))


def group_delete_user(*args, **kwargs):
    client = get_client(**kwargs)
    group_id = kwargs.pop('group_id')
    user_id = kwargs.pop('user_id')
    return client.delete_from_group(int(group_id), int(user_id))


def group_delete(*args, **kwargs):
    client = get_client(**kwargs)
    group_id = kwargs.pop('group_id')
    client.delete_group(int(group_id))


def permission_list(*args, **kwargs):
    client = get_client(**kwargs)
    return client.permissions()


def permission_create(*args, **kwargs):
    client = get_client(**kwargs)
    permission_name = kwargs.pop('permission_name')
    return client.create_permission(permission_name)


def permission_show(*args, **kwargs):
    client = get_client(**kwargs)
    permission_id = kwargs.pop('permission_id')
    return client.permission(int(permission_id))


def permission_add_group(*args, **kwargs):
    client = get_client(**kwargs)
    permission_id = kwargs.pop('permission_id')
    group_id = kwargs.pop('group_id')
    return client.allow_group(int(permission_id), int(group_id))


def permission_delete_group(*args, **kwargs):
    client = get_client(**kwargs)
    permission_id = kwargs.pop('permission_id')
    group_id = kwargs.pop('group_id')
    return client.disallow_group(int(permission_id), int(group_id))


def permission_delete(*args, **kwargs):
    client = get_client(**kwargs)
    permission_id = kwargs.pop('permission_id')
    client.delete_permission(int(permission_id))


def main(args):
    parser = argparse.ArgumentParser()

    parser.add_argument('-H', '--host',
                        default=os.environ.get('UAMHNACH_API_HOST', None))
    parser.add_argument('-e', '--email',
                        default=os.environ.get('UAMHNACH_EMAIL', None))
    parser.add_argument('-p', '--password',
                        default=os.environ.get('UAMHNACH_PASSWORD', None))

    subparsers = parser.add_subparsers(title='Commands')

    parser_user_list = subparsers.add_parser('user-list')
    parser_user_list.set_defaults(func=user_list)

    parser_user_create = subparsers.add_parser('user-create')
    parser_user_create.add_argument('--user-name', required=True)
    parser_user_create.add_argument('--user-email', required=True)
    parser_user_create.add_argument('--user-password', required=True)
    parser_user_create.add_argument('--create-group', action='store_true',
                                    default=False)
    parser_user_create.set_defaults(func=user_create)

    parser_user_show = subparsers.add_parser('user-show')
    parser_user_show.add_argument('-u', '--user-id', required=True)
    parser_user_show.set_defaults(func=user_show)

    parser_user_update = subparsers.add_parser('user-update')
    parser_user_update.add_argument('-u', '--user-id', required=True)
    parser_user_update.add_argument('--user-name')
    parser_user_update.add_argument('--user-email')
    parser_user_update.add_argument('--user-password')
    parser_user_update.set_defaults(func=user_update)

    parser_user_delete = subparsers.add_parser('user-delete')
    parser_user_delete.add_argument('-u', '--user-id', required=True)
    parser_user_delete.set_defaults(func=user_delete)

    parser_group_list = subparsers.add_parser('group-list')
    parser_group_list.set_defaults(func=group_list)

    parser_group_create = subparsers.add_parser('group-create')
    parser_group_create.add_argument('--group-name', required=True)
    parser_group_create.set_defaults(func=group_create)

    parser_group_show = subparsers.add_parser('group-show')
    parser_group_show.add_argument('-g', '--group-id', required=True)
    parser_group_show.set_defaults(func=group_show)

    parser_group_add_user = subparsers.add_parser('group-add-user')
    parser_group_add_user.add_argument('-g', '--group-id', required=True)
    parser_group_add_user.add_argument('-u', '--user-id', required=True)
    parser_group_add_user.set_defaults(func=group_add_user)

    parser_group_delete_user = subparsers.add_parser('group-delete-user')
    parser_group_delete_user.add_argument('-g', '--group-id', required=True)
    parser_group_delete_user.add_argument('-u', '--user-id', required=True)
    parser_group_delete_user.set_defaults(func=group_delete_user)

    parser_group_delete = subparsers.add_parser('group-delete')
    parser_group_delete.add_argument('-g', '--group-id', required=True)
    parser_group_delete.set_defaults(func=group_delete)

    parser_permission_list = subparsers.add_parser('permission-list')
    parser_permission_list.set_defaults(func=permission_list)

    parser_permission_create = subparsers.add_parser('permission-create')
    parser_permission_create.add_argument('--permission-name',
                                          required=True)
    parser_permission_create.set_defaults(func=permission_create)

    parser_permission_show = subparsers.add_parser('permission-show')
    parser_permission_show.add_argument('-p', '--permission-id',
                                        required=True)
    parser_permission_show.set_defaults(func=permission_show)

    parser_permission_add_group = \
        subparsers.add_parser('permission-add-group')
    parser_permission_add_group.add_argument('-p', '--permission-id',
                                             required=True)
    parser_permission_add_group.add_argument('-g', '--group-id',
                                             required=True)
    parser_permission_add_group.set_defaults(func=permission_add_group)

    parser_permission_delete_group = \
        subparsers.add_parser('permission-delete-group')
    parser_permission_delete_group.add_argument('-p', '--permission-id',
                                                required=True)
    parser_permission_delete_group.add_argument('-g', '--group-id',
                                                required=True)
    parser_permission_delete_group.set_defaults(func=permission_delete_group)

    parser_permission_delete = subparsers.add_parser('permission-delete')
    parser_permission_delete.add_argument('-p', '--permission-id',
                                          required=True)
    parser_permission_delete.set_defaults(func=permission_delete)

    args = parser.parse_args(args)

    if args.host is None:
        raise ClientException('You must specify api_host either via --host ',
                              'or os.environ[\'UAMHNACH_API_HOST\']')
    if args.email is None:
        raise ClientException('You must specify an email either via --email ',
                              'or os.environ[\'UAMHNACH_EMAIL\']')
    if args.password is None:
        raise ClientException('You must specify a password either via '
                              '--password or '
                              'os.environ[\'UAMHNACH_PASSWORD\']')

    print json.dumps(args.func(**vars(args)), indent=2)
