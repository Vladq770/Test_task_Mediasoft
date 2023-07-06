def update_likes(sender, instance, **kwargs):
    instance.post.likes += 1
    instance.post.save()

