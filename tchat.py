import click
import requests
import os

BASE_URL = 'http://localhost:5000/api'

# click command to create a user using API
@click.command()
@click.option('--name', prompt='Name', help='The name of the user.')
def create_user(name):
    click.echo('Creating user %s' % name)
    res = requests.post(BASE_URL + '/users/', data={'name': name})
    if res.status_code == 201:
        user_id = res.json()['data']['id']
        os.environ["TCHAT_ID"] = "%s" % user_id
        click.echo('User created!')
    else:
        click.echo('Error creating user: %s' % res.json()['error'])

# click command to send a message using API
@click.command()
@click.option('--content', prompt='Content', help='The content of the message.')
def send_message(content):
    user_id = os.environ.get('TCHAT_ID')
    if user_id is None:
        click.echo('You must create a user first!')
        return
    
    click.echo('Sending message...')
    res = requests.post(BASE_URL + '/messages/', data={
        'content': content,
        'sender_id': user_id
    })
    if res.status_code == 201:
        click.echo('Message created!')
    else:
        click.echo('Error creating message: %s' % res.json()['error'])
