from rest_framework import serializers
from kanmind_board_app.models import Board,Task,Comment
from users.models import User


class BoardSerializer(serializers.ModelSerializer):

    owner_id = serializers.PrimaryKeyRelatedField(queryset= User.objects.all(), source='boards_owner', write_only =True)
    members = serializers.PrimaryKeyRelatedField(queryset= User.objects.all(), write_only=True, many=True)
    member_count = serializers.SerializerMethodField()
    ticket_count = serializers.SerializerMethodField()
    tasks_to_do_count = serializers.SerializerMethodField()
    tasks_high_prio_count = serializers.SerializerMethodField()

    class Meta:
        model = Board
        fields = ['id', 'title', 'members', 'member_count', 'ticket_count', 'tasks_to_do_count', 'tasks_high_prio_count', 'owner_id']


    def get_market_count(self, obj):
        return obj.members.count()
    

    def get_tasks_to_do_count(self, obj):
        return obj.tasks.filter(status='TO_DO').count()

    def get_tasks_high_prio_count(self, obj):
        return obj.tasks.filter(priority='HIGH').count()

