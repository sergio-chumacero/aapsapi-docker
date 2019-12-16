from rest_framework import serializers
from ambiental import models
from performance.models import EPSA
from drf_queryfields import QueryFieldsMixin
from collections import OrderedDict
from rest_framework.relations import PKOnlyObject

class TecnicalDataSubSerializer(QueryFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = models.TecnicalDataSub
        exclude = ('id','sarh',)

class TecnicalDataSupSerializer(QueryFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = models.TecnicalDataSup
        exclude = ('id','sarh',)

class SARHListSerializer(serializers.ListSerializer):
    def is_valid(self,raise_exception=False):
        if not hasattr(self, '_validated_data'):
            self._validated_data = self.initial_data
            self._errors = {}
        return True

    def create(self, validated_data):
        ret = []
        for data_dict in validated_data:
            sarh_id = data_dict.get('sarh_id')
            sub_list = data_dict.pop('tecnical_sub', None)
            sup_list = data_dict.pop('tecnical_sup', None)

            if not sarh_id:
                ret.append({'ignorado':{'no_identificable':'No se proporcionaron todos los campos necesarios para identificar la instancia de manera única.'}})
                continue
            qs = models.SARH.objects.filter(sarh_id=sarh_id)
            if qs.count() > 0:
                sarh = qs[0]
                qs.update(**data_dict)
                ret_key = 'actualizado'
            else:
                sarh = models.SARH.objects.create(**data_dict)
                ret_key = 'creado'
            if sub_list:
                models.TecnicalDataSub.objects.filter(sarh=sarh).delete()
                for sub_data in sub_list:
                    if sub_data.get('sarh'):
                        del sub_data['sarh']
                    models.TecnicalDataSub.objects.create(sarh=sarh,**sub_data)
            if sup_list:
                models.TecnicalDataSup.objects.filter(sarh=sarh).delete()
                for sup_data in sup_list:
                    if sup_data.get('sarh'):
                        del sup_data['sarh']
                    models.TecnicalDataSup.objects.create(sarh=sarh,**sup_data)
            ret.append({ret_key: data_dict})
        return ret


class SARHSerializer(QueryFieldsMixin, serializers.ModelSerializer):
    epsa = serializers.CharField(allow_blank=True,required=False)
    tecnical_sub = TecnicalDataSubSerializer(required=False,many=True)
    tecnical_sup = TecnicalDataSupSerializer(required=False,many=True)

    class Meta:
        model = models.SARH
        fields = '__all__'
        list_serializer_class = SARHListSerializer

    def create(self, validated_data):
        epsa_code = validated_data.pop('epsa',None)
        sub_list = validated_data.pop('tecnical_sub', None)
        sup_list = validated_data.pop('tecnical_sup', None)

        if epsa_code:
            epsa_tuple = EPSA.objects.get_or_create(code=epsa_code)
            sarh = models.SARH.objects.create(epsa=epsa_tuple[0], **validated_data)
        else:
            sarh = models.SARH.objects.create(**validated_data)

        if sub_list is not None:
            for sub_data in sub_list:
                models.TecnicalDataSub.objects.create(sarh=sarh,**sub_data)
        if sup_list is not None:
            for sup_data in sup_list:
                models.TecnicalDataSup.objects.create(sarh=sarh,**sup_data)

        return sarh

    def to_representation(self, instance):
        ret = OrderedDict()
        fields = self._readable_fields

        for field in fields:
            try:
                attribute = field.get_attribute(instance)
            except SkipField:
                continue

            if attribute in [None, '', []]:
                continue

            check_for_none = attribute.pk if isinstance(attribute, PKOnlyObject) else attribute
            if check_for_none is None:
                ret[field.field_name] = None
            else:
                ret[field.field_name] = field.to_representation(attribute)

        return ret