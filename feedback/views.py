from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Feedback

# Create your views here.

def contact(request):
    if request.method == 'POST':
        try:
            # 创建新的反馈记录
            feedback = Feedback(
                name=request.POST.get('name'),
                email=request.POST.get('email'),
                feedback_type=request.POST.get('feedback_type'),
                subject=request.POST.get('subject'),
                message=request.POST.get('message')
            )
            feedback.save()

            # 添加成功消息
            messages.success(request, 'Thank you for your feedback! We will get back to you soon.')
            return redirect('contact')

        except Exception as e:
            # 添加错误消息
            messages.error(request, 'An error occurred while submitting your feedback. Please try again.')

    return render(request, 'contact.html')
