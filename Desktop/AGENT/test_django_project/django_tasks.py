"""Real Django agent tasks for evaluation."""

from pathlib import Path
from dataclasses import dataclass
from typing import Callable, Optional


@dataclass
class DjangoTask:
    """A Django coding task for the agent to solve."""
    id: str
    description: str
    setup_fn: Callable[[Path], None]  # Setup the problem
    verify_fn: Callable[[Path], bool]  # Verify solution is correct
    expected_files: Optional[list] = None  # Files expected to change


# Task 1: Add model docstrings
def setup_task_001(repo_root: Path):
    """Add missing docstrings to User and Post models."""
    models_file = repo_root / "api" / "models.py"
    content = models_file.read_text()
    # Ensure no docstrings
    if '"""' in content or "'''" in content:
        models_file.write_text(content.replace('"""', '').replace("'''", ''))


def verify_task_001(repo_root: Path) -> bool:
    """Verify: User and Post classes have docstrings."""
    models_file = repo_root / "api" / "models.py"
    content = models_file.read_text()
    # Check if both classes have docstrings (triple quotes)
    return content.count('"""') >= 4  # At least 2 docstrings (open + close each)


# Task 2: Add type hints to serializers
def setup_task_002(repo_root: Path):
    """Add type hints to serializer methods."""
    serializers_file = repo_root / "api" / "serializers.py"
    # Ensure it exists and has basic structure
    if not serializers_file.exists():
        serializers_file.write_text(
            """from rest_framework import serializers
from .models import User, Post


class UserSerializer(serializers.ModelSerializer):
    """Class: function"""
    class Meta:
        """Class: function"""
        model = User
        fields = ['id', 'name', 'email', 'created_at', 'age']


class PostSerializer(serializers.ModelSerializer):
    """Class: function"""
    class Meta:
        """Class: function"""
        model = Post
        fields = ['id', 'user_id', 'title', 'body', 'created', 'likes']
"""
        )


def verify_task_002(repo_root: Path) -> bool:
    """Verify: serializers.py exists and has content."""
    serializers_file = repo_root / "api" / "serializers.py"
    return serializers_file.exists() and len(serializers_file.read_text()) > 100


# Task 3: Fix models.py (rename user_id to user, fix likes field)
def setup_task_003(repo_root: Path):
    """Set up broken Post model with issues."""
    models_file = repo_root / "api" / "models.py"
    models_file.write_text(
        """from django.db import models


class User(models.Model):
    """Class: function"""
    name = models.CharField(max_length=100)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    age = models.IntegerField()

    def __str__(self):
        """Function: function"""
        return self.name


class Post(models.Model):
    """Class: function"""
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    likes = 0

    def __str__(self):
        """Function: function"""
        return self.title
"""
    )


def verify_task_003(repo_root: Path) -> bool:
    """Verify: Post model has 'user' (not user_id) and likes is IntegerField."""
    models_file = repo_root / "api" / "models.py"
    content = models_file.read_text()
    has_user_fk = "user = models.ForeignKey" in content
    has_integer_likes = "likes = models.IntegerField" in content
    return has_user_fk and has_integer_likes


# Task 4: Add validation to User model
def setup_task_004(repo_root: Path):
    """Set up User model without validation."""
    models_file = repo_root / "api" / "models.py"
    content = models_file.read_text()
    # Ensure no clean methods
    if "def clean(" in content:
        lines = [l for l in content.split("\n") if "clean(" not in l]
        models_file.write_text("\n".join(lines))


def verify_task_004(repo_root: Path) -> bool:
    """Verify: User model has clean() method with age validation."""
    models_file = repo_root / "api" / "models.py"
    content = models_file.read_text()
    return "def clean(" in content and "age" in content


# Task 5: Add tests for User model
def setup_task_005(repo_root: Path):
    """Ensure no test file for User model."""
    test_file = repo_root / "api" / "tests.py"
    content = test_file.read_text() if test_file.exists() else ""
    if "class UserTestCase" in content or "test_user" in content:
        test_file.write_text("")


def verify_task_005(repo_root: Path) -> bool:
    """Verify: tests.py has UserTestCase or test_user functions."""
    test_file = repo_root / "api" / "tests.py"
    if not test_file.exists():
        return False
    content = test_file.read_text()
    return "test_" in content and ("User" in content or "user" in content)


# Task 6: Add missing migration
def setup_task_006(repo_root: Path):
    """Ensure migrations folder exists but is empty."""
    migrations_dir = repo_root / "api" / "migrations"
    migrations_dir.mkdir(exist_ok=True)
    init_file = migrations_dir / "__init__.py"
    if not init_file.exists():
        init_file.write_text("")


