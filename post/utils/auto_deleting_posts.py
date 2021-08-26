from rest_framework.pagination import PageNumberPagination


def paginate(queryset, request, serializer_class):
    paginator = PageNumberPagination()
    paginator.page_size = 1
    paginator.page_size_query_param = 'page_size'
    paginated_outcome = paginator.paginate_queryset(queryset, request)
    return paginator.get_paginated_response(serializer_class(paginated_outcome, many=True).data)