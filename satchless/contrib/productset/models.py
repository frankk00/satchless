from django.db import models
from django.utils.translation import ugettext_lazy as _
from localeurl.models import reverse

from satchless.product.models import Variant
from satchless.product.models import DescribedModel
from satchless.image.models import Image

class ProductSet(DescribedModel):
    slug = models.SlugField(max_length=50)

    @models.permalink
    def get_absolute_url(self):
        return ('satchless.contrib.productset.views.details', (self.slug,))

    def get_url(self):
        return reverse('satchless.contrib.productset.views.details', args=(self.slug,))

    class Meta:
        verbose_name = _("product set")
        verbose_name_plural = _("product sets")

    def variant_instances(self):
        return [psi.variant.get_subtype_instance() for psi in self.items.all()]

class ProductSetItem(models.Model):
    productset = models.ForeignKey(ProductSet, related_name='items')
    variant = models.ForeignKey(Variant)
    sort = models.PositiveIntegerField()

    def __unicode__(self):
        return u"Default variant %s" % self.variant

    class Meta:
        ordering = ['sort', 'id']
        verbose_name = _("set item")
        verbose_name_plural = _("set items")

class ProductSetImage(Image):
    product = models.ForeignKey(ProductSet, related_name='images')
    sort = models.PositiveIntegerField()

    class Meta:
        ordering = ['sort', 'id']
