from django.shortcuts import render

def novo_flashcard(request):
    if request.method == 'GET':
        return render(
            request,
            'novo_flashcard.html'
        )