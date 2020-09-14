from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer, Serializer
from .models import TestGroup, TestCategory, TestTasks, TestGroupCategory, TestGroupUser


class TestGroupSerializer(ModelSerializer):
    class Meta:
        model = TestGroup
        fields = '__all__'


class TestGroupUserSerializer(ModelSerializer):
    class Meta:
        model = TestGroupUser
        fields = '__all__'


class TestGroupClosedSerializer(ModelSerializer):
    closed = serializers.SerializerMethodField('get_closed')

    def get_closed(self, obj):
        return True

    class Meta:
        model = TestGroup
        fields = ('id', 'name', 'closed')


class TestCategorySerializer(ModelSerializer):
    test_groups = serializers.SerializerMethodField('get_test_groups')

    def get_test_groups(self, obj):
        user = self.context['request'].user
        test_groups = obj.test_groups.all()
        group_list = []
        for group in test_groups:
            if group.free:
                serializer = TestGroupSerializer(group)
            else:
                modules = group.testgroupuser_set.filter(user=user).filter(verified=True)
                if len(modules) > 0:
                    serializer = TestGroupSerializer(group)
                else:
                    serializer = TestGroupClosedSerializer(group)
            group_list.append(serializer.data)
        return group_list

    class Meta:
        model = TestCategory
        fields = '__all__'


class TestTasksSerializer(ModelSerializer):
    class Meta:
        model = TestTasks
        fields = '__all__'


class TestGroupCategorySerializer(ModelSerializer):
    class Meta:
        model = TestGroupCategory
        fields = '__all__'


class TestGroupDetailedSerializer(ModelSerializer):
    test_group_categories = TestGroupCategorySerializer(many=True)

    class Meta:
        model = TestGroup
        fields = '__all__'


class TestGroupCategoryDetailedSerializer(ModelSerializer):
    tests = TestTasksSerializer(many=True)

    class Meta:
        model = TestGroupCategory
        fields = '__all__'


class FilteredListSerializer(serializers.ListSerializer):

    def to_representation(self, instance):
        instance = instance.exclude(testgroupuser__user_id=self.context['request'].user.id,
                                    testgroupuser__verified=True)
        return super(FilteredListSerializer, self).to_representation(instance)


class TestGroupDetailedPriceSerializer(ModelSerializer):
    test_group_categories = TestGroupCategorySerializer(many=True)

    class Meta:
        list_serializer_class = FilteredListSerializer
        model = TestGroup
        fields = '__all__'


class TestCategoryPriceSerializer(ModelSerializer):
    test_groups = SerializerMethodField('get_test_groups')

    def get_test_groups(self, obj):
        return TestGroupDetailedPriceSerializer(instance=obj.test_groups.filter(free=False), many=True, context=self.context).data

    class Meta:
        model = TestCategory
        fields = '__all__'
