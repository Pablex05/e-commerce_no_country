from django.views.defaults import page_not_found


def error404(request):
    name_template = 'store/errors/404.html'
    return page_not_found(request, template_name=name_template)


def error500(request):
    name_template = "store/errors/500.html"
    return page_not_found(request, template_name=name_template)
