from typing import Any, Dict
from django.db.models.query import QuerySet
from django.contrib.auth import get_user_model
from django.views.generic import (
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
    ListView
)
from django.urls import reverse_lazy
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin
)
from accounts.models import Role, Team
from .models import Issue, Priority, Status

class IssueCreateView(LoginRequiredMixin, CreateView):
    template_name = "issues/new.html"
    model = Issue
    fields = ["summary", "body", "assignee", "status", "priority"]

    def test_func(self):
        po_role = Role.objects.get(name="product owner")
        return self.request.user.role == po_role

    def form_valid(self, form):
        form.instance.reporter = self.request.user
        return super().form_valid(form)
    
class IssueDetailView(LoginRequiredMixin, DetailView):
    template_name = "issues/detail.html"
    model = Issue

class IssueUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = "issues/edit.html"
    model = Issue
    fields = ["summary", "body", "assignee", "status", "priority"]

    def test_func(self):
        issue = self.get_object()
        return issue.reporter == self.request.user

class IssueDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = "issues/delete.html"
    model = Issue
    success_url = reverse_lazy("list")

    def test_func(self):
        issue = self.get_object()
        return issue.reporter == self.request.user
    
class IssueListView(LoginRequiredMixin, ListView):
    template_name = "issues/list.html"
    model = Issue

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team_list = Team.objects.all()
        User = get_user_model()

        team_issues = {}
        for team in team_list:
            team_issues[team.name] = Issue.objects.filter(
                assignee_team=team,
                assignee_in=User.objects.filter(team=team)).order_by("-priority")
        context["team_issues"] = team_issues
        return context

        ## return post.reporter == self.request.user
