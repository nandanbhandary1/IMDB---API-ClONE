from rest_framework import serializers

from watchlist_app.models import WatchList, StreamPlatform, Review


class ReviewSerializer(serializers.ModelSerializer):
# You declare review_user separately because you want to change how the ForeignKey is represented in the API response.
    review_user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Review
        # fields = '__all__'
        exclude = ('whatslist',)

"""model serializer"""
class WatchListSerializer(serializers.ModelSerializer):
    # Because of related_name="reviews":
    # reviews =  ReviewSerializer(many=True, read_only=True) # “When serializing a WatchList object, also include all related reviews using ReviewSerializer.” 
    # len_name = serializers.SerializerMethodField()
    # platform = serializers.CharField(source='platform.name', read_only=True) # TO DISPLAY PLATFORM NAME CUZ IT'S A FK, SOURCE AND MENTION TO WHICH MODEL AND WHICH FIELD WE ARE GOING TO TARGET
    platform = serializers.SlugRelatedField(queryset=StreamPlatform.objects.all(),slug_field='name')
    class Meta:
        model = WatchList
        fields = '__all__'
        
        
        #HyperlinkedModelSerializer
class StreamPlatformSerializer(serializers.ModelSerializer):
    watchlist = WatchListSerializer(many=True, read_only=True) # To establish a retation use same related name given in db, it gives u the complete details
    # watchlist = serializers.StringRelatedField(many=True)
    # watchlist = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # watchlist = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='movie-detail')
    # it shows a a particular platfor has how many movies antha
    class Meta:
        model = StreamPlatform
        fields = '__all__'
    
          
    # def get_len_name(self, object):
    #     length = len(object.name)
    #     return length
    
    # def validate_name(self, value):
    #     if len(value) <2:
    #         raise serializers.ValidationError("Name is too short! ")
    #     else:
    #         return value
        
    # def validate(self, data):
    #     if data['name'] == data['description']:
    #         raise serializers.ValidationError("Title and description shoudn't be same")
    #     else:
    #         return data 


""" 
1. serializers.Serializer
"""
# def name_length(value):
#     if len(value)<2:
#         raise serializers.ValidationError("Name is too short!")
    

# class MovieSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)  # can't edit just accessable
#     name = serializers.CharField(validators=[name_length])
#     description = serializers.CharField()
#     active = serializers.BooleanField()


#     def create(self, validated_data):
#         # Create and return a new 'db_name' instance, given the validated data.
#         return WatchList.objects.create(**validated_data)
    
#     def update(self, instance, validated_data): # instance -> old values, validated_data-> new values
#         instance.name = validated_data.get('name', instance.name) # update old instance to new data and pass old data too
#         instance.description = validated_data.get('name', instance.description)
#         instance.active = validated_data.get('name', instance.active)
#         instance.save() # save the instance
#         return instance
    
#     def validate_name(self, value):
#         if len(value) <2:
#             raise serializers.ValidationError("Name is too short! ")
#         else:
#             return value
        
    # def validate(self, data):
    #     if data['name'] == data['description']:
    #         raise serializers.ValidationError("Title and description shoudn't be same")
    #     else:
    #         return data 
        
