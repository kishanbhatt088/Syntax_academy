import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.text import slugify
from datetime import timedelta
import random

User = get_user_model()

# Import all models
from courses.models import Category, Course, Video, Note, Task, Enrollment, UserVideoProgress
from quiz.models import Quiz, Question, Choice, QuizAttempt, Answer
from qna.models import Question as QnaQuestion, Reply

print("="*70)
print("🎓 Syntax Academy - Complete Database Population")
print("="*70)


# ================================================================
# 1. CREATE ADMIN USERS
# ================================================================
print("\n📌 Step 1: Creating Admin Users...")

admin_users = [
    {
        'username': 'admin',
        'email': 'admin@syntaxacademy.com',
        'password': 'admin123',
        'first_name': 'Admin',
        'last_name': 'User',
        'is_staff': True,
        'is_superuser': True,
    },
    {
        'username': 'instructor1',
        'email': 'instructor1@syntaxacademy.com',
        'password': 'instructor123',
        'first_name': 'Rajesh',
        'last_name': 'Kumar',
        'is_staff': True,
        'is_superuser': False,
    },
    {
        'username': 'instructor2',
        'email': 'instructor2@syntaxacademy.com',
        'password': 'instructor123',
        'first_name': 'Priya',
        'last_name': 'Sharma',
        'is_staff': True,
        'is_superuser': False,
    },
]

created_admins = []
for admin_data in admin_users:
    password = admin_data.pop('password')
    user, created = User.objects.get_or_create(
        username=admin_data['username'],
        defaults=admin_data
    )
    if created:
        user.set_password(password)
        user.save()
        print(f"  ✓ Created admin: {user.username} ({user.email})")
    else:
        print(f"  ⚠ Already exists: {user.username}")
    created_admins.append(user)


# ================================================================
# 2. CREATE STUDENT USERS
# ================================================================
print("\n📌 Step 2: Creating Student Users...")

student_users = [
    {
        'username': 'rahul_singh',
        'email': 'rahul.singh@gmail.com',
        'password': 'student123',
        'first_name': 'Rahul',
        'last_name': 'Singh',
    },
    {
        'username': 'sneha_patel',
        'email': 'sneha.patel@gmail.com',
        'password': 'student123',
        'first_name': 'Sneha',
        'last_name': 'Patel',
    },
    {
        'username': 'amit_verma',
        'email': 'amit.verma@gmail.com',
        'password': 'student123',
        'first_name': 'Amit',
        'last_name': 'Verma',
    },
    {
        'username': 'priya_gupta',
        'email': 'priya.gupta@gmail.com',
        'password': 'student123',
        'first_name': 'Priya',
        'last_name': 'Gupta',
    },
    {
        'username': 'vikram_sharma',
        'email': 'vikram.sharma@gmail.com',
        'password': 'student123',
        'first_name': 'Vikram',
        'last_name': 'Sharma',
    },
    {
        'username': 'anita_reddy',
        'email': 'anita.reddy@gmail.com',
        'password': 'student123',
        'first_name': 'Anita',
        'last_name': 'Reddy',
    },
    {
        'username': 'mohit_jain',
        'email': 'mohit.jain@gmail.com',
        'password': 'student123',
        'first_name': 'Mohit',
        'last_name': 'Jain',
    },
    {
        'username': 'deepika_nair',
        'email': 'deepika.nair@gmail.com',
        'password': 'student123',
        'first_name': 'Deepika',
        'last_name': 'Nair',
    },
    {
        'username': 'arjun_das',
        'email': 'arjun.das@gmail.com',
        'password': 'student123',
        'first_name': 'Arjun',
        'last_name': 'Das',
    },
    {
        'username': 'kavya_menon',
        'email': 'kavya.menon@gmail.com',
        'password': 'student123',
        'first_name': 'Kavya',
        'last_name': 'Menon',
    },
    {
        'username': 'rohan_mishra',
        'email': 'rohan.mishra@gmail.com',
        'password': 'student123',
        'first_name': 'Rohan',
        'last_name': 'Mishra',
    },
    {
        'username': 'sanya_kapoor',
        'email': 'sanya.kapoor@gmail.com',
        'password': 'student123',
        'first_name': 'Sanya',
        'last_name': 'Kapoor',
    },
    {
        'username': 'karan_thakur',
        'email': 'karan.thakur@gmail.com',
        'password': 'student123',
        'first_name': 'Karan',
        'last_name': 'Thakur',
    },
    {
        'username': 'meera_iyer',
        'email': 'meera.iyer@gmail.com',
        'password': 'student123',
        'first_name': 'Meera',
        'last_name': 'Iyer',
    },
    {
        'username': 'aditya_rao',
        'email': 'aditya.rao@gmail.com',
        'password': 'student123',
        'first_name': 'Aditya',
        'last_name': 'Rao',
    },
]

created_students = []
for student_data in student_users:
    password = student_data.pop('password')
    user, created = User.objects.get_or_create(
        username=student_data['username'],
        defaults=student_data
    )
    if created:
        user.set_password(password)
        user.save()
        print(f"  ✓ Created student: {user.username} ({user.first_name} {user.last_name})")
    else:
        print(f"  ⚠ Already exists: {user.username}")
    created_students.append(user)


# ================================================================
# 3. CREATE CATEGORIES
# ================================================================
print("\n📌 Step 3: Creating Categories...")

categories_data = [
    {
        'name': 'Python',
        'slug': 'python',
        'description': 'Learn Python programming from basics to advanced. Python is one of the most popular and versatile programming languages used in web development, data science, AI, and automation.',
        'icon': 'fa-python',
        'color': '#3776AB',
        'is_active': True,
        'order': 1,
    },
    {
        'name': 'Java',
        'slug': 'java',
        'description': 'Master Java programming language. Java is widely used in enterprise applications, Android development, and large-scale systems.',
        'icon': 'fa-java',
        'color': '#F89820',
        'is_active': True,
        'order': 2,
    },
    {
        'name': 'JavaScript',
        'slug': 'javascript',
        'description': 'Learn JavaScript for web development. JavaScript is essential for building interactive websites, web apps, and server-side applications with Node.js.',
        'icon': 'fa-js',
        'color': '#F7DF1E',
        'is_active': True,
        'order': 3,
    },
    {
        'name': 'HTML & CSS',
        'slug': 'html-css',
        'description': 'Master the fundamentals of web design with HTML and CSS. Learn to create beautiful, responsive websites from scratch.',
        'icon': 'fa-html5',
        'color': '#E34F26',
        'is_active': True,
        'order': 4,
    },
    {
        'name': 'React',
        'slug': 'react',
        'description': 'Build modern user interfaces with React.js. Learn component-based architecture, state management, hooks, and more.',
        'icon': 'fa-react',
        'color': '#61DAFB',
        'is_active': True,
        'order': 5,
    },
    {
        'name': 'Django',
        'slug': 'django',
        'description': 'Build powerful web applications with Django. Learn the Python web framework that handles everything from database to templates.',
        'icon': 'fa-python',
        'color': '#092E20',
        'is_active': True,
        'order': 6,
    },
    {
        'name': 'Data Science',
        'slug': 'data-science',
        'description': 'Dive into data science with Python. Learn data analysis, visualization, machine learning, and statistical modeling.',
        'icon': 'fa-chart-bar',
        'color': '#FF6F61',
        'is_active': True,
        'order': 7,
    },
    {
        'name': 'SQL & Database',
        'slug': 'sql-database',
        'description': 'Master SQL and database management. Learn to design, query, and manage relational databases like MySQL, PostgreSQL, and SQLite.',
        'icon': 'fa-database',
        'color': '#4479A1',
        'is_active': True,
        'order': 8,
    },
]

