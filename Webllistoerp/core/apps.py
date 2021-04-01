from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class ProfilesConfig(AppConfig):
    name = 'core'
    verbose_name = _('core')

    def ready(self):
        import core.signals  # noqa