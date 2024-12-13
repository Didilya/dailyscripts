import csv
import environ
from contextlib import contextmanager
from user.models import User


@contextmanager
def s3_file(path='export', filename=None, prefix=''):
    import boto3
    from datetime import datetime
    from io import StringIO
    from django.utils.crypto import get_random_string

    env = environ.Env()
    encoding = 'utf-8'
    now = datetime.now().strftime('%Y%m%dT%H%M%S')
    random_name = get_random_string(8)
    filename = filename or f'{path}/{prefix}{now}-{random_name}.csv'

    f = StringIO()
    try:
        yield f
    finally:
        f.seek(0)

    s3_resource = boto3.resource('s3')
    s3_resource.Object(env("AWS_STORAGE_BUCKET_NAME"), filename).put(Body=f.getvalue().encode(encoding))
    print(f"Uploaded to http://{env('AWS_STORAGE_BUCKET_NAME')}.s3.amazonaws.com/{filename}")


with s3_file(prefix='users_phones-') as f:
    writer = csv.writer(f)
    writer.writerow([
        "id", "uid", "name",
        "surname", "phone", "created",
    ])
    for obj in User.objects.filter(created__gte='2025-11-30').filter(created__lte='2024-12-01').order_by('-created'):
        writer.writerow([obj.id, obj.uid, obj.name, obj.surname, obj.phone, obj.created])
