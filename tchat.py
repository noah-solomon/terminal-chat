import datetime
import click
import requests
import os
import json

BASE_URL = 'http://localhost:8000/api'
USER_ID_FILENAME = os.path.join(os.path.expanduser("~"), ".tchat_id")


@click.group()
def cli():
    pass


@cli.command()
@click.option('--name', prompt='Name', help='The name of the user.')
def sign_up(name):
    """Command to sign up."""
    if os.path.exists(USER_ID_FILENAME):
        click.echo('You already have a user!')
        return
    click.echo('Creating user %s' % name)
    res = requests.post(BASE_URL + '/users/', json={'name': name})
    if res.status_code == 201:
        user_id = res.json()['data']['id']
        with open(USER_ID_FILENAME, "w") as file:
            file.write(str(user_id))
        click.echo('User created!')
    else:
        click.echo(f'Error creating user: \n {res.text}')


@cli.command()
def send():
    """Command to send a message."""
    user_id = get_user_id()
    if user_id is None:
        click.echo('You must create a user first!')
        return

    content = click.prompt('Message content', type=str)

    receiver_options = requests.get(BASE_URL + '/users/').json()['data']
    if receiver_options is []:
        click.echo('No users to send messages to!')
        return

    click.echo('Receiver ID options:')
    for user in receiver_options:
        click.echo('ID: %s, Name: %s' % (user['id'], user['name']))

    receiver_id = click.prompt('Receiver ID', type=int)

    click.echo('Sending message...')
    res = requests.post(BASE_URL + '/messages/', json={
        'content': content,
        'sender_id': user_id,
        'receiver_id': receiver_id
    })
    if res.status_code == 201:
        click.echo('Message sent!')
    else:
        click.echo(f'Error creating message: \n {res.text}')


# @cli.command()
# def get_unread():
#     """Command to get unread messages (and mark as read)."""
#     user_id = get_user_id()
#     if user_id is None:
#         click.echo('You must create a user first!')
#         return

#     res = requests.get(f'{BASE_URL}/users/{user_id}/messages?unread=true')
#     if res.status_code == 200:
#         data = res.json().get('data')
#         for message in data:
#             date = message.get("date")
#             content = message.get("content")
#             sender_id = message.get("sender_id")
#             sender_name = message.get("sender_name")
#             click.echo(f'{date} - {sender_name} ({sender_id}): {content}')
#         if data == []:
#             click.echo('No unread messages.')
#     else:
#         click.echo(f'Error getting messages: \n {res.text}')


@cli.command()
@click.option('--all/-a', is_flag=True, help='Get all messages.')
def read(all):
    """Command to get unread messages. Use --all to get all messages."""
    user_id = get_user_id()
    if user_id is None:
        click.echo('You must create a user first!')
        return

    res = requests.get(
        '{}/users/{}/messages/{}'.format(BASE_URL,
                                         user_id, '' if all else '?unread=true')
    )
    if res.status_code == 200:
        data = res.json().get('data')
        click.echo()
        for message in data:
            date = datetime.datetime.strptime(
                message.get("date"), '%Y-%m-%d %H:%M:%S.%f')
            content = message.get("content")
            sender_id = message.get("sender_id")
            sender_name = message.get("sender_name")
            if date.year == datetime.datetime.now().year:
                if date.day == datetime.datetime.now().day:
                    date_formatted = date.strftime('today at %H:%M%p')
                elif date.day == datetime.datetime.now().day - 1:
                    date_formatted = date.strftime('yesterday at %H:%M%p')
                else:
                    date_formatted = date.strftime('on %b %d at %H:%M%p')
            else:
                date_formatted = date.strftime('on %b %d, %Y at %H:%M%p')
            click.echo(
                f'{sender_name} (ID: {sender_id}) {date_formatted}: {content}')
        if not data:
            click.echo('No{} messages.'.format('' if all else ' unread'))
        click.echo()
    else:
        click.echo(f'Error getting messages: \n {res.text}')


def get_user_id():
    """Helper to get a user id from the ID file."""
    user_id = None
    if os.path.exists(USER_ID_FILENAME):
        with open(USER_ID_FILENAME, "r") as file:
            user_id = int(file.read())
    return user_id


if __name__ == '__main__':
    cli()
