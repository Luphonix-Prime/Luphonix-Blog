from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.blocks import CharBlock, TextBlock, StructBlock
from wagtail.snippets.models import register_snippet


class HeroSectionBlock(StructBlock):
    heading = CharBlock(required=True)
    subheading = TextBlock(required=True)
    background_image = ImageChooserBlock(required=False)
    cta_text = CharBlock(required=False)
    cta_link = CharBlock(required=False)


class FeatureBlock(StructBlock):
    title = CharBlock(required=True)
    description = TextBlock(required=True)
    icon = CharBlock(required=False, help_text="Font Awesome icon class")


class ServiceBlock(StructBlock):
    title = CharBlock(required=True)
    description = TextBlock(required=True)
    icon = CharBlock(required=False, help_text="Font Awesome icon class")
    link = CharBlock(required=False)


class CTABlock(StructBlock):
    heading = CharBlock(required=True)
    subheading = TextBlock(required=False)
    button_text = CharBlock(required=True)
    button_link = CharBlock(required=True)
    background_color = CharBlock(required=False, default="#0077aa", help_text="Hex color code")


class HomePage(Page):
    template = "home/home_page.html"

    hero_title = models.CharField(max_length=255, blank=True)
    hero_subtitle = models.TextField(blank=True)
    hero_cta_text = models.CharField(max_length=100, blank=True)
    hero_cta_link = models.CharField(max_length=255, blank=True)
    hero_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    intro_title = models.CharField(max_length=255, blank=True)
    intro_text = RichTextField(blank=True)

    features_title = models.CharField(max_length=255, blank=True)
    features = StreamField([
        ('feature', FeatureBlock()),
    ], use_json_field=True, blank=True)

    services_title = models.CharField(max_length=255, blank=True)
    services = StreamField([
        ('service', ServiceBlock()),
    ], use_json_field=True, blank=True)

    cta = StreamField([
        ('cta', CTABlock()),
    ], use_json_field=True, blank=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('hero_title'),
            FieldPanel('hero_subtitle'),
            FieldPanel('hero_cta_text'),
            FieldPanel('hero_cta_link'),
            FieldPanel('hero_image'),
        ], heading="Hero Section"),
        MultiFieldPanel([
            FieldPanel('intro_title'),
            FieldPanel('intro_text'),
        ], heading="Introduction"),
        MultiFieldPanel([
            FieldPanel('features_title'),
            FieldPanel('features'),
        ], heading="Features"),
        MultiFieldPanel([
            FieldPanel('services_title'),
            FieldPanel('services'),
        ], heading="Services"),
        FieldPanel('cta'),
    ]


class AboutPage(Page):
    template = "home/about_page.html"

    intro_title = models.CharField(max_length=255, blank=True)
    intro_text = RichTextField(blank=True)

    vision_title = models.CharField(max_length=255, blank=True)
    vision_text = RichTextField(blank=True)

    mission_title = models.CharField(max_length=255, blank=True)
    mission_text = RichTextField(blank=True)

    history_title = models.CharField(max_length=255, blank=True)
    history_text = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('intro_title'),
            FieldPanel('intro_text'),
        ], heading="Introduction"),
        MultiFieldPanel([
            FieldPanel('vision_title'),
            FieldPanel('vision_text'),
        ], heading="Vision"),
        MultiFieldPanel([
            FieldPanel('mission_title'),
            FieldPanel('mission_text'),
        ], heading="Mission"),
        MultiFieldPanel([
            FieldPanel('history_title'),
            FieldPanel('history_text'),
        ], heading="History"),
    ]


class ServicesPage(Page):
    template = "home/services_page.html"

    intro_title = models.CharField(max_length=255, blank=True)
    intro_text = RichTextField(blank=True)

    services = StreamField([
        ('service', ServiceBlock()),
    ], use_json_field=True, blank=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('intro_title'),
            FieldPanel('intro_text'),
        ], heading="Introduction"),
        FieldPanel('services'),
    ]


class ContactPage(Page):
    template = "home/contact_page.html"

    intro_title = models.CharField(max_length=255, blank=True)
    intro_text = RichTextField(blank=True)

    address = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)

    map_location = models.CharField(
        max_length=255, 
        blank=True, 
        help_text="Coordinates for the map"
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('intro_title'),
            FieldPanel('intro_text'),
        ], heading="Introduction"),
        MultiFieldPanel([
            FieldPanel('address'),
            FieldPanel('phone'),
            FieldPanel('email'),
            FieldPanel('map_location'),
        ], heading="Contact Information"),
    ]


@register_snippet
class TeamMember(models.Model):
    name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    bio = RichTextField(blank=True)
    photo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    email = models.EmailField(blank=True)
    linkedin = models.URLField(blank=True)
    twitter = models.URLField(blank=True)

    panels = [
        FieldPanel('name'),
        FieldPanel('position'),
        FieldPanel('bio'),
        FieldPanel('photo'),
        FieldPanel('email'),
        FieldPanel('linkedin'),
        FieldPanel('twitter'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Team Member"
        verbose_name_plural = "Team Members"