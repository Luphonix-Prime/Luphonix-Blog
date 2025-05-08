INSTALLED_APPS = [
    // ... existing code ...
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # Add the providers you want to enable
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.github',
    // ... existing code ...
]

MIDDLEWARE = [
    // ... existing code ...
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    // ... existing code ...
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

SITE_ID = 1

# Provider specific settings
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': 'your-client-id',
            'secret': 'your-secret-key',
            'key': ''
        }
    },
    'github': {
        'APP': {
            'client_id': 'your-client-id',
            'secret': 'your-secret-key',
            'key': ''
        }
    }
}

# Authentication settings
LOGIN_URL = 'account_login'
LOGIN_REDIRECT_URL = '/'
ACCOUNT_LOGOUT_REDIRECT_URL = '/'