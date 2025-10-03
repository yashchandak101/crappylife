from rest_framework import viewsets, permissions
from .models import Article, Category, Tag
from .serializers import ArticleSerializer, CategorySerializer, TagSerializer
from rest_framework.decorators import action
from rest_framework.response import Response



from django.shortcuts import get_object_or_404

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all().order_by("-published_at")
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    @action(detail=False, methods=["get"])
    def featured(self, request):
        featured_articles = Article.objects.filter(is_featured=True).order_by("-published_at")
        serializer = self.get_serializer(featured_articles, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="by-category/(?P<slug>[^/.]+)")
    def by_category(self, request, slug=None):
        category = get_object_or_404(Category, slug=slug)
        articles = Article.objects.filter(category=category).order_by("-published_at")
        serializer = self.get_serializer(articles, many=True)
        return Response(serializer.data)
    
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
