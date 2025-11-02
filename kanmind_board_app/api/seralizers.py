from rest_framework import serializers
from kanmind_board_app.models import Board,Task,Comment
from users.models import User
from users.api.seralizer import UserProfileSerializer

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



class BoardDetailSerializer(serializers.ModelSerializer):

    owner_id = serializers.IntegerField(read_only=True)
    members = UserProfileSerializer(read_only=True, many=True)

    class Meta:
        model = Board
        fields = ['id', 'title', 'owner_id', 'members']