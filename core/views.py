import os
import csv
import datetime

from pytz import timezone
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView, logout_then_login
from django.contrib.auth import (
    login, logout, authenticate, update_session_auth_hash
)
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import (
    User,
    InventoryItem,
    ItemNotes,
    ItemStatus,
    Area,
    MapLocation,
    Manufacturer,
    Assignee,
    ApprovalList
)
from .forms import (
    AuthenticationFormWithCaptchaField,
    NewUserForm,
    EditProfileForm,
    ContactForm,
    NoteForm,
    InventoryForm
)
from django.core.mail import EmailMultiAlternatives
from django.urls import reverse_lazy
from .signals import log_user_logout


EST = timezone('US/Eastern')


class PasswordsChangeView(PasswordChangeView):
    model = User
    form_class = PasswordChangeForm
    success_url = reverse_lazy('core:password_changed')


@login_required
def password_changed(request):
    return render(
        request=request,
        template_name='accounts/password_changed.html'
    )


@login_required
def password_change_request(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(
                request,
                "Your password was updated successfully."
            )
            return redirect('core:profile')

    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form': form}
        return render(
            request=request,
            template_name="accounts/password_change.html",
            context=args
        )


def password_reset_complete(request):
    return render(
        request=request,
        template_name='accounts/password_reset_complete.html'
    )


def index(request):
    return render(request=request,
                  template_name="core/index.html"
                  )


@login_required
def inventory(request):
    inventory_list = InventoryItem.objects.all()
    return render(request=request,
                  template_name="core/inventory.html",
                  context={
                      'inventory_list': inventory_list
                  }
                  )


@login_required
def load_areas(request):
    loc = request.GET.get('location')
    areas = Area.objects.all().filter(map_loc_id=loc).order_by('name').values()
    return render(request=request,
                  template_name="core/areasOpts.html",
                  context={
                      'loc': loc,
                      'areas': areas
                  }
                  )


@login_required
def add_item(request):
    stats = ItemStatus.objects.all().values().order_by('name').values()
    areas = Area.objects.all().values().order_by('name').values()
    locations = MapLocation.objects.all().values().order_by('name').values()
    mfgs = Manufacturer.objects.all().order_by('name').values()
    assignees = Assignee.objects.all().order_by('name').values()
    approvers = ApprovalList.objects.all().order_by('name').values()

    if request.method == "POST":
        form = InventoryForm(request.POST)

        if form.is_valid():

            item_to_insert = form.save(commit=False)
            item_to_insert.stat = form.cleaned_data['stat']
            item_to_insert.name = form.cleaned_data['name']
            item_to_insert.description = form.cleaned_data['description']
            item_to_insert.location = form.cleaned_data['location']
            item_to_insert.mfg = form.cleaned_data['mfg']
            item_to_insert.model_no = form.cleaned_data['model_no']
            item_to_insert.serial_no = form.cleaned_data['serial_no']
            item_to_insert.qty = form.cleaned_data['qty']
            item_to_insert.total_cost = form.cleaned_data['total_cost']
            item_to_insert.assigned_to = form.cleaned_data['assigned_to']
            item_to_insert.approved_by = form.cleaned_data['approved_by']
            item_to_insert.approved_date = form.cleaned_data['approved_date']
            item_to_insert.purchase_date = form.cleaned_data['purchase_date']
            item_to_insert.inserted_by = request.user
            item_to_insert.inserted_date = datetime.datetime.now(tz=EST)
            item_to_insert.save()
            messages.success(
                request,
                'New inventory item added successfully!'
            )

            return redirect('core:inventory')

        else:
            return render(
                request=request,
                template_name="core/add_item.html",
                context={"form": form}
            )

    else:
        form = NoteForm()
        return render(
            request=request,
            template_name="core/add_item.html",
            context={
                'stats': stats,
                'areas': areas,
                'locations': locations,
                'mfgs': mfgs,
                'assignees': assignees,
                'approvers': approvers
            }
        )


@login_required
def edit_item(request, id):
    # Obtain record to edit by id
    entry_to_edit = InventoryItem.objects.get(id=id)

    # Obtain list of status in order by name, except the selected value
    # by id from the form
    stat_list = ItemStatus.objects.exclude(
        id=entry_to_edit.stat.pk
    ).order_by('name')

    # Obtain list of locations in order by name, except the selected value
    # by id from the form
    loc_list = MapLocation.objects.exclude(
        id=entry_to_edit.location.pk
    ).order_by('name')

    # Get area
    # current_area = entry_to_edit.location.name
    # lst = (list(current_area.split(" ")))
    # cur_area = lst[0]

    # Obtain list of areas in order by name, except the selected value
    # by id from the form
    area_list = Area.objects.exclude(
        id=entry_to_edit.location.pk
    ).order_by('name')

    # Obtain list of manufacturers in order by name, except the selected value
    # by id from the form
    mfg_list = Manufacturer.objects.exclude(
        id=entry_to_edit.mfg.pk
    ).order_by('name')

    # Obtain list of assignees in order by name, except the selected value
    # by id from the form
    assignee_list = Assignee.objects.exclude(
        id=entry_to_edit.assigned_to.pk
    ).order_by('name')

    # Obtain list of approvers in order by name, except the selected value
    # by id from the form
    approvers_list = ApprovalList.objects.exclude(
        id=entry_to_edit.approved_by.pk
    ).order_by('name')

    if request.method == "POST":
        form = InventoryForm(request.POST, instance=entry_to_edit)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Updated successfully!'
            )
            return redirect('core:inventory')
        else:
            messages.error(
                    request,
                    form.errors
            )
            return redirect('core:inventory')

    else:
        form = InventoryForm(instance=entry_to_edit)
        return render(
            request=request,
            template_name='core/edit_item.html',
            context={
                'stat_list': stat_list,
                'loc_list': loc_list,
                'area_list': area_list,
                'mfg_list': mfg_list,
                'assignee_list': assignee_list,
                'approvers_list': approvers_list,
                'entry_to_edit': entry_to_edit,
                'form': form
            }
        )


