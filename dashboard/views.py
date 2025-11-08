from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegistrationForm, UploadForm
from .models import UploadedFile, ActivityLog
from dashboard.utils.security_utils import encrypt_file, decrypt_file
from dashboard.utils.malware_scan import scan_file
from dashboard.utils.file_organizer import organize_file
from dashboard.utils.log_utils import add_log
from django.conf import settings
import os

# ---------- USER REGISTRATION ----------
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful! Please log in.")
            return redirect('login')
        else:
            messages.error(request, form.errors.as_json())
    else:
        form = RegistrationForm()
    return render(request, 'dashboard/register.html', {'form': form})


# ---------- LOGIN ----------
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            add_log(user, "Logged in")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid credentials")
    return render(request, 'dashboard/login.html')


# ---------- LOGOUT ----------
def logout_view(request):
    add_log(request.user, "Logged out")
    logout(request)
    return redirect('login')


# ---------- DASHBOARD ----------
@login_required
def dashboard_view(request):
    files = UploadedFile.objects.filter(user=request.user)
    logs = ActivityLog.objects.filter(user=request.user).order_by('-timestamp')[:10]
    return render(request, 'dashboard/dashboard.html', {'files': files, 'logs': logs})


# ---------- UPLOAD FILE ----------
@login_required
def upload_file(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded = form.save(commit=False)
            uploaded.user = request.user
            uploaded.save()

            file_path = uploaded.file.path
            try:
                new_path = organize_file(file_path, base_dir="uploads")
                uploaded.file.name = os.path.relpath(new_path, settings.MEDIA_ROOT)
                uploaded.save()
            except Exception as e:
                messages.warning(request, f"File organization failed: {e}")

            scan = scan_file(new_path)
            uploaded.scan_result = scan["result"]
            uploaded.save()

            messages.success(request, f"File uploaded and scanned ({scan['result']})")
            add_log(request.user, f"Uploaded {uploaded.file.name}")
            return redirect('dashboard')
    else:
        form = UploadForm()
    return render(request, 'dashboard/upload.html', {'form': form})


# ---------- ENCRYPT ----------
@login_required
def encrypt_file_view(request, file_id):
    file = get_object_or_404(UploadedFile, id=file_id, user=request.user)
    try:
        enc_path = encrypt_file(file.file.path)
        organize_file(enc_path, "encrypted")
        file.status = True
        file.save()
        add_log(request.user, f"Encrypted {file.file.name}")
        messages.success(request, "File encrypted successfully.")
    except Exception as e:
        messages.error(request, f"Error encrypting: {e}")
    return redirect('dashboard')


# ---------- DECRYPT ----------

@login_required
def decrypt_file_view(request, file_id):
    obj = get_object_or_404(UploadedFile, id=file_id, user=request.user)

    # Map to encrypted path.
    stored_path = obj.file.path
    if os.sep + "encrypted" + os.sep in stored_path:
        enc_path = stored_path
    else:
        enc_path = stored_path.replace(os.sep + "uploads" + os.sep, os.sep + "encrypted" + os.sep)

    print("[VIEW] decrypt requested, stored_path:", stored_path)
    print("[VIEW] calculated enc_path:", enc_path)

    if not os.path.exists(enc_path):
        messages.error(request, f"Encrypted file not found: {enc_path}")
        return redirect('dashboard')

    try:
        dest_path = decrypt_file(enc_path)   # single-arg call
        # update model to point to decrypted version if you want
        obj.encrypted = False
        obj.file.name = os.path.relpath(dest_path, settings.MEDIA_ROOT)
        obj.save()
        add_log(request.user, f"Decrypted {enc_path} -> {dest_path}")
        messages.success(request, f"Decrypted and saved to: {dest_path}")
    except Exception as e:
        messages.error(request, f"Error decrypting file: {e}")
        print("[ERROR] decrypt exception:", e)

    return redirect('dashboard')



# ---------- DELETE ----------
@login_required
def delete_file(request, file_id):
    file = get_object_or_404(UploadedFile, id=file_id, user=request.user)
    file.delete()
    add_log(request.user, f"Deleted {file.file.name}")
    messages.success(request, "File deleted successfully.")
    return redirect('dashboard')


# ---------- SCAN ----------
@login_required
def scan_file_view(request, file_id):
    file = get_object_or_404(UploadedFile, id=file_id, user=request.user)
    try:
        result = scan_file(file.file.path)
        file.scan_result = result["result"]
        file.save()
        messages.success(request, f"Scan result: {result['result']}")
        add_log(request.user, f"Scanned {file.file.name}")
    except Exception as e:
        messages.error(request, f"Error scanning file: {e}")
    return redirect('dashboard')