created_categories = []
for cat_data in categories_data:
    category, created = Category.objects.get_or_create(
        slug=cat_data['slug'],
        defaults=cat_data
    )
    if created:
        print(f"  ✓ Created category: {category.name}")
    else:
        print(f"  ⚠ Already exists: {category.name}")
    created_categories.append(category)


# ================================================================
# 4. CREATE COURSES
# ================================================================
print("\n📌 Step 4: Creating Courses...")

courses_data = [
    # Python Courses
    {
        'category': 'python',
        'title': 'Python for Beginners',
        'slug': 'python-for-beginners',
        'description': 'Start your programming journey with Python. This course covers Python basics including variables, data types, control flow, functions, and object-oriented programming. Perfect for absolute beginners with no prior coding experience.',
        'difficulty_level': 'BEGINNER',
        'estimated_duration': 20,
        'prerequisites': 'No prior programming experience required. Just a computer and willingness to learn!',
        'learning_outcomes': 'Variables and Data Types\nControl Flow (if/else, loops)\nFunctions and Modules\nFile Handling\nBasic OOP Concepts\nError Handling',
        'is_published': True,
        'order': 1,
    },
    {
        'category': 'python',
        'title': 'Advanced Python Programming',
        'slug': 'advanced-python-programming',
        'description': 'Take your Python skills to the next level. Learn advanced concepts including decorators, generators, context managers, metaclasses, and design patterns in Python.',
        'difficulty_level': 'ADVANCED',
        'estimated_duration': 30,
        'prerequisites': 'Python for Beginners or equivalent Python knowledge',
        'learning_outcomes': 'Decorators and Closures\nGenerators and Iterators\nContext Managers\nMetaclasses\nDesign Patterns\nAdvanced OOP',
        'is_published': True,
        'order': 2,
    },
    {
        'category': 'python',
        'title': 'Python Data Structures',
        'slug': 'python-data-structures',
        'description': 'Master Python data structures including lists, tuples, dictionaries, sets, stacks, queues, and trees. Learn algorithmic thinking and problem solving.',
        'difficulty_level': 'INTERMEDIATE',
        'estimated_duration': 25,
        'prerequisites': 'Basic Python programming knowledge',
        'learning_outcomes': 'Lists and Tuples\nDictionaries and Sets\nStacks and Queues\nLinked Lists\nTrees and Graphs\nSorting Algorithms',
        'is_published': True,
        'order': 3,
    },
    # Java Courses
    {
        'category': 'java',
        'title': 'Java Fundamentals',
        'slug': 'java-fundamentals',
        'description': 'Learn Java from scratch. This comprehensive course covers Java syntax, OOP principles, collections, exception handling, and file I/O. Build a strong foundation for enterprise development.',
        'difficulty_level': 'BEGINNER',
        'estimated_duration': 25,
        'prerequisites': 'No prior Java experience required. Basic understanding of programming concepts is helpful.',
        'learning_outcomes': 'Java Syntax and Basics\nObject-Oriented Programming\nCollections Framework\nException Handling\nFile I/O\nMultithreading Basics',
        'is_published': True,
        'order': 1,
    },
    {
        'category': 'java',
        'title': 'Java OOP Mastery',
        'slug': 'java-oop-mastery',
        'description': 'Deep dive into Object-Oriented Programming with Java. Learn inheritance, polymorphism, abstraction, encapsulation, interfaces, and design patterns.',
        'difficulty_level': 'INTERMEDIATE',
        'estimated_duration': 20,
        'prerequisites': 'Java Fundamentals or basic Java knowledge',
        'learning_outcomes': 'Inheritance\nPolymorphism\nAbstraction\nEncapsulation\nInterfaces\nDesign Patterns',
        'is_published': True,
        'order': 2,
    },
    # JavaScript Courses
    {
        'category': 'javascript',
        'title': 'JavaScript Essentials',
        'slug': 'javascript-essentials',
        'description': 'Master JavaScript fundamentals. Learn variables, functions, DOM manipulation, events, async programming, and ES6+ features.',
        'difficulty_level': 'BEGINNER',
        'estimated_duration': 22,
        'prerequisites': 'Basic HTML knowledge is helpful',
        'learning_outcomes': 'Variables and Data Types\nFunctions\nDOM Manipulation\nEvent Handling\nAsync/Await\nES6+ Features',
        'is_published': True,
        'order': 1,
    },
    {
        'category': 'javascript',
        'title': 'Advanced JavaScript',
        'slug': 'advanced-javascript',
        'description': 'Advanced JavaScript concepts including closures, prototypes, design patterns, module systems, and performance optimization.',
        'difficulty_level': 'ADVANCED',
        'estimated_duration': 28,
        'prerequisites': 'JavaScript Essentials or equivalent knowledge',
        'learning_outcomes': 'Closures\nPrototypes\nDesign Patterns\nModule Systems\nPerformance Optimization\nTesting',
        'is_published': True,
        'order': 2,
    },
    # HTML & CSS Courses
    {
        'category': 'html-css',
        'title': 'HTML & CSS Masterclass',
        'slug': 'html-css-masterclass',
        'description': 'Complete guide to HTML5 and CSS3. Learn semantic HTML, CSS layouts, Flexbox, Grid, animations, and responsive design.',
        'difficulty_level': 'BEGINNER',
        'estimated_duration': 18,
        'prerequisites': 'No prerequisites. Perfect for beginners!',
        'learning_outcomes': 'HTML5 Semantic Elements\nCSS3 Properties\nFlexbox Layout\nCSS Grid\nAnimations\nResponsive Design',
        'is_published': True,
        'order': 1,
    },
    # Django Courses
    {
        'category': 'django',
        'title': 'Django Web Development',
        'slug': 'django-web-development',
        'description': 'Build full-stack web applications with Django. Learn models, views, templates, forms, authentication, REST APIs, and deployment.',
        'difficulty_level': 'INTERMEDIATE',
        'estimated_duration': 35,
        'prerequisites': 'Python programming knowledge required. HTML/CSS basics helpful.',
        'learning_outcomes': 'Django Models\nViews and Templates\nForms\nAuthentication\nREST APIs\nDeployment',
        'is_published': True,
        'order': 1,
    },
    # Data Science
    {
        'category': 'data-science',
        'title': 'Data Science with Python',
        'slug': 'data-science-with-python',
        'description': 'Learn data science using Python. Cover NumPy, Pandas, Matplotlib, Seaborn, and Scikit-learn for data analysis and machine learning.',
        'difficulty_level': 'INTERMEDIATE',
        'estimated_duration': 40,
        'prerequisites': 'Python programming knowledge required',
        'learning_outcomes': 'NumPy\nPandas\nData Visualization\nStatistical Analysis\nMachine Learning Basics\nProject Building',
        'is_published': True,
        'order': 1,
    },
    # SQL
    {
        'category': 'sql-database',
        'title': 'SQL Complete Course',
        'slug': 'sql-complete-course',
        'description': 'Master SQL from basics to advanced. Learn SELECT, JOIN, subqueries, indexes, stored procedures, and database design.',
        'difficulty_level': 'BEGINNER',
        'estimated_duration': 20,
        'prerequisites': 'No prerequisites required',
        'learning_outcomes': 'SQL Basics\nJOINs\nSubqueries\nIndexes\nStored Procedures\nDatabase Design',
        'is_published': True,
        'order': 1,
    },
    # React
    {
        'category': 'react',
        'title': 'React.js Complete Guide',
        'slug': 'reactjs-complete-guide',
        'description': 'Build modern web apps with React. Learn components, hooks, state management, routing, and API integration.',
        'difficulty_level': 'INTERMEDIATE',
        'estimated_duration': 30,
        'prerequisites': 'JavaScript knowledge required. HTML/CSS basics needed.',
        'learning_outcomes': 'React Components\nHooks\nState Management\nRouting\nAPI Integration\nProject Deployment',
        'is_published': True,
        'order': 1,
    },
]

