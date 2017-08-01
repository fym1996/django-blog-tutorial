
from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post

from .models import Comment
from .forms import CommentForm

def post_comment(request,post_pk):
    #首先获取被评论的文章，因为后面需要把评论和被评论的文章关联起来
    #使用Django提供的快捷函数get_object_or_404,其作用是当获取的文章存在时，则获取，否则返回404页面给用户
    post = get_object_or_404(Post,pk=post_pk)

    if request.method == 'POST':
        #用户提交的数据存在request.POST中，这是一个类字典对象
        #我们利用这些数据构造了CommentForm的实例，这样Django的表单就生成了
        form = CommentForm(request.POST)

        if form.is_valid():
            #检查到数据时合法的，调用表单的save方法保存数据到数据库
            #commit=False的作用是仅仅利用表单的数据生成Comment模型类的实例，但还不保存评论数据到数据库
            comment = form.save(commit=False)

            #将评论和被评论的文章关联起来
            comment.post = post

            #最终将评论数据保存到数据库，调用模型实例的save方法
            comment.save()

            #重定向到post的详情页
            #然后重定向到get_absolute_url方法返回的URL

            return redirect(post)
        else:
            #检查到数据不合法，重新渲染详情页，并且渲染表单的错误
            #post.comment_set.all()方法，其作用是获取这篇post的全部评论，这个用法类似于Post.objects.all()
            comment_list = post.commet_set.all()
            context  = {
                'post':post,
                'form':form,
                'comment_list':comment_list
            }
            return render(request,'blog/detail.html',context=context)
        #不是post请求，说明用户没有提交数据，重定向到文章详情页。
        return redirect(post)




