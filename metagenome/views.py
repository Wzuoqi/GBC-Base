from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Metagenome
from django.db import models

def metagenomees(request):
    """
    View to display and filter metagenomic sequencing data.
    Supports searching by run ID, bioproject, habitat, and host.
    """
    # Get query parameters
    query = request.GET.get('q', '')
    habitat = request.GET.get('habitat', '')  # Filter by habitat
    sort_by = request.GET.get('sort', 'run_id')  # Default sort by run_id

    # Base queryset
    metagenome_list = Metagenome.objects.all()

    # Apply search filter if query exists
    if query:
        metagenome_list = metagenome_list.filter(
            Q(run_id__icontains=query) |
            Q(bioproject__icontains=query) |
            Q(habitat__icontains=query) |
            Q(host__icontains=query) |
            Q(geo_location__icontains=query)
        )

    # Apply habitat filter if specified
    if habitat:
        metagenome_list = metagenome_list.filter(habitat=habitat)

    # Apply sorting
    valid_sort_fields = {
        'run_id': 'run_id',
        'bioproject': 'bioproject',
        'habitat': 'habitat',
        'host': 'host',
        'bases': 'bases',
        'collection_date': 'collection_date',
        '-run_id': '-run_id',
        '-bioproject': '-bioproject',
        '-habitat': '-habitat',
        '-host': '-host',
        '-bases': '-bases',
        '-collection_date': '-collection_date',
    }

    if sort_by in valid_sort_fields:
        metagenome_list = metagenome_list.order_by(valid_sort_fields[sort_by])

    # Pagination
    paginator = Paginator(metagenome_list, 20)  # Show 20 metagenomes per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Prepare context with additional data
    context = {
        'page_obj': page_obj,
        'query': query,
        'habitat': habitat,
        'sort_by': sort_by,
        # Add summary statistics
        'total_metagenomes': Metagenome.objects.count(),
        'total_bases': Metagenome.objects.filter(bases__isnull=False).count(),
        # Get unique values for filtering
        'habitats': Metagenome.objects.values_list('habitat', flat=True)
                                     .exclude(habitat__isnull=True)
                                     .exclude(habitat='')
                                     .distinct()
                                     .order_by('habitat'),
        'hosts': Metagenome.objects.values_list('host', flat=True)
                                  .exclude(host__isnull=True)
                                  .exclude(host='')
                                  .distinct()
                                  .order_by('host'),
        # Add sequencing statistics
        'sequencing_stats': {
            'total_bases': Metagenome.objects.filter(bases__isnull=False)
                                           .aggregate(total=models.Sum('bases'))['total'],
            'avg_bases': Metagenome.objects.filter(bases__isnull=False)
                                         .aggregate(avg=models.Avg('bases'))['avg'],
        }
    }

    return render(request, 'metagenomes.html', context)

def metagenome_detail(request, run_id):
    """
    View to display detailed information about a specific metagenomic dataset.
    """
    metagenome = get_object_or_404(Metagenome, run_id=run_id)

    # Get related metagenomes (same habitat or host)
    related_metagenomes = Metagenome.objects.filter(
        Q(habitat=metagenome.habitat) | Q(host=metagenome.host)
    ).exclude(run_id=metagenome.run_id)[:5]

    # Get location information
    location_info = {
        'coordinates': metagenome.get_coordinates(),
        'country': metagenome.location_country,
        'region': metagenome.location_region,
    }

    # Get sequencing information
    sequencing_info = {
        'strategy': metagenome.strategy,
        'library_source': metagenome.library_source,
        'instrument': metagenome.instrument,
        'layout': metagenome.layout,
        'size_gb': metagenome.sequencing_size_gb,
    }

    context = {
        'metagenome': metagenome,
        'related_metagenomes': related_metagenomes,
        'location_info': location_info,
        'sequencing_info': sequencing_info,
    }

    return render(request, 'metagenome_detail.html', context)