created_courses = []
admin_user = created_admins[0]
for course_data in courses_data:
    cat_slug = course_data.pop('category')
    category = Category.objects.get(slug=cat_slug)
    
    course, created = Course.objects.get_or_create(
        slug=course_data['slug'],
        defaults={**course_data, 'category': category, 'created_by': admin_user}
    )
    if created:
        print(f"  ✓ Created course: {course.title}")
    else:
        print(f"  ⚠ Already exists: {course.title}")
    created_courses.append(course)


# ================================================================
# 5. CREATE VIDEOS FOR EACH COURSE
# ================================================================
print("\n📌 Step 5: Creating Videos...")

videos_data = {
    'python-for-beginners': [
        {'title': 'Introduction to Python', 'description': 'What is Python? Why learn Python? Installation and setup guide.', 'duration': 15, 'order': 1, 'is_preview': True},
        {'title': 'Variables and Data Types', 'description': 'Understanding variables, integers, floats, strings, and booleans in Python.', 'duration': 25, 'order': 2, 'is_preview': False},
        {'title': 'Operators in Python', 'description': 'Arithmetic, comparison, logical, and assignment operators explained.', 'duration': 20, 'order': 3, 'is_preview': False},
        {'title': 'Conditional Statements', 'description': 'if, elif, else statements. Making decisions in Python programs.', 'duration': 22, 'order': 4, 'is_preview': False},
        {'title': 'Loops - For and While', 'description': 'For loops, while loops, break, continue, and nested loops.', 'duration': 30, 'order': 5, 'is_preview': False},
        {'title': 'Functions in Python', 'description': 'Creating functions, parameters, return values, and scope.', 'duration': 28, 'order': 6, 'is_preview': False},
        {'title': 'Lists and Tuples', 'description': 'Working with lists and tuples. Methods, slicing, and comprehensions.', 'duration': 35, 'order': 7, 'is_preview': False},
        {'title': 'Dictionaries and Sets', 'description': 'Dictionary operations, methods, and set operations explained.', 'duration': 25, 'order': 8, 'is_preview': False},
        {'title': 'String Manipulation', 'description': 'String methods, formatting, and regular expressions basics.', 'duration': 20, 'order': 9, 'is_preview': False},
        {'title': 'File Handling', 'description': 'Reading and writing files. Working with CSV and JSON files.', 'duration': 25, 'order': 10, 'is_preview': False},
        {'title': 'Error Handling', 'description': 'Try/except blocks, raising exceptions, and custom exceptions.', 'duration': 18, 'order': 11, 'is_preview': False},
        {'title': 'Object-Oriented Programming', 'description': 'Classes, objects, inheritance, polymorphism, and encapsulation.', 'duration': 40, 'order': 12, 'is_preview': False},
    ],
    'java-fundamentals': [
        {'title': 'Introduction to Java', 'description': 'What is Java? JDK installation and first Java program.', 'duration': 18, 'order': 1, 'is_preview': True},
        {'title': 'Java Syntax and Variables', 'description': 'Java syntax, data types, variables, and type casting.', 'duration': 25, 'order': 2, 'is_preview': False},
        {'title': 'Operators and Expressions', 'description': 'Arithmetic, relational, logical operators in Java.', 'duration': 20, 'order': 3, 'is_preview': False},
        {'title': 'Control Flow Statements', 'description': 'if-else, switch-case, for, while, do-while loops.', 'duration': 30, 'order': 4, 'is_preview': False},
        {'title': 'Arrays in Java', 'description': 'Single and multi-dimensional arrays. Array operations.', 'duration': 25, 'order': 5, 'is_preview': False},
        {'title': 'Methods and Functions', 'description': 'Creating methods, method overloading, and recursion.', 'duration': 28, 'order': 6, 'is_preview': False},
        {'title': 'Classes and Objects', 'description': 'OOP basics - classes, objects, constructors, and this keyword.', 'duration': 35, 'order': 7, 'is_preview': False},
        {'title': 'Inheritance', 'description': 'Single, multilevel, hierarchical inheritance and super keyword.', 'duration': 30, 'order': 8, 'is_preview': False},
        {'title': 'Exception Handling', 'description': 'Try-catch, finally, throw, throws, and custom exceptions.', 'duration': 22, 'order': 9, 'is_preview': False},
        {'title': 'Collections Framework', 'description': 'ArrayList, LinkedList, HashMap, HashSet, and iterators.', 'duration': 35, 'order': 10, 'is_preview': False},
    ],
    'javascript-essentials': [
        {'title': 'Introduction to JavaScript', 'description': 'What is JavaScript? Setting up development environment.', 'duration': 15, 'order': 1, 'is_preview': True},
        {'title': 'Variables and Data Types', 'description': 'var, let, const. Primitive and reference types.', 'duration': 22, 'order': 2, 'is_preview': False},
        {'title': 'Functions', 'description': 'Function declarations, expressions, arrow functions, and callbacks.', 'duration': 28, 'order': 3, 'is_preview': False},
        {'title': 'DOM Manipulation', 'description': 'Selecting elements, modifying content, and creating elements.', 'duration': 35, 'order': 4, 'is_preview': False},
        {'title': 'Events', 'description': 'Event listeners, event objects, and event delegation.', 'duration': 25, 'order': 5, 'is_preview': False},
        {'title': 'Arrays and Objects', 'description': 'Array methods, object manipulation, and destructuring.', 'duration': 30, 'order': 6, 'is_preview': False},
        {'title': 'Async JavaScript', 'description': 'Promises, async/await, and fetch API.', 'duration': 32, 'order': 7, 'is_preview': False},
        {'title': 'ES6+ Features', 'description': 'Template literals, spread operator, modules, and classes.', 'duration': 28, 'order': 8, 'is_preview': False},
    ],
    'html-css-masterclass': [
        {'title': 'HTML Basics', 'description': 'HTML structure, tags, attributes, and document structure.', 'duration': 20, 'order': 1, 'is_preview': True},
        {'title': 'HTML Forms', 'description': 'Form elements, input types, validation, and accessibility.', 'duration': 25, 'order': 2, 'is_preview': False},
        {'title': 'CSS Selectors', 'description': 'Element, class, ID, attribute, and pseudo selectors.', 'duration': 22, 'order': 3, 'is_preview': False},
        {'title': 'CSS Box Model', 'description': 'Margin, padding, border, and box-sizing explained.', 'duration': 18, 'order': 4, 'is_preview': False},
        {'title': 'Flexbox Layout', 'description': 'Complete Flexbox guide - containers, items, and alignment.', 'duration': 30, 'order': 5, 'is_preview': False},
        {'title': 'CSS Grid', 'description': 'Grid containers, grid items, and complex layouts.', 'duration': 32, 'order': 6, 'is_preview': False},
        {'title': 'Responsive Design', 'description': 'Media queries, mobile-first design, and responsive images.', 'duration': 28, 'order': 7, 'is_preview': False},
        {'title': 'CSS Animations', 'description': 'Transitions, transforms, keyframes, and animation properties.', 'duration': 25, 'order': 8, 'is_preview': False},
    ],
    'django-web-development': [
        {'title': 'Introduction to Django', 'description': 'What is Django? MVC/MVT architecture and project setup.', 'duration': 20, 'order': 1, 'is_preview': True},
        {'title': 'Django Models', 'description': 'Creating models, fields, relationships, and migrations.', 'duration': 35, 'order': 2, 'is_preview': False},
        {'title': 'Django Views', 'description': 'Function-based views, class-based views, and URL routing.', 'duration': 30, 'order': 3, 'is_preview': False},
        {'title': 'Django Templates', 'description': 'Template language, inheritance, filters, and tags.', 'duration': 28, 'order': 4, 'is_preview': False},
        {'title': 'Django Forms', 'description': 'Creating forms, ModelForms, validation, and widgets.', 'duration': 32, 'order': 5, 'is_preview': False},
        {'title': 'Authentication System', 'description': 'User registration, login, logout, and permissions.', 'duration': 35, 'order': 6, 'is_preview': False},
        {'title': 'Django Admin', 'description': 'Customizing admin panel, ModelAdmin, and inline forms.', 'duration': 25, 'order': 7, 'is_preview': False},
        {'title': 'REST API with Django', 'description': 'Building REST APIs using Django REST Framework.', 'duration': 40, 'order': 8, 'is_preview': False},
        {'title': 'Django Deployment', 'description': 'Deploying Django apps to production servers.', 'duration': 30, 'order': 9, 'is_preview': False},
    ],
}

