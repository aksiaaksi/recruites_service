from django.core.mail import send_mail
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from rservice.forms import RecruitForm, TestForm, ShadowHandForm
from rservice.models import Sith, Recruit, Test


def index(request):
    u"""
    Рендеринг шаблона главной страницы.
    :param request: Запрос клиента.
    :return: Рендеринг шаблона.
    """
    return render(request, 'rservice/index.html')


def sith(request):
    u"""
    Получение списка ситхов и рендеринг шаблона.
    :param request: Запрос клиента.
    :return: Рендеринг шаблона.
    """
    siths = Sith.objects.all()
    context = {'siths': siths}
    return render(request, 'rservice/sith.html', context)


def recruit_list(request, sith_id):
    u"""
    Рендеринг списка рекрутов прошедших тестирование.
    :param request: Запрос клиента.
    :param sith_id: ID ситха, выполняющего отбор рекрутов.
    """

    # реализация поиска по имени рекрута и планете обитания
    search_query = request.GET.get('search', '')

    if search_query:
        recruits = Recruit.objects.filter(Q(name__icontains=search_query) |
                                          Q(planet_habitat__planet_name__icontains=search_query))
    else:
        recruits = Recruit.objects.all()

    # зачисление выбранного рекрута с отправкой письма на Email
    sith = Sith.objects.get(pk=sith_id)
    if request.method == 'POST':
        shf = ShadowHandForm(request.POST, instance=sith)
        if shf.is_valid():
            shf.save()
            context = {'recruits': recruits}
            email = sith.shadow_hand.email
            send_mail('Приглашение!', 'Вы зачислены в Орден ситхов!', 'sith@starwars.com', [email], fail_silently=True)
            return HttpResponseRedirect(reverse('shadow_hand'), context)
        else:
            context = {'form': shf, 'recruits': recruits}
            return render(request, 'rservice/recruit_list.html', context)
    else:
        shf = TestForm()
        context = {'form': shf, 'recruits': recruits}
        return render(request, 'rservice/recruit_list.html', context)


def shadow_hand(request):
    u"""
    Рендеринг шаблона принятых рекрутов.
    :param request: Запрос клиента.
    :return: Рендеринг шаблона.
    """
    return render(request, 'rservice/shadow_hand.html')


def add_and_save(request):
    u"""
    Форма добавления и сохранения данных по новому рекруту.
    :param request: Запрос клиента.
    :return: Рендеринг шаблона.
    """
    if request.method == 'POST':
        recruitf = RecruitForm(request.POST)
        if recruitf.is_valid():
            recruitf.save()
            return HttpResponseRedirect(reverse('test', kwargs={'recruit_id': Recruit.objects.latest('published').id}))
        else:
            context = {'form': recruitf}
            return render(request, 'rservice/recruit.html', context)
    else:
        recruitf = RecruitForm()
        context = {'form': recruitf}
        return render(request, 'rservice/recruit.html', context)


def test(request, recruit_id):
    u"""
    Форма тестового задания для нового рекрута.
    :param request: Запрос клиента.
    :param recruit_id: ID нового рекрута.
    :return: Рендеринг шаблона.
    """
    qqs = Test.objects.order_by('questions')
    recruit = Recruit.objects.get(pk=recruit_id)
    if request.method == 'POST':
        testf = TestForm(request.POST, instance=recruit)
        if testf.is_valid():
            testf.save()
            context = {'qqs': qqs}
            return HttpResponseRedirect(reverse('result_test'), context)
        else:
            context = {'form': testf, 'qqs': qqs}
            return render(request, 'rservice/test.html', context)
    else:
        testf = TestForm()
        context = {'form': testf, 'qqs': qqs}
        return render(request, 'rservice/test.html', context)


def result_test(request):
    u"""
    Рендеринг шаблона с результатами тестов.
    :param request: Запрос клиента.
    :return: Рендеринг шаблона.
    """
    return render(request, 'rservice/result_test.html')



