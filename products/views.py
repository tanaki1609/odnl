from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProductSerializer
from .models import Product


@api_view(['GET', 'POST'])
def product_list_create_api_view(request):
    if request.method == 'GET':
        # step 1. collect data from DB
        data = Product.objects.select_related('category').prefetch_related('tags', 'reviews').all()

        # step 2. reformat QuerySet to List of Dictionary
        list_ = ProductSerializer(data, many=True).data

        # step 3. return list of dictionary
        return Response(data=list_)
    elif request.method == 'POST':
        # step 1: Receive data from request body
        title = request.data.get('title')
        price = request.data.get('price')
        description = request.data.get('description')
        is_active = request.data.get('is_active')
        category_id = request.data.get('category_id')
        tags = request.data.get('tags')

        # step 2: Create product by this data
        product = Product.objects.create(
            title=title,
            price=price,
            description=description,
            is_active=is_active,
            category_id=category_id,
        )
        product.tags.set(tags)
        product.save()

        # step 3: Return response as created product and status
        return Response(data={'product_id': product.id, 'title': product.title},
                        status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def product_detail_api_view(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(data={'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = ProductSerializer(product).data
        return Response(data=data)
    elif request.method == 'PUT':
        product.title = request.data.get('title')
        product.description = request.data.get('description')
        product.is_active = request.data.get('is_active')
        product.price = request.data.get('price')
        product.category_id = request.data.get('category_id')
        product.tags.set(request.data.get('tags'))
        product.save()
        return Response(status=status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