for course_slug, videos in videos_data.items():
    try:
        course = Course.objects.get(slug=course_slug)
        for video_data in videos:
            video, created = Video.objects.get_or_create(
                course=course,
                slug=slugify(video_data['title']),
                defaults={
                    'title': video_data['title'],
                    'description': video_data['description'],
                    'duration': video_data['duration'],
                    'order': video_data['order'],
                    'is_preview': video_data['is_preview'],
                    'video_url': f'https://www.youtube.com/embed/dQw4w9WgXcQ',
                }
            )
            if created:
                print(f"  ✓ Video: {video.title}")
    except Course.DoesNotExist:
        print(f"  ⚠ Course {course_slug} not found")


# ================================================================
# 6. CREATE NOTES FOR EACH COURSE
# ================================================================
print("\n📌 Step 6: Creating Notes...")

notes_data = {
    'python-for-beginners': [
        {'title': 'Python Installation Guide', 'content': 'Step 1: Download Python from python.org\nStep 2: Run the installer\nStep 3: Check "Add Python to PATH"\nStep 4: Verify installation with python --version\n\nRecommended IDE: VS Code or PyCharm', 'order': 1},
        {'title': 'Variables and Data Types Cheatsheet', 'content': '# Variables\nname = "John"\nage = 25\nprice = 19.99\nis_active = True\n\n# Data Types\nint - Integer numbers (1, 2, 3)\nfloat - Decimal numbers (1.5, 2.7)\nstr - Strings ("Hello")\nbool - Boolean (True/False)\nlist - Ordered collection [1, 2, 3]\ntuple - Immutable collection (1, 2, 3)\ndict - Key-value pairs {"key": "value"}\nset - Unique collection {1, 2, 3}', 'order': 2},
        {'title': 'Control Flow Reference', 'content': '# If-Elif-Else\nif condition:\n    # code\nelif another_condition:\n    # code\nelse:\n    # code\n\n# For Loop\nfor item in iterable:\n    print(item)\n\n# While Loop\nwhile condition:\n    # code\n\n# Break and Continue\nfor i in range(10):\n    if i == 5:\n        break\n    if i == 3:\n        continue', 'order': 3},
        {'title': 'Functions Guide', 'content': '# Function Definition\ndef greet(name):\n    return f"Hello, {name}!"\n\n# Default Parameters\ndef greet(name="World"):\n    return f"Hello, {name}!"\n\n# *args and **kwargs\ndef func(*args, **kwargs):\n    print(args)\n    print(kwargs)\n\n# Lambda Functions\nsquare = lambda x: x ** 2', 'order': 4},
        {'title': 'OOP Concepts Summary', 'content': '# Class Definition\nclass Animal:\n    def __init__(self, name):\n        self.name = name\n    \n    def speak(self):\n        pass\n\n# Inheritance\nclass Dog(Animal):\n    def speak(self):\n        return "Woof!"\n\n# Polymorphism\nclass Cat(Animal):\n    def speak(self):\n        return "Meow!"\n\n# Usage\ndog = Dog("Buddy")\nprint(dog.speak())  # Output: Woof!', 'order': 5},
    ],
    'java-fundamentals': [
        {'title': 'Java Setup Guide', 'content': 'Step 1: Download JDK from Oracle\nStep 2: Install JDK\nStep 3: Set JAVA_HOME environment variable\nStep 4: Verify with java --version\n\nFirst Program:\npublic class Hello {\n    public static void main(String[] args) {\n        System.out.println("Hello World!");\n    }\n}', 'order': 1},
        {'title': 'Java Data Types Reference', 'content': 'Primitive Types:\nbyte - 8 bits (-128 to 127)\nshort - 16 bits\nint - 32 bits\nlong - 64 bits\nfloat - 32 bits decimal\ndouble - 64 bits decimal\nchar - 16 bits character\nboolean - true/false\n\nReference Types:\nString, Arrays, Objects', 'order': 2},
        {'title': 'OOP in Java', 'content': '// Class\npublic class Car {\n    private String brand;\n    private int year;\n    \n    public Car(String brand, int year) {\n        this.brand = brand;\n        this.year = year;\n    }\n    \n    public String getBrand() {\n        return brand;\n    }\n}\n\n// Inheritance\npublic class ElectricCar extends Car {\n    private int battery;\n}', 'order': 3},
    ],
    'javascript-essentials': [
        {'title': 'JavaScript Basics', 'content': '// Variables\nlet name = "John";\nconst PI = 3.14;\nvar age = 25;  // avoid using var\n\n// Functions\nfunction greet(name) {\n    return `Hello, ${name}!`;\n}\n\n// Arrow Functions\nconst greet = (name) => `Hello, ${name}!`;\n\n// Arrays\nconst fruits = ["apple", "banana", "orange"];\nfruits.push("grape");\nfruits.map(f => f.toUpperCase());', 'order': 1},
        {'title': 'DOM Manipulation Guide', 'content': '// Select Elements\nconst el = document.getElementById("myId");\nconst els = document.querySelectorAll(".myClass");\n\n// Modify Content\nel.textContent = "New text";\nel.innerHTML = "<strong>Bold</strong>";\n\n// Modify Styles\nel.style.color = "red";\nel.classList.add("active");\n\n// Create Elements\nconst div = document.createElement("div");\ndiv.textContent = "Hello";\ndocument.body.appendChild(div);', 'order': 2},
    ],
}

