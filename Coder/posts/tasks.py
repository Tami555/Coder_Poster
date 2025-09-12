from psycopg import DatabaseError
from Coder.celery import app
from .models import Post
from .checks_posts import RussianProfanityFilter


@app.task(bind=True, max_retries=3, default_retry_delay=300)
def check_correct_post(self, id_post, title, description, content):
    try:
        post = Post.objects.get(pk=id_post)
        # запуск проверок:
        # проверка на цензурность
        profanity = RussianProfanityFilter()
        if profanity.contains_profanity(title):
            post.moderator_comment = 'заголовок поста содержит нецензурную лексику'

        elif profanity.contains_profanity(description):
            post.moderator_comment = 'описание поста содержит нецензурную лексику'

        elif profanity.contains_profanity(content):
            post.moderator_comment = 'контент поста содержит нецензурную лексику'

        post.status = Post.Status.APPROVED if not post.moderator_comment else Post.Status.BLOCKED
        post.save()

    except DatabaseError as ex:
        # Повторить при ошибках БД
        print(f"Ошибка БД, повтор через 5 минут: {ex}")
        raise self.retry(exc=ex, countdown=300)

    except Exception as ex:
        print(f"Неизвестная ошибка: {ex}")
        return {"status": "error", "message": str(ex)}