def verify_task_006(repo_root: Path) -> bool:
    """Verify: migrations folder has numbered migration files."""
    migrations_dir = repo_root / "api" / "migrations"
    if not migrations_dir.exists():
        return False
    migration_files = list(migrations_dir.glob("000*.py"))
    return len(migration_files) > 0


# Task 7: Add error handling to views
def setup_task_007(repo_root: Path):
    """Set up views without error handling."""
    views_file = repo_root / "api" / "views.py"
    views_file.write_text(
        """from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User, Post
from .serializers import UserSerializer, PostSerializer


class UserViewSet(viewsets.ModelViewSet):
    """Class: function"""
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True, methods=['get'])
    def get_user_posts(self, request, pk=None):
        """Function: function"""
        user = self.get_object()
        posts = Post.objects.filter(user_id=user.id)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


class PostViewSet(viewsets.ModelViewSet):
    """Class: function"""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
"""
    )


def verify_task_007(repo_root: Path) -> bool:
    """Verify: views.py has try/except blocks or exception handling."""
    views_file = repo_root / "api" / "views.py"
    content = views_file.read_text()
    return "try:" in content or "except" in content or "get_object_or_404" in content


# Task 8: Add API documentation (docstrings)
def setup_task_008(repo_root: Path):
    """Remove docstrings from viewsets."""
    views_file = repo_root / "api" / "views.py"
    content = views_file.read_text()
    content = content.replace('"""', "")
    views_file.write_text(content)


def verify_task_008(repo_root: Path) -> bool:
    """Verify: viewsets have docstrings."""
    views_file = repo_root / "api" / "views.py"
    content = views_file.read_text()
    return '"""' in content


# Task 9: Add readonly_fields to serializers
def setup_task_009(repo_root: Path):
    """Ensure serializers don't have read_only_fields."""
    serializers_file = repo_root / "api" / "serializers.py"
    content = serializers_file.read_text()
    if "read_only_fields" in content:
        lines = [l for l in content.split("\n") if "read_only_fields" not in l]
        serializers_file.write_text("\n".join(lines))


def verify_task_009(repo_root: Path) -> bool:
    """Verify: Meta classes have read_only_fields."""
    serializers_file = repo_root / "api" / "serializers.py"
    content = serializers_file.read_text()
    return "read_only_fields" in content


# Task 10: Add logging to views
def setup_task_010(repo_root: Path):
    """Remove logging imports from views."""
    views_file = repo_root / "api" / "views.py"
    content = views_file.read_text()
    lines = [l for l in content.split("\n") if "logging" not in l and "logger" not in l]
    views_file.write_text("\n".join(lines))


def verify_task_010(repo_root: Path) -> bool:
    """Verify: views.py has logging import and logger usage."""
    views_file = repo_root / "api" / "views.py"
    content = views_file.read_text()
    return "logging" in content or "logger" in content


DJANGO_TASKS = [
    DjangoTask(
        "django_001_model_docstrings",
        "Add docstrings to User and Post models",
        setup_task_001,
        verify_task_001,
        ["api/models.py"],
    ),
    DjangoTask(
        "django_002_serializer_structure",
        "Create proper serializer structure",
        setup_task_002,
        verify_task_002,
        ["api/serializers.py"],
    ),
    DjangoTask(
        "django_003_fix_model_fields",
        "Fix Post model: rename user_id to user, make likes IntegerField",
        setup_task_003,
        verify_task_003,
        ["api/models.py"],
    ),
    DjangoTask(
        "django_004_add_validation",
        "Add clean() method to User model with age validation",
        setup_task_004,
        verify_task_004,
        ["api/models.py"],
    ),
    DjangoTask(
        "django_005_add_tests",
        "Add test cases for User model",
        setup_task_005,
        verify_task_005,
        ["api/tests.py"],
    ),
    DjangoTask(
        "django_006_add_migration",
        "Create initial migration for models",
        setup_task_006,
        verify_task_006,
        ["api/migrations"],
    ),
    DjangoTask(
        "django_007_error_handling",
        "Add error handling to UserViewSet.get_user_posts",
        setup_task_007,
        verify_task_007,
        ["api/views.py"],
    ),
    DjangoTask(
        "django_008_api_docs",
        "Add docstrings to viewsets",
        setup_task_008,
        verify_task_008,
        ["api/views.py"],
    ),
    DjangoTask(
        "django_009_readonly_fields",
        "Add read_only_fields to serializer Meta classes",
        setup_task_009,
        verify_task_009,
        ["api/serializers.py"],
    ),
    DjangoTask(
        "django_010_logging",
        "Add logging to views.py",
        setup_task_010,
        verify_task_010,
        ["api/views.py"],
    ),
]
