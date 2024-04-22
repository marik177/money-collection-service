from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from collection_project.api.pagination import (
    LimitOffsetPagination,
    get_paginated_response,
)
from collection_project.money_collections.models import Payment
from collection_project.money_collections.selectors.payments import (
    payments_list,
)
from collection_project.money_collections.services.payments import (
    get_contributor_full_name_or_email,
    payment_create,
)


class PaymentListApi(APIView):
    """List all payments"""

    class Pagination(LimitOffsetPagination):
        default_limit = 5

    class OutputSerializer(serializers.ModelSerializer):
        contributor = serializers.SerializerMethodField()
        collection = serializers.ReadOnlyField(source="collection.title")

        class Meta:
            model = Payment
            fields = (
                "amount",
                "payment_date",
                "collection",
                "contributor",
            )

        def get_contributor(self, obj: Payment) -> str:
            return get_contributor_full_name_or_email(payment=obj)

    def get(self, request) -> Response:
        payments = payments_list()
        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=payments,
            request=request,
            view=self,
        )


class PaymentCreateApi(APIView):
    """Create a payment"""

    class InputSerializer(serializers.Serializer):
        email = serializers.EmailField()
        first_name = serializers.CharField(required=False)
        last_name = serializers.CharField(required=False)
        collection_id = serializers.IntegerField()
        amount = serializers.IntegerField()

    def post(self, request) -> Response:
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payment_create(**serializer.validated_data)
        return Response(
            status=status.HTTP_201_CREATED,
        )
