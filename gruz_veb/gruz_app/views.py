from django.shortcuts import render, redirect, get_object_or_404
from .models import Route, Request, Cargo, User, Transport, Status, Role, TransportType
from .forms import RouteForm, RequestFormSet
from django.db import transaction

def index(request):
    return render(request, 'index.html')

def admin_transport_list(request):
    transports = Transport.objects.select_related('transport_type').order_by('id')
    
    context = {
        'transports': transports
    }
    return render(request, 'admin/transport_list.html', context)

def admin_transport_create(request):
    """Создание нового транспорта"""
    if request.method == 'POST':
        brand = request.POST.get('brand')
        model = request.POST.get('model')
        transport_type_id = request.POST.get('transport_type')
        transport_number = request.POST.get('transport_number')
        capacity = request.POST.get('capacity')
        
        # Получаем объект типа транспорта
        t_type = get_object_or_404(TransportType, id=transport_type_id)
        
        # Создаем запись
        Transport.objects.create(
            brand=brand,
            model=model,
            transport_type=t_type,
            transport_number=transport_number,
            capacity=capacity
        )
        return redirect('admin_transport_list')
    
    # GET запрос: показываем пустую форму
    transport_types = TransportType.objects.all()
    return render(request, 'admin/transport_form.html', {'transport_types': transport_types})

def admin_transport_edit(request, pk):
    """Редактирование транспорта"""
    transport = get_object_or_404(Transport, pk=pk)
    
    if request.method == 'POST':
        transport.brand = request.POST.get('brand')
        transport.model = request.POST.get('model')
        transport_type_id = request.POST.get('transport_type')
        transport.transport_number = request.POST.get('transport_number')
        transport.capacity = request.POST.get('capacity')
        
        t_type = get_object_or_404(TransportType, id=transport_type_id)
        transport.transport_type = t_type
        
        transport.save()
        return redirect('admin_transport_list')
    
    # GET запрос: показываем форму с данными
    transport_types = TransportType.objects.all()
    return render(request, 'admin/transport_form.html', {
        'transport': transport,
        'transport_types': transport_types
    })

def admin_transport_delete(request, pk):
    transport = get_object_or_404(Transport, pk=pk)
    transport.delete()
    return redirect('admin_transport_list')

def admin_type_list(request):
    """Список всех типов транспорта"""
    types = TransportType.objects.order_by('name')
    return render(request, 'admin/type_list.html', {'types': types})

def admin_type_create(request):
    """Создание нового типа"""
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            TransportType.objects.create(name=name)
            return redirect('admin_type_list')
    return render(request, 'admin/type_form.html')

def admin_type_edit(request, pk):
    """Редактирование типа"""
    t_type = get_object_or_404(TransportType, pk=pk)
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            t_type.name = name
            t_type.save()
            return redirect('admin_type_list')
    return render(request, 'admin/type_form.html', {'type': t_type})

def admin_type_delete(request, pk):
    """Удаление типа"""
    t_type = get_object_or_404(TransportType, pk=pk)
    # Проверка: нельзя удалить тип, если есть машины этого типа
    if t_type.transports.exists():
        # В реальном проекте лучше вернуть ошибку или сообщение
        return render(request, 'admin/type_error.html', {
            'message': f'Нельзя удалить тип "{t_type.name}", так как есть транспортные средства, использующие его.'
        })
    
    t_type.delete()
    return redirect('admin_type_list')

def admin_user_list(request):
    users = User.objects.select_related('role').order_by('surname')
    return render(request, 'admin/user_list.html', {'users': users})

def admin_user_create(request):
    if request.method == 'POST':
        surname = request.POST.get('surname')
        first_name = request.POST.get('first_name')
        patronymic = request.POST.get('patronymic')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        role_id = request.POST.get('role')
        
        role = get_object_or_404(Role, id=role_id)
        User.objects.create(
            surname=surname, first_name=first_name, patronymic=patronymic,
            phone=phone, address=address, role=role
        )
        return redirect('admin_user_list')
    
    roles = Role.objects.all()
    return render(request, 'admin/user_form.html', {'roles': roles})

