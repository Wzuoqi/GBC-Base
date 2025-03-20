from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Genome

def genomes(request):
    """
    View to display and filter genome data.
    Supports searching by multiple fields and quality filtering.
    """
    # Get query parameters
    query = request.GET.get('q', '')
    quality_filter = request.GET.get('quality', '')
    sort_by = request.GET.get('sort', 'bin_id')

    # Base queryset
    genome_list = Genome.objects.all()

    # Apply search filter if query exists
    if query:
        genome_list = genome_list.filter(
            Q(bin_id__icontains=query) |
            Q(source__icontains=query) |
            Q(habitat__icontains=query) |
            Q(gtdb_classification__icontains=query)
        )

    # Apply quality filter if specified
    if quality_filter:
        if quality_filter == 'high':
            genome_list = genome_list.filter(completeness__gt=90, contamination__lt=5)
        elif quality_filter == 'medium':
            genome_list = genome_list.filter(completeness__gt=50, contamination__lt=10)
        elif quality_filter == 'low':
            genome_list = genome_list.filter(
                Q(completeness__lte=50) | Q(contamination__gte=10)
            )

    # Apply sorting
    valid_sort_fields = {
        'bin_id': 'bin_id',
        'source': 'source',
        'completeness': 'completeness',
        'contamination': 'contamination',
        'habitat': 'habitat',
        '-bin_id': '-bin_id',
        '-source': '-source',
        '-completeness': '-completeness',
        '-contamination': '-contamination',
        '-habitat': '-habitat',
    }

    if sort_by in valid_sort_fields:
        genome_list = genome_list.order_by(valid_sort_fields[sort_by])

    # Pagination
    paginator = Paginator(genome_list, 20)  # Show 20 genomes per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Prepare context with additional data
    context = {
        'page_obj': page_obj,
        'query': query,
        'quality_filter': quality_filter,
        'sort_by': sort_by,
        # Add summary statistics
        'total_genomes': Genome.objects.count(),
        'high_quality_count': Genome.objects.filter(completeness__gt=90, contamination__lt=5).count(),
        'medium_quality_count': Genome.objects.filter(completeness__gt=50, contamination__lt=10).count(),
        # Add unique habitats for filtering
        'habitats': Genome.objects.values_list('habitat', flat=True).distinct().order_by('habitat'),
    }

    return render(request, 'genomes.html', context)

def genome_detail(request, bin_id):
    """
    View to display detailed information about a specific genome.
    """
    genome = get_object_or_404(Genome, bin_id=bin_id)

    context = {
        'genome': genome,
        # Add any additional context data needed for the detail view
    }

    return render(request, 'genome_detail.html', context)