from django.shortcuts import render, redirect
from django.contrib.auth.models import User

def cadastro(request):
    if request.method == 'GET':
        return render(request, 'cadastro.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        confirma_senha = request.POST.get('confirma_senha')

        if not senha == confirma_senha:
            return redirect('/usuarios/cadastro')
        
        user = User.objects.filter(username=username)

        if user.exists():
            return redirect('/usuarios/cadastro')

        try:
            User.objects.create_user(
                username=username,
                password=senha
            )
            return redirect('/usuarios/login')
        except:
            return redirect('/usuarios/cadastro')
