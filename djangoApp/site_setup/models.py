from django.db import models
from utils.model_validators import validate_png
from utils.images import resize_image
# Create your models here.

class MenuLink(models.Model):
    class Meta:
        verbose_name = 'Menu Link'
        verbose_name_plural = 'Menu Links'
    
    text = models.CharField(max_length=50)
    url_or_path = models.CharField(max_length=2048)
    new_tab = models.BooleanField(default=False)
    site_setup = models.ForeignKey(
        'SiteSetup', on_delete=models.CASCADE, blank=True, null=True,
        default=None,
    )

    def __str__(self): 
        return self.text
    
class SiteSetup(models.Model):
    class Meta:
        verbose_name = 'Setup'
        verbose_name_plural = 'Setup'

    title = models.CharField(max_length=65)
    description = models.CharField(max_length=255)

    show_header = models.BooleanField(default=True)
    show_search = models.BooleanField(default=True)
    show_menu = models.BooleanField(default=True)
    show_description = models.BooleanField(default=True)
    show_pagination = models.BooleanField(default=True)
    show_footer = models.BooleanField(default=True)
    fave_icon = models.ImageField(upload_to='assets/faveicon/%Y/%m/', blank=True, default='', validators=[validate_png,])

    def save(self):
        current_faveicon_name = str(self.fave_icon.name)
        super().save()
        faveIcon_changed = False

        if self.fave_icon:
            faveIcon_changed = current_faveicon_name != self.fave_icon.name

        if faveIcon_changed:
            resize_image(self.fave_icon, 32)
            
    def __str__(self):
        return self.title