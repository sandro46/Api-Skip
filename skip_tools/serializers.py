from rest_framework import serializers

# from django.contrib.auth.models import User
from skip_tools.models import Task, Search, Template, FilePackage


class TaskSerialize(serializers.ModelSerializer):
    """Serialization of skip types"""

    class Meta:
        model = Task
        fields = ("id", "template_id", "search_type", "is_ok", "prio")



class SearchSerialize(serializers.ModelSerializer):
    """Serialization of skip Search"""

    class Meta:
        model = Search
        fields = ("id", "fio", "search_str", "search_date",
                  "date_search", "date_parsed")


class TemplatesSerialize(serializers.ModelSerializer):
    """Serialization of skip Template"""

    class Meta:
        model = Template
        fields = ("id", "name", "template", "creator", "created")


class FilePackageSerialize(serializers.ModelSerializer):
    """Serialization of file with ids """

    class Meta:
        model = FilePackage
        fields = ("id", "object_id")


class SearchSerializer(serializers.ModelSerializer):
    fk_search_task = serializers.StringRelatedField(many=True)

    class Meta:
        model = Search
        fields = ("id", "search_str", 'fk_search_task')