for course_slug, notes in notes_data.items():
    try:
        course = Course.objects.get(slug=course_slug)
        for note_data in notes:
            note, created = Note.objects.get_or_create(
                course=course,
                slug=slugify(note_data['title']),
                defaults={
                    'title': note_data['title'],
                    'content': note_data['content'],
                    'order': note_data['order'],
                }
            )
            if created:
                print(f"  ✓ Note: {note.title}")
    except Course.DoesNotExist:
        print(f"  ⚠ Course {course_slug} not found")


# ================================================================
# 7. CREATE TASKS FOR EACH COURSE
# ================================================================
print("\n📌 Step 7: Creating Tasks...")

tasks_data = {
    'python-for-beginners': [
        {'title': 'Calculator Program', 'description': 'Build a simple calculator that can perform addition, subtraction, multiplication, and division. Handle division by zero error.', 'difficulty': 'BEGINNER', 'estimated_time': 2, 'order': 1},
        {'title': 'Number Guessing Game', 'description': 'Create a number guessing game where the computer generates a random number and the user has to guess it. Provide hints (higher/lower).', 'difficulty': 'BEGINNER', 'estimated_time': 3, 'order': 2},
        {'title': 'Student Grade Manager', 'description': 'Build a program that manages student grades. Allow adding students, recording grades, calculating averages, and displaying results.', 'difficulty': 'INTERMEDIATE', 'estimated_time': 4, 'order': 3},
        {'title': 'File Organizer', 'description': 'Create a Python script that organizes files in a directory by their extension (images, documents, videos, etc.).', 'difficulty': 'INTERMEDIATE', 'estimated_time': 3, 'order': 4},
        {'title': 'Library Management System', 'description': 'Build a complete library management system with OOP. Include book management, member management, borrowing, and returning books.', 'difficulty': 'ADVANCED', 'estimated_time': 6, 'order': 5},
    ],
    'java-fundamentals': [
        {'title': 'Hello World Program', 'description': 'Write your first Java program that prints "Hello, World!" and your name.', 'difficulty': 'BEGINNER', 'estimated_time': 1, 'order': 1},
        {'title': 'Banking System', 'description': 'Create a simple banking system with deposit, withdrawal, and balance checking features using OOP concepts.', 'difficulty': 'INTERMEDIATE', 'estimated_time': 4, 'order': 2},
        {'title': 'Student Management System', 'description': 'Build a student management system with CRUD operations using ArrayList and file storage.', 'difficulty': 'INTERMEDIATE', 'estimated_time': 5, 'order': 3},
    ],
    'javascript-essentials': [
        {'title': 'Todo List App', 'description': 'Build a todo list application with add, delete, and mark complete features using DOM manipulation.', 'difficulty': 'BEGINNER', 'estimated_time': 3, 'order': 1},
        {'title': 'Weather App', 'description': 'Create a weather application that fetches weather data from an API and displays it beautifully.', 'difficulty': 'INTERMEDIATE', 'estimated_time': 4, 'order': 2},
        {'title': 'Quiz Application', 'description': 'Build an interactive quiz application with timer, score tracking, and result display.', 'difficulty': 'INTERMEDIATE', 'estimated_time': 5, 'order': 3},
    ],
}

for course_slug, tasks in tasks_data.items():
    try:
        course = Course.objects.get(slug=course_slug)
        for task_data in tasks:
            task, created = Task.objects.get_or_create(
                course=course,
                slug=slugify(task_data['title']),
                defaults={
                    'title': task_data['title'],
                    'description': task_data['description'],
                    'difficulty': task_data['difficulty'],
                    'estimated_time': task_data['estimated_time'],
                    'order': task_data['order'],
                }
            )
            if created:
                print(f"  ✓ Task: {task.title}")
    except Course.DoesNotExist:
        print(f"  ⚠ Course {course_slug} not found")


# ================================================================
# 8. CREATE QUIZZES
# ================================================================
print("\n📌 Step 8: Creating Quizzes with Questions...")

