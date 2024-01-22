from django.shortcuts import render, redirect
from .models import Categoria
from .models import Flashcard
from .models import Desafio, FlashcardDesafio
from django.contrib.messages import constants
from django.contrib import messages

def novo_flashcard(request):
    if not request.user.is_authenticated:
        return redirect('/usuarios/logar')
    
    if request.method == 'GET':
        categorias = Categoria.objects.all()
        dificuldades = Flashcard.DIFICULDADE_CHOICES
        flashcards = Flashcard.objects.filter(user=request.user)

        categoria_filtrar = request.GET.get('categoria')
        dificuldade_filtrar = request.GET.get('dificuldade')

        if categoria_filtrar:
            flashcards = flashcards.filter(categoria__id=categoria_filtrar)

        if dificuldade_filtrar:
            flashcards = flashcards.filter(dificuldade=dificuldade_filtrar)

        return render(
            request,
            'novo_flashcard.html',
            {
                'categorias': categorias,
                'dificuldades': dificuldades,
                'flashcards': flashcards,
            }
        )
    
    if request.method == 'POST':
        pergunta = request.POST.get('pergunta')
        resposta = request.POST.get('resposta')
        categoria = request.POST.get('categoria')
        dificuldade = request.POST.get('dificuldade')

        if len(pergunta.strip()) == 0 or len(resposta.strip()) == 0:
            messages.add_message(
                request,
                constants.ERROR,
                'Preencha os campos de pergunta e resposta',
            )
            return redirect('/flashcard/novo_flashcard')
        
        flashcard = Flashcard(
            user=request.user,
            pergunta=pergunta,
            resposta=resposta,
            categoria_id=categoria,
            dificuldade=dificuldade,
        )

        flashcard.save()

        messages.add_message(
            request, constants.SUCCESS, 'Flashcard cadastrado com sucesso'
        )
        return redirect('/flashcard/novo_flashcard')
    
def deletar_flashcard(request, id):
    flashcard = Flashcard.objects.get(id=id)

    if request.user.id == flashcard.user.id:
        flashcard.delete()
        messages.add_message(
            request, constants.SUCCESS, 'Flashcard deletado com sucesso!'
        )
    else:
        messages.add_message(
            request, constants.ERROR, 'Erro ao deletar o flashcard!'
        )

    return redirect('/flashcard/novo_flashcard')

def iniciar_desafio(request):
    if request.method == 'GET':
        categorias = Categoria.objects.all()
        dificuldades = Flashcard.DIFICULDADE_CHOICES
        return render(request, 'iniciar_desafio.html', {'categorias': categorias, 'dificuldades': dificuldades})
    
    elif request.method == 'POST':
        titulo = request.POST.get('titulo')
        categorias = request.POST.getlist('categoria')
        dificuldade = request.POST.get('dificuldade')
        qtd_perguntas = request.POST.get('qtd_perguntas')

        desafio = Desafio(
            user = request.user,
            titulo=titulo,
            quantidade_perguntas=qtd_perguntas,
            dificuldade=dificuldade
        )
        desafio.save()

        for categoria in categorias:
            desafio.categoria.add(categoria)

        flashcards = (
            Flashcard.objects.filter(user=request.user)
            .filter(dificuldade=dificuldade)
            .filter(categoria_id__in=categorias)
            .order_by('?')
        )

        if flashcards.counts() < int(qtd_perguntas):
            return redirect('/flashcard/iniciar_desafio/')
        
        flashcards = flashcards[:int(qtd_perguntas)]

        for f in flashcards:
            flashcard_desafio = FlashcardDesafio(fashcard=f,)
            flashcard_desafio.save()
            desafio.flashcards.add(flashcard_desafio)

        desafio.save()
        return redirect(f'/flashcard/desafio/{desafio.id}')