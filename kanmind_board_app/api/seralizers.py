from rest_framework import serializers
from kanmind_board_app.models import Board, Task, Comment
from users.models import User
from users.api.seralizers import UserProfileSerializer


class BoardSerializer(serializers.ModelSerializer):
    """
    Serializer for representing boards including
    members, owner, and various counts
    (members, tickets, task status).
    """
    owner_id = serializers.IntegerField(read_only=True)  
    members = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True, many=True)  
    member_count = serializers.SerializerMethodField()  
    ticket_count = serializers.SerializerMethodField()  
    tasks_to_do_count = serializers.SerializerMethodField()  
    tasks_high_prio_count = serializers.SerializerMethodField()  

    class Meta:
        model = Board
        fields = [
            'id', 'title', 'members', 'member_count', 'ticket_count',
            'tasks_to_do_count', 'tasks_high_prio_count', 'owner_id'
        ]

    def get_member_count(self, obj):
        return obj.members.count()

    def get_tasks_to_do_count(self, obj):
        return obj.tasks.filter(status='to_do').count()

    def get_tasks_high_prio_count(self, obj):
        return obj.tasks.filter(priority='high').count()

    def get_ticket_count(self, obj):
        return obj.tasks.count()


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for tasks of a board including
    comment count and simplified user info
    for assignees and reviewers.
    """
    assignee_id = serializers.IntegerField(write_only=True)  
    reviewer_id = serializers.IntegerField(write_only=True)  
    assignee = UserProfileSerializer(read_only=True)  
    reviewer = UserProfileSerializer(read_only=True)  
    id = serializers.IntegerField(read_only=True)
    comments_count = serializers.SerializerMethodField()  

    class Meta:
        model = Task
        fields = [
            'id', 'board', 'title', 'description', 'status', 'priority',
            'assignee_id', 'reviewer_id', 'due_date', 'assignee', 'reviewer', 'comments_count'
        ]

    def get_comments_count(self, obj):
        return obj.comments.count()

    def create(self, validated_data):
        """
        Create a Task including Assignee and Reviewer from their IDs
        """
        assignee_id = validated_data.pop('assignee_id')
        reviewer_id = validated_data.pop('reviewer_id')

        assignee = User.objects.get(id=assignee_id)
        reviewer = User.objects.get(id=reviewer_id)
        task = Task.objects.create(
            **validated_data,
            assignee=assignee,
            reviewer=reviewer
        )
        return task


class BoardDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for boards with full
    user information for members and tasks.
    """
    owner_id = serializers.IntegerField(read_only=True)
    members = UserProfileSerializer(read_only=True, many=True)
    tasks = TaskSerializer(read_only=True, many=True)

    class Meta:
        model = Board
        fields = ['id', 'title', 'owner_id', 'members', 'tasks']


class BoardDetailForPatchSerializer(serializers.ModelSerializer):
    """
    Serializer for updating boards, showing owner and
    members as read-only fields using UserProfileSerializer and owner_data as just.
    """
    owner_data = UserProfileSerializer(read_only=True)
    members_data = UserProfileSerializer(read_only=True, many=True)
    members = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.all(),
        required=False,
        write_only=True
    )

    class Meta:
        model = Board
        fields = ['id', 'title', 'owner_data', 'members_data', 'members']

class TaskAssignOrReviewerSerializer(serializers.ModelSerializer):
    """
   Serializes Task objects for list views where a user is:
    assignee (assigned user)
    reviewer (reviewing user)
    """
    assignee = UserProfileSerializer(read_only=True)
    reviewer = UserProfileSerializer(read_only=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ['id', 'board', 'title', 'description', 'status', 'priority',
                  'due_date', 'assignee', 'reviewer', 'due_date', 'comments_count']

    def get_comments_count(self, obj):
        return obj.comments.count()


class TaskDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for a single task
    with assignees and reviewers as nested user data.
    """
    assignee_id = serializers.IntegerField(write_only=True)
    reviewer_id = serializers.IntegerField(write_only=True)
    assignee = UserProfileSerializer(read_only=True)
    reviewer = UserProfileSerializer(read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'priority',
                  'assignee_id', 'reviewer_id', 'due_date', 'assignee', 'reviewer']

    def update(self, instance, validated_data):
        """
        Update a Task including Assignee and Reviewer
        """
        assignee_id = validated_data.pop('assignee_id', None)
        reviewer_id = validated_data.pop('reviewer_id', None)

        if assignee_id is not None:
            assignee = User.objects.get(id=assignee_id)
            instance.assignee = assignee

        if reviewer_id is not None:
            reviewer = User.objects.get(id=reviewer_id)
            instance.reviewer = reviewer

        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.status = validated_data.get('status', instance.status)
        instance.priority = validated_data.get('priority', instance.priority)
        instance.due_date = validated_data.get('due_date', instance.due_date)

        instance.save()
        return instance
    

class CommentResponseSerializer(serializers.ModelSerializer):
    """
    Serializer for returning comments with author's username, id, created_at.
    """

    author = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'author', 'content', 'created_at']

    def get_author(self, obj):
        """
        Return the full name of the comment author
        """
        return f"{obj.author.first_name} {obj.author.last_name}".strip()


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for creating comments with only the content field.
    """    
    class Meta:
        model = Comment
        fields = ['content']
