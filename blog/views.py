from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post, Answer, Qvote, Avote
from .bad_words import isBad
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from oauth2_provider.views.generic import ProtectedResourceView
from django.http import HttpResponse

def home(request):
    context ={
        'posts': Post.objects.all()

    }
    return render(request, 'blog/home.html', context)

class ApiEndpoint(APIView):


    def get(self, request):
        taglist = request.data['tags']
        taglist = taglist.split(';')

        questions = Post.objects.all()
        qlist = []
        for question in questions:
            tags = question.tags
            if tags:
                tags = tags.split(',')
                temp = []
                for tag in tags:
                    if tag in taglist:
                        temp.append({
                            'title': question.title,
                            'content': question.content
                        })
                        qlist += (temp)
                        break
        return Response(qlist)

    def post(self, request):

        username = request.data['username']
        title = request.data['title']
        content = request.data['content']
        tags = request.data['tags']

        prof = User.objects.get(username=username)
        prof = prof.id

        new_post = Post(title=title, content=content, tags=tags, author_id=prof)
        new_post.save()
        content = {'message': 'Question posted'}
        return Response(content)
class RestView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        taglist = request.data['tags']
        taglist = taglist.split(';')

        questions = Post.objects.all()
        qlist = []
        for question in questions:
            tags = question.tags
            if tags:
                tags = tags.split(',')
                temp = []
                for tag in tags:
                    if tag in taglist:

                        temp.append({
                            'title': question.title,
                            'content': question.content
                        })
                        qlist+=(temp)
                        break
        return Response(qlist)
    def post(self, request):

        username = request.data['username']
        title = request.data['title']
        content = request.data['content']
        tags = request.data['tags']

        prof = User.objects.get(username=username)
        prof = prof.id

        new_post = Post(title=title, content= content, tags= tags, author_id=prof)
        new_post.save()
        content = {'message': 'Question posted'}
        return Response(content)


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']

def upvote(request, *args, **kwargs):
    new_vote = Qvote(votes =1, author_id =request.user.id,question_id=kwargs['pk']  )
    new_vote.save()
    return redirect(request.META['HTTP_REFERER'])

def downvote(request, *args, **kwargs):
    new_vote = Qvote(votes =-1, author_id =request.user.id,question_id=kwargs['pk']  )
    new_vote.save()
    return redirect(request.META['HTTP_REFERER'])
def PostDetail(request, *args, **kwargs):


    if request.POST:
        if 'found' in request.POST:
            ques = Post.objects.get(id =kwargs['pk'] )
            ques.read = 1;

            ques.save()
        else:



            user = request.user.id
            cont = request.POST['answer']
            if not isBad((cont)):
                new_ans = Answer(content=cont, author_id = user, question_id=kwargs['pk'])
                new_ans.save()
    try:
        ans = Answer.objects.filter(question_id=kwargs['pk'])


    except:
        ans = None

    votelist = Qvote.objects.filter(question_id =kwargs['pk'] )
    done = Qvote.objects.filter(question_id=kwargs['pk'], author_id=request.user.id)

    voted =1

    if not done:
        voted = 0

    totvote = 0
    for vote in votelist:
        totvote = totvote + vote.votes


    context = {
        'object': Post.objects.get(id =kwargs['pk'] ),
        'answers': ans,
        'vote': totvote,
        'voted': voted
    }
    return render(request, 'blog/post_detail.html', context)




class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):

    model = Post
    fields = ['title', 'content', 'tags']

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})