def admin_user_edit(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.surname = request.POST.get('surname')
        user.first_name = request.POST.get('first_name')
        user.patronymic = request.POST.get('patronymic')
        user.phone = request.POST.get('phone')
        user.address = request.POST.get('address')
        role_id = request.POST.get('role')
        
        role = get_object_or_404(Role, id=role_id)
        user.role = role
        user.save()
        return redirect('admin_user_list')
    
    roles = Role.objects.all()
    return render(request, 'admin/user_form.html', {'user': user, 'roles': roles})

def admin_user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    # Проверка: нельзя удалить, если есть активные маршруты (опционально)
    # if user.driver_routes.exists() or user.client_routes.exists(): ...
    user.delete()
    return redirect('admin_user_list')

# =========================================================
# ГРУЗЫ
# =========================================================

def admin_cargo_list(request):
    cargos = Cargo.objects.order_by('name')
    return render(request, 'admin/cargo_list.html', {'cargos': cargos})

def admin_cargo_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        weight = request.POST.get('weight')
        volume = request.POST.get('volume')
        
        Cargo.objects.create(name=name, weight=weight, volume=volume)
        return redirect('admin_cargo_list')
    
    return render(request, 'admin/cargo_form.html')

def admin_cargo_edit(request, pk):
    cargo = get_object_or_404(Cargo, pk=pk)
    if request.method == 'POST':
        cargo.name = request.POST.get('name')
        cargo.weight = request.POST.get('weight')
        cargo.volume = request.POST.get('volume')
        cargo.save()
        return redirect('admin_cargo_list')
    
    return render(request, 'admin/cargo_form.html', {'cargo': cargo})

def admin_cargo_delete(request, pk):
    cargo = get_object_or_404(Cargo, pk=pk)
    cargo.delete()
    return redirect('admin_cargo_list')


def admin_role_list(request):
    """Список всех ролей"""
    roles = Role.objects.order_by('name')
    return render(request, 'admin/role_list.html', {'roles': roles})

def admin_role_create(request):
    """Создание новой роли"""
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            Role.objects.create(name=name)
            return redirect('admin_role_list')
    return render(request, 'admin/role_form.html')

def admin_role_edit(request, pk):
    """Редактирование роли"""
    role = get_object_or_404(Role, pk=pk)
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            role.name = name
            role.save()
            return redirect('admin_role_list')
    return render(request, 'admin/role_form.html', {'role': role})

def admin_role_delete(request, pk):
    """Удаление роли"""
    role = get_object_or_404(Role, pk=pk)
    
    # Проверка: нельзя удалить роль, если есть пользователи с этой ролью
    # Связь в модели User: role = ForeignKey(Role, related_name='users')
    if role.users.exists():
        return render(request, 'admin/role_error.html', {
            'message': f'Нельзя удалить роль "{role.name}", так как есть пользователи, назначенные на эту роль.'
        })
    
    role.delete()
    return redirect('admin_role_list')
    
def route_list(request):
    """Публичный список маршрутов (без боковой панели админки)"""
    routes = Route.objects.select_related('driver', 'client', 'transport', 'status').order_by('-departure_date')
    return render(request, 'routes/route_list.html', {'routes': routes})

def route_create(request):
    if request.method == 'POST':
        route_form = RouteForm(request.POST)
        formset = RequestFormSet(request.POST)
        
        if route_form.is_valid() and formset.is_valid():
            with transaction.atomic():
                # 1. Сохраняем основной маршрут
                route = route_form.save()
                
                # 2. Проходим по формам грузов и сохраняем их вручную
                for form in formset:
                    if form.cleaned_data: # Если форма не пустая
                        # Проверка на удаление (если галочка стоит)
                        if form.cleaned_data.get('DELETE'):
                            continue
                        
                        # Создаем объект Request
                        request_obj = form.save(commit=False)
                        request_obj.route = route # ВРУЧНУЮ привязываем к маршруту
                        request_obj.save()
            
            return redirect('route_detail', pk=route.id)
    else:
        route_form = RouteForm()
        formset = RequestFormSet()
    
    return render(request, 'routes/route_form.html', {
        'route_form': route_form,
        'formset': formset,
        'title': 'Новый маршрут'
    })

def route_detail(request, pk):
    """Детали маршрута"""
    route = get_object_or_404(Route.objects.select_related('driver', 'client', 'transport', 'status'), pk=pk)
    requests = route.requests.select_related('cargo').all()
    return render(request, 'routes/route_detail.html', {'route': route, 'requests': requests})

def route_edit(request, pk):
    route = get_object_or_404(Route, pk=pk)
    
    if request.method == 'POST':
        route_form = RouteForm(request.POST, instance=route)
        formset = RequestFormSet(request.POST)
        
        if route_form.is_valid() and formset.is_valid():
            with transaction.atomic():
                # 1. Сохраняем изменения маршрута
                route = route_form.save()
                
                # 2. Удаляем старые грузы, которые помечены на удаление или отсутствуют в новой форме
                # Простой подход: удаляем все текущие грузы этого маршрута и создаем новые из формы
                # (Это проще и надежнее для старой версии Django, чем синхронизация ID)
                route.requests.all().delete()
                
                # 3. Создаем новые записи грузов
                for form in formset:
                    if form.cleaned_data:
                        if form.cleaned_data.get('DELETE'):
                            continue
                        
                        request_obj = form.save(commit=False)
                        request_obj.route = route
                        request_obj.save()
            
            return redirect('route_detail', pk=route.id)
    else:
        route_form = RouteForm(instance=route)
        # При редактировании заполняем формсет существующими грузами
        initial_data = []
        for req in route.requests.all():
            initial_data.append({
                'cargo': req.cargo.id,
                'quantity': req.quantity,
            })
        formset = RequestFormSet(initial=initial_data)
    
    return render(request, 'routes/route_form.html', {
        'route_form': route_form,
        'formset': formset,
        'title': 'Редактирование маршрута',
        'route': route
    })


def route_delete(request, pk):
    """Удаление маршрута"""
    route = get_object_or_404(Route, pk=pk)
    if request.method == 'POST':
        route.delete()
        return redirect('route_list')
    return render(request, 'routes/route_confirm_delete.html', {'route': route})