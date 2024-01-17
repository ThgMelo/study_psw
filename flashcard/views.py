from django.shortcuts import render, redirect
from .models import Categoria
from .models import Flashcard

def novo_flashcard(request):
    if not request.user.is_authenticated:
        return redirect('/usuarios/logar')
    
    if request.method == 'GET':
        categorias = Categoria.objects.all()
        dificuldades = Flashcard.DIFICULDADE_CHOICES

        return render(
            request,
            'novo_flashcard.html',
            {
                'categorias': categorias,
                'dificuldades': dificuldades,
            }
        )