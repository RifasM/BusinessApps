from django.shortcuts import render


def index(request):
    """
    Business Logic for home/index page
    :param request: User Request(Get)
    :return: Index or Landing Page
    """
    return render(request, "index.html")


def create_quotation(request):
    """
    Return and process Requests involving
    Creation of Quotations
    :param request: User Request (Get and Post)
    :return: Creation Page on GET, Display Quotation on POST
    """
    pass


def handler404(request, exception):
    print(">>> 404: ", exception)
    return render(request, '404.html', status=404)


def handler500(request):
    return render(request, '500.html', status=500)
