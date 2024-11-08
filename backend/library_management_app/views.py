from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Book, Member, Transaction
from .serializers import BookSerializer, MemberSerializer, TransactionSerializer

@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_book_list(request):
    search_query = request.query_params.get('q', '')
    books = Book.objects.filter(
        Q(title__icontains=search_query) |
        Q(author__icontains=search_query)
    ).order_by('title')

    page = request.query_params.get('page', 1)
    paginator = Paginator(books, 10)
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    serializer = BookSerializer(page_obj, many=True)
    return Response({
        'results': serializer.data,
        'total_pages': paginator.num_pages,
        'current_page': page_obj.number
    })

@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    serializer = BookSerializer(book)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def create_book(request):
    serializer = BookSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_member_list(request):
    search_query = request.query_params.get('q', '')
    members = Member.objects.filter(
        Q(name__icontains=search_query) |
        Q(email__icontains=search_query) |
        Q(phone__icontains=search_query)
    ).order_by('name')

    page = request.query_params.get('page', 1)
    paginator = Paginator(members, 10)
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    serializer = MemberSerializer(page_obj, many=True)
    return Response({
        'results': serializer.data,
        'total_pages': paginator.num_pages,
        'current_page': page_obj.number
    })

@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_member(request, pk):
    member = get_object_or_404(Member, pk=pk)
    serializer = MemberSerializer(member)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def create_member(request):
    serializer = MemberSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_transaction_list(request):
    transactions = Transaction.objects.all().order_by('-issue_date')

    page = request.query_params.get('page', 1)
    paginator = Paginator(transactions, 10)
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    serializer = TransactionSerializer(page_obj, many=True)
    return Response({
        'results': serializer.data,
        'total_pages': paginator.num_pages,
        'current_page': page_obj.number
    })

@api_view(['POST'])
@permission_classes([IsAdminUser])
def issue_book(request):
    serializer = TransactionSerializer(data=request.data)
    if serializer.is_valid():
        book = serializer.validated_data['book']
        member = serializer.validated_data['member']

        if not member.can_borrow():
            return Response({'error': 'Member has outstanding debt above KES 500'}, status=400)

        if book.quantity < 1:
            return Response({'error': 'Book is out of stock'}, status=400)

        transaction = serializer.save()
        book.quantity -= 1
        book.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def return_book(request):
    transaction_id = request.data.get('transaction_id')
    transaction = get_object_or_404(Transaction, pk=transaction_id)

    if transaction.issue_status == Transaction.RETURNED:
        return Response({'error': 'Book has already been returned'}, status=400)

    days_borrowed = (transaction.return_date - transaction.issue_date).days
    fee = days_borrowed * transaction.book.daily_fee
    transaction.fee_charged = fee
    transaction.issue_status = Transaction.RETURNED
    transaction.save()

    transaction.member.outstanding_debt += fee
    transaction.member.save()

    transaction.book.quantity += 1
    transaction.book.save()

    serializer = TransactionSerializer(transaction)
    return Response(serializer.data)