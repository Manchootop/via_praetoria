CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_IMAGE_BACKEND = "pillow"
CKEDITOR_CONFIGS = {
    "default": {
        "toolbar": "Custom",
        "toolbar_Custom": [
            ["Bold", "Italic", "Underline"],
            ["NumberedList", "BulletedList", "-", "Link", "Unlink"],
            ["RemoveFormat", "Source"],
        ],
    },
}

'''
Include CKEditor in Your Templates:

In your HTML templates where you want to use the CKEditor, you'll need to include the CKEditor script. Add the following
 line within your template's <head> section:

html

<script src="{% static 'ckeditor/ckeditor-init.js' %}"></script>

And wherever you want the CKEditor to appear, use the ckeditor widget:

html

    {{ form.rich_text_content|safe }}

    Make sure to replace form.rich_text_content with the actual field you're using.

That's it! Following these steps should enable you to use the RichTextField from ckeditor.fields and the HStoreField 
from django.contrib.postgres.fields in your Django project.'''
