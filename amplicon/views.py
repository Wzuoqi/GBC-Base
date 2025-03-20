from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Amplicon
from django.db import models

def amplicons(request):
    """
    View to display and filter amplicon sequencing data.
    Supports searching by run ID, bioproject, habitat, host, and amplicon type.
    """
    # Get query parameters
    query = request.GET.get('q', '')
    amplicon_type = request.GET.get('type', '')  # Filter by amplicon type (16S, ITS, etc.)
    habitat = request.GET.get('habitat', '')  # Filter by habitat
    sort_by = request.GET.get('sort', 'run')  # Default sort by run ID

    # Base queryset
    amplicon_list = Amplicon.objects.all()

    # Apply search filter if query exists
    if query:
        amplicon_list = amplicon_list.filter(
            Q(run__icontains=query) |
            Q(bioproject__icontains=query) |
            Q(biosample__icontains=query) |
            Q(habitat__icontains=query) |
            Q(host__icontains=query) |
            Q(geo_location__icontains=query)
        )

    # Apply amplicon type filter if specified
    if amplicon_type:
        amplicon_list = amplicon_list.filter(amplicon_type=amplicon_type)

    # Apply habitat filter if specified
    if habitat:
        amplicon_list = amplicon_list.filter(habitat=habitat)

    # Apply sorting
    valid_sort_fields = {
        'run': 'run',
        'bioproject': 'bioproject',
        'habitat': 'habitat',
        'host': 'host',
        'amplicon_type': 'amplicon_type',
        'collection_date': 'collection_date',
        'bases': 'bases',
        '-run': '-run',
        '-bioproject': '-bioproject',
        '-habitat': '-habitat',
        '-host': '-host',
        '-amplicon_type': '-amplicon_type',
        '-collection_date': '-collection_date',
        '-bases': '-bases',
    }

    if sort_by in valid_sort_fields:
        amplicon_list = amplicon_list.order_by(valid_sort_fields[sort_by])

    # Pagination
    paginator = Paginator(amplicon_list, 20)  # Show 20 amplicons per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Prepare context with additional data
    context = {
        'page_obj': page_obj,
        'query': query,
        'amplicon_type': amplicon_type,
        'habitat': habitat,
        'sort_by': sort_by,
        # Add summary statistics
        'total_amplicons': Amplicon.objects.count(),
        'total_bases': Amplicon.objects.filter(bases__isnull=False).count(),
        # Get unique values for filtering
        'amplicon_types': Amplicon.objects.values_list('amplicon_type', flat=True)
                                        .exclude(amplicon_type__isnull=True)
                                        .exclude(amplicon_type='')
                                        .distinct()
                                        .order_by('amplicon_type'),
        'habitats': Amplicon.objects.values_list('habitat', flat=True)
                                   .exclude(habitat__isnull=True)
                                   .exclude(habitat='')
                                   .distinct()
                                   .order_by('habitat'),
        'hosts': Amplicon.objects.values_list('host', flat=True)
                                .exclude(host__isnull=True)
                                .exclude(host='')
                                .distinct()
                                .order_by('host'),
        # Add sequencing statistics
        'sequencing_stats': {
            'total_bases': Amplicon.objects.filter(bases__isnull=False)
                                         .aggregate(total=models.Sum('bases'))['total'],
            'avg_bases': Amplicon.objects.filter(bases__isnull=False)
                                       .aggregate(avg=models.Avg('bases'))['avg'],
        }
    }

    return render(request, 'amplicons.html', context)

def amplicon_detail(request, run):
    """
    View to display detailed information about a specific amplicon dataset.
    """
    amplicon = get_object_or_404(Amplicon, run=run)

    # Get related amplicons (same amplicon type, habitat, or host)
    related_amplicons = Amplicon.objects.filter(
        Q(amplicon_type=amplicon.amplicon_type) |
        Q(habitat=amplicon.habitat) |
        Q(host=amplicon.host)
    ).exclude(run=amplicon.run)[:5]

    # Get location information
    location_info = {
        'coordinates': f"{amplicon.latitude}, {amplicon.longitude}" if amplicon.latitude and amplicon.longitude else None,
        'geo_location': amplicon.geo_location,
    }

    # Get sequencing information
    sequencing_info = {
        'assay_type': amplicon.assay_type,
        'amplicon_type': amplicon.amplicon_type,
        'library_source': amplicon.library_source,
        'instrument': amplicon.instrument,
        'layout': amplicon.layout,
        'bases': f"{round(amplicon.bases / 1_000_000_000, 2)} Gb" if amplicon.bases else None,
    }

    # Get sample information
    sample_info = {
        'biosample': amplicon.biosample,
        'host': amplicon.host,
        'sample_isolated': amplicon.sample_isolated,
        'collection_date': amplicon.collection_date,
    }

    context = {
        'amplicon': amplicon,
        'related_amplicons': related_amplicons,
        'location_info': location_info,
        'sequencing_info': sequencing_info,
        'sample_info': sample_info,
    }

    return render(request, 'amplicon_detail.html', context)
