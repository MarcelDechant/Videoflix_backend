from django.conf import settings
from rest_framework import serializers
from content.models import GenreModel, VideoModel


def generate_media_url(request, obj, file_type, file_field):
    """
    Generate a media URL for video files (thumbnail or video).
    """
    if getattr(obj, file_field):
        return f"{request.scheme}://{request.get_host()}{settings.MEDIA_URL}videos/{obj.id}/{file_type}.jpg"
    return None

        
class VideoModelListSerializer(serializers.ModelSerializer):
    
    thumbnail_url = serializers.SerializerMethodField()
    class Meta:
        model = VideoModel
        fields = ['id', 'title', 'description', 'created_at', 'genres', 'thumbnail_url']
        
    def get_thumbnail_url(self, obj):
        """
        Generate and return the thumbnail URL for the video.
        """
        request = self.context.get('request')
        return generate_media_url(request, obj, 'thumbnail', 'thumbnail_img')

class GenreModelSerializer(serializers.ModelSerializer):
    videos = VideoModelListSerializer(many=True, read_only=True)

    class Meta:
        model = GenreModel
        fields = ['id', 'name', 'videos']  
        
        
class VideoModelDetailSerializer(serializers.ModelSerializer):
    
    thumbnail_url = serializers.SerializerMethodField()
    video_url = serializers.SerializerMethodField()
    class Meta:
        model = VideoModel
        fields = ['id', 'title', 'description', 'created_at', 'genres', 'thumbnail_url', 'video_url']
        
    def get_video_url(self, obj):
        """
        Generate the URL for streaming the video.
        """
        request = self.context.get('request')
        if obj.video_file:
            video_url = f"{request.scheme}://{request.get_host()}/api/videos/{obj.id}/stream/"
            return video_url
        return None
    
    def get_thumbnail_url(self, obj):
        """
        Generate and return the thumbnail URL for the video.
        """
        request = self.context.get('request')
        return generate_media_url(request, obj, 'thumbnail', 'thumbnail_img')