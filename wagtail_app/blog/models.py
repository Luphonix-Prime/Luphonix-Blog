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
from wagtail.blocks import CharBlock, TextBlock, StructBlock, StreamBlock
from wagtail.images.blocks import ImageChooserBlock
from taggit.models import Tag


class BlogIndexPage(Page):
    template = "blog/blog_index_page.html"
    
    intro = RichTextField(blank=True)
    
    content_panels = Page.content_panels + [
        FieldPanel('intro')
    ]
    
    def get_context(self, request, *args, **kwargs):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request, *args, **kwargs)
    
        blogpages = self.get_children().live().order_by('-first_published_at')
        
        # Add search query
        search_query = request.GET.get('search', '')
        if search_query:
            blogpages = blogpages.search(search_query)
        
        # Get all tags from all blog posts
        all_tags = Tag.objects.all()
    
        # Add to context
        context['all_tags'] = all_tags
        context['popular_tags'] = all_tags  # Add this line to make tags available in the template
        
        context['search_query'] = search_query
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


class BlogContentBlock(StreamBlock):
    """
    Custom StreamBlock that groups heading, paragraph, and image together
    to be automatically added when pressing the + button
    """
    heading = CharBlock(form_classname="title")
    subheading = CharBlock(required=False, help_text="Add a subheading (optional)")
    paragraph = TextBlock()
    image = CaptionedImageBlock()
    
    class Meta:
        # This makes the block automatically expand when added
        icon = 'placeholder'
        label = 'Content Section'
        template = 'blog/blocks/content_section.html'
        default = [
            ('heading', 'Your Heading Here'),
            ('subheading', 'Your Subheading Here'),
            ('paragraph', 'Start writing your content here...')
        ]


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
        ('content_section', BlogContentBlock()),
        ('code', CodeBlock()),
        ('raw_html', TextBlock()),
    ], use_json_field=True, default=[
        ('content_section', [
            ('heading', 'Your Heading Here'),
            ('subheading', 'Your Subheading Here'),
            ('paragraph', 'Start writing your content here...')
        ])
    ])
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)
    categories = ParentalManyToManyField('blog.BlogCategory', blank=True)
    
    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]
    
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            # Remove FieldPanel('author') since it will be set automatically
            FieldPanel('tags'),
            FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
        ], heading="Blog Information"),
        FieldPanel('banner_image'),
        FieldPanel('intro'),
        FieldPanel('body'),
    ]

    def save(self, *args, **kwargs):
        if not self.author_id:
            # Get the current user
            current_user = getattr(self, 'owner', None)
            if current_user:
                try:
                    # Get the author that was created during user registration
                    # by checking both email and name matching the user
                    author = Author.objects.get(
                        email=current_user.email,
                        name=current_user.username
                    )
                    self.author = author
                except Author.DoesNotExist:
                    # Create new author if doesn't exist
                    author = Author.objects.create(
                        name=current_user.username,  # Use username consistently
                        email=current_user.email
                    )
                    self.author = author
                except Author.MultipleObjectsReturned:
                    # If multiple authors exist, get the one with matching username
                    author = Author.objects.filter(
                        email=current_user.email,
                        name=current_user.username
                    ).first()
                    if author:
                        self.author = author
                    else:
                        # If no exact match found, create a new author
                        author = Author.objects.create(
                            name=current_user.username,
                            email=current_user.email
                        )
                        self.author = author
        
        # Store the original author before save
        original_author = self.author
        
        # Perform the standard save
        super().save(*args, **kwargs)
        
        # Restore the original author if it was changed during save
        if original_author and self.author_id != original_author.id:
            self.author = original_author
            BlogPage.objects.filter(id=self.id).update(author=original_author)

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