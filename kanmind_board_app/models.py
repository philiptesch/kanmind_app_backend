from django.db import models
from django.contrib.auth.models import User



# Create your models here.
class Board(models.Model):
    title = models.CharField(max_length=30)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='boards_owner')
    #owner can has many boards but a board can has only one owner
    members = models.ManyToManyField(User, related_name='boards_member', blank=True)


    def __str__(self):
        return self.title
    
    
class Task(models.Model):
    class Status(models.TextChoices):
        HIGH = "HIGH", "High"
        MEDIUM = "MEDIUM", "Medium"
        LOW = "LOW", "Low"

    class Priority(models.TextChoices):
        TO_DO = "TO_DO", "To Do"
        IN_PROGRESS = "IN_PROGRESS", "In Progress"
        IN_REVIEW = "IN_REVIEW", "In Review"
        DONE = "DONE", "Done"

    title = models.CharField(max_length=30)
    description = models.TextField(blank=True)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='tasks')
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.MEDIUM)
    priority = models.CharField(max_length=20, choices=Priority.choices, default=Priority.TO_DO)
    assignee = models.ForeignKey(User,on_delete=models.CASCADE, related_name='assigned_tasks')
    reviewer = models.ForeignKey(User,on_delete=models.CASCADE, related_name='reviewed_tasks')
    due_date = models.DateField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='task_owner', null=True, blank=True)

    def __str__(self):
        return self.title
    

class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authored_comments')
    content = models.TextField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'Comment by {self.author.username} on {self.task.title}'

    