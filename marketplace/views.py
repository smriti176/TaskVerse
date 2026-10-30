from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import FreelancerProfileForm, ProjectForm, BidForm,ReviewForm
from .models import FreelancerProfile, Project, Bid, Notification, Review, Message
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.db.models import Avg
from django.contrib.auth.models import User
from .models import FreelancerProfile, Project
from django.core.paginator import Paginator
from django.contrib import messages




def home(request):

    total_users = User.objects.count()

    total_freelancers = FreelancerProfile.objects.count()

    total_projects = Project.objects.count()

    featured_freelancers = FreelancerProfile.objects.all()[:3]

    latest_projects = Project.objects.order_by("-created_at")[:3]

    return render(
        request,
        "marketplace/home.html",
        {
            "total_users": total_users,
            "total_freelancers": total_freelancers,
            "total_projects": total_projects,
            "featured_freelancers": featured_freelancers,
            "latest_projects": latest_projects,
        }
    )


@login_required
def dashboard(request):

    total_projects = Project.objects.filter(
        client=request.user
    ).count()

    total_bids = Bid.objects.filter(
        project__client=request.user
    ).count()

    accepted_bids = Bid.objects.filter(
        project__client=request.user,
        status="Accepted"
    ).count()

    rejected_bids = Bid.objects.filter(
        project__client=request.user,
        status="Rejected"
    ).count()

    pending_bids = Bid.objects.filter(
        project__client=request.user,
        status="Pending"
    ).count()

    return render(
        request,
        "marketplace/dashboard.html",
        {
            "total_projects": total_projects,
            "total_bids": total_bids,
            "accepted_bids": accepted_bids,
            "rejected_bids": rejected_bids,
            "pending_bids": pending_bids,
        }
    )


@login_required
def create_profile(request):

    profile, created = FreelancerProfile.objects.get_or_create(
        user=request.user,
        defaults={
            "name": request.user.get_full_name() or request.user.username,
            "skills": "",
            "experience": 0,
            "portfolio": "",
            "hourly_rate": 0,
            "bio": "",
        }
    )

    if request.method == "POST":

        form = FreelancerProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Profile updated successfully."
            )

            return redirect("freelancer_profile")

    else:

        form = FreelancerProfileForm(instance=profile)

    return render(
        request,
        "marketplace/create_profile.html",
        {
            "form": form
        }
    )

@login_required
def create_project(request):

    if request.method == "POST":

        form = ProjectForm(request.POST)

        if form.is_valid():

            project = form.save(commit=False)

            project.client = request.user

            project.save()

            return redirect("dashboard")

    else:
        form = ProjectForm()

    return render(
        request,
        "marketplace/create_project.html",
        {"form": form}
    )



def project_list(request):

    query = request.GET.get("q")
    category = request.GET.get("category")
    budget = request.GET.get("budget")

    projects = Project.objects.all().order_by("-created_at")

    # Search by title or skills
    if query:
        projects = projects.filter(
            Q(title__icontains=query) |
            Q(skills_required__icontains=query)
        )

    # Filter by category
    if category:
        projects = projects.filter(category=category)

    # Filter by budget
    if budget == "10000":
        projects = projects.filter(budget__lt=10000)

    elif budget == "50000":
        projects = projects.filter(
            budget__gte=10000,
            budget__lte=50000
        )

    elif budget == "50001":
        projects = projects.filter(
            budget__gt=50000
        )

    return render(
        request,
        "marketplace/project_list.html",
        {
            "projects": projects,
            "query": query,
            "category": category,
        }
    )

from django.shortcuts import get_object_or_404

def project_detail(request, pk):

    project = get_object_or_404(Project, id=pk)

    bids = project.bids.all()

    return render(
        request,
        "marketplace/project_detail.html",
        {
            "project": project,
            "bids": bids,
        }
    )

@login_required
def apply_bid(request, project_id):

    project = get_object_or_404(Project, id=project_id)

    if request.method == "POST":

        form = BidForm(request.POST)

        if form.is_valid():

            bid = form.save(commit=False)

            bid.project = project

            bid.freelancer = request.user

            bid.save()

            Notification.objects.create(
              user=project.client,
              message=f"{request.user.username} applied for your project '{project.title}'."
            )

            return redirect("project_detail", project.id)

    else:

        form = BidForm()

    return render(
        request,
        "marketplace/apply_bid.html",
        {
            "form": form,
            "project": project
        }
    )

@login_required
def my_projects(request):

    projects = Project.objects.filter(client=request.user)

    return render(
        request,
        "marketplace/my_projects.html",
        {
            "projects": projects
        }
    )

