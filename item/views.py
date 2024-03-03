from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.db.models import Q
from django.http import HttpResponseBadRequest

from .models import Article, Category, Comment
from .forms import NewArticleForm, CommentForm, CategoryForm


def index(request):
    articles = Article.objects.all().order_by("-created_at")[0:6]
    categories = Category.objects.all()
    ctx = {"articles": articles, "categories": categories}
    return render(request, "item/index.html", ctx)



class NewArticle(LoginRequiredMixin, View):
    def get(self, request):
        article_form = NewArticleForm()
        category_form = CategoryForm()
        ctx = {"form": article_form, 
               "category_form": category_form,
               "title": "New Article"}
        return render(request, "item/new.html", ctx)

    def post(self, request):
        article_form = NewArticleForm(request.POST, request.FILES)
        category_form = CategoryForm(request.POST)

        if not article_form.is_valid() and not category_form.is_valid():
            ctx = {"article_form": article_form, 
               "category_form": category_form,
               "title": "New Article"}
            return render(request, "item/new.html", ctx)

        category = category_form.save()

        article = article_form.save(commit=False)
        article.category = category
        article.author = request.user
        article.save()

        return redirect("item:detail", pk=article.id)


class ArticleDetail(View):
    template_name = "item/detail.html"

    def get(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        related_articles = Article.objects.filter(category=article.category).exclude(
            pk=pk
        )[0:4]
        comment_form = CommentForm()
        comments = Comment.objects.filter(article=article).order_by("-updated_at")

        context = {
            "article": article,
            "related_articles": related_articles,
            "comment_form": comment_form,
            "comments": comments,
        }

        return render(request, self.template_name, context)


class ArticleUpdateView(LoginRequiredMixin, View):
    model = Article
    template = "item/article_Update_form.html"

    def get(self, request, pk):
        article = get_object_or_404(self.model, pk=pk, author=request.user)
        form = NewArticleForm(instance=article)
        ctx = {"form": form}
        return render(request, self.template, ctx)

    def post(self, request, pk):
        article = get_object_or_404(self.model, pk=pk, author=request.user)
        form = NewArticleForm(request.POST, request.FILES, instance=article)

        if not form.is_valid():
            ctx = {"form": form}
            return render(request, self.template, ctx)

        form.save()

        return redirect("item:detail", pk=article.id)


class ArticleDeleteView(LoginRequiredMixin, View):
    model = Article
    template = "item/article_delete.html"

    def get(self, request, pk):
        article = get_object_or_404(self.model, pk=pk, author=request.user)
        form = NewArticleForm(instance=article)
        ctx = {"form": form, "article": article}

        return render(request, self.template, ctx)

    def post(self, request, pk):
        article = get_object_or_404(self.model, pk=pk, author=request.user)
        article.delete()
        return redirect("item:index")


class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        # print(request.POST)
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.article = article
            comment.created_by = request.user
            comment.save()
            return redirect("item:detail", pk=article.id)
        else:
            return HttpResponseBadRequest("Invalid form data")


class BrowseView(View):
    def get(self, request):
        query = request.GET.get("query", "")
        category_id = request.GET.get("category", 0)
        categories = Category.objects.all()
        articles = Article.objects.all()

        if category_id:
            articles = articles.filter(category_id=category_id)

        if query:
            articles = articles.filter(
                Q(topic__icontains=query) | Q(content__icontains=query)
            )

        ctx = {
            "articles": articles,
            "query": query,
            "categories": categories,
            "category_id": int(category_id),
        }

        return render(request, "item/browse.html", ctx)
