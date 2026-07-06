# create_structure.py

import os

def create_directory_structure():
    """Create all necessary directories for the project"""
    
    # Base directories
    base_dirs = [
        'templates',
        'static/css',
        'static/js',
        'static/images',
        'media/videos',
        'media/notes',
        'media/tasks',
        'media/profile_pics',
        'media/course_thumbnails',
        'media/video_thumbnails',
    ]
    
    # App template directories
    app_template_dirs = [
        'accounts/templates/accounts',
        'courses/templates/courses/admin',
        'quiz/templates/quiz/admin',
        'qna/templates/qna/admin',
        'dashboard/templates/dashboard',
    ]
    
    # Other necessary directories
    other_dirs = [
        'courses/templatetags',
        'accounts/management/commands',
    ]
    
    # Combine all directories
    all_dirs = base_dirs + app_template_dirs + other_dirs
    
    # Create directories
    for directory in all_dirs:
        os.makedirs(directory, exist_ok=True)
        print(f'✓ Created: {directory}')
    
    # Create __init__.py files for Python packages
    init_files = [
        'courses/templatetags/__init__.py',
        'accounts/management/__init__.py',
        'accounts/management/commands/__init__.py',
    ]
    
    for init_file in init_files:
        with open(init_file, 'w') as f:
            f.write('# This file makes Python treat directories as packages\n')
        print(f'✓ Created: {init_file}')
    
    print('\n✅ All directories created successfully!')

if __name__ == '__main__':
    create_directory_structure()