@login_required
def edit_project(request, project_id):

    project = get_object_or_404(
        Project,
        id=project_id,
        client=request.user
    )

    if request.method == "POST":

        form = ProjectForm(request.POST, instance=project)

        if form.is_valid():
            form.save()
            return redirect("my_projects")

    else:
        form = ProjectForm(instance=project)

    return render(
        request,
        "marketplace/edit_project.html",
        {
            "form": form
        }
    )

@login_required
def delete_project(request, project_id):

    project = get_object_or_404(
        Project,
        id=project_id,
        client=request.user
    )

    if request.method == "POST":
        project.delete()
        return redirect("my_projects")

    return render(
        request,
        "marketplace/delete_project.html",
        {
            "project": project
        }
    )

@login_required
def my_bids(request):

    bids = Bid.objects.filter(freelancer=request.user)

    return render(
        request,
        "marketplace/my_bids.html",
        {
            "bids": bids
        }
    )

@login_required
def accept_bid(request, bid_id):

    bid = get_object_or_404(Bid, id=bid_id)

    if bid.project.client != request.user:
        return redirect("project_detail", pk=bid.project.id)

    Bid.objects.filter(project=bid.project).update(status="Rejected")

    bid.status = "Accepted"
    bid.save()
    Notification.objects.create(
       user=bid.freelancer,
       message=f"Congratulations! Your bid for '{bid.project.title}' has been accepted."
    )

    return redirect("project_detail", pk=bid.project.id)

@login_required
def reject_bid(request, bid_id):

    bid = get_object_or_404(Bid, id=bid_id)

    if bid.project.client != request.user:
        return redirect("project_detail", pk=bid.project.id)

    bid.status = "Rejected"
    bid.save()
    Notification.objects.create(
       user=bid.freelancer,
       message=f"Your bid for '{bid.project.title}' has been rejected."
    )

    return redirect("project_detail", pk=bid.project.id)

@login_required
def close_project(request, project_id):

    project = get_object_or_404(
        Project,
        id=project_id,
        client=request.user
    )

    project.status = "Closed"

    project.save()
    Notification.objects.create(
       user=project.client,
       message=f"Your project '{project.title}' has been closed."
    )

    return redirect(
        "project_detail",
        pk=project.id
    )


@login_required
def open_project(request, project_id):

    project = get_object_or_404(
        Project,
        id=project_id,
        client=request.user
    )

    project.status = "Open"

    project.save()
    Notification.objects.create(
       user=project.client,
       message=f"Your project '{project.title}' has been reopened."
    )

    return redirect(
        "project_detail",
        pk=project.id
    )

@staff_member_required
def admin_dashboard(request):

    context = {
        "users": FreelancerProfile.objects.count(),
        "projects": Project.objects.count(),
        "bids": Bid.objects.count(),
        "open_projects": Project.objects.filter(status="Open").count(),
        "closed_projects": Project.objects.filter(status="Closed").count(),
    }

    return render(
        request,
        "marketplace/admin_dashboard.html",
        context
    )

def freelancer_profile(request, user_id):

    profile = get_object_or_404(
        FreelancerProfile,
        user_id=user_id
    )

    return render(
        request,
        "marketplace/freelancer_profile.html",
        {
            "profile": profile
        }
    )

from django.shortcuts import render, redirect, get_object_or_404

@login_required
def freelancer_profile(request):

    try:
        profile = FreelancerProfile.objects.get(user=request.user)

    except FreelancerProfile.DoesNotExist:

        messages.warning(
            request,
            "Please complete your freelancer profile first."
        )

        return redirect("profile")

    return render(
        request,
        "marketplace/freelancer_profile.html",
        {
            "profile": profile
        }
    )

@login_required
def edit_profile(request):

    profile = request.user.freelancerprofile

    if request.method == "POST":

        form = FreelancerProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Profile updated successfully."
            )

            return redirect("freelancer_profile")

    else:

        form = FreelancerProfileForm(instance=profile)

    return render(
        request,
        "marketplace/edit_profile.html",
        {
            "form": form
        }
    )

@login_required
def notifications(request):

    notifications = Notification.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(
        request,
        "marketplace/notifications.html",
        {
            "notifications": notifications
        }
    )

@login_required
def complete_project(request, project_id):

    project = get_object_or_404(
        Project,
        id=project_id,
        client=request.user
    )

    project.status = "Completed"
    project.save()

    return redirect("project_detail", pk=project.id)

