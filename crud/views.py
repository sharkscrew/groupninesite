from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import Genders,Users
from django.contrib.auth.hashers import make_password, check_password
from django.core.paginator import Paginator

def gender_list(request):
  try:
    genders =Genders.objects.all()

    data = {
      'genders':genders
    }

    return render(request, 'gender/GendersList.html', data)
  except Exception as e:
    return HttpResponse(f'Error occured while loading genders: {e}')

def add_gender(request):
  try:
    if request.method == 'POST':  
      gender=request.POST.get('gender')

      Genders.objects.create(gender=gender)
      messages.success(request, 'Gender added successfully!')
      return redirect('/gender/list')  
    else:
      return render(request,'gender/AddGender.html')
  except Exception as e:
    return HttpResponse(f'Error occurred during add gender: {e}')
  
def edit_gender(request, genderId):
  try:
    if request.method == 'POST':
      genderObj = Genders.objects.get(pk=genderId)

      gender = request.POST.get('gender')

      genderObj.gender = gender
      genderObj.save()

      messages.success(request,  'Gender updated successfully')

      data = {
        'gender' : genderObj
      }

      return render(request, 'gender/EditGender.html', data)
    else:
      genderObj = Genders.objects.get(pk=genderId)

      data = {
        'gender' : genderObj
      }

      return render(request, 'gender/EditGender.html', data)
    
  except Exception as e:
    return HttpResponse(f'Error occured during edit gender: {e}')
  
def delete_gender(request, genderId):
  try: 
    if request.method == 'POST':
      genderObj = Genders.objects.get(pk=genderId)
      genderObj.delete()

      messages.success(request, 'Gender deleted successfully!')
      return redirect('/gender/list')
    
    else:
      genderObj = Genders.objects.get(pk=genderId)

      data = {
        'gender' : genderObj
      }

    return render(request, 'gender/DeleteGender.html', data)
    
  except Exception as e:
    return HttpResponse(f'Error occured during deleting gender: {e}')

def user_list(request):
  try:
    search_query = request.GET.get('search', '')
    userObj = Users.objects.select_related('gender')
    if search_query:
        userObj = userObj.filter(full_name__icontains=search_query)  # Adjust field as needed

    paginator = Paginator(userObj, 10)  # Show 1 users per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    data = {
        'users': page_obj.object_list,
        'page_obj': page_obj,
        'search_query': search_query,
    }

    return render(request, 'user/UsersList.html', data)
  except Exception as e:
    return HttpResponse(f'Error occured while Loading users: {e}')

def add_user(request):
  try:
    if request.method == 'POST':
      full_name = request.POST.get('full_name')
      gender = request.POST.get('gender')
      birthdate = request.POST.get('birthdate')
      address = request.POST.get('address')
      contact_number = request.POST.get('contact_number')
      email = request.POST.get('email') 
      username = request.POST.get('username') 
      password = request.POST.get('password')
      confirm_Password = request.POST.get('confirm_password')

      if password != confirm_Password:
        messages.error(request, 'Password and Confirm Password do not match!')
        return redirect('/user/add')  
    
      Users.objects.create(
        full_name=full_name,
        gender=Genders.objects.get(pk=gender),
        birthdate=birthdate,
        address=address,
        contact_numbers=contact_number,
        email=email,
        username=username,
        password= make_password(password) 
      )

      messages.success(request, 'User added successfully!')
      return redirect('/user/add')
    else:
      genderObj = Genders.objects.all()

      data ={
        'genders': genderObj
      }
      return render(request, 'user/AddUser.html', data)

  except Exception as e:
    messages.error(request, f'Error occured while adding users')
    return redirect('/user/add')
  
def edit_user(request, userId):
  try:
      userObj = Users.objects.get(pk=userId)

      if request.method == 'POST':
          full_name = request.POST.get('full_name')
          gender = request.POST.get('gender')
          birthdate = request.POST.get('birthdate')
          address = request.POST.get('address')
          contact_number = request.POST.get('contact_number')
          email = request.POST.get('email')
          username = request.POST.get('username')
          password = request.POST.get('password')
          confirm_password = request.POST.get('confirm_password')

          if password != confirm_password:
              messages.error(request, 'Password and Confirm Password do not match!')
              return redirect(f'/user/edit/{userId}')

          userObj.full_name = full_name
          userObj.birthdate = birthdate
          userObj.address = address
          userObj.contact_numbers = contact_number
          userObj.email = email
          userObj.username = username

          if password: 
              userObj.password = make_password(password)

          userObj.save()

          messages.success(request, 'User updated successfully!')
          return redirect('/user/list')
      else:
          genders = Genders.objects.all()
          data = {
              'user': userObj,
              'genders': genders
          }
          return render(request, 'user/EditUser.html', data)

  except Exception as e:
      return HttpResponse(f'Error occurred while editing user: {e}')
    
def delete_user(request, userId):
  try:
      userObj = Users.objects.get(pk=userId)

      if request.method == 'POST':
          userObj.delete()
          messages.success(request, 'User deleted successfully!')
          return redirect('/user/list')
      else:
          data = {
              'user': userObj
          }
          return render(request, 'user/DeleteUser.html', data)

  except Exception as e:
      return HttpResponse(f'Error occurred while deleting user: {e}') 

def login_user(request):
  try:
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = Users.objects.get(username=username)
            if check_password(password, user.password):
                request.session['user_id'] = user.user_id
                request.session['user_name'] = user.full_name
                request.session['is_authenticated'] = True

                messages.success(request, 'Login successful!')
                return redirect('/user/list')
            else:
                messages.error(request, 'Invalid username or password')
                return redirect('/user/login?error=1')
        except Users.DoesNotExist:
            messages.error(request, 'User does not exist')
            return redirect('/user/login?error=1')
    else:  
      return render(request, 'user/Login.html')
  except Exception as e:
    messages.error(request, f'An Error Occured:{str(e)}')
    return redirect('/user/login?error=1')