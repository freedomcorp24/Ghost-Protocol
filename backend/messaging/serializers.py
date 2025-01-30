from rest_framework import serializers
from .models import EphemeralMessage, VaultItem, ShareLink
from .group_models import GroupChat, GroupMembership
from .conversation_models import Conversation

class EphemeralMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = EphemeralMessage
        fields = '__all__'

class VaultItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = VaultItem
        fields = '__all__'

class ShareLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShareLink
        fields = '__all__'

class GroupChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupChat
        fields = '__all__'

class GroupMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupMembership
        fields = '__all__'

class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = '__all__'
