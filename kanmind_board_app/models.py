from django.db import models
from django.contrib.auth.models import User



# board Model
class Board(models.Model):
    title = models.CharField(max_length=30)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='boards_owner')
    members = models.ManyToManyField(User, related_name='boards_member', blank=True)


    def __str__(self):
        return self.title
     
     
# Task Model for the board   
class Task(models.Model):
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
    
# Comment Model for each Task    
class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authored_comments')
    content = models.TextField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'Comment by {self.author.username} on {self.task.title}'

    