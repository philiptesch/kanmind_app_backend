from rest_framework import serializers
from kanmind_board_app.models import Board, Task, Comment
from users.models import User
from users.api.seralizers import UserProfileSerializer


# Serializer for Board overview (for list view)
class BoardSerializer(serializers.ModelSerializer):
    owner_id = serializers.IntegerField(read_only=True)  # ID of the board owner
    members = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True, many=True)  # Members by ID
    member_count = serializers.SerializerMethodField()  # Number of members
    ticket_count = serializers.SerializerMethodField()  # Total number of tasks
    tasks_to_do_count = serializers.SerializerMethodField()  # Number of "to_do" tasks
    tasks_high_prio_count = serializers.SerializerMethodField()  # Number of high-priority tasks

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


# Serializer for Task creation and representation
class TaskSerializer(serializers.ModelSerializer):
    assignee_id = serializers.IntegerField(write_only=True)  # ID of the assigned user
    reviewer_id = serializers.IntegerField(write_only=True)  # ID of the reviewer
    assignee = UserProfileSerializer(read_only=True)  # Assignee details
    reviewer = UserProfileSerializer(read_only=True)  # Reviewer details
    id = serializers.IntegerField(read_only=True)
    comments_count = serializers.SerializerMethodField()  # Number of comments

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


# Serializer for Board details including tasks
class BoardDetailSerializer(serializers.ModelSerializer):
    owner_id = serializers.IntegerField(read_only=True)
    members = UserProfileSerializer(read_only=True, many=True)
    tasks = TaskSerializer(read_only=True, many=True)

    class Meta:
        model = Board
        fields = ['id', 'title', 'owner_id', 'members', 'tasks']


# Serializer for Board PATCH (partial update)
class BoardDetailForPatchSerializer(serializers.ModelSerializer):
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


# Serializer for Task assignment list view
class TaskAssignSerializer(serializers.ModelSerializer):
    assignee = UserProfileSerializer(read_only=True)
    reviewer = UserProfileSerializer(read_only=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ['id', 'board', 'title', 'description', 'status', 'priority',
                  'due_date', 'assignee', 'reviewer', 'due_date', 'comments_count']

    def get_comments_count(self, obj):
        return obj.comments.count()


# Serializer for Task detail view (PATCH/UPDATE)
class TaskDetailSerializer(serializers.ModelSerializer):
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

# Serializer for Comment response (GET)
class CommentResponseSerializer(serializers.ModelSerializer):
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


# Serializer for Comment creation (POST)
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['content']
