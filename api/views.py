from rest_framework import  generics, viewsets, filters, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from .models import Profile, Application
from .serializers import UserSerializer, ProfileSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .models import ExamRequest
from .serializers import ExamRequestSerializer, ApplicationSerializer, ApplicationSerializer
from rest_framework.decorators import action
from rest_framework.response import Response


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            return self.request.user.profile
        except Profile.DoesNotExist:
            # Create a default profile
            return Profile.objects.create(
                user=self.request.user,
                role='Requester',
                academic_level='Unknown',
                institution='Unknown'
            )

class ExamRequestViewSet(viewsets.ModelViewSet):
    queryset = ExamRequest.objects.all().order_by('-exam_date')
    serializer_class = ExamRequestSerializer
    permission_classes = [IsAuthenticated]

    # FILTERING ENGINE
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['university', 'semester', 'location',]
    search_fields = ['module_name', 'branch'] # Partial search (e.g. "Alg" finds "Algebra")

    def perform_create(self, serializer):
        # auto-assign the logged-in user as the requester
        serializer.save(requester=self.request.user)


    @action(detail=True, methods=['post'])
    def apply(self, request, pk=None):
        exam = self.get_object()

        # is the user a Scribe?

        if request.user.profile.role != 'Scribe':
            return Response({'error': 'Only scribes can apply!'}, status=403)

        # create the Application
        # The 'unique_together' in Application model will prevent duplicates automatically

        try:
            application = Application.objects.create(
                scribe=request.user,
                exam_request=exam
            )
            serializer = ApplicationSerializer(application)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {'reminder': 'You have already applied for this exam.'},
                status=status.HTTP_400_BAD_REQUEST
            )


class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]


    @action(detail=True, methods=['patch'])
    def respond(self, request, pk=None):
        #get the application
        application = self.get_object()

        #is the person clicking "Accept" actually the owner of the request?
        request_owner = application.exam_request.requester
        if request.user != request_owner:
            return Response(
                {'error': 'You are not the owner of this exam request!'},
                status=status.HTTP_403_FORBIDDEN
            )

        #get the new status from the user's input (Body)
        new_status = request.data.get('status')

        #validate input
        valid_statuses = ['Accepted', 'Rejected']
        if new_status not in valid_statuses:
            return Response(
                {'error': f'Invalid status. Choose from: {valid_statuses}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        application.status = new_status
        application.save()

        return Response({'status': f'Application marked as {new_status}'})