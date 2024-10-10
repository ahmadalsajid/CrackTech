from django.shortcuts import get_object_or_404
from django.db import IntegrityError, transaction
from drf_spectacular.utils import extend_schema, PolymorphicProxySerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from icecream import ic
from users.serializers import StudentSerializer, LoginViewSerializer, StudentCreateSerializer
from users.models import Student, User
from rest_framework import viewsets
from rest_framework.response import Response


class LoginView(TokenObtainPairView):
    serializer_class = LoginViewSerializer


class StudentViewSet(viewsets.ViewSet):
    # permission_classes = [AllowAny, ]

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @extend_schema(
        responses=PolymorphicProxySerializer(
            component_name='StudentViewSet.list.responses',
            serializers=[StudentSerializer, ],
            resource_type_field_name=None,
            many=True
        )
    )
    def list(self, request):
        queryset = Student.objects.all()
        serializer = StudentSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        request=PolymorphicProxySerializer(
            component_name='StudentViewSet.create.request',
            serializers=[StudentCreateSerializer, ],
            resource_type_field_name='StudentViewSet.create.request',
        ),
        responses=PolymorphicProxySerializer(
            component_name='StudentViewSet.create.responses',
            serializers=[StudentSerializer, ],
            resource_type_field_name=None,
        )
    )
    def create(self, request):
        _data = request.data
        _username = _data.get('email'),
        try:
            with transaction.atomic():
                if User.objects.filter(username=_username).exists():
                    return Response(
                        {'error': 'Username is not unique'},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                _serializer = StudentCreateSerializer(data=_data)
                if _serializer.is_valid():
                    _new_student = _serializer.save()
                    _student_serializer = StudentSerializer(_new_student)
                    return Response(
                        {
                            'detail': 'Student created successfully.',
                            'student': _student_serializer.data,
                        },
                        status=status.HTTP_201_CREATED,
                    )
                else:
                    raise Exception(_serializer.errors)

        except IntegrityError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        responses=PolymorphicProxySerializer(
            component_name='StudentViewSet.retrieve.responses',
            serializers=[StudentSerializer, ],
            resource_type_field_name=None,
        )
    )
    def retrieve(self, request, pk=None):
        queryset = Student.objects.all()
        student = get_object_or_404(queryset, pk=pk)
        serializer = StudentSerializer(student)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        pass

    @extend_schema(
        request=PolymorphicProxySerializer(
            component_name='StudentViewSet.patch.request',
            serializers=[StudentCreateSerializer, ],
            resource_type_field_name='StudentViewSet.patch.request',
        ),
        responses=PolymorphicProxySerializer(
            component_name='StudentViewSet.patch.responses',
            serializers=[StudentSerializer, ],
            resource_type_field_name=None,
        )
    )
    def partial_update(self, request, pk=None):
        _data = request.data
        try:
            with transaction.atomic():
                queryset = Student.objects.all()
                student = get_object_or_404(queryset, pk=pk)
                # if the new username is not the same as the existing one, i.e. username updated,
                # and that is already taken by someone else, then raise error
                _new_username = _data.get('user').get('username')
                if student.user.username != _new_username and User.objects.filter(username=_new_username).exists():
                    return Response(
                        {'error': 'Username is not unique'},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                _serializer = StudentCreateSerializer(instance=student, data=_data, partial=True)
                if _serializer.is_valid():
                    _student = _serializer.save()
                    _student_serializer = StudentSerializer(_student)
                    return Response(
                        {
                            'detail': 'Student partial update completed successfully.',
                            'student': _student_serializer.data,
                        },
                        status=status.HTTP_200_OK,
                    )
                else:
                    raise Exception(_serializer.errors)

        except IntegrityError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            _student = Student.objects.get(pk=pk)
            _user = _student.user
            _student.delete()
            _user.delete()
            return Response(
                {
                    'detail': 'Student deleted successfully.',
                },
                status=status.HTTP_204_NO_CONTENT,
            )
        except Exception as e:
            ic(e)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

