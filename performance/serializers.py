from rest_framework import serializers
from collections import OrderedDict
from rest_framework.relations import PKOnlyObject
from drf_queryfields import QueryFieldsMixin
from performance.models import EPSA, Variable, Indicator, VariableReport, IndicatorMeasurement

class CustomModelSerializer(QueryFieldsMixin,serializers.ModelSerializer):
    def to_representation(self,instance):
        fields = self._readable_fields
        ret = OrderedDict()
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

class CustomListModelSerializer(serializers.ListSerializer):
    def is_valid(self,raise_exception=False):
        if not hasattr(self, '_validated_data'):
            self._validated_data = self.initial_data
            self._errors = {}
        return True

def bulk_create_or_update(model,data,unique_together=[]):
    ret = []
    for props in data:
        if not set(unique_together) <= set(props.keys()):
            ret.append({'ignorado':{'no_identificable':'No se proporcionaron todos los campos necesarios para identificar la instancia de manera única.'}})
            continue
        key_vals = [props.get(key_prop) for key_prop in unique_together]
        if not any(key_vals):
            ret.append({'ignorado':{'objeto_en_blanco':'Todas las propiedades clave de este objeto estan en blanco.'}})
            continue
        qs = model.objects.filter(**{k:v for k,v in zip(unique_together,key_vals)})
        if qs.count() > 0:
            qs.update(**props)
            ret_key = 'actualizado'
        else:
            e,created = model.objects.get_or_create(**props)
            if created:
                ret_key = 'creado'
            else:
                ret_key = 'ignorado'
        ret.append({ret_key: props})
    return ret

class EPSAListSerializer(CustomListModelSerializer):
    def create(self, validated_data):
        unique_together = ['code',]
        return bulk_create_or_update(EPSA,validated_data,unique_together)
class EPSASerializer(CustomModelSerializer):
    class Meta:
        model = EPSA
        fields = '__all__'
        list_serializer_class = EPSAListSerializer

class VariableListSerializer(CustomListModelSerializer):
    def create(self, validated_data):
        unique_together = ['code',]
        return bulk_create_or_update(Variable,validated_data,unique_together)
class VariableSerializer(CustomModelSerializer):
    class Meta:
        model = Variable
        fields = '__all__'
        list_serializer_class = VariableListSerializer

class IndicatorListSerializer(CustomListModelSerializer):
    def create(self, validated_data):
        unique_together = ['code',]
        return bulk_create_or_update(Indicator,validated_data,unique_together)
class IndicatorSerializer(QueryFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Indicator
        fields = '__all__'
        list_serializer_class = IndicatorListSerializer

class VariableReportListSerializer(CustomListModelSerializer):
    def create(self, validated_data):
        unique_together = ['epsa','year','month',]
        return bulk_create_or_update(VariableReport,validated_data,unique_together)
class VariableReportSerializer(QueryFieldsMixin, serializers.ModelSerializer):
    # epsa = serializers.CharField(allow_blank=True,required=False)
    class Meta:
        model = VariableReport
        fields = '__all__'
        list_serializer_class = VariableReportListSerializer
    # def create(self, validated_data):
    #     epsa_code = validated_data.pop('epsa',None)

    #     if epsa_code:
    #         epsa_tuple = EPSA.objects.get_or_create(code=epsa_code)
    #         measurement = IndicatorMeasurement.objects.create(epsa=epsa_tuple[0], **validated_data)
    #     else:
    #         measurement = IndicatorMeasurement.objects.create(**validated_data)

    #     return measurement

class IndicatorMeasurementListSerializer(CustomListModelSerializer):
    def create(self, validated_data):
        unique_together = ['epsa','year','month',]
        return bulk_create_or_update(IndicatorMeasurement,validated_data,unique_together)
class IndicatorMeasurementSerializer(QueryFieldsMixin, serializers.ModelSerializer):
    # epsa = serializers.CharField(allow_blank=True,required=False)
    class Meta:
        model = IndicatorMeasurement
        fields = '__all__'
        list_serializer_class = IndicatorMeasurementListSerializer
    
    # def create(self, validated_data):
    #     epsa_code = validated_data.pop('epsa',None)

    #     if epsa_code:
    #         epsa_tuple = EPSA.objects.get_or_create(code=epsa_code)
    #         measurement = IndicatorMeasurement.objects.create(epsa=epsa_tuple[0], **validated_data)
    #     else:
    #         measurement = IndicatorMeasurement.objects.create(**validated_data)

    #     return measurement
    