quizzes_data = {
    'python-for-beginners': [
        {
            'title': 'Python Basics Quiz',
            'slug': 'python-basics-quiz',
            'description': 'Test your knowledge of Python basics including variables, data types, and operators.',
            'time_limit': 15,
            'passing_score': 60,
            'max_attempts': 3,
            'order': 1,
            'questions': [
                {
                    'text': 'What is the correct way to declare a variable in Python?',
                    'explanation': 'Python uses dynamic typing - no need to declare types.',
                    'points': 1,
                    'choices': [
                        ('int x = 5', False),
                        ('x = 5', True),
                        ('var x = 5', False),
                        ('declare x = 5', False),
                    ]
                },
                {
                    'text': 'Which of the following is a mutable data type in Python?',
                    'explanation': 'Lists are mutable (can be changed), while tuples and strings are immutable.',
                    'points': 1,
                    'choices': [
                        ('Tuple', False),
                        ('String', False),
                        ('List', True),
                        ('Integer', False),
                    ]
                },
                {
                    'text': 'What is the output of print(type(3.14))?',
                    'explanation': '3.14 is a decimal number, so its type is float.',
                    'points': 1,
                    'choices': [
                        ("<class 'int'>", False),
                        ("<class 'float'>", True),
                        ("<class 'str'>", False),
                        ("<class 'double'>", False),
                    ]
                },
                {
                    'text': 'How do you start a comment in Python?',
                    'explanation': 'Single line comments in Python start with #',
                    'points': 1,
                    'choices': [
                        ('//', False),
                        ('/*', False),
                        ('#', True),
                        ('--', False),
                    ]
                },
                {
                    'text': 'What does the len() function do?',
                    'explanation': 'len() returns the number of items in an object.',
                    'points': 1,
                    'choices': [
                        ('Returns the largest item', False),
                        ('Returns the length/count of items', True),
                        ('Returns the type of object', False),
                        ('Returns the last item', False),
                    ]
                },
                {
                    'text': 'Which keyword is used to define a function in Python?',
                    'explanation': 'The "def" keyword is used to define functions in Python.',
                    'points': 1,
                    'choices': [
                        ('function', False),
                        ('func', False),
                        ('def', True),
                        ('define', False),
                    ]
                },
                {
                    'text': 'What is the output of print(2 ** 3)?',
                    'explanation': '** is the exponentiation operator. 2**3 = 2^3 = 8',
                    'points': 1,
                    'choices': [
                        ('6', False),
                        ('8', True),
                        ('5', False),
                        ('23', False),
                    ]
                },
                {
                    'text': 'Which method is used to add an element to the end of a list?',
                    'explanation': 'append() adds a single element to the end of a list.',
                    'points': 1,
                    'choices': [
                        ('add()', False),
                        ('insert()', False),
                        ('append()', True),
                        ('push()', False),
                    ]
                },
                {
                    'text': 'What does the "break" statement do in a loop?',
                    'explanation': 'break exits the loop immediately.',
                    'points': 1,
                    'choices': [
                        ('Skips the current iteration', False),
                        ('Exits the loop', True),
                        ('Restarts the loop', False),
                        ('Pauses the loop', False),
                    ]
                },
                {
                    'text': 'What is a dictionary in Python?',
                    'explanation': 'A dictionary stores data in key-value pairs.',
                    'points': 1,
                    'choices': [
                        ('An ordered list of elements', False),
                        ('A collection of key-value pairs', True),
                        ('A set of unique numbers', False),
                        ('A type of function', False),
                    ]
                },
            ]
        },
        {
            'title': 'Python Functions Quiz',
            'slug': 'python-functions-quiz',
            'description': 'Test your understanding of Python functions, parameters, and return values.',
            'time_limit': 10,
            'passing_score': 70,
            'max_attempts': 3,
            'order': 2,
            'questions': [
                {
                    'text': 'What is a lambda function in Python?',
                    'explanation': 'Lambda functions are small anonymous functions defined with the lambda keyword.',
                    'points': 1,
                    'choices': [
                        ('A function that returns nothing', False),
                        ('A small anonymous function', True),
                        ('A function with no parameters', False),
                        ('A built-in Python function', False),
                    ]
                },
                {
                    'text': 'What does *args do in a function definition?',
                    'explanation': '*args allows a function to accept any number of positional arguments.',
                    'points': 1,
                    'choices': [
                        ('Accepts keyword arguments', False),
                        ('Accepts a fixed number of arguments', False),
                        ('Accepts any number of positional arguments', True),
                        ('Multiplies arguments', False),
                    ]
                },
                {
                    'text': 'What is the default return value of a function without a return statement?',
                    'explanation': 'If no return statement is used, a function returns None.',
                    'points': 1,
                    'choices': [
                        ('0', False),
                        ('Empty string', False),
                        ('None', True),
                        ('False', False),
                    ]
                },
                {
                    'text': 'What is recursion?',
                    'explanation': 'Recursion is when a function calls itself to solve a problem.',
                    'points': 1,
                    'choices': [
                        ('A loop that runs forever', False),
                        ('A function that calls itself', True),
                        ('A function with many parameters', False),
                        ('A built-in Python module', False),
                    ]
                },
                {
                    'text': 'What does **kwargs do?',
                    'explanation': '**kwargs allows a function to accept any number of keyword arguments as a dictionary.',
                    'points': 1,
                    'choices': [
                        ('Accepts positional arguments', False),
                        ('Accepts keyword arguments as dictionary', True),
                        ('Raises an error', False),
                        ('Creates a new class', False),
                    ]
                },
            ]
        },
    ],
    'java-fundamentals': [
        {
            'title': 'Java Basics Quiz',
            'slug': 'java-basics-quiz',
            'description': 'Test your Java programming fundamentals.',
            'time_limit': 15,
            'passing_score': 60,
            'max_attempts': 3,
            'order': 1,
            'questions': [
                {
                    'text': 'Which keyword is used to create a class in Java?',
                    'explanation': 'The "class" keyword is used to define a class in Java.',
                    'points': 1,
                    'choices': [
                        ('Class', False),
                        ('class', True),
                        ('create', False),
                        ('new', False),
                    ]
                },
                {
                    'text': 'What is the entry point of a Java program?',
                    'explanation': 'The main method (public static void main(String[] args)) is the entry point.',
                    'points': 1,
                    'choices': [
                        ('start() method', False),
                        ('init() method', False),
                        ('main() method', True),
                        ('run() method', False),
                    ]
                },
                {
                    'text': 'Which data type is used to store decimal numbers in Java?',
                    'explanation': 'double is used for decimal numbers in Java.',
                    'points': 1,
                    'choices': [
                        ('int', False),
                        ('float/double', True),
                        ('String', False),
                        ('char', False),
                    ]
                },
                {
                    'text': 'What is the size of int in Java?',
                    'explanation': 'int is 32 bits (4 bytes) in Java.',
                    'points': 1,
                    'choices': [
                        ('8 bits', False),
                        ('16 bits', False),
                        ('32 bits', True),
                        ('64 bits', False),
                    ]
                },
                {
                    'text': 'Which of these is NOT a Java access modifier?',
                    'explanation': 'friend is not a Java access modifier. Java has public, private, protected, and default.',
                    'points': 1,
                    'choices': [
                        ('public', False),
                        ('private', False),
                        ('friend', True),
                        ('protected', False),
                    ]
                },
            ]
        },
    ],
    'javascript-essentials': [
        {
            'title': 'JavaScript Basics Quiz',
            'slug': 'javascript-basics-quiz',
            'description': 'Test your JavaScript fundamentals.',
            'time_limit': 12,
            'passing_score': 60,
            'max_attempts': 3,
            'order': 1,
            'questions': [
                {
                    'text': 'Which keyword declares a block-scoped variable?',
                    'explanation': 'let declares a block-scoped variable, unlike var which is function-scoped.',
                    'points': 1,
                    'choices': [
                        ('var', False),
                        ('let', True),
                        ('define', False),
                        ('variable', False),
                    ]
                },
                {
                    'text': 'What is the result of typeof null?',
                    'explanation': 'typeof null returns "object" - this is a known JavaScript bug.',
                    'points': 1,
                    'choices': [
                        ('"null"', False),
                        ('"undefined"', False),
                        ('"object"', True),
                        ('"boolean"', False),
                    ]
                },
                {
                    'text': 'Which method is used to parse a JSON string?',
                    'explanation': 'JSON.parse() converts a JSON string to a JavaScript object.',
                    'points': 1,
                    'choices': [
                        ('JSON.stringify()', False),
                        ('JSON.parse()', True),
                        ('JSON.convert()', False),
                        ('JSON.read()', False),
                    ]
                },
                {
                    'text': 'What does === compare in JavaScript?',
                    'explanation': '=== checks both value AND type (strict equality).',
                    'points': 1,
                    'choices': [
                        ('Only value', False),
                        ('Only type', False),
                        ('Value and type', True),
                        ('Reference', False),
                    ]
                },
                {
                    'text': 'What is a Promise in JavaScript?',
                    'explanation': 'A Promise represents the eventual completion or failure of an async operation.',
                    'points': 1,
                    'choices': [
                        ('A synchronous function', False),
                        ('An object representing async operation result', True),
                        ('A type of loop', False),
                        ('A variable declaration', False),
                    ]
                },
            ]
        },
    ],
}

