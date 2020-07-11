""" Data serializers - used for the REST API """

from django.contrib.auth.models import User
from rest_framework import serializers

from visualizer.graphCreator.graphCreator import BadJSONError
from .models import JsonConfig
from .validators import try_to_load_json

#pylint: disable=too-few-public-methods


class JsonConfigSerializer(serializers.HyperlinkedModelSerializer):
    """ The rest_framework serializer for a JsonConfig Model """

    class Meta:
        """ The meta class to simplify construction of the serializer """
        model = JsonConfig
        fields = JsonConfig.get_all_non_auto_fields() + ['owner']
        owner = serializers.ReadOnlyField(source='owner.username')

    #pylint: disable=invalid-name
    @classmethod
    def validate_jsonFile(cls, value):
        """ Validate that the upload JSON is successfully parsable """
        try:
            try_to_load_json(value)
        except BadJSONError as exception:
            raise serializers.ValidationError("JSON is not valid: " + str(exception))
        except Exception as exception:
            raise serializers.ValidationError("Unknown error: " + str(exception))
        return value


class UserSerializer(serializers.ModelSerializer):
    """ The rest_framework serializer for a User Model """
    this_users_jsons = serializers.PrimaryKeyRelatedField(
        many=True, queryset=JsonConfig.objects.all())  # pylint: disable=no-member

    class Meta:
        """ The meta class to simplify construction of the serializer """
        model = User
        fields = ['id', 'username', 'this_users_jsons']
