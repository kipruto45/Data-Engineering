from rest_framework import generics, permissions
from .models import Election, Position
from .serializers import ElectionSerializer, PositionSerializer


class ElectionListView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Election.objects.filter(is_published=True)
    serializer_class = ElectionSerializer


class PositionListView(generics.ListCreateAPIView):
    serializer_class = PositionSerializer

    class PositionListPermission(permissions.BasePermission):
        def has_permission(self, request, view):
            # allow any authenticated user to list
            if request.method in permissions.SAFE_METHODS:
                return request.user and request.user.is_authenticated
            # allow POST only for admins
            return IsAdminProfile().has_permission(request, view)

    permission_classes = (PositionListPermission,)

    def get_queryset(self):
        election_id = self.kwargs.get("election_id")
        return Position.objects.filter(election_id=election_id)

    def perform_create(self, serializer):
        election_id = self.kwargs.get("election_id")
        election = generics.get_object_or_404(Election, id=election_id)
        serializer.save(election=election)



class IsAdminProfile(permissions.BasePermission):
    """Allow access only to users whose Profile.role == 'admin' or Django is_staff."""

    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            if getattr(request.user, "is_staff", False):
                return True
            profile = getattr(request.user, "profile", None)
            return bool(profile and profile.role == "admin")
        return False


class PositionCreateView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated, IsAdminProfile)
    serializer_class = PositionSerializer

    def perform_create(self, serializer):
        election_id = self.kwargs.get("election_id")
        election = generics.get_object_or_404(Election, id=election_id)
        serializer.save(election=election)


class PositionDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated, IsAdminProfile)
    serializer_class = PositionSerializer
    queryset = Position.objects.all()
