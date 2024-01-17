from django.shortcuts import render, redirect

def novo_flashcard(request):
    if not request.user.is_authenticated:
        return redirect('/usuarios/logar')
    
    if request.method == 'GET':
        return render(
            request,
            'novo_flashcard.html'
        )