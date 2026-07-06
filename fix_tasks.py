import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from courses.models import Task
from django.core.files.base import ContentFile

def fix_tasks():
    print("Fixing Task Files...")
    
    # Ensure media/tasks directory exists
    tasks_dir = os.path.join('media', 'tasks')
    if not os.path.exists(tasks_dir):
        os.makedirs(tasks_dir)
        print(f"  Created directory: {tasks_dir}")
    
    # Get all tasks missing files
    tasks_missing_files = Task.objects.filter(task_file='')
    print(f"  Found {tasks_missing_files.count()} tasks missing files.")
    
    for task in tasks_missing_files:
        # Create a sample PDF-like content
        content = f"Syntax Academy - Assignment\n\nTask: {task.title}\nDescription: {task.description}\n\nPlease complete this task and submit it through the student portal."
        
        # Save dummy file to the task
        filename = f"{task.slug}_assignment.txt"
        task.task_file.save(filename, ContentFile(content))
        task.save()
        print(f"  Fixed task: {task.title} (File: {filename})")

if __name__ == '__main__':
    fix_tasks()
    print("All tasks fixed!")
