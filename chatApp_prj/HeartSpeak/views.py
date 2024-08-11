from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .models import Message
from .forms import MessageForm, SigninForm, SignupForm
from cryptography.fernet import Fernet
from django.conf import settings

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Optionally log in the user after signup
            return redirect('default_chat_view')  # Redirect to a different page after signup
    else:
        form = SignupForm()
    return render(request, 'HeartSpeak/registration/signup.html', {'form': form})


def signin_view(request):
    if request.method == 'POST':
        form = SigninForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('chat_view')  # Redirect to the chat view after successful login
    else:
        form = SigninForm()
    return render(request, 'HeartSpeak/registration/login.html', {'form': form})


@login_required
def chat_view(request, recipient_id=None):
    if recipient_id:
        recipient = User.objects.get(id=recipient_id)
    else:
        recipient = None

    messages = Message.objects.filter(
        sender=request.user,
        recipient=recipient
    ).order_by('timestamp')

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            encrypted_content = settings.cipher_suite.encrypt(content.encode())
            Message.objects.create(
                sender=request.user,
                recipient=recipient,
                encrypted_content=encrypted_content.decode()
            )
            return redirect('chat_view', recipient_id=recipient.id)
    else:
        form = MessageForm()

    decrypted_messages = []
    for message in messages:
        decrypted_content = settings.cipher_suite.decrypt(message.encrypted_content.encode()).decode()
        decrypted_messages.append({
            'sender': message.sender,
            'content': decrypted_content,
            'timestamp': message.timestamp
        })

    return render(request, 'HeartSpeak/chat.html', {
        'messages': decrypted_messages,
        'form': form,
        'recipient': recipient,
    })

from django.shortcuts import render

@login_required
def default_chat_view(request):
    # Logic for the default chat view, e.g., showing a list of available chat recipients
    return render(request, 'HeartSpeak/default_chat.html')  # Create this template to handle the default chat page
