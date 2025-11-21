from datetime import timedelta

from django.db.models import OuterRef, Subquery, Q
from django.shortcuts import render
from django.utils import timezone
from django.core.paginator import Paginator
from django.utils.timesince import timesince

from .models import Customer, Interaction


def customer_list(request):
    queryset_clientes = Customer.objects.select_related('company', 'sales_rep')

    subquery_ultima_fecha = (
        Interaction.objects
        .filter(customer=OuterRef('pk'))
        .order_by('-timestamp')
        .values('timestamp')[:1]
    )
    subquery_ultimo_tipo = (
        Interaction.objects
        .filter(customer=OuterRef('pk'))
        .order_by('-timestamp')
        .values('interaction_type')[:1]
    )
    
    queryset_clientes = queryset_clientes.annotate(
        fecha_ultima_interaccion=Subquery(subquery_ultima_fecha),
        tipo_ultima_interaccion=Subquery(subquery_ultimo_tipo)
    )

    busqueda = request.GET.get('q')
    if busqueda:
        queryset_clientes = queryset_clientes.filter(
            Q(first_name__icontains=busqueda) | 
            Q(last_name__icontains=busqueda) | 
            Q(company__name__icontains=busqueda)
        )

    filtro_cumpleanos = request.GET.get('birthday')
    if filtro_cumpleanos == 'this_week':
        hoy = timezone.now().date()
        dias_semana = [hoy + timedelta(days=i) for i in range(7)]
        pares_mes_dia = [(dia.month, dia.day) for dia in dias_semana]
        
        filtro_q = Q()
        for mes, dia in pares_mes_dia:
            filtro_q |= Q(birthday__month=mes, birthday__day=dia)
        queryset_clientes = queryset_clientes.filter(filtro_q)

    orden = request.GET.get('sort', 'name')
    if orden == 'name':
        queryset_clientes = queryset_clientes.order_by('first_name', 'last_name')
    elif orden == 'company':
        queryset_clientes = queryset_clientes.order_by('company__name')
    elif orden == 'birthday':
        queryset_clientes = queryset_clientes.order_by('birthday')
    elif orden == 'last_interaction':
        queryset_clientes = queryset_clientes.order_by('-fecha_ultima_interaccion')

    paginador = Paginator(queryset_clientes, 25)
    numero_pagina = request.GET.get('page')
    pagina = paginador.get_page(numero_pagina)

    for cliente in pagina:
        cliente.nombre_completo = cliente.full_name
        
        cliente.nombre_empresa = cliente.company.name if cliente.company else 'Sin compañía'

        if cliente.birthday:
            meses_espanol = {
                1: 'enero', 2: 'febrero', 3: 'marzo', 4: 'abril',
                5: 'mayo', 6: 'junio', 7: 'julio', 8: 'agosto',
                9: 'septiembre', 10: 'octubre', 11: 'noviembre', 12: 'diciembre'
            }
            dia = cliente.birthday.day
            mes = meses_espanol[cliente.birthday.month]
            cliente.cumpleanos_formateado = f"{dia} de {mes}"
        else:
            cliente.cumpleanos_formateado = 'Sin fecha'
        
        if cliente.fecha_ultima_interaccion and cliente.tipo_ultima_interaccion:
            tiempo_transcurrido = timesince(cliente.fecha_ultima_interaccion, timezone.now())
            tipo_interaccion = cliente.tipo_ultima_interaccion
            cliente.ultima_interaccion_formateada = f"hace {tiempo_transcurrido} ({tipo_interaccion})"
        else:
            cliente.ultima_interaccion_formateada = 'Sin interacciones'

    contexto = {
        'page_obj': pagina,
        'request': request,
    }

    return render(request, 'crm/customer_list.html', contexto)
