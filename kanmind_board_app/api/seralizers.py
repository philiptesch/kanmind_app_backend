from rest_framework import serializers
from kanmind_board_app.models import Board,Task,Comment
from users.models import User
from users.api.seralizers import UserProfileSerializer, UserCommentSerializer

class BoardSerializer(serializers.ModelSerializer):

    owner_id = serializers.IntegerField(read_only=True)
    members = serializers.PrimaryKeyRelatedField(queryset= User.objects.all(), write_only=True, many=True)
    member_count = serializers.SerializerMethodField()
    ticket_count = serializers.SerializerMethodField()
    tasks_to_do_count = serializers.SerializerMethodField()
    tasks_high_prio_count = serializers.SerializerMethodField()

    class Meta:
        model = Board
        fields = ['id', 'title', 'members', 'member_count', 'ticket_count', 'tasks_to_do_count', 'tasks_high_prio_count', 'owner_id']



    def get_member_count(self, obj):
        return obj.members.count()
    

    def get_tasks_to_do_count(self, obj):
        return obj.tasks.filter(status='TO_DO').count()

    def get_tasks_high_prio_count(self, obj):
        return obj.tasks.filter(priority='HIGH').count()
    
    def get_ticket_count(self, obj):
        return obj.tasks.count()

class TaskSerializer(serializers.ModelSerializer):
    assignee_id= serializers.IntegerField(write_only=True)
    reviewer_id= serializers.IntegerField(write_only=True)
    assignee = UserProfileSerializer(read_only=True)
    reviewer = UserProfileSerializer(read_only=True)    

    class Meta:
        model = Task
        fields = ['board', 'title', 'description', 'status', 'priority', 'assignee_id', 'reviewer_id', 'due_date', 'assignee', 'reviewer' ]


    def create(self, validated_data):
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

    owner_id = serializers.IntegerField(read_only=True)
    members = UserProfileSerializer(read_only=True, many=True)
    tasks = TaskSerializer(read_only=True, many=True)
    class Meta:
        model = Board
        fields = ['id', 'title', 'owner_id', 'members', 'tasks']



      
class TaskAssignSerializer(serializers.ModelSerializer):
    assignee = UserProfileSerializer(read_only=True)
    reviewer = UserProfileSerializer(read_only=True)    
    comments_count = serializers.SerializerMethodField()



    def get_comments_count(self, obj):
        return obj.comments.count()
    class Meta:
        model = Task
        fields = ['id', 'board', 'title', 'description', 'status', 'priority',  'due_date', 'assignee', 'reviewer', 'due_date', 'comments_count']


class TaskDetailSerializer(serializers.ModelSerializer):
    assignee_id= serializers.IntegerField(write_only=True)
    reviewer_id= serializers.IntegerField(write_only=True)
    assignee = UserProfileSerializer(read_only=True)
    reviewer = UserProfileSerializer(read_only=True)    
    
    
    class Meta:
        model = Task
        fields = ['id','title', 'description', 'status', 'priority', 'assignee_id', 'reviewer_id', 'due_date', 'assignee', 'reviewer' ]


    def update(self, instance, validated_data):
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

        #for attr, value in validated_data.items():
        #    setattr(instance, attr, value)

        instance.save()
        return instance
    
class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    comment_id = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(read_only=True)


    def get_comment_id(self, obj):
        return obj.id

    def get_author(self, obj):
        return f"{obj.author.first_name} {obj.author.last_name}".strip()
    

    class Meta:
        model = Comment
        fields = ['comment_id', 'author', 'content', 'created_at']