for course_slug, quizzes in quizzes_data.items():
    try:
        course = Course.objects.get(slug=course_slug)
        for quiz_data in quizzes:
            questions_list = quiz_data.pop('questions')
            
            quiz, created = Quiz.objects.get_or_create(
                course=course,
                slug=quiz_data['slug'],
                defaults={
                    'title': quiz_data['title'],
                    'description': quiz_data['description'],
                    'time_limit': quiz_data['time_limit'],
                    'passing_score': quiz_data['passing_score'],
                    'max_attempts': quiz_data['max_attempts'],
                    'order': quiz_data['order'],
                    'is_active': True,
                }
            )
            
            if created:
                print(f"  ✓ Quiz: {quiz.title}")
                
                for i, q_data in enumerate(questions_list, 1):
                    question = Question.objects.create(
                        quiz=quiz,
                        question_text=q_data['text'],
                        explanation=q_data['explanation'],
                        points=q_data['points'],
                        order=i,
                    )
                    
                    for j, (choice_text, is_correct) in enumerate(q_data['choices'], 1):
                        Choice.objects.create(
                            question=question,
                            choice_text=choice_text,
                            is_correct=is_correct,
                            order=j,
                        )
                    
                    print(f"    ✓ Question {i}: {q_data['text'][:50]}...")
    except Course.DoesNotExist:
        print(f"  ⚠ Course {course_slug} not found")


# ================================================================
# 9. CREATE ENROLLMENTS
# ================================================================
print("\n📌 Step 9: Creating Enrollments...")

enrollment_data = [
    ('rahul_singh', ['python-for-beginners', 'java-fundamentals', 'django-web-development']),
    ('sneha_patel', ['python-for-beginners', 'javascript-essentials', 'html-css-masterclass']),
    ('amit_verma', ['java-fundamentals', 'python-for-beginners']),
    ('priya_gupta', ['python-for-beginners', 'data-science-with-python', 'sql-complete-course']),
    ('vikram_sharma', ['javascript-essentials', 'reactjs-complete-guide', 'html-css-masterclass']),
    ('anita_reddy', ['python-for-beginners', 'django-web-development']),
    ('mohit_jain', ['java-fundamentals', 'sql-complete-course']),
    ('deepika_nair', ['python-for-beginners', 'advanced-python-programming', 'python-data-structures']),
    ('arjun_das', ['javascript-essentials', 'advanced-javascript', 'reactjs-complete-guide']),
    ('kavya_menon', ['html-css-masterclass', 'javascript-essentials', 'python-for-beginners']),
    ('rohan_mishra', ['python-for-beginners', 'java-fundamentals', 'sql-complete-course']),
    ('sanya_kapoor', ['html-css-masterclass', 'reactjs-complete-guide']),
    ('karan_thakur', ['django-web-development', 'python-for-beginners']),
    ('meera_iyer', ['data-science-with-python', 'python-for-beginners', 'sql-complete-course']),
    ('aditya_rao', ['java-fundamentals', 'python-for-beginners', 'javascript-essentials']),
]

for username, course_slugs in enrollment_data:
    try:
        user = User.objects.get(username=username)
        for course_slug in course_slugs:
            try:
                course = Course.objects.get(slug=course_slug)
                enrollment, created = Enrollment.objects.get_or_create(
                    user=user,
                    course=course,
                    defaults={
                        'progress_percentage': random.uniform(10, 95),
                    }
                )
                if created:
                    print(f"  ✓ {username} enrolled in {course.title}")
            except Course.DoesNotExist:
                pass
    except User.DoesNotExist:
        pass


# ================================================================
# 10. CREATE VIDEO PROGRESS
# ================================================================
print("\n📌 Step 10: Creating Video Progress...")

progress_count = 0
for username, course_slugs in enrollment_data[:8]:
    try:
        user = User.objects.get(username=username)
        for course_slug in course_slugs[:1]:
            try:
                course = Course.objects.get(slug=course_slug)
                videos = Video.objects.filter(course=course)[:5]
                
                for video in videos:
                    progress, created = UserVideoProgress.objects.get_or_create(
                        user=user,
                        video=video,
                        defaults={
                            'is_completed': random.choice([True, True, False]),
                            'watch_time': random.randint(60, video.duration * 60),
                            'last_position': random.randint(0, video.duration * 60),
                        }
                    )
                    if created:
                        progress_count += 1
            except Course.DoesNotExist:
                pass
    except User.DoesNotExist:
        pass

print(f"  ✓ Created {progress_count} video progress records")


# ================================================================
# 11. CREATE QUIZ ATTEMPTS
# ================================================================
print("\n📌 Step 11: Creating Quiz Attempts...")

attempt_count = 0
for student in created_students[:10]:
    quizzes = Quiz.objects.all()[:3]
    
    for quiz in quizzes:
        # Check if already attempted
        if QuizAttempt.objects.filter(user=student, quiz=quiz).exists():
            continue
        
        score = random.uniform(40, 100)
        points = int(quiz.total_points * score / 100) if quiz.total_points > 0 else 0
        
        attempt = QuizAttempt.objects.create(
            user=student,
            quiz=quiz,
            score=round(score, 2),
            points_earned=points,
            total_points=quiz.total_points,
            is_passed=score >= quiz.passing_score,
            time_taken=random.randint(120, quiz.time_limit * 60) if quiz.time_limit > 0 else random.randint(120, 600),
            completed_at=timezone.now() - timedelta(days=random.randint(1, 30)),
        )
        
        # Create answers
        questions = quiz.questions.all()
        for question in questions:
            choices = list(question.choices.all())
            if choices:
                if random.random() < score / 100:
                    correct_choices = [c for c in choices if c.is_correct]
                    selected = correct_choices[0] if correct_choices else random.choice(choices)
                else:
                    wrong_choices = [c for c in choices if not c.is_correct]
                    selected = random.choice(wrong_choices) if wrong_choices else random.choice(choices)
                
                Answer.objects.create(
                    attempt=attempt,
                    question=question,
                    selected_choice=selected,
                )
        
        attempt_count += 1

print(f"  ✓ Created {attempt_count} quiz attempts")


# ================================================================
# 12. CREATE Q&A QUESTIONS AND REPLIES
# ================================================================
print("\n📌 Step 12: Creating Q&A Questions and Replies...")

