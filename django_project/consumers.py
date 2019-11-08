from channels import Group
from channels.sessions import channel_session
from blog.models import Post, Answer
import json


@channel_session
def ws_connect(message):

    label = message['path'].strip('/')
    label =label.split('/')
    Group("main").add(message.reply_channel)
    message.reply_channel.send({"accept": True})

@channel_session
def ws_receive(message):

    label = message['path'].strip('/')
    label = label.split('/')
    pos = Post.objects.get(id=label[2])
    answers = Answer.objects.filter(id =label[2])



    person = pos.author_id
    data = {}
    data['handle'] = pos.author_id
    data['message'] = pos.title
    # m = room.messages.create(handle=data['handle'], message=data['message'])
    Group("main").send({'text': json.dumps(data)})

    # room = Post.objects.get(id=label[2])
    # data = json.loads(message['text'])
    # m = room.messages.create(handle=data['handle'], message=data['message'])
    # Group('chat-'+label).send({'text': json.dumps(m.as_dict())})