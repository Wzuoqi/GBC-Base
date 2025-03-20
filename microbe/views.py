from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Microbe

def microbes(request):
    """
    View to display and filter microbial records.
    Supports searching by taxonomy, functions, and habitats.
    """
    # Get query parameters
    query = request.GET.get('q', '')
    habitat = request.GET.get('habitat', '')  # Filter by habitat
    sort_by = request.GET.get('sort', 'taxonomy')

    # Base queryset
    microbe_list = Microbe.objects.all()

    # Apply search filter if query exists
    if query:
        microbe_list = microbe_list.filter(
            Q(taxonomy__icontains=query) |
            Q(domain__icontains=query) |
            Q(phylum__icontains=query) |
            Q(class_name__icontains=query) |
            Q(order__icontains=query) |
            Q(family__icontains=query) |
            Q(genus__icontains=query) |
            Q(species__icontains=query) |
            Q(functions__contains=[query]) |  # ArrayField search
            Q(habitats__contains=[query])     # ArrayField search
        )

    # Apply habitat filter if specified
    if habitat:
        microbe_list = microbe_list.filter(habitats__contains=[habitat])

    # Apply sorting
    valid_sort_fields = {
        'taxonomy': 'taxonomy',
        'domain': 'domain',
        'phylum': 'phylum',
        'genus': 'genus',
        '-taxonomy': '-taxonomy',
        '-domain': '-domain',
        '-phylum': '-phylum',
        '-genus': '-genus',
    }

    if sort_by in valid_sort_fields:
        microbe_list = microbe_list.order_by(valid_sort_fields[sort_by])

    # Pagination
    paginator = Paginator(microbe_list, 20)  # Show 20 microbes per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Get unique habitats for filtering
    unique_habitats = set()
    for microbe in Microbe.objects.all():
        unique_habitats.update(microbe.habitats)

    # Prepare context with additional data
    context = {
        'page_obj': page_obj,
        'query': query,
        'habitat': habitat,
        'sort_by': sort_by,
        'total_records': Microbe.objects.count(),
        'habitats': sorted(unique_habitats),  # Sorted list of unique habitats
    }

    return render(request, 'microbes.html', context)

def microbe_detail(request, id):
    """
    View to display detailed information about a specific microbe.
    """
    microbe = get_object_or_404(Microbe, id=id)

    # Get related microbes (same genus or habitat)
    related_microbes = Microbe.objects.filter(
        Q(genus=microbe.genus) | Q(habitats__overlap=microbe.habitats)
    ).exclude(id=microbe.id)[:5]

    # Prepare taxonomic hierarchy
    taxonomy_levels = {
        'Domain': microbe.domain,
        'Phylum': microbe.phylum,
        'Class': microbe.class_name,
        'Order': microbe.order,
        'Family': microbe.family,
        'Genus': microbe.genus,
        'Species': microbe.species,
    }

    context = {
        'microbe': microbe,
        'related_microbes': related_microbes,
        'taxonomy_levels': taxonomy_levels,
        'functions': microbe.functions,  # List of functions
        'habitats': microbe.habitats,    # List of habitats
        'sources': microbe.sources,      # List of sources
        'sources_count': microbe.get_sources_count(),
    }

    return render(request, 'microbe_detail.html', context)

def microbe_functions(request):
    """
    View to display function-based statistics and groupings.
    """
    # Get all unique functions
    all_functions = set()
    function_counts = {}

    for microbe in Microbe.objects.all():
        for function in microbe.functions:
            all_functions.add(function)
            function_counts[function] = function_counts.get(function, 0) + 1

    # Sort functions by count
    sorted_functions = sorted(
        function_counts.items(),
        key=lambda x: x[1],
        reverse=True
    )

    context = {
        'functions': sorted_functions,
        'total_functions': len(all_functions),
        'total_microbes': Microbe.objects.count(),
    }

    return render(request, 'microbe_functions.html', context)

def microbe_habitats(request):
    """
    View to display habitat-based statistics and groupings.
    """
    # Get all unique habitats
    all_habitats = set()
    habitat_counts = {}

    for microbe in Microbe.objects.all():
        for habitat in microbe.habitats:
            all_habitats.add(habitat)
            habitat_counts[habitat] = habitat_counts.get(habitat, 0) + 1

    # Sort habitats by count
    sorted_habitats = sorted(
        habitat_counts.items(),
        key=lambda x: x[1],
        reverse=True
    )

    context = {
        'habitats': sorted_habitats,
        'total_habitats': len(all_habitats),
        'total_microbes': Microbe.objects.count(),
    }

    return render(request, 'microbe_habitats.html', context)