@login_required
def notes(request, id):
    item = InventoryItem.objects.get(id=id)
    item_notes = ItemNotes.objects.filter(item=item)

    if request.method == "POST":
        form = NoteForm(request.POST)

        if form.is_valid():

            note_to_insert = form.save(commit=False)
            note_to_insert.item_id = id
            note_to_insert.comment = form.cleaned_data['comment']
            note_to_insert.inserted_by = request.user
            note_to_insert.inserted_date = datetime.datetime.now(tz=EST)
            note_to_insert.save()
            messages.success(
                request,
                'Note added successfully!'
            )

            return redirect('core:notes', id=id)

        else:
            return render(
                request=request,
                template_name="core/notes.html",
                context={
                    'item': item,
                    'item_notes': item_notes
                }
            )

    else:
        form = NoteForm()
        return render(
            request=request,
            template_name="core/notes.html",
            context={
                'item': item,
                'item_notes': item_notes
            }
        )


@login_required
def export_to_excel(request):

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="inventory.csv"'

    writer = csv.writer(response)
    writer.writerow(
        [
            'ID',
            'Status',
            'Item',
            'Description',
            'Model #',
            'Serial #',
            'Qty',
            'Total Cost',
            'Assigned To',
            'Approval Date',
            'Purchase Date',
            'Inserted By Last Name',
            'Inserted By First Name',
            'Inserted Date',
            'Modified By',
            'Modified Date',
            'Approved By',
            'Location',
            'Mfg'
        ]
    )

    items = InventoryItem.objects.all().values_list(
        'id',
        'stat__name',
        'name',
        'description',
        'model_no',
        'serial_no',
        'qty',
        'total_cost',
        'assigned_to',
        'approved_date',
        'purchase_date',
        'inserted_by__last_name',
        'inserted_by__first_name',
        'inserted_date',
        'modified_by',
        'modified_date',
        'approved_by_id__name',
        'location_id__name',
        'mfg_id__name'
    )

    for item in items:
        writer.writerow(item)
    return response