@login_required
def freelancer_list(request):

    freelancers = FreelancerProfile.objects.all()

    return render(
        request,
        "marketplace/freelancer_list.html",
        {
            "freelancers": freelancers
        }
    )

@login_required
def freelancer_profile_detail(request, freelancer_id):

    freelancer = get_object_or_404(
        FreelancerProfile,
        id=freelancer_id
    )

    reviews = Review.objects.filter(
        freelancer=freelancer.user
    ).order_by("-created_at")

    average_rating = reviews.aggregate(
        Avg("rating")
    )["rating__avg"]

    total_reviews = reviews.count()

    return render(
        request,
        "marketplace/freelancer_profile_detail.html",
        {
            "freelancer": freelancer,
            "reviews": reviews,
            "average_rating": average_rating,
            "total_reviews": total_reviews,
        }
    )

@login_required
def leave_review(request, project_id):

    project = get_object_or_404(
        Project,
        id=project_id,
        client=request.user
    )

    # Allow reviews only for completed projects
    if project.status != "Completed":
        return HttpResponse("Project is not completed yet.")

    # Prevent duplicate reviews
    if Review.objects.filter(project=project).exists():
        return HttpResponse("Review already exists for this project.")

    # Find the accepted bid
    accepted_bid = Bid.objects.filter(
        project=project,
        status="Accepted"
    ).first()

    if accepted_bid is None:
        return HttpResponse("No accepted bid found for this project.")

    if request.method == "POST":

        form = ReviewForm(request.POST)

        if form.is_valid():

            review = form.save(commit=False)
            review.project = project
            review.client = request.user
            review.freelancer = accepted_bid.freelancer
            review.save()

            return redirect("project_detail", pk=project.id)

    else:

        form = ReviewForm()

    return render(
        request,
        "marketplace/review.html",
        {
            "form": form,
            "project": project,
        }
    )

@login_required
def completed_projects(request):

    projects = Project.objects.filter(
        client=request.user,
        status="Completed"
    ).order_by("-created_at")

    return render(
        request,
        "marketplace/completed_projects.html",
        {
            "projects": projects
        }
    )

@login_required
def account_settings(request):

    return render(
        request,
        "marketplace/account_settings.html"
    )

@login_required
def project_list(request):

    query = request.GET.get("q")

    projects = Project.objects.all()

    if query:
        projects = projects.filter(
            Q(title__icontains=query) |
            Q(skills_required__icontains=query) |
            Q(category__icontains=query)
        )

    projects = projects.order_by("-created_at")

    paginator = Paginator(projects, 6)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "marketplace/project_list.html",
        {
            "page_obj": page_obj,
            "query": query,
        }
    )

@login_required
def freelancer_list(request):

    freelancers = FreelancerProfile.objects.all().order_by("name")

    paginator = Paginator(freelancers, 6)   # 6 freelancers per page

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "marketplace/freelancer_list.html",
        {
            "page_obj": page_obj,
        }
    )

@login_required
def freelancer_list(request):

    query = request.GET.get("q")

    freelancers = FreelancerProfile.objects.all()

    if query:

        freelancers = freelancers.filter(
            Q(name__icontains=query) |
            Q(skills__icontains=query)
        )

    freelancers = freelancers.order_by("name")

    paginator = Paginator(freelancers, 6)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "marketplace/freelancer_list.html",
        {
            "page_obj": page_obj,
            "query": query,
        }
    )



@login_required
def inbox(request):

    users = User.objects.exclude(id=request.user.id)

    # Add unread message count for each user
    for user in users:
        user.unread = Message.objects.filter(
            sender=user,
            receiver=request.user,
            is_read=False
        ).count()

    context = {
        "users": users,
    }

    return render(
        request,
        "marketplace/messages.html",
        context
    )

@login_required
def chat(request, user_id):

    receiver = get_object_or_404(User, id=user_id)

    chats = (
        Message.objects.filter(
            sender=request.user,
            receiver=receiver
        ) |
        Message.objects.filter(
            sender=receiver,
            receiver=request.user
        )
    ).order_by("timestamp")

    # Mark received messages as read
    Message.objects.filter(
        sender=receiver,
        receiver=request.user,
        is_read=False
    ).update(is_read=True)

    users = User.objects.exclude(id=request.user.id)

    for user in users:
        user.unread = Message.objects.filter(
            sender=user,
            receiver=request.user,
            is_read=False
        ).count()

    return render(
        request,
        "marketplace/messages.html",
        {
            "users": users,
            "receiver": receiver,
            "chats": chats,
        }
    )