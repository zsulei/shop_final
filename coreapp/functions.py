

def handle_upload_avatar(avatar):
    new_avatar = 'avatars/' + avatar.name
    with open('media/' + new_avatar, 'wb+') as f:
        for chunk in avatar.chunks():
            f.write(chunk)
    return new_avatar