def login_request(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = AuthenticationFormWithCaptchaField(request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                login(request, user)
                messages.success(
                    request,
                    f'{username} logged in successfully.'
                )
                return redirect("core:inventory")

            elif User.objects.filter(
                    username=form.cleaned_data.get('username')).exists():
                user = User.objects.filter(
                    username=form.cleaned_data.get('username')).values()
                if(user[0]['is_active'] is False):
                    messages.info(
                        request,
                        "Contact the administrator to activate your account!"
                    )
                    return redirect("core:login_request")

                else:
                    return render(
                        request=request,
                        template_name="registration/login.html",
                        context={"form": form}
                    )

            else:
                return render(
                    request=request,
                    template_name="registration/login.html",
                    context={"form": form}
                )
        else:
            form = AuthenticationFormWithCaptchaField()
            return render(
                request=request,
                template_name="registration/login.html",
                context={"form": form}
            )
    else:
        messages.info(
            request,
            '''You are already logged in.  You must log out to log in as
            another user.'''
        )
        return redirect("core:index")


def check_username(request):
    username = request.POST.get('username')
    try:
        user = User.objects.get(username=username)
        return HttpResponse('<div id="username-error" class="error">This username already exists!</div>')
    except User.DoesNotExist:
        return HttpResponse('<div id="username-error" class="success">This username is available.</div>')


def check_email(request):
    email = request.POST.get('email')
    try:
        user = User.objects.get(email=email)
        return HttpResponse('<div id="email-error" class="error">This email already exists!</div>')
    except User.DoesNotExist:
        return HttpResponse('<div id="email-error" class="success">This email is available.</div>')


def register(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = NewUserForm(request.POST)
            if form.is_valid():
                form.save()
                first_name = form.cleaned_data.get("first_name")
                last_name = form.cleaned_data.get("last_name")
                username = form.cleaned_data.get("username")
                email = form.cleaned_data.get("email")
                password = form.cleaned_data.get("password1")

                # START AUTOMATICALLY ALLOW USERS TO ACCESS APP
                ''' user = authenticate(username=username, password=password)
                login(request, user)
                form.send_registration_email()
                messages.success(
                    request,
                    f"New account created for {username}."
                )
                messages.success(
                    request,
                    f"Successfully logged in as {username}."
                ) '''
                # END AUTOMATICALLY ALLOW USERS TO ACCESS APP

                # START USER ACTIVE SET TO FALSE BY DEFAULT
                form.send_registration_email()
                messages.info(
                    request,
                    "Email sent to Admin to activate your account."
                )
                # END USER ACTIVE SET TO FALSE BY DEFAULT
                return redirect("core:index")
            else:
                return render(
                    request=request,
                    template_name="registration/register.html",
                    context={"form": form}
                )
        else:

            form = NewUserForm
            return render(
                request=request,
                template_name="registration/register.html",
                context={"form": form}
            )
    else:
        messages.info(
            request,
            '''You are already registered.  You must log out to register
            another user.'''
        )
        return redirect("core:index")


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            fullname = form.cleaned_data.get("fullname")
            contact_email = form.cleaned_data.get("contact_email")
            contact_subject = form.cleaned_data.get("contact_subject")
            contact_message = form.cleaned_data.get("contact_message")

            subject, from_email, to = contact_subject, os.environ.get(
                'MAIL_USERNAME'), os.environ.get('MAIL_RECIPIENTS')
            text_content = f'''
            Message from ...

            Full Name: {fullname}\n
            Email Address: {contact_email}\n
            Contact Message: {contact_message}
            '''
            html_content = f'''
                <p>Message from core App User...</p>

                <p><strong>Full Name:</strong> {fullname}</p>
                <p><strong>Email Address:</strong> {contact_email}</p>
                <p><strong>Message:</strong> {contact_message}</p>
                '''
            msg = EmailMultiAlternatives(
                subject, text_content, from_email, [to]
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            messages.success(
                request,
                "Email sent!  Thank you for contacting us."
            )
            return redirect("core:index")
        else:
            return render(
                request=request,
                template_name="core/contact.html",
                context={"form": form}
            )

    form = ContactForm
    return render(
        request=request,
        template_name="core/contact.html",
        context={"form": form}
    )


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Your profile was updated successfully."
            )
            return redirect('core:edit_profile')

    else:
        form = EditProfileForm(instance=request.user)
        args = {'form': form}
        return render(
            request=request,
            template_name="core/edit_profile.html",
            context=args
        )


@login_required
def logout_request(request):
    return logout_then_login(request, login_url='/')
