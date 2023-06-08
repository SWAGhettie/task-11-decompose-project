from djangogramm.models import *
from base.settings.base import *
import random

from faker import Faker

FAKE_AVATARS_DIR = 'fake/fake_avatars/'
FAKE_POST_IMAGES_DIR = 'fake/fake_post_images/'

AVATAR_FILES_LIST = os.listdir(MEDIA_URL + FAKE_AVATARS_DIR)
POST_FILES_LIST = os.listdir(MEDIA_URL + FAKE_POST_IMAGES_DIR)

username_list = []
fake = Faker()
fake_tags = [fake.word().lower() for i in range(30)]
image_choices_list = []


def create_fake_user(avatar_filename=None):
    if not avatar_filename:
        return False
    avatar_path = os.path.join(MEDIA_ROOT, FAKE_AVATARS_DIR, avatar_filename)

    username = fake.user_name()
    email = f'{username}@gmail.com'
    password = f'{username}password'
    full_name = fake.name()
    bio = fake.sentence(nb_words=random.randint(15, 30))

    upload_result = cloudinary.uploader.upload(avatar_path,
                                               transformation=[
                                                   {'width': 200, 'height': 200, 'crop': 'fill'}
                                               ])
    avatar_url = upload_result['public_id'] if upload_result['public_id'] else None

    user = User.objects.create_user(username=username,
                                    email=email,
                                    password=password,
                                    bio=bio,
                                    avatar=avatar_url,
                                    full_name=full_name,
                                    )
    if user:

        username_list.append(user.username)
        return user
    else:
        print("There was an error!")
        return False


def create_media(post_id):
    post = Post.objects.filter(pk=post_id).first()
    if not post:
        return False
    filename = random.choice(POST_FILES_LIST)
    if filename in image_choices_list:
        while filename in image_choices_list:
            filename = random.choice(POST_FILES_LIST)
            if len(image_choices_list) >= len(POST_FILES_LIST):
                image_choices_list.clear()
    image_choices_list.append(filename)
    file_path = os.path.join(MEDIA_ROOT, FAKE_POST_IMAGES_DIR, filename)
    upload_result = cloudinary.uploader.upload(file_path,
                                               transformation=[
                                                   {
                                                       'height': 700,
                                                       'crop': 'scale',
                                                   }
                                               ])
    file_url = upload_result['public_id'] if upload_result['public_id'] else None

    media = Media.objects.create(image=file_url, post=post)
    if not media:
        return False


def create_fake_post(username=None):
    username = username
    user = User.objects.filter(username=username).first()
    if not user:
        print(f"There was an error finding user {username}!")
        return False
    description = fake.sentence(nb_words=random.randint(10, 25))
    if len(description) > 254:
        while description >= 255:
            description = fake.sentence(nb_words=random.randint(10, 25))
    post = Post.objects.create(author=user, description=description)
    for media in range(1, random.randint(2, 4)):
        create_media(post_id=post.id)
    if post.images:
        post.generate_preview()

    tags = random.choices(fake_tags, k=random.randint(3, 5))
    for tag in tags:
        tag_obj, created = Tag.objects.get_or_create(title=tag, slug=f'#{tag}')
        post.tags.add(tag_obj)
    post.save()
    image_count = post.images.count()
    tag_count = post.tags.count()
    return post


def create_users():
    users_num = len(AVATAR_FILES_LIST)
    curr_user_count = 1
    for avatar in AVATAR_FILES_LIST:
        user = create_fake_user(avatar_filename=avatar)
        if user:
            print(f"{curr_user_count}/{users_num} User '{user.username}' created!")
            curr_user_count += 1
    return True


def create_posts():
    users = User.objects.filter(is_staff=False).all()
    if not users:
        return False
    posts_num = random.randint(15, 20)
    curr_posts_count = 1
    for post in range(1, posts_num + 1):
        user = random.choice(users)
        post = create_fake_post(username=user.username)
        if post:
            images_count = post.images.count()
            tag_count = post.tags.count()
            print(f"{curr_posts_count}/{posts_num} Post id:{post.id} created! Images:{images_count},"
                  f" Tags:{tag_count}| {post.author.username}: {post.author.posts.count()}")
            curr_posts_count += 1

    return True


def main():
    users_bool = create_users()
    posts_bool = create_posts()
    if not users_bool and not posts_bool:
        return False
    return True


if __name__ == '__main__':
    main()
