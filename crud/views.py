from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import Genders,Users

# Create your views here.

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

      Genders.objects.create(gender=gender).save()
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

def add_user(request):
  try:
    if request.method == 'POST':
      fullName = request.POST.get('full_name')
      gender = request.POST.get('gender')
      birthdate = request.POST.get('birthdate')
      address = request.POST.get('address')
      contactNumber = request.POST.get('contact_number')
      email = request.POST.get('email') 
      username = request.POST.get('username') 
      password = request.POST.get('password')
      confirm_Password = request.POST.get('confirm_password')

      # if password != confirm_Password:
      #   messages.error(request, 'Password and Confirm Password do not match!')
      #   return redirect('/user/add')  
    
      Users.objects.create(
        full_name=fullName,
        gender=Genders.objects.get(pk=gender),
        birthdate=birthdate,
        address=address,
        contact_numbers=contactNumber,
        email=email,
        username=username,
        password=password 
      ).save()

      messages.success(request, 'User added successfully!')
      return redirect('/user/add')
    else:
      genderObj = Genders.objects.all()

      data ={
        'genders': genderObj
      }

    return render(request, 'user/AddUser.html', data)
  except Exception as e:
    return HttpResponse(f'Error occurred during add user: {e}')