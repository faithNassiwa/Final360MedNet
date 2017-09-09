from django.shortcuts import render


def about_us(request):
    return render(request, 'website/about_us.html')


def privacy_policy(request):
    return render(request, 'website/privacy_policy.html')


def terms_of_use(request):
    return render(request, 'website/terms_of_use.html')


def website_help(request):
    return render(request, 'website/help.html')
