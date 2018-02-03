LOG_DIR = 'Log'

def log_path(filename):
    return LOG_DIR + '/' + filename

LOG_CONFIG = {
        'version': 1,
        'formatters': {
            'simple': {
                'format': '%(asctime)s - %(name)s - %(levelname)s -\n%(message)s',
                },
            },
        'handlers': {
            'plot': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'filename': log_path('plot.log'),
                'formatter': 'simple',
                'mode': 'a',
                },
            'clean': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'filename': log_path('clean.log'),
                'formatter': 'simple',
                'mode': 'a',
                },
            },
        'loggers': {
            'plot': {
                'handlers': ['plot'],
                'propagate': False,
                },
            'clean': {
                'handlers': ['clean'],
                'propagate': False,
                },
            },
        'root': {
            'level': 'DEBUG',
            },
        }

