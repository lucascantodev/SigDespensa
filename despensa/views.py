# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Despensa
from core.models import Usuario
from .forms import DespensaForm
from django.views.decorators.http import require_safe, require_POST, require_http_methods
from django.contrib.auth.decorators import login_required

@login_required
@require_safe
def despensa_list(request):
    despensas = Despensa.objects.all()

    rendered_page = render(request, 'despensa/list.html', {'despensas': despensas})

    return HttpResponse(rendered_page)

@login_required
@require_safe
def despensa_detail(request, id):
    despensa = get_object_or_404(Despensa, id=id)

    rendered_page = render(request, 'despensa/detail.html', {'despensa': despensa})

    return HttpResponse(rendered_page)

@login_required
@require_POST
def despensa_create(request):
    nome = request.POST.get('nome')
    quantTotal = request.POST.get('quantTotal')
    capacidade = request.POST.get('capacidade')

    # testar se funciona: Cadastrar despensa para o usuário atual     
    # usuario = Usuario.objects.get(username=request.user.username)
    # Despensa.objects.create(nome=nome, quantTotal=quantTotal, capacidade=capacidade, usuarios=usuario)
    
    Despensa.objects.create(nome=nome, quantTotal=quantTotal, capacidade=capacidade)
    return redirect('despensas:despensa_list')

#@require_POST
#def despensa_create(request):

    despensa_form = DespensaForm(request.POST)

    if despensa_form.is_valid():
        cleaned_data_despensa = despensa_form.cleaned_data

        nome = cleaned_data_despensa.get('nome')
        quantTotal = cleaned_data_despensa.get('quantTotal')
        capacidade = cleaned_data_despensa.get('capacidade')

        Despensa.objects.despensa_create(nome=nome,
                                quantTotal=quantTotal,
                                capacidade=capacidade,)

        rendered_page = render(request, 'users/index.html', {"usuario_form": DespensaForm()})
        return HttpResponse(rendered_page)
    else:
        print(despensa_form.errors)
        rendered_page = render(request, 'users/index.html', {"usuario_form": DespensaForm(), "errors": despensa_form.errors})
        return HttpResponse(rendered_page)

@login_required
@require_safe
def despensa_update(request, id):
    despensa = Despensa.objects.get(id=id)

    rendered_page = render(request, 'despensa/update.html', {'form': DespensaForm(), 'despensa': despensa})
    return HttpResponse(rendered_page)

@login_required
@require_POST
def update(request, id):

    form = DespensaForm(request.POST)
    despensa = Despensa.objects.get(id=id)

    if form.is_valid():
        cleaned_data = form.cleaned_data

        nome = cleaned_data.get('nome')
        quantTotal = cleaned_data.get('quantTotal')
        capacidade = cleaned_data.get('capacidade')

        despensa.nome = nome
        despensa.quantTotal = quantTotal
        despensa.capacidade = capacidade
        despensa.save()

        return redirect('despensas:despensa_list')
    else:

        rendered_page = render(request, 'despensa/update.html', {'form': DespensaForm(), 'despensa': despensa})
        return HttpResponse(rendered_page)

@login_required
@require_safe
def despensa_delete(request, id):
    despensa = Despensa.objects.get(id=id)
    despensa.delete()
    return redirect('despensas:despensa_list')

@login_required
@require_safe
def despensa_form(request):
    rendered_page = render(request, 'despensa/form.html', {"form": DespensaForm()})
    return HttpResponse(rendered_page)
