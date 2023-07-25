from site_setup.models import SiteSetup

def example(req):
    return {
        'exemplo': 'TESTANDO SAMERDA AKI'
    }

def site_setup(req):
    data = SiteSetup.objects.order_by('-id').first()
    return {
        'site_setup': data
    }