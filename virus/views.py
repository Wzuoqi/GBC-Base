from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Virus

def viruses(request):
    query = request.GET.get('q')
    if query:
        virus_list = Virus.objects.filter(
            Q(type__icontains=query) | Q(quality__icontains=query) | Q(taxonomy__icontains=query)
        )
    else:
        virus_list = Virus.objects.all()

    paginator = Paginator(virus_list, 10)  # Show 10 viruses per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'viruses.html', {'page_obj': page_obj})

def virus_detail(request, virus_id):
    """
    View to display detailed information about a specific virus.
    """
    virus = get_object_or_404(Virus, virus_id=virus_id)

    context = {
        'virus': virus,
    }

    return render(request, 'virus_detail.html', context)