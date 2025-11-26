from django.db import models
from django.contrib.auth.models import User




class Board(models.Model):
    """
    Represents a board in the system
    Fields:
    - title: Name of the board
    - owner: User who created the board (one-to-many)
    - members: Users who are members of the board (many-to-many)
    """
    title = models.CharField(max_length=30)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='boards_owner')
    members = models.ManyToManyField(User, related_name='boards_member', blank=True)


    def __str__(self):
        return self.title
     

class Task(models.Model):
    """
    Represents a task within a board.
    Fields:
     - title: Name of the task
    - description: Optional description
    - board: Board the task belongs to (many-to-one)
    - status: Current status of the task (To Do, In Progress, In Review, Done)
    - priority: Priority of the task (High, Medium, Low)
    - assignee: User assigned to complete the task
    - reviewer: User assigned to review the task
    - due_date: Deadline for the task
    - owner: User who created the task
    """
    class Status(models.TextChoices):
        to_do = "to_do", "To Do"
        progress = "progress", "In Progress"
        review = "review", "In Review"
        done = "done", "Done"
    class Priority(models.TextChoices):
      high = "high", "High"
      medium = "medium", "Medium"
      low = "low", "Low"

    title = models.CharField(max_length=30)
    description = models.TextField(blank=True)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='tasks')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.to_do)
    priority = models.CharField(max_length=20, choices=Priority.choices, default=Priority.medium)
    assignee = models.ForeignKey(User,on_delete=models.CASCADE, related_name='assigned_tasks')
    reviewer = models.ForeignKey(User,on_delete=models.CASCADE, related_name='reviewed_tasks')
    due_date = models.DateField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='task_owner', null=True, blank=True)

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    """
    Represents a comment made on a task.
    Fields:
    - task: Task this comment belongs to (many-to-one)
    - author: User who wrote the comment
    - content: Text content of the comment 
    - created_at: Timestamp of when the comment was created
    """
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authored_comments')
    content = models.TextField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'Comment by {self.author.username} on {self.task.title}'

    