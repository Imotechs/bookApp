from django.shortcuts import render,redirect
from . forms import UserRegisterForm
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic import (TemplateView,ListView,View,
                CreateView,DeleteView,DetailView,UpdateView)
from .models import Books, Profile,CheckedBook
from django.db.models import Q
from .functions import get_date_due
from django.contrib.auth.decorators import login_required
from . import mail

# Create your views here.

def register(request):
    if request.method == 'POST':
        if User.objects.filter(email = request.POST['email']):
            context = {
                'msg': 'Email already registered!',
            }
            return render(request,'register.html',context)
        else:
            form = UserRegisterForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username','email')
                messages.success(request, f'{username}, Your account was created!  Login Now')
                return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {"form":form,"title":"User Registration"})

def login(request):
    form = UserRegisterForm()
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request,user)
                messages.info(request,'Welcome!')
                return redirect('profile')
            else:
                msg = {'msg':'Your Account is not active!'}
                return render(request,'login.html', {'msg':msg,'form':form})
        elif user is None:
            context = {
                'msg':'No User with this Credentials!',
                'form':form
            }
                
            return render(request,'login.html', context)

    context = {
                'form':form
            }   
    return render(request,'login.html',context)


def home(request):
    books = Books.objects.all().order_by('-date_added')
    '''   
    we can manually send libraian mails with users interaction as below
    or set a task that execute at intervals cheking the status of checked books
    and send mails to libralians at due time
    '''
    #get list af all books not returned
    checked_book = CheckedBook.objects.filter(has_returned =False)
    #get the curent dade and time
    today = timezone.now()
    for item in checked_book:
        #compare the dates and send mail if is due
        if today >= item.date_due:
            #send a mail to all librarians
            response = mail.send_admin_mail(item)
    context = {
        'books':books
    }
    return render(request,'book/index.html',context)

def search(request):
    search = request.POST.get('search')
    if search is None or search == '':
        messages.info(request,'Cannot use None as a search value')
        return redirect('home')
    books = Books.objects.filter(
            Q(title__icontains=search) | Q(ISBN__icontains=search) | Q(publisher__icontains=search) | Q(date_added__icontains=search) )    
    context = {
        'books':books
    }
    return render(request,'book/search.html',context)

# regular Users views
class UserProfile(LoginRequiredMixin,TemplateView):
    template_name = 'book/profile.html'
    def get_context_data(self, *args, **kwargs):
        context =super(UserProfile,self).get_context_data( *args, **kwargs)
        books = CheckedBook.objects.filter(user = self.request.user,has_returned = False).order_by('-date_checked')
        profile,created = Profile.objects.get_or_create(user = self.request.user)
        profile.save()
        context.update({'books':books})
        return context
    def post(self):
        pass

@login_required
def bookcheckout(request,*args,**kwargs):
    book_id = kwargs.get('id')
    #get the requested book
    book = Books.objects.get(id = book_id)
    #chek if user already owns the book and hasnt returned
    profile,created = Profile.objects.get_or_create(user = request.user)
    if book in profile.books.all():
        #that means he wants to return the book
        checked_book = CheckedBook.objects.get(user = request.user,book = book)
        checked_book.has_returned = True
        checked_book.save()
        #He returned the book so remove it fdrom his profile
        profile.books.remove(book)
        profile.save()
        messages.info(request,'thank you for returning this book')
        return redirect('home')
    else:
        #else create record for his checkings
        new_checked_book = CheckedBook.objects.create(
            user = request.user,
            book = book,
            date_due = get_date_due()[1]
        
        )
        #add the book to his profile
        profile,created= Profile.objects.get_or_create(user = request.user)
        profile.books.add(book)
        profile.save()
        new_checked_book.save()
        messages.info(request,'You now have this book')
        return redirect('profile')


''' Users Edit profile view'''
class EditProfile(LoginRequiredMixin,UpdateView):
    model = Profile 
    fields = ['photo']
    template_name = 'book/eddit_profile.html'
    success_url = '/profile/me/'


#Librarian/admin panel
'''librarian Add book View'''
class AddBook(LoginRequiredMixin,UserPassesTestMixin,CreateView):
    model = Books
    fields = ['title','cover_image','ISBN','revision_number',
            'published_date','publisher','author','genre']
    template_name = 'book/add_books.html'
    success_url = '/store/manager/'
    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()

        form = super(AddBook, self).get_form(form_class)
        form.fields['published_date'].widget.attrs={'placeholder': 'Y-m-d'}
        return form
    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False

'''Librarian View'''
class AdminManageView(LoginRequiredMixin,UserPassesTestMixin,TemplateView):
    template_name = 'book/manage.html'
    def get_context_data(self, *args, **kwargs):
        context =super(AdminManageView,self).get_context_data( *args, **kwargs)
        users =  User.objects.all().order_by('-date_joined')
        books = Books.objects.all().order_by('-date_added')
        context.update({'books':books,'users':users})
        return context
    def test_func(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return True
        return False


'''Librarian View'''
class ADminManageCkeckedBooksView(LoginRequiredMixin,UserPassesTestMixin,TemplateView):
    template_name = 'book/checked_books.html'
    def get_context_data(self, *args, **kwargs):
        context =super(ADminManageCkeckedBooksView,self).get_context_data( *args, **kwargs)
        users =  User.objects.all().order_by('-date_joined')
        books = CheckedBook.objects.filter(has_returned =False).order_by('-date_checked')
        context.update({'books':books,'users':users})
        return context
    def test_func(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return True
        return False

'''Librarian Eddit books  View'''
class AdminEditBooksView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    template_name = 'book/addit_books.html'
    success_url = '/store/manager/'
    fields = ['title','cover_image','ISBN','revision_number',
            'published_date','publisher','author','genre']
    model = Books
    def test_func(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return True
        return False