from django.db import models
from django import forms

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.snippets.models import register_snippet
from wagtail.search import index
from wagtail.blocks import CharBlock, TextBlock, StructBlock
from wagtail.images.blocks import ImageChooserBlock


class BlogIndexPage(Page):
    template = "blog/blog_index_page.html"
    
    intro = RichTextField(blank=True)
    
    content_panels = Page.content_panels + [
        FieldPanel('intro')
    ]
    
    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        blogpages = self.get_children().live().order_by('-first_published_at')
        context['blogpages'] = blogpages
        return context


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'BlogPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


@register_snippet
class BlogCategory(models.Model):
    name = models.CharField(max_length=255)
    icon = models.CharField(max_length=255, blank=True, help_text="Font Awesome icon class")
    description = models.TextField(blank=True)
    
    panels = [
        FieldPanel('name'),
        FieldPanel('icon'),
        FieldPanel('description'),
    ]
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'blog categories'


@register_snippet
class Author(models.Model):
    name = models.CharField(max_length=255)
    photo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    bio = RichTextField(blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    
    panels = [
        FieldPanel('name'),
        FieldPanel('photo'),
        FieldPanel('bio'),
        FieldPanel('email'),
        FieldPanel('website'),
        FieldPanel('twitter'),
        FieldPanel('linkedin'),
    ]
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Authors'


class CodeBlock(StructBlock):
    language = CharBlock(required=True, default='python')
    code = TextBlock(required=True)
    
    class Meta:
        template = 'blog/blocks/code_block.html'
        icon = 'code'
        label = 'Code'


class CaptionedImageBlock(StructBlock):
    image = ImageChooserBlock(required=True)
    caption = CharBlock(required=False)
    
    class Meta:
        template = 'blog/blocks/captioned_image_block.html'
        icon = 'image'
        label = 'Image with Caption'


class BlogPage(Page):
    template = "blog/blog_page.html"
    
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    author = models.ForeignKey(
        'blog.Author',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    banner_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    body = StreamField([
        ('heading', CharBlock(form_classname="title")),
        ('paragraph', TextBlock()),
        ('code', CodeBlock()),
        ('image', CaptionedImageBlock()),
        ('raw_html', TextBlock()),
    ], use_json_field=True)
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)
    categories = ParentalManyToManyField('blog.BlogCategory', blank=True)
    
    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]
    
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('author'),
            FieldPanel('tags'),
            FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
        ], heading="Blog Information"),
        FieldPanel('banner_image'),
        FieldPanel('intro'),
        FieldPanel('body'),
    ]
    
    def get_context(self, request):
        # Add related posts to context
        context = super().get_context(request)
        
        # Get tags and categories
        tags = self.tags.all()
        categories = self.categories.all()
        
        # Filter related posts by tag or category
        if tags:
            related_posts = BlogPage.objects.live().filter(tags__in=tags).exclude(id=self.id).distinct()[:3]
            context['related_posts'] = related_posts
        
        return context