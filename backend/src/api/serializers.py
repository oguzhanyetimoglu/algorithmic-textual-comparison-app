from rest_framework import serializers

from .models import NAICSCode, SICCode, TenK, TenKFileUpload


class SICCodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = SICCode
        fields = '__all__'


class NAICSCodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = NAICSCode
        fields = '__all__'


class TenKSerializer(serializers.ModelSerializer):

    class Meta:
        model = TenK
        fields = '__all__'


class TenKFileUploadSerializer(serializers.ModelSerializer):

    class Meta:
        model = TenKFileUpload
        fields = "__all__"


class DynamicFieldsTenKSerializer(TenKSerializer):

    class Meta(TenKSerializer.Meta):
        exclude = ()

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super().__init__(*args, **kwargs)

        if fields:
            existing_fields = set(self.fields.keys())
            for field_name in existing_fields - set(fields):
                self.fields.pop(field_name)
