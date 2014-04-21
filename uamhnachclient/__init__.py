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
    return client.create_user(name=name, email=email, password=password)


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