qna_data = [
    {
        'user': 'rahul_singh',
        'course': 'python-for-beginners',
        'title': 'What is the difference between list and tuple?',
        'content': 'I am confused about when to use a list and when to use a tuple in Python. Can someone explain the key differences between them? Both seem to store multiple values, so why do we need both?',
        'status': 'ANSWERED',
        'replies': [
            {'user': 'admin', 'content': 'Great question! The main differences are:\n\n1. **Mutability**: Lists are mutable (can be changed), tuples are immutable (cannot be changed after creation).\n\n2. **Syntax**: Lists use square brackets [], tuples use parentheses ().\n\n3. **Performance**: Tuples are slightly faster than lists because they are immutable.\n\n4. **Use Cases**: Use lists when you need to modify data, use tuples for fixed data like coordinates (x, y).\n\nExample:\n```python\nmy_list = [1, 2, 3]  # Mutable\nmy_tuple = (1, 2, 3)  # Immutable\n```', 'is_solution': True},
            {'user': 'sneha_patel', 'content': 'Additionally, tuples can be used as dictionary keys while lists cannot, because tuples are hashable!'},
        ]
    },
    {
        'user': 'sneha_patel',
        'course': 'python-for-beginners',
        'title': 'How do I read a CSV file in Python?',
        'content': 'I need to read a CSV file in my Python project. What is the best way to do this? Should I use the built-in csv module or pandas?',
        'status': 'ANSWERED',
        'replies': [
            {'user': 'admin', 'content': 'You can use either the built-in csv module or pandas:\n\n**Method 1: csv module**\n```python\nimport csv\nwith open("data.csv", "r") as file:\n    reader = csv.reader(file)\n    for row in reader:\n        print(row)\n```\n\n**Method 2: pandas (recommended for data analysis)**\n```python\nimport pandas as pd\ndf = pd.read_csv("data.csv")\nprint(df.head())\n```\n\nFor simple tasks, use csv module. For data analysis, use pandas.', 'is_solution': True},
        ]
    },
    {
        'user': 'amit_verma',
        'course': 'java-fundamentals',
        'title': 'Difference between == and .equals() in Java?',
        'content': 'When comparing strings in Java, should I use == or .equals()? I tried using == but it sometimes gives wrong results. Can someone explain why?',
        'status': 'ANSWERED',
        'replies': [
            {'user': 'admin', 'content': 'In Java:\n\n- **==** compares object references (memory addresses)\n- **.equals()** compares the actual content/values\n\nFor Strings, always use .equals():\n```java\nString a = new String("Hello");\nString b = new String("Hello");\n\na == b        // false (different objects)\na.equals(b)   // true (same content)\n```\n\nThe == operator works with primitives (int, char, etc.) but for objects, always use .equals().', 'is_solution': True},
            {'user': 'mohit_jain', 'content': 'This confused me too! Thanks for the clear explanation.'},
        ]
    },
    {
        'user': 'vikram_sharma',
        'course': 'javascript-essentials',
        'title': 'What is the difference between let, const, and var?',
        'content': 'I see JavaScript code using var, let, and const. When should I use each one? I heard var is bad practice - is that true?',
        'status': 'ANSWERED',
        'replies': [
            {'user': 'admin', 'content': 'Here is a comparison:\n\n**var:**\n- Function-scoped\n- Can be redeclared\n- Hoisted (moved to top)\n- Avoid using in modern JS\n\n**let:**\n- Block-scoped\n- Cannot be redeclared in same scope\n- Use when value will change\n\n**const:**\n- Block-scoped\n- Cannot be reassigned\n- Use by default\n\n**Best Practice:** Use const by default, let when you need to reassign, and avoid var.', 'is_solution': True},
        ]
    },
    {
        'user': 'priya_gupta',
        'course': 'python-for-beginners',
        'title': 'How do I handle errors in Python?',
        'content': 'My Python program crashes when the user enters wrong input. How can I handle errors properly so the program doesn\'t crash?',
        'status': 'ANSWERED',
        'replies': [
            {'user': 'admin', 'content': 'Use try-except blocks:\n\n```python\ntry:\n    number = int(input("Enter a number: "))\n    result = 10 / number\n    print(f"Result: {result}")\nexcept ValueError:\n    print("Please enter a valid number!")\nexcept ZeroDivisionError:\n    print("Cannot divide by zero!")\nexcept Exception as e:\n    print(f"An error occurred: {e}")\nfinally:\n    print("This runs no matter what")\n```\n\nAlways handle specific exceptions before general ones.', 'is_solution': True},
        ]
    },
    {
        'user': 'deepika_nair',
        'course': 'python-for-beginners',
        'title': 'What is the __init__ method?',
        'content': 'I keep seeing __init__ in Python classes. What is it and why do we need it? Also, what does self mean?',
        'status': 'PENDING',
    },
    {
        'user': 'arjun_das',
        'course': 'javascript-essentials',
        'title': 'How does async/await work?',
        'content': 'I am struggling to understand async/await in JavaScript. Can someone explain it with a simple example? What happens when we use the await keyword?',
        'status': 'PENDING',
    },
    {
        'user': 'kavya_menon',
        'course': 'html-css-masterclass',
        'title': 'Flexbox vs Grid - When to use which?',
        'content': 'Both Flexbox and CSS Grid seem to do similar things. When should I use Flexbox and when should I use Grid? Can you give practical examples?',
        'status': 'PENDING',
    },
    {
        'user': 'rohan_mishra',
        'course': 'python-for-beginners',
        'title': 'Best way to learn Python quickly?',
        'content': 'I want to learn Python as fast as possible for a job interview. What topics should I focus on? Any tips for quick learning?',
        'status': 'ANSWERED',
        'replies': [
            {'user': 'admin', 'content': 'Here is a focused learning path:\n\n1. **Week 1**: Variables, Data Types, Operators\n2. **Week 2**: Control Flow, Loops, Functions\n3. **Week 3**: Lists, Dictionaries, Strings\n4. **Week 4**: OOP Basics, File Handling\n5. **Week 5**: Practice Problems and Projects\n\n**Tips:**\n- Code every day (even 30 minutes)\n- Build small projects\n- Practice on LeetCode/HackerRank\n- Don\'t just watch videos - write code!', 'is_solution': False},
            {'user': 'sneha_patel', 'content': 'I agree with the roadmap! I would also recommend building a portfolio project like a todo app or calculator.'},
        ]
    },
    {
        'user': 'karan_thakur',
        'course': 'django-web-development',
        'title': 'How to deploy Django app to production?',
        'content': 'I have built a Django app locally and want to deploy it. What are the steps to deploy it to a live server? Which hosting platform is best for beginners?',
        'status': 'PENDING',
    },
]

for qna in qna_data:
    try:
        user = User.objects.get(username=qna['user'])
        course = Course.objects.get(slug=qna['course'])
        
        question, created = QnaQuestion.objects.get_or_create(
            user=user,
            title=qna['title'],
            defaults={
                'course': course,
                'content': qna['content'],
                'status': qna['status'],
                'is_public': True,
            }
        )
        
        if created:
            print(f"  ✓ Q&A: {question.title[:50]}...")
            
            if 'replies' in qna:
                for reply_data in qna['replies']:
                    reply_user = User.objects.get(username=reply_data['user'])
                    Reply.objects.create(
                        question=question,
                        user=reply_user,
                        content=reply_data['content'],
                        is_solution=reply_data.get('is_solution', False),
                    )
                    print(f"    ✓ Reply by {reply_data['user']}")
    except (User.DoesNotExist, Course.DoesNotExist) as e:
        print(f"  ⚠ Error: {e}")


print("\n✅ Data seeding completed successfully!")