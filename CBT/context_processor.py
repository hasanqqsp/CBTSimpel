from CBT import settings
def global_variables(request):
    return {
        "SITE_NAME" : settings.SITE_NAME,
        "SITE_ADDRESS" : settings.SITE_ADDRESS
    }