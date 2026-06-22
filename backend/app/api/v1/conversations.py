from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db, get_current_user
from app.models.user import User
from app.models.conversation import Conversation
from app.schemas.conversation import (
    ConversationCreate,
    ConversationUpdate,
    ConversationResponse,
    ConversationSummary,
    ConversationList,
    AddMessageRequest,
)
from app.db.repository import BaseRepository

router = APIRouter(tags=["conversations"])


def _summary(conv: Conversation) -> dict:
    return {
        "id": conv.id,
        "user_id": conv.user_id,
        "title": conv.title,
        "model": conv.model,
        "message_count": len(conv.messages) if conv.messages else 0,
        "created_at": conv.created_at.isoformat() if conv.created_at else None,
        "updated_at": conv.updated_at.isoformat() if conv.updated_at else None,
    }


@router.get("")
async def list_conversations(
    q: str = "",
    skip: int = 0,
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = BaseRepository(Conversation, db)
    convs = await repo.get_multi(
        skip=skip,
        limit=limit,
        filters={"user_id": current_user.id},
        order_by=Conversation.updated_at.desc(),
        search=q if q else None,
        search_fields=["title"],
    )
    total = await repo.count(
        filters={"user_id": current_user.id},
        search=q if q else None,
        search_fields=["title"],
    )
    return ConversationList(
        items=[ConversationSummary(**_summary(c)) for c in convs],
        total=total,
    )


@router.post("", status_code=201)
async def create_conversation(
    body: ConversationCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = BaseRepository(Conversation, db)
    conv = await repo.create(
        user_id=current_user.id,
        title=body.title,
        messages=body.messages,
        model=body.model,
    )
    return ConversationResponse(
        id=conv.id,
        user_id=conv.user_id,
        title=conv.title,
        messages=conv.messages,
        model=conv.model,
        created_at=conv.created_at,
        updated_at=conv.updated_at,
    )


@router.get("/{conversation_id}")
async def get_conversation(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = BaseRepository(Conversation, db)
    conv = await repo.get(conversation_id)
    if not conv or conv.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return ConversationResponse(
        id=conv.id,
        user_id=conv.user_id,
        title=conv.title,
        messages=conv.messages,
        model=conv.model,
        created_at=conv.created_at,
        updated_at=conv.updated_at,
    )


@router.put("/{conversation_id}")
async def update_conversation(
    conversation_id: int,
    body: ConversationUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = BaseRepository(Conversation, db)
    conv = await repo.get(conversation_id)
    if not conv or conv.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Conversation not found")
    kwargs = {k: v for k, v in body.model_dump(exclude_none=True).items() if v is not None}
    if kwargs:
        conv = await repo.update(conversation_id, **kwargs)
    return ConversationResponse(
        id=conv.id,
        user_id=conv.user_id,
        title=conv.title,
        messages=conv.messages,
        model=conv.model,
        created_at=conv.created_at,
        updated_at=conv.updated_at,
    )


@router.delete("/{conversation_id}", status_code=204)
async def delete_conversation(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = BaseRepository(Conversation, db)
    conv = await repo.get(conversation_id)
    if not conv or conv.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Conversation not found")
    await repo.delete(conversation_id)


@router.post("/{conversation_id}/messages")
async def add_message(
    conversation_id: int,
    body: AddMessageRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = BaseRepository(Conversation, db)
    conv = await repo.get(conversation_id)
    if not conv or conv.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Conversation not found")
    messages = list(conv.messages or [])
    messages.append({"role": body.role, "content": body.content})
    if len(messages) == 1:
        title = body.content[:80]
        conv = await repo.update(conversation_id, messages=messages, title=title)
    else:
        conv = await repo.update(conversation_id, messages=messages)
    return ConversationResponse(
        id=conv.id,
        user_id=conv.user_id,
        title=conv.title,
        messages=conv.messages,
        model=conv.model,
        created_at=conv.created_at,
        updated_at=conv.updated_at,
    )


@router.put("/{conversation_id}/title")
async def update_title(
    conversation_id: int,
    body: dict,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    title = body.get("title", "")
    if not title:
        raise HTTPException(status_code=400, detail="Title is required")
    repo = BaseRepository(Conversation, db)
    conv = await repo.get(conversation_id)
    if not conv or conv.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Conversation not found")
    await repo.update(conversation_id, title=title)
    return {"status": "ok"}
