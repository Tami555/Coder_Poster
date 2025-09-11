from Coder.celery import app
from .models import Post

@app.task
def check_correct_post(id_post, text):
    print(id_post, text)
    post = Post.objects.get(pk=id_post)
    post.status = Post.Status.APPROVED
    post.save()
    print('ОДОБРЕННО !!!!!!!!!!!!')