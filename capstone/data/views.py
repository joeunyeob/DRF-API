from django_filters.rest_framework import DjangoFilterBackend
from data.models import Facility, Other, Community, Professional, Jaega, All, UserModel
from data.serializers import FacilitySerializer, OtherSerializer, CommunitySerializer,\
    ProfessionalSerializer, JaeGaSerializer, AllSerializer, UserSerializer
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework import viewsets
from rest_framework.response import Response
from . import Recommend
from . import KeyWordSearch


@api_view(['GET', 'POST'])
def api_root(request, format=None):
    print(request)
    if request.method == 'GET':
        return Response({
            'account': reverse('account-list', request=request, format=format),
            'facility': reverse('facility-list', request=request, format=format),
            'jaega': reverse('jaega-list', request=request, format=format),
            'other': reverse('other-list', request=request, format=format),
            'community': reverse('community-list', request=request, format=format),
            'professional': reverse('professional-list', request=request, format=format),
            'login': reverse('login-list', request=request, format=format)
         })
    elif request.method == 'POST':
        pass


class FacilityViewSet(viewsets.ModelViewSet):
    queryset = Facility.objects.all()
    serializer_class = FacilitySerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly,
    #                       IsOwnerOrReadOnly]


class OtherViewSet(viewsets.ModelViewSet):
    queryset = Other.objects.all()
    serializer_class = OtherSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly,
    #                       IsOwnerOrReadOnly]


class JaeGaViewSet(viewsets.ModelViewSet):
    queryset = Jaega.objects.all()
    serializer_class = JaeGaSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly,
    #                       IsOwnerOrReadOnly]


class CommunityViewSet(viewsets.ModelViewSet):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly,
    #                       IsOwnerOrReadOnly]


class ProfessionalViewSet(viewsets.ModelViewSet):
    queryset = Professional.objects.all()
    serializer_class = ProfessionalSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly,
    #                       IsOwnerOrReadOnly]


class AllViewSet(viewsets.ModelViewSet):
    queryset = All.objects.all()
    serializer_class = AllSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title']
    #
    # def create(self, request, *args, **kwargs):
    #     print(request.data)
    #     return super().create(request, args, kwargs)

    # permission_classes = [permissions.IsAuthenticatedOrReadOnly,
    #                       IsOwnerOrReadOnly]


class SearchViewSet(viewsets.ModelViewSet):

    serializer_class = AllSerializer

    def get_queryset(self):
        queryset = All.objects.all()
        title = self.request.query_params.get('title', None)

        qs1 = KeyWordSearch.keyword_search(title)[0]
        qs2 = KeyWordSearch.keyword_search(title)[1]

        if qs1 or qs2 or title is not None:
            queryset1 = queryset.filter(title__contains=qs1)
            queryset2 = queryset.filter(title__contains=qs2)
            queryset3 = queryset.filter(title__contains=title)

            queryset = queryset1 | queryset2 | queryset3

            return queryset


# class RecommendViewSet(viewsets.ModelViewSet):
#
#     serializer_class = AllSerializer
#
#     def get_queryset(self):
#         queryset = All.objects.all()
#         location = self.request.query_params.get('location', None)
#         gender = self.request.query_params.get('gender', None)
#
#         qs1 = KeyWordSearch.keyword_search(location)
#         qs2 = KeyWordSearch.keyword_search(gender)
#
#         if qs1 or qs2 or title is not None:
#             queryset1 = queryset.filter(title__contains=qs1)
#             queryset2 = queryset.filter(title__contains=qs2)
#             queryset3 = queryset.filter(title__contains=title)
#
#             queryset = queryset1 | queryset2 | queryset3
#
#             return queryset


class UserViewSet(viewsets.ModelViewSet):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user_id']

    def create(self, request, *args, **kwargs):
        print(request.data)
        return super().create(request, args, kwargs)
