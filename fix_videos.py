# fix_videos.py

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from courses.models import Video

# Real YouTube tutorial video embed URLs (free educational videos)
real_video_urls = {
    # Python Videos
    'introduction-to-python': 'https://www.youtube.com/embed/kqtD5dpn9C8',
    'variables-and-data-types': 'https://www.youtube.com/embed/cQT33yu9pY8',
    'operators-in-python': 'https://www.youtube.com/embed/v5MR5JnKcZI',
    'conditional-statements': 'https://www.youtube.com/embed/DZwmZ8Usvnk',
    'loops-for-and-while': 'https://www.youtube.com/embed/6iF8Xb7Z3wQ',
    'functions-in-python': 'https://www.youtube.com/embed/9Os0o3wzS_I',
    'lists-and-tuples': 'https://www.youtube.com/embed/W8KRzm-HUcc',
    'dictionaries-and-sets': 'https://www.youtube.com/embed/daefaLgNkw0',
    'string-manipulation': 'https://www.youtube.com/embed/k9TUPpGqYTo',
    'file-handling': 'https://www.youtube.com/embed/Uh2ebFW8OYM',
    'error-handling': 'https://www.youtube.com/embed/NIWwJbo-9_8',
    'object-oriented-programming': 'https://www.youtube.com/embed/JeznW_7DlB0',
    
    # Java Videos
    'introduction-to-java': 'https://www.youtube.com/embed/eIrMbAQSU34',
    'java-syntax-and-variables': 'https://www.youtube.com/embed/le-URjBhevE',
    'operators-and-expressions': 'https://www.youtube.com/embed/xsl5glJnaq0',
    'control-flow-statements': 'https://www.youtube.com/embed/ldYLYRNaucM',
    'arrays-in-java': 'https://www.youtube.com/embed/ei_4Nt7XWOw',
    'methods-and-functions': 'https://www.youtube.com/embed/cCgOESMQe44',
    'classes-and-objects': 'https://www.youtube.com/embed/IUqKuGNasdM',
    'inheritance': 'https://www.youtube.com/embed/Zs342ePFvRI',
    'exception-handling': 'https://www.youtube.com/embed/1XAfapkBQjk',
    'collections-framework': 'https://www.youtube.com/embed/GdAon80-0KA',
    
    # JavaScript Videos
    'introduction-to-javascript': 'https://www.youtube.com/embed/W6NZfCO5SIk',
    'variables-and-data-types-1': 'https://www.youtube.com/embed/edlFjlzxkSI',
    'functions': 'https://www.youtube.com/embed/FOD408a0EzU',
    'dom-manipulation': 'https://www.youtube.com/embed/y17RuWkWdn8',
    'events': 'https://www.youtube.com/embed/YiOlaiscqDY',
    'arrays-and-objects': 'https://www.youtube.com/embed/oigfaZ5ApsM',
    'async-javascript': 'https://www.youtube.com/embed/PoRJizFvM7s',
    'es6-features': 'https://www.youtube.com/embed/NCwa_xi0Uuc',
    
    # HTML CSS Videos
    'html-basics': 'https://www.youtube.com/embed/qz0aGYrrlhU',
    'html-forms': 'https://www.youtube.com/embed/fNcJuPIZ2WE',
    'css-selectors': 'https://www.youtube.com/embed/l1mER1bV0N0',
    'css-box-model': 'https://www.youtube.com/embed/rIO5326FgPE',
    'flexbox-layout': 'https://www.youtube.com/embed/fYq5PXgSsbE',
    'css-grid': 'https://www.youtube.com/embed/jV8B24rSN5o',
    'responsive-design': 'https://www.youtube.com/embed/srvUrASNj0s',
    'css-animations': 'https://www.youtube.com/embed/SgmNxE9lWcY',
    
    # Django Videos
    'introduction-to-django': 'https://www.youtube.com/embed/rHux0gMZ3Eg',
    'django-models': 'https://www.youtube.com/embed/F5mRW0jo-U4',
    'django-views': 'https://www.youtube.com/embed/GGkFg52Ot5o',
    'django-templates': 'https://www.youtube.com/embed/crHk_9cJqc0',
    'django-forms': 'https://www.youtube.com/embed/6oOHlcnkRdU',
    'authentication-system': 'https://www.youtube.com/embed/WuyKxdLcjms',
    'django-admin': 'https://www.youtube.com/embed/GGkFg52Ot5o',
    'rest-api-with-django': 'https://www.youtube.com/embed/cJveiktaOSQ',
    'django-deployment': 'https://www.youtube.com/embed/Sa_kQheCnds',
}

print("="*60)
print("Updating Video URLs")
print("="*60)

updated = 0
for video in Video.objects.all():
    slug = video.slug
    if slug in real_video_urls:
        video.video_url = real_video_urls[slug]
        video.save()
        print(f"  ✓ {video.title} -> Updated")
        updated += 1
    else:
        # Assign a default Python tutorial video
        video.video_url = 'https://www.youtube.com/embed/kqtD5dpn9C8'
        video.save()
        print(f"  ⚠ {video.title} -> Default video assigned")
        updated += 1

print(f"\n✅ Updated {updated} videos!")
print("\nRestart server: python manage.py runserver")