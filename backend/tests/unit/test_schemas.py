from pydantic import ValidationError
import pytest
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse, RefreshRequest, ForgotPasswordRequest, ResetPasswordRequest
from app.schemas.user import UserCreate, UserUpdate
from app.schemas.project import ProjectCreate, ProjectUpdate
from app.schemas.component import ComponentCreate, ComponentUpdate
from app.schemas.conversation import ConversationCreate, AddMessageRequest
from app.schemas.common import BaseSchema


class TestAuthSchemas:
    def test_register_request_valid(self):
        data = RegisterRequest(email="test@example.com", username="testuser", password="SecurePass123!")
        assert data.email == "test@example.com"

    def test_register_request_invalid_email(self):
        with pytest.raises(ValidationError):
            RegisterRequest(email="not-an-email", username="testuser", password="SecurePass123!")

    def test_register_request_short_password(self):
        with pytest.raises(ValidationError):
            RegisterRequest(email="test@example.com", username="testuser", password="short")

    def test_login_request_valid(self):
        data = LoginRequest(email="test@example.com", password="password")
        assert data.email == "test@example.com"

    def test_token_response(self):
        data = TokenResponse(access_token="abc", refresh_token="def", token_type="bearer")
        assert data.access_token == "abc"


class TestUserSchemas:
    def test_user_create_valid(self):
        data = UserCreate(email="a@b.com", username="user", password="SecurePass123!")
        assert data.username == "user"

    def test_user_create_optional_fields(self):
        data = UserCreate(email="a@b.com", username="user", password="SecurePass123!",
                          display_name="Test User", avatar_url="http://example.com/avatar.png")
        assert data.display_name == "Test User"

    def test_user_update_empty(self):
        data = UserUpdate()
        assert data.model_dump(exclude_unset=True) == {}

    def test_user_update_partial(self):
        data = UserUpdate(display_name="New Name")
        assert data.display_name == "New Name"


class TestProjectSchemas:
    def test_project_create_required_only(self):
        data = ProjectCreate(title="Test Project")
        assert data.title == "Test Project"
        assert data.description is None
        assert data.is_public is False

    def test_project_create_full(self):
        data = ProjectCreate(title="Full Project", description="Desc", is_public=True)
        assert data.is_public is True

    def test_project_update_empty(self):
        data = ProjectUpdate()
        assert data.model_dump(exclude_unset=True) == {}

    def test_project_update_partial(self):
        data = ProjectUpdate(description="Updated desc")
        assert data.description == "Updated desc"

    def test_project_update_status(self):
        data = ProjectUpdate(status="completed")
        assert data.status == "completed"


class TestComponentSchemas:
    def test_component_create_valid(self):
        data = ComponentCreate(name="Resistor", category="resistor")
        assert data.name == "Resistor"
        assert data.datasheet_url is None

    def test_component_create_full(self):
        data = ComponentCreate(name="2N2222", category="transistor",
                               manufacturer="NXP", datasheet_url="http://example.com/ds.pdf")
        assert data.manufacturer == "NXP"

    def test_component_update(self):
        data = ComponentUpdate(name="Updated Resistor")
        assert data.name == "Updated Resistor"

    def test_component_update_empty(self):
        data = ComponentUpdate()
        assert data.model_dump(exclude_unset=True) == {}


class TestConversationSchemas:
    def test_conversation_create_default_title(self):
        data = ConversationCreate()
        assert data.title == "New Chat"

    def test_conversation_create_custom_title(self):
        data = ConversationCreate(title="My Chat")
        assert data.title == "My Chat"

    def test_add_message_request(self):
        data = AddMessageRequest(role="user", content="Hello!")
        assert data.content == "Hello!"

    def test_add_message_request_empty_content(self):
        data = AddMessageRequest(role="user", content="")
        assert data.content == ""
