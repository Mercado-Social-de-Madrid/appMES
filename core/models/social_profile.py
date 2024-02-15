from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.translation import gettext as _
from polymorphic.models import PolymorphicModel


class SocialNetwork(models.Model):
    name = models.CharField(primary_key=True, max_length=50, verbose_name=_("Nombre"))
    logo = models.FileField(verbose_name=_("Logo"), upload_to="logos_redes_sociales", validators=[FileExtensionValidator(["svg"]), ])

    class Meta:
        verbose_name = _('Red Social')
        verbose_name_plural = _('Redes Sociales')

    def __str__(self):
        return self.name


class SocialProfile(PolymorphicModel):
    social_network = models.ForeignKey(SocialNetwork, verbose_name=_("Red social"), on_delete=models.CASCADE)
    url = models.URLField(verbose_name=_("Enlace a la red social"))


class NodeSocialProfile(SocialProfile):
    # Social profile related to a node
    node = models.ForeignKey("core.Node", verbose_name=_("Mercado"), on_delete=models.CASCADE, related_name="social_profiles")


class ProviderSocialProfile(SocialProfile):
    # Social profile related to a provider
    provider = models.ForeignKey("market.Provider", verbose_name=_("Proveedora"), on_delete=models.CASCADE, related_name="social_profiles")
