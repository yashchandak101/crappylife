from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from articles.models import Article
from events.models import Event
from .serializers import ArticleSearchSerializer, EventSearchSerializer

class SearchView(APIView):
    def get(self, request):
        query = request.GET.get("q", "")
        category = request.GET.get("category", "")
        tag = request.GET.get("tag", "")

        articles = Article.objects.all()
        events = Event.objects.all()

        if query:
            articles = articles.filter(title__icontains=query) | articles.filter(content__icontains=query)
            events = events.filter(title__icontains=query) | events.filter(description__icontains=query)

        if category:
            articles = articles.filter(category__slug=category)

        if tag:
            articles = articles.filter(tags__slug=tag)

        articles = ArticleSearchSerializer(articles.distinct(), many=True).data
        events = EventSearchSerializer(events.distinct(), many=True).data

        return Response({
            "articles": articles,
            "events": events
        }, status=status.HTTP_200_OK)
