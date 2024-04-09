from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from api.models import TenK
from api.serializers import TenKSerializer

from .utils import find_most_similar_sentences, clustering_
from datetime import datetime


@api_view(['POST'])
def clustering(request):
    '''Call clustering helper function based on the input data and method.
    - year
    - embedding_type 
    - clustering_technique
    - n_clusters
    - dim_reduction_technique
    - preprocessing    
    '''

    try:
        data = request.data

        year = data['year']
        embedding_type = data['embedding_type']
        clustering_technique = data['clustering_technique']
        n_clusters = data.get('n_clusters', 10)  # Default value is 10
        dim_reduction_technique = data['dim_reduction_technique']
        preprocessing = (data['preprocessing'] == "1")

        if year is not None and year != "":
            start_date = datetime.strptime(f"{year}-01-01", "%Y-%m-%d")
            end_date = datetime.strptime(f"{year}-12-31", "%Y-%m-%d")
            entry_list_with_ids = TenK.objects.filter(is_active=True, filing_date__range=(start_date, end_date)).exclude(item_1__isnull=True).exclude(item_1__exact='').values_list('id', 'item_1', 'company', 'filing_date')
        else:
            entry_list_with_ids = TenK.objects.filter(is_active=True).exclude(item_1__isnull=True).exclude(item_1__exact='').values_list('id', 'item_1', 'company', 'filing_date')

        entry_list_with_ids = list(entry_list_with_ids)

        if not entry_list_with_ids:
            return Response({'message': 'No entries found.'}, status=status.HTTP_404_NOT_FOUND)

        if embedding_type not in ('tfidf', 'word2vec', 'bert'):
            return Response({'error': 'Vectorization method not supported'},
                            status=status.HTTP_400_BAD_REQUEST)

        labels = clustering_(
            entry_list_with_ids=entry_list_with_ids,
            embedding_type=embedding_type,
            clustering_technique=clustering_technique,
            dim_reduction_technique=dim_reduction_technique,
            n_clusters=n_clusters,
            preprocessing=preprocessing)

        return Response({
            'message': 'Clustering performed successfully.',
            'labels': labels
        })

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def similarity(request):
    '''Call the helper function given request data.
    - year    
    - embedding_type
    - similarity_technique
    - text_query
    - num_similar = 10
    '''

    #try:
    data = request.data
    
    # sentences = data['sentences']
    if data["year"] is not None and data["year"] != "":
        year = data['year']
        start_date = datetime.strptime(f"{year}-01-01", "%Y-%m-%d")
        end_date = datetime.strptime(f"{year}-12-31", "%Y-%m-%d")
        entry_list_with_ids = TenK.objects.filter(is_active=True, filing_date__range=(start_date, end_date)).exclude(item_1__isnull=True).exclude(item_1__exact='').values_list('id', 'item_1')
    else:
        entry_list_with_ids = TenK.objects.filter(is_active=True).exclude(item_1__isnull=True).exclude(item_1__exact='').values_list('id', 'item_1')
    entry_list_with_ids = list(entry_list_with_ids)
    # return Response({'message': 'Similarity calculated successfully.'})
    if not entry_list_with_ids:
        return Response({'message': 'No entries found.'}, status=status.HTTP_404_NOT_FOUND)
    text_query = data['text_query']
    embedding_type = data['embedding_type']
    similarity_technique = data['similarity_technique']
    preprocessing = (data['preprocessing'] == "1")

    if embedding_type not in ('tfidf', 'word2vec', 'bert'):
        return Response({'error': 'Vectorization method not supported'},
                        status=status.HTTP_400_BAD_REQUEST)

    result_list = find_most_similar_sentences(
        entry_list_with_ids=entry_list_with_ids,
        text_query=text_query,
        embedding_type=embedding_type,
        similarity_technique=similarity_technique,
        preprocessing=preprocessing)

    result_ids = [e['id'] for e in result_list]
    result_tenk_entries = TenK.objects.filter(id__in=result_ids)

    for entry in result_list:
        entry['object'] = TenKSerializer(
            result_tenk_entries.get(id=entry['id'])).data

    # Filter out entries with similarity score < 0.001
    result_list = list(
        filter(lambda e: e['similarity'] > 0.001, result_list))

    return Response({
        'message': 'Similarity calculated successfully.',
        'result_list': result_list
    })

    #except Exception as e:
    #    return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
