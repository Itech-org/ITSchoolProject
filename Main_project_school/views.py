from django.shortcuts import render


def entry_page_view(request):
    return render(request, 'entry_page.html')