# create_all_admin_templates.py

import os

templates = {

    'templates/dashboard/admin_qna_pending.html': '''{% extends 'base.html' %}
{% block title %}Pending Questions - Admin{% endblock %}
{% block content %}
<div class="container-fluid py-4">
    <div class="d-flex justify-content-between mb-4">
        <h2 class="fw-bold"><i class="fas fa-clock text-warning me-2"></i>Pending Questions</h2>
        <a href="{% url 'dashboard:admin_qna_list' %}" class="btn btn-outline-secondary">All Questions</a>
    </div>

    {% for question in questions %}
    <div class="card shadow-sm mb-3">
        <div class="card-body">
            <div class="d-flex justify-content-between align-items-start">
                <div>
                    <h5 class="fw-bold mb-1">{{ question.title }}</h5>
                    <p class="text-muted mb-2">{{ question.content|truncatewords:50 }}</p>
                    <small class="text-muted">
                        <i class="fas fa-user me-1"></i>{{ question.user.username }}
                        <span class="mx-2">•</span>
                        <i class="fas fa-book me-1"></i>{{ question.course.title }}
                        <span class="mx-2">•</span>
                        <i class="fas fa-clock me-1"></i>{{ question.created_at|timesince }} ago
                    </small>
                </div>
                <a href="{% url 'qna:question_detail' question.pk %}" class="btn btn-primary btn-sm">
                    <i class="fas fa-reply me-1"></i>Reply
                </a>
            </div>
        </div>
    </div>
    {% empty %}
    <div class="alert alert-success text-center py-5">
        <i class="fas fa-check-circle fa-3x mb-3"></i>
        <h4>No Pending Questions!</h4>
        <p class="text-muted">All questions have been answered.</p>
    </div>
    {% endfor %}
</div>
{% endblock %}''',

    'templates/dashboard/admin_qna_list.html': '''{% extends 'base.html' %}
{% block title %}All Questions - Admin{% endblock %}
{% block content %}
<div class="container-fluid py-4">
    <div class="d-flex justify-content-between mb-4">
        <h2 class="fw-bold">All Questions</h2>
        <a href="{% url 'dashboard:admin_qna_pending' %}" class="btn btn-warning">
            <i class="fas fa-clock me-1"></i>Pending Only
        </a>
    </div>
    <div class="card shadow-sm">
        <div class="table-responsive">
            <table class="table table-hover mb-0">
                <thead class="bg-light">
                    <tr>
                        <th>Question</th>
                        <th>User</th>
                        <th>Course</th>
                        <th>Status</th>
                        <th>Replies</th>
                        <th>Date</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {% for question in questions %}
                    <tr>
                        <td>{{ question.title|truncatechars:40 }}</td>
                        <td>{{ question.user.username }}</td>
                        <td>{{ question.course.title|truncatechars:20 }}</td>
                        <td>
                            <span class="badge {% if question.status == 'PENDING' %}bg-warning{% elif question.status == 'ANSWERED' %}bg-success{% else %}bg-secondary{% endif %}">
                                {{ question.get_status_display }}
                            </span>
                        </td>
                        <td>{{ question.reply_count }}</td>
                        <td>{{ question.created_at|date:"M d, Y" }}</td>
                        <td>
                            <a href="{% url 'qna:question_detail' question.pk %}" class="btn btn-sm btn-primary">
                                <i class="fas fa-reply"></i>
                            </a>
                        </td>
                    </tr>
                    {% empty %}
                    <tr><td colspan="7" class="text-center py-4 text-muted">No questions yet</td></tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
</div>
{% endblock %}''',

    'templates/dashboard/admin_category_list.html': '''{% extends 'base.html' %}
{% block title %}Manage Categories{% endblock %}
{% block content %}
<div class="container-fluid py-4">
    <div class="d-flex justify-content-between mb-4">
        <h2 class="fw-bold">Manage Categories</h2>
        <a href="{% url 'dashboard:admin_category_create' %}" class="btn btn-primary"><i class="fas fa-plus me-1"></i>Add Category</a>
    </div>
    <div class="card shadow-sm">
        <div class="table-responsive">
            <table class="table table-hover mb-0">
                <thead class="bg-light">
                    <tr><th>Color</th><th>Name</th><th>Slug</th><th>Courses</th><th>Status</th><th>Order</th><th>Actions</th></tr>
                </thead>
                <tbody>
                    {% for category in categories %}
                    <tr>
                        <td><span style="display:inline-block;width:20px;height:20px;background:{{ category.color }};border-radius:50%;"></span></td>
                        <td><i class="fab {{ category.icon }} me-1" style="color:{{ category.color }}"></i>{{ category.name }}</td>
                        <td><code>{{ category.slug }}</code></td>
                        <td><span class="badge bg-primary">{{ category.course_count }}</span></td>
                        <td>{% if category.is_active %}<span class="badge bg-success">Active</span>{% else %}<span class="badge bg-danger">Inactive</span>{% endif %}</td>
                        <td>{{ category.order }}</td>
                        <td>
                            <a href="{% url 'dashboard:admin_category_edit' category.pk %}" class="btn btn-sm btn-warning"><i class="fas fa-edit"></i></a>
                            <a href="{% url 'dashboard:admin_category_delete' category.pk %}" class="btn btn-sm btn-danger"><i class="fas fa-trash"></i></a>
                        </td>
                    </tr>
                    {% empty %}
                    <tr><td colspan="7" class="text-center py-4">No categories yet. <a href="{% url 'dashboard:admin_category_create' %}">Create one!</a></td></tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
</div>
{% endblock %}''',

    'templates/dashboard/admin_category_form.html': '''{% extends 'base.html' %}
{% block title %}{{ title }}{% endblock %}
{% block content %}
<div class="container py-4">
    <h2 class="fw-bold mb-4">{{ title }}</h2>
    <div class="card shadow-sm">
        <div class="card-body">
            <form method="POST">
                {% csrf_token %}
                <div class="mb-3"><label class="form-label fw-bold">Name *</label><input type="text" name="name" class="form-control" value="{{ category.name|default:'' }}" required></div>
                <div class="mb-3"><label class="form-label fw-bold">Slug *</label><input type="text" name="slug" class="form-control" value="{{ category.slug|default:'' }}" required></div>
                <div class="mb-3"><label class="form-label fw-bold">Description</label><textarea name="description" class="form-control" rows="3">{{ category.description|default:'' }}</textarea></div>
                <div class="row">
                    <div class="col-md-4 mb-3"><label class="form-label fw-bold">Icon Class</label><input type="text" name="icon" class="form-control" value="{{ category.icon|default:'fa-code' }}" placeholder="fa-python"></div>
                    <div class="col-md-4 mb-3"><label class="form-label fw-bold">Color</label><input type="color" name="color" class="form-control" value="{{ category.color|default:'#007bff' }}"></div>
                    <div class="col-md-4 mb-3"><label class="form-label fw-bold">Display Order</label><input type="number" name="order" class="form-control" value="{{ category.order|default:0 }}"></div>
                </div>
                <div class="mb-4 form-check"><input type="checkbox" name="is_active" class="form-check-input" id="is_active" {% if category.is_active %}checked{% elif not category %}checked{% endif %}><label class="form-check-label" for="is_active">Active</label></div>
                <button type="submit" class="btn btn-primary"><i class="fas fa-save me-1"></i>{{ action }}</button>
                <a href="{% url 'dashboard:admin_category_list' %}" class="btn btn-secondary ms-2">Cancel</a>
            </form>
        </div>
    </div>
</div>
{% endblock %}''',

    'templates/dashboard/admin_category_confirm_delete.html': '''{% extends 'base.html' %}
{% block content %}
<div class="container py-4">
    <div class="row justify-content-center">
        <div class="col-md-6">
            <div class="card border-danger shadow-sm">
                <div class="card-header bg-danger text-white"><h4 class="mb-0"><i class="fas fa-exclamation-triangle me-2"></i>Delete Category</h4></div>
                <div class="card-body">
                    <p>Are you sure you want to delete <strong>{{ category.name }}</strong>?</p>
                    <p class="text-danger"><small>This will also delete all courses in this category!</small></p>
                    <form method="POST">{% csrf_token %}
                        <button type="submit" class="btn btn-danger"><i class="fas fa-trash me-1"></i>Yes, Delete</button>
                        <a href="{% url 'dashboard:admin_category_list' %}" class="btn btn-secondary ms-2">Cancel</a>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}''',

    'templates/dashboard/admin_course_list.html': '''{% extends 'base.html' %}
{% block title %}Manage Courses{% endblock %}
{% block content %}
<div class="container-fluid py-4">
    <div class="d-flex justify-content-between mb-4">
        <h2 class="fw-bold">Manage Courses</h2>
        <a href="{% url 'dashboard:admin_course_create' %}" class="btn btn-primary"><i class="fas fa-plus me-1"></i>Add Course</a>
    </div>
    <div class="card shadow-sm">
        <div class="table-responsive">
            <table class="table table-hover mb-0">
                <thead class="bg-light"><tr><th>Title</th><th>Category</th><th>Level</th><th>Videos</th><th>Enrollments</th><th>Published</th><th>Actions</th></tr></thead>
                <tbody>
                    {% for course in courses %}
                    <tr>
                        <td>{{ course.title|truncatechars:35 }}</td>
                        <td>{{ course.category.name }}</td>
                        <td><span class="badge bg-{% if course.difficulty_level == 'BEGINNER' %}success{% elif course.difficulty_level == 'INTERMEDIATE' %}warning{% else %}danger{% endif %}">{{ course.difficulty_level }}</span></td>
                        <td>{{ course.video_count }}</td>
                        <td>{{ course.enrollment_count }}</td>
                        <td>{% if course.is_published %}<span class="badge bg-success">Yes</span>{% else %}<span class="badge bg-danger">No</span>{% endif %}</td>
                        <td>
                            <a href="{% url 'dashboard:admin_video_list' course.pk %}" class="btn btn-sm btn-info" title="Videos"><i class="fas fa-video"></i></a>
                            <a href="{% url 'dashboard:admin_course_edit' course.pk %}" class="btn btn-sm btn-warning" title="Edit"><i class="fas fa-edit"></i></a>
                            <a href="{% url 'dashboard:admin_course_delete' course.pk %}" class="btn btn-sm btn-danger" title="Delete"><i class="fas fa-trash"></i></a>
                        </td>
                    </tr>
                    {% empty %}
                    <tr><td colspan="7" class="text-center py-4">No courses yet.</td></tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
</div>
{% endblock %}''',

    'templates/dashboard/admin_course_form.html': '''{% extends 'base.html' %}
{% block title %}{{ title }}{% endblock %}
{% block content %}
<div class="container py-4">
    <h2 class="fw-bold mb-4">{{ title }}</h2>
    <div class="card shadow-sm"><div class="card-body">
        <form method="POST">{% csrf_token %}
            <div class="mb-3"><label class="form-label fw-bold">Category *</label><select name="category" class="form-select" required>{% for cat in categories %}<option value="{{ cat.id }}" {% if course.category_id == cat.id %}selected{% endif %}>{{ cat.name }}</option>{% endfor %}</select></div>
            <div class="mb-3"><label class="form-label fw-bold">Title *</label><input type="text" name="title" class="form-control" value="{{ course.title|default:'' }}" required></div>
            <div class="mb-3"><label class="form-label fw-bold">Slug *</label><input type="text" name="slug" class="form-control" value="{{ course.slug|default:'' }}" required></div>
            <div class="mb-3"><label class="form-label fw-bold">Description *</label><textarea name="description" class="form-control" rows="4" required>{{ course.description|default:'' }}</textarea></div>
            <div class="row">
                <div class="col-md-6 mb-3"><label class="form-label fw-bold">Difficulty</label><select name="difficulty_level" class="form-select"><option value="BEGINNER" {% if course.difficulty_level == 'BEGINNER' %}selected{% endif %}>Beginner</option><option value="INTERMEDIATE" {% if course.difficulty_level == 'INTERMEDIATE' %}selected{% endif %}>Intermediate</option><option value="ADVANCED" {% if course.difficulty_level == 'ADVANCED' %}selected{% endif %}>Advanced</option></select></div>
                <div class="col-md-6 mb-3"><label class="form-label fw-bold">Duration (hours)</label><input type="number" name="estimated_duration" class="form-control" value="{{ course.estimated_duration|default:0 }}"></div>
            </div>
            <div class="mb-3"><label class="form-label fw-bold">Prerequisites</label><textarea name="prerequisites" class="form-control" rows="2">{{ course.prerequisites|default:'' }}</textarea></div>
            <div class="mb-3"><label class="form-label fw-bold">Learning Outcomes</label><textarea name="learning_outcomes" class="form-control" rows="2">{{ course.learning_outcomes|default:'' }}</textarea></div>
            <div class="mb-4 form-check"><input type="checkbox" name="is_published" class="form-check-input" {% if course.is_published %}checked{% endif %}><label class="form-check-label">Published</label></div>
            <button type="submit" class="btn btn-primary"><i class="fas fa-save me-1"></i>{{ action }}</button>
            <a href="{% url 'dashboard:admin_course_list' %}" class="btn btn-secondary ms-2">Cancel</a>
        </form>
    </div></div>
</div>
{% endblock %}''',

    'templates/dashboard/admin_course_confirm_delete.html': '''{% extends 'base.html' %}
{% block content %}
<div class="container py-4"><div class="row justify-content-center"><div class="col-md-6">
    <div class="card border-danger"><div class="card-header bg-danger text-white"><h4 class="mb-0">Delete Course</h4></div>
    <div class="card-body"><p>Delete <strong>{{ course.title }}</strong>?</p>
    <form method="POST">{% csrf_token %}<button class="btn btn-danger">Yes, Delete</button><a href="{% url 'dashboard:admin_course_list' %}" class="btn btn-secondary ms-2">Cancel</a></form></div></div>
</div></div></div>
{% endblock %}''',

    'templates/dashboard/admin_video_list.html': '''{% extends 'base.html' %}
{% block title %}Videos - {{ course.title }}{% endblock %}
{% block content %}
<div class="container-fluid py-4">
    <div class="d-flex justify-content-between mb-4">
        <div>
            <h2 class="fw-bold">Videos</h2>
            <p class="text-muted">Course: {{ course.title }}</p>
        </div>
        <div>
            <a href="{% url 'dashboard:admin_video_create' course.pk %}" class="btn btn-primary"><i class="fas fa-plus me-1"></i>Add Video</a>
            <a href="{% url 'dashboard:admin_course_list' %}" class="btn btn-outline-secondary ms-2">Back to Courses</a>
        </div>
    </div>
    <div class="card shadow-sm"><div class="table-responsive"><table class="table table-hover mb-0">
        <thead class="bg-light"><tr><th>Order</th><th>Title</th><th>Duration</th><th>Preview</th><th>Actions</th></tr></thead>
        <tbody>{% for video in videos %}<tr>
            <td>{{ video.order }}</td><td>{{ video.title }}</td><td>{{ video.duration }} min</td>
            <td>{% if video.is_preview %}<span class="badge bg-info">Yes</span>{% else %}<span class="badge bg-secondary">No</span>{% endif %}</td>
            <td><a href="{% url 'dashboard:admin_video_edit' video.pk %}" class="btn btn-sm btn-warning"><i class="fas fa-edit"></i></a>
            <a href="{% url 'dashboard:admin_video_delete' video.pk %}" class="btn btn-sm btn-danger"><i class="fas fa-trash"></i></a></td>
        </tr>{% empty %}<tr><td colspan="5" class="text-center py-4">No videos yet.</td></tr>{% endfor %}</tbody>
    </table></div></div>
</div>
{% endblock %}''',

    'templates/dashboard/admin_video_form.html': '''{% extends 'base.html' %}
{% block title %}{{ title }}{% endblock %}
{% block content %}
<div class="container py-4">
    <h2 class="fw-bold mb-4">{{ title }}</h2>
    <div class="card shadow-sm"><div class="card-body">
        <form method="POST">{% csrf_token %}
            <div class="mb-3"><label class="form-label fw-bold">Title *</label><input type="text" name="title" class="form-control" value="{{ video.title|default:'' }}" required></div>
            <div class="mb-3"><label class="form-label fw-bold">Description</label><textarea name="description" class="form-control" rows="3">{{ video.description|default:'' }}</textarea></div>
            <div class="mb-3"><label class="form-label fw-bold">Video URL</label><input type="url" name="video_url" class="form-control" value="{{ video.video_url|default:'' }}" placeholder="https://youtube.com/embed/..."></div>
            <div class="row">
                <div class="col-md-4 mb-3"><label class="form-label fw-bold">Duration (min)</label><input type="number" name="duration" class="form-control" value="{{ video.duration|default:0 }}"></div>
                <div class="col-md-4 mb-3"><label class="form-label fw-bold">Order</label><input type="number" name="order" class="form-control" value="{{ video.order|default:0 }}"></div>
                <div class="col-md-4 mb-3 pt-4"><div class="form-check mt-2"><input type="checkbox" name="is_preview" class="form-check-input" {% if video.is_preview %}checked{% endif %}><label class="form-check-label">Preview Video</label></div></div>
            </div>
            <button type="submit" class="btn btn-primary"><i class="fas fa-save me-1"></i>{{ action }}</button>
        </form>
    </div></div>
</div>
{% endblock %}''',

    'templates/dashboard/admin_video_confirm_delete.html': '''{% extends 'base.html' %}
{% block content %}
<div class="container py-4"><div class="row justify-content-center"><div class="col-md-6">
    <div class="card border-danger"><div class="card-header bg-danger text-white"><h4 class="mb-0">Delete Video</h4></div>
    <div class="card-body"><p>Delete video <strong>{{ video.title }}</strong>?</p>
    <form method="POST">{% csrf_token %}<button class="btn btn-danger">Yes, Delete</button></form></div></div>
</div></div></div>
{% endblock %}''',

    'templates/dashboard/admin_quiz_list.html': '''{% extends 'base.html' %}
{% block title %}Manage Quizzes{% endblock %}
{% block content %}
<div class="container-fluid py-4">
    <h2 class="fw-bold mb-4">Manage Quizzes</h2>
    <div class="card shadow-sm"><div class="table-responsive"><table class="table table-hover mb-0">
        <thead class="bg-light"><tr><th>Quiz</th><th>Course</th><th>Questions</th><th>Attempts</th><th>Pass Score</th><th>Actions</th></tr></thead>
        <tbody>{% for quiz in quizzes %}<tr>
            <td>{{ quiz.title }}</td><td>{{ quiz.course.title|truncatechars:25 }}</td>
            <td><span class="badge bg-primary">{{ quiz.question_count }}</span></td>
            <td><span class="badge bg-info">{{ quiz.attempt_count }}</span></td>
            <td>{{ quiz.passing_score }}%</td>
            <td><a href="{% url 'dashboard:admin_question_list' quiz.pk %}" class="btn btn-sm btn-info"><i class="fas fa-list me-1"></i>Questions</a></td>
        </tr>{% empty %}<tr><td colspan="6" class="text-center py-4">No quizzes yet.</td></tr>{% endfor %}</tbody>
    </table></div></div>
</div>
{% endblock %}''',

    'templates/dashboard/admin_question_list.html': '''{% extends 'base.html' %}
{% block title %}Questions - {{ quiz.title }}{% endblock %}
{% block content %}
<div class="container-fluid py-4">
    <div class="d-flex justify-content-between mb-4">
        <div>
            <h2 class="fw-bold">Quiz Questions</h2>
            <p class="text-muted">{{ quiz.title }} | {{ quiz.course.title }}</p>
        </div>
        <a href="{% url 'dashboard:admin_quiz_list' %}" class="btn btn-outline-secondary">Back to Quizzes</a>
    </div>
    {% for question in questions %}
    <div class="card shadow-sm mb-3">
        <div class="card-header bg-white">
            <strong>Q{{ question.order }}: {{ question.question_text }}</strong>
            <span class="badge bg-primary float-end">{{ question.points }} points</span>
        </div>
        <div class="card-body">
            <ul class="list-group list-group-flush">
                {% for choice in question.choices.all %}
                <li class="list-group-item {% if choice.is_correct %}list-group-item-success{% endif %}">
                    {% if choice.is_correct %}<i class="fas fa-check-circle text-success me-2"></i>{% else %}<i class="fas fa-circle text-muted me-2"></i>{% endif %}
                    {{ choice.choice_text }}
                </li>
                {% endfor %}
            </ul>
            {% if question.explanation %}
            <div class="mt-2 p-2 bg-light rounded">
                <small><i class="fas fa-info-circle me-1"></i><strong>Explanation:</strong> {{ question.explanation }}</small>
            </div>
            {% endif %}
        </div>
    </div>
    {% empty %}
    <div class="alert alert-info">No questions in this quiz yet.</div>
    {% endfor %}
</div>
{% endblock %}''',

    'templates/dashboard/admin_users.html': '''{% extends 'base.html' %}
{% block title %}Manage Users{% endblock %}
{% block content %}
<div class="container-fluid py-4">
    <h2 class="fw-bold mb-4">Manage Users</h2>
    <div class="card shadow-sm mb-4"><div class="card-body">
        <form method="GET" class="d-flex">
            <input type="text" name="search" class="form-control me-2" placeholder="Search users..." value="{{ search_query }}">
            <button type="submit" class="btn btn-primary"><i class="fas fa-search"></i></button>
        </form>
    </div></div>
    <div class="card shadow-sm"><div class="table-responsive"><table class="table table-hover mb-0">
        <thead class="bg-light"><tr><th>Username</th><th>Name</th><th>Email</th><th>Joined</th><th>Actions</th></tr></thead>
        <tbody>{% for u in users %}<tr>
            <td>{{ u.username }}</td><td>{{ u.first_name }} {{ u.last_name }}</td><td>{{ u.email }}</td>
            <td>{{ u.date_joined|date:"M d, Y" }}</td>
            <td><a href="{% url 'dashboard:admin_user_detail' u.id %}" class="btn btn-sm btn-info"><i class="fas fa-eye me-1"></i>View</a></td>
        </tr>{% empty %}<tr><td colspan="5" class="text-center py-4">No users found.</td></tr>{% endfor %}</tbody>
    </table></div></div>
</div>
{% endblock %}''',

    'templates/dashboard/admin_user_detail.html': '''{% extends 'base.html' %}
{% block title %}User: {{ profile_user.username }}{% endblock %}
{% block content %}
<div class="container py-4">
    <a href="{% url 'dashboard:admin_users' %}" class="btn btn-outline-secondary mb-3"><i class="fas fa-arrow-left me-1"></i>Back to Users</a>
    <div class="row">
        <div class="col-md-4">
            <div class="card shadow-sm">
                <div class="card-body text-center">
                    <i class="fas fa-user-circle fa-5x text-muted mb-3"></i>
                    <h4>{{ profile_user.first_name }} {{ profile_user.last_name }}</h4>
                    <p class="text-muted">@{{ profile_user.username }}</p>
                    <p><i class="fas fa-envelope me-1"></i>{{ profile_user.email }}</p>
                    <p><small class="text-muted">Joined: {{ profile_user.date_joined|date:"M d, Y" }}</small></p>
                </div>
            </div>
        </div>
        <div class="col-md-8">
            <div class="card shadow-sm mb-4">
                <div class="card-header bg-white"><h5 class="mb-0">Enrolled Courses</h5></div>
                <div class="list-group list-group-flush">
                    {% for enrollment in enrollments %}
                    <div class="list-group-item d-flex justify-content-between">
                        <span>{{ enrollment.course.title }}</span>
                        <span class="badge bg-primary">{{ enrollment.progress_percentage|floatformat:0 }}%</span>
                    </div>
                    {% empty %}
                    <div class="list-group-item text-muted">No enrollments</div>
                    {% endfor %}
                </div>
            </div>
            <div class="card shadow-sm">
                <div class="card-header bg-white"><h5 class="mb-0">Quiz Attempts</h5></div>
                <div class="list-group list-group-flush">
                    {% for attempt in quiz_attempts %}
                    <div class="list-group-item d-flex justify-content-between">
                        <span>{{ attempt.quiz.title }}</span>
                        <span class="badge {% if attempt.is_passed %}bg-success{% else %}bg-danger{% endif %}">{{ attempt.score|floatformat:0 }}%</span>
                    </div>
                    {% empty %}
                    <div class="list-group-item text-muted">No quiz attempts</div>
                    {% endfor %}
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}''',

    'templates/dashboard/user_dashboard.html': '''{% extends 'base.html' %}
{% block title %}My Dashboard{% endblock %}
{% block content %}
<div class="container py-5">
    <h2 class="fw-bold mb-4">Welcome, {{ user.first_name|default:user.username }}!</h2>
    <div class="row g-4">
        <div class="col-md-4">
            <div class="card shadow-sm text-center h-100"><div class="card-body">
                <i class="fas fa-graduation-cap fa-3x text-primary mb-3"></i>
                <h5>My Courses</h5>
                <a href="{% url 'dashboard:user_courses' %}" class="btn btn-primary mt-2">View Courses</a>
            </div></div>
        </div>
        <div class="col-md-4">
            <div class="card shadow-sm text-center h-100"><div class="card-body">
                <i class="fas fa-chart-line fa-3x text-success mb-3"></i>
                <h5>My Progress</h5>
                <a href="{% url 'dashboard:user_progress' %}" class="btn btn-success mt-2">View Progress</a>
            </div></div>
        </div>
        <div class="col-md-4">
            <div class="card shadow-sm text-center h-100"><div class="card-body">
                <i class="fas fa-comments fa-3x text-info mb-3"></i>
                <h5>Q&A Forum</h5>
                <a href="{% url 'qna:question_list' %}" class="btn btn-info mt-2">Ask Question</a>
            </div></div>
        </div>
    </div>
    <div class="row mt-4">
        <div class="col-md-6">
            <div class="card shadow-sm"><div class="card-header bg-white"><h5 class="mb-0">Recent Enrollments</h5></div>
            <div class="list-group list-group-flush">
                {% for enrollment in enrollments %}
                <a href="{% url 'courses:course_detail' enrollment.course.slug %}" class="list-group-item list-group-item-action">
                    {{ enrollment.course.title }} <span class="badge bg-primary float-end">{{ enrollment.progress_percentage|floatformat:0 }}%</span>
                </a>
                {% empty %}<div class="list-group-item text-muted">No courses yet. <a href="{% url 'courses:course_list' %}">Browse courses!</a></div>
                {% endfor %}
            </div></div>
        </div>
        <div class="col-md-6">
            <div class="card shadow-sm"><div class="card-header bg-white"><h5 class="mb-0">Recent Quiz Results</h5></div>
            <div class="list-group list-group-flush">
                {% for attempt in quiz_attempts %}
                <div class="list-group-item d-flex justify-content-between">
                    <span>{{ attempt.quiz.title }}</span>
                    <span class="badge {% if attempt.is_passed %}bg-success{% else %}bg-danger{% endif %}">{{ attempt.score|floatformat:0 }}%</span>
                </div>
                {% empty %}<div class="list-group-item text-muted">No quiz attempts yet.</div>
                {% endfor %}
            </div></div>
        </div>
    </div>
</div>
{% endblock %}''',

    'templates/dashboard/user_courses.html': '''{% extends 'base.html' %}
{% block title %}My Courses{% endblock %}
{% block content %}
<div class="container py-5">
    <h2 class="fw-bold mb-4">My Courses</h2>
    <div class="row g-4">
        {% for enrollment in enrollments %}
        <div class="col-md-6 col-lg-4">
            <div class="card shadow-sm h-100">
                <div class="card-body">
                    <h5 class="card-title">{{ enrollment.course.title }}</h5>
                    <p class="text-muted">{{ enrollment.course.category.name }}</p>
                    <div class="progress mb-2" style="height:8px;"><div class="progress-bar bg-success" style="width:{{ enrollment.progress_percentage }}%"></div></div>
                    <small class="text-muted">{{ enrollment.progress_percentage|floatformat:0 }}% Complete</small>
                </div>
                <div class="card-footer bg-transparent">
                    <a href="{% url 'courses:course_detail' enrollment.course.slug %}" class="btn btn-primary btn-sm w-100">Continue Learning</a>
                </div>
            </div>
        </div>
        {% empty %}
        <div class="col-12 text-center py-5">
            <i class="fas fa-book-open fa-4x text-muted mb-3"></i>
            <h4>No courses yet</h4>
            <a href="{% url 'courses:course_list' %}" class="btn btn-primary">Browse Courses</a>
        </div>
        {% endfor %}
    </div>
</div>
{% endblock %}''',

    'templates/dashboard/user_progress.html': '''{% extends 'base.html' %}
{% block title %}My Progress{% endblock %}
{% block content %}
<div class="container py-5">
    <h2 class="fw-bold mb-4">My Learning Progress</h2>
    <div class="row">
        <div class="col-md-6">
            <div class="card shadow-sm"><div class="card-header bg-white"><h5 class="mb-0">Video Progress</h5></div>
            <div class="list-group list-group-flush">
                {% for progress in video_progress %}
                <div class="list-group-item d-flex justify-content-between">
                    <span>{{ progress.video.title }}</span>
                    {% if progress.is_completed %}<span class="badge bg-success">Completed</span>{% else %}<span class="badge bg-warning">In Progress</span>{% endif %}
                </div>
                {% empty %}<div class="list-group-item text-muted">No videos watched yet.</div>
                {% endfor %}
            </div></div>
        </div>
        <div class="col-md-6">
            <div class="card shadow-sm"><div class="card-header bg-white"><h5 class="mb-0">Quiz Results</h5></div>
            <div class="list-group list-group-flush">
                {% for result in quiz_results %}
                <div class="list-group-item d-flex justify-content-between">
                    <span>{{ result.quiz.title }}</span>
                    <span class="badge {% if result.is_passed %}bg-success{% else %}bg-danger{% endif %}">{{ result.score|floatformat:0 }}%</span>
                </div>
                {% empty %}<div class="list-group-item text-muted">No quizzes taken yet.</div>
                {% endfor %}
            </div></div>
        </div>
    </div>
</div>
{% endblock %}''',
}

# Create all templates
print("Creating ALL dashboard templates...\n")
count = 0
for filepath, content in templates.items():
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  ✓ {filepath}")
    count += 1

print(f"\n✅ Created {count} templates!")
print("\nRestart server: python manage.py runserver")