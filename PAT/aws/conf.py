import datetime

AWS_GROUP_NAME = "VERDIA_USERS"
AWS_USERNAME = "verdia-it-user"
AWS_ACCESS_KEY_ID = "AKIA4VO5AW357L6WZQO7"
AWS_SECRET_ACCESS_KEY = "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"

AWS_FILE_EXPIRE = 200
AWS_PRELOAD_METADATA = True
AWS_QUERYSTRING_AUTH = True

DEFAULT_FILE_STORAGE = 'PAT.aws.utils.MediaRootS3BotoStorage'
STATICFILES_STORAGE = 'PAT.aws.utils.StaticRootS3BotoStorage'
AWS_STORAGE_BUCKET_NAME = 'verdia-it'
S3DIRECT_REGION = 'ap-southeast-2'
S3_URL = '//%s.s3-ap-southeast-2.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
MEDIA_URL = '//%s.s3-ap-southeast-2.amazonaws.com/media/' % AWS_STORAGE_BUCKET_NAME
MEDIA_ROOT = MEDIA_URL
STATIC_URL = S3_URL + 'static/'
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

two_months = datetime.timedelta(days=61)
date_two_months_later = datetime.date.today() + two_months
expires = date_two_months_later.strftime("%A, %d %B %Y 20:00:00 GMT")

AWS_HEADERS = { 
    'Expires': expires,
    'Cache-Control': 'max-age=%d' % (int(two_months.total_seconds()), ),
}

AWS_QUERYSTRING_AUTH = True