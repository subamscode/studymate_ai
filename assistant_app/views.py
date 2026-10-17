from pathlib import Path
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .forms import AskQuestionForm, RegisterForm, UploadDocumentForm
from .models import ChatMessage, ChatSession, StudyDocument
from .services import answer_question, index_document, remove_document_chunks
def home(request):
    return redirect("chat") if request.user.is_authenticated else render(request, "assistant_app/home.html")
def register_view(request):
    if request.user.is_authenticated: return redirect("chat")
    form=RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user=form.save(); login(request, user); messages.success(request, "Welcome to StudyMate AI!"); return redirect("chat")
    return render(request, "assistant_app/register.html", {"form":form})
def login_view(request):
    if request.user.is_authenticated: return redirect("chat")
    error=None
    if request.method == "POST":
        user=authenticate(request, username=request.POST.get("username", "").strip(), password=request.POST.get("password", ""))
        if user: login(request, user); return redirect(request.GET.get("next") or "chat")
        error="Username or password is incorrect."
    return render(request, "assistant_app/login.html", {"error":error})
@require_POST
def logout_view(request):
    logout(request); return redirect("home")
@login_required
def chat_view(request, session_id=None):
    if session_id is None:
        session=ChatSession.objects.filter(user=request.user).first() or ChatSession.objects.create(user=request.user)
        return redirect("chat_session", session_id=session.id)
    session=get_object_or_404(ChatSession, id=session_id, user=request.user); form=AskQuestionForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        question=form.cleaned_data["message"].strip()
        if question:
            first=not session.messages.filter(role="user").exists()
            previous=list(session.messages.values("role", "content"))[-8:]
            ChatMessage.objects.create(session=session, role="user", content=question)
            try: answer, _=answer_question(request.user.id, question, previous)
            except Exception as exc:
                answer=f"I could not get an AI response. {exc}"; messages.error(request, "AI connection problem. Check Ollama is running.")
            ChatMessage.objects.create(session=session, role="assistant", content=answer)
            if first: session.title=question[:55]+("…" if len(question)>55 else "")
            session.save(); return redirect("chat_session", session_id=session.id)
    return render(request, "assistant_app/chat.html", {"session":session, "chat_sessions":ChatSession.objects.filter(user=request.user), "messages_list":session.messages.all(), "form":form, "documents":StudyDocument.objects.filter(user=request.user, status="ready")})
@login_required
@require_POST
def new_chat_view(request):
    session=ChatSession.objects.create(user=request.user); return redirect("chat_session", session_id=session.id)
@login_required
def documents_view(request):
    form=UploadDocumentForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        uploaded=form.cleaned_data["file"]
        doc=StudyDocument.objects.create(user=request.user, file=uploaded, original_name=Path(uploaded.name).name)
        try:
            count=index_document(request.user.id, doc.id, doc.file.path); doc.status="ready"; doc.chunk_count=count; doc.save(update_fields=["status", "chunk_count"]); messages.success(request, f"Indexed {doc.original_name} into {count} chunks.")
        except Exception as exc:
            doc.status="failed"; doc.error_message=str(exc); doc.save(update_fields=["status", "error_message"]); messages.error(request, f"Could not process file: {exc}")
        return redirect("documents")
    return render(request, "assistant_app/documents.html", {"form":form, "documents":StudyDocument.objects.filter(user=request.user)})
@login_required
@require_POST
def delete_document_view(request, document_id):
    doc=get_object_or_404(StudyDocument, id=document_id, user=request.user)
    remove_document_chunks(request.user.id, doc.id)
    if doc.file: doc.file.delete(save=False)
    doc.delete(); messages.success(request, "Document deleted."); return redirect("documents")
