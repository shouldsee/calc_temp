
import sys
TESTING = len(sys.argv) > 1 and sys.argv[1] == 'test'
USE_MODELLER = 0
os.environ['USE_MODELLER']  = '%d'%USE_MODELLER

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'GB'
USE_I18N = True
USE_L10N = True
USE_TZ = True


STATIC_URL = '/static/'
TEMPLATE_STRING_IF_INVALID = 'No attr:'

INSTALLED_APPS += (
	'tst.apps.Config',
	'django_extensions',
)

if os.getenv('TRAVIS', None):
	# Configuration for travis
	SECRET_KEY = "SecretKeyForUseOnTravis"
	DEBUG = False
	TEMPLATE_DEBUG = True

	DATABASES['default'] = {
			'ENGINE': 'django.db.backends.mysql',
			'NAME': 'django',
			'TEST':{
				'NAME':'test_django'
				},
			# 'USER': 'root',
			'USER': 'travis',
			'PASSWORD': '',
			'HOST': '127.0.0.1',
			# 'PORT': '3306',
		}
else:
    #Non-travis DB configuration goes here
    ### Please edit to fit your database config!
    DATABASES['default'] = {
            'ENGINE': 'django.db.backends.mysql',
            # 'NAME': 'mtest_django',  #### This is for manual testing
            'NAME': 'django',
	        'TEST': {
	            'NAME': 'test_django',
	            },            
            'USER': 'django',
            'PASSWORD': 'Django_passw0rd',
            'HOST': '127.0.0.1',
            'PORT': '3306',
        }        


ALLOWED_HOSTS += [
'testserver',
'localhost',
'127.0.0.1',
]