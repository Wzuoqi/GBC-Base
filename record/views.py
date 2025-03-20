from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Record

def recordes(request):
    """
    View to display and filter taxonomic records.
    Supports searching by taxonomy, function, and habitat.
    """
    # Get query parameters
    query = request.GET.get('q', '')
    function_type = request.GET.get('type', '')  # Filter by function type (C, N, etc.)
    sort_by = request.GET.get('sort', 'taxonomy')

    # Base queryset
    record_list = Record.objects.all()

    # Apply search filter if query exists
    if query:
        record_list = record_list.filter(
            Q(taxonomy__icontains=query) |
            Q(function__icontains=query) |
            Q(habitat__icontains=query) |
            Q(function_type__icontains=query)
        )

    # Apply function type filter if specified
    if function_type:
        record_list = record_list.filter(function_type=function_type)

    # Apply sorting
    valid_sort_fields = {
        'taxonomy': 'taxonomy',
        'function': 'function',
        'function_type': 'function_type',
        'habitat': 'habitat',
        '-taxonomy': '-taxonomy',
        '-function': '-function',
        '-function_type': '-function_type',
        '-habitat': '-habitat',
    }

    if sort_by in valid_sort_fields:
        record_list = record_list.order_by(valid_sort_fields[sort_by])

    # Pagination
    paginator = Paginator(record_list, 20)  # Show 20 records per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Prepare context with additional data
    context = {
        'page_obj': page_obj,
        'query': query,
        'function_type': function_type,
        'sort_by': sort_by,
        # Add summary statistics
        'total_records': Record.objects.count(),
        # Get unique function types and habitats for filtering
        'function_types': Record.objects.values_list('function_type', flat=True).distinct().order_by('function_type'),
        'habitats': Record.objects.values_list('habitat', flat=True).distinct().order_by('habitat'),
    }

    return render(request, 'records.html', context)

def record_detail(request, id):
    """
    View to display detailed information about a specific taxonomic record.
    """
    record = get_object_or_404(Record, id=id)

    # Get related records (same function type or habitat)
    related_records = Record.objects.filter(
        Q(function_type=record.function_type) | Q(habitat=record.habitat)
    ).exclude(id=record.id)[:5]

    context = {
        'record': record,
        'related_records': related_records,
        # Add taxonomic hierarchy
        'taxonomy_levels': {
            'Domain': record.get_domain(),
            'Phylum': record.get_phylum(),
            'Class': record.get_class(),
            'Order': record.get_order(),
            'Family': record.get_family(),
            'Genus': record.get_genus(),
            'Species': record.get_species(),
        }
    }

    return render(request, 'record_detail.html', context)
