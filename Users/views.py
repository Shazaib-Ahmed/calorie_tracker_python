from datetime import datetime
from django.shortcuts import get_object_or_404, render,redirect
from django.http import HttpResponse
from django.template import loader
from .models import User,FoodData,ActivityData
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse
from django.contrib import messages
import Users
from django.db.models import Sum
from django.contrib.sessions.models import Session
from django.core import serializers
from django.utils import timezone

def signup(request):
    template = loader.get_template('sign-up.html')
    return HttpResponse(template.render())


def user_list(request):
    users = User.objects.all()
    return render(request, 'user-list.html', {'users': users})


def signUpBtnClick(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        weight = request.POST.get('weight')
        height = request.POST.get('height')
        gender = request.POST.get('gender')
        age = request.POST.get('age')
        
        user = User.objects.create(
            name=name,
            weight=weight,
            height=height,
            sex=gender,
            age=age
        )
        return redirect('user_list')
    else:
        return render(request, 'sign-up.html')
    

def save_food_data(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')  
        food = request.POST.get("food")
        date = request.POST.get("date")
        food_group = request.POST.get("food_group")
        meal_type = request.POST.get("meal_type")
        serving = request.POST.get("serving")
        calorie = request.POST.get("calorie")

        user = User.objects.get(id=user_id)

        foodData = FoodData.objects.create(
            user=user,                   
            food=food,
            date=date,
            food_group=food_group,
            meal_type=meal_type,
            serving=serving,
            calorie=calorie,
        )
        return redirect(request.META.get('HTTP_REFERER', 'user'))
    return redirect(request.META.get('HTTP_REFERER', 'user'))


def save_activity_data(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')  
        activityName = request.POST.get("activityName")
        date = request.POST.get("date")
        activityDescription = request.POST.get("activityDescription")
        metValue = request.POST.get("metValue")
        duration = request.POST.get("duration")

        user = User.objects.get(id=user_id)

        activityData = ActivityData.objects.create(
            user = user,
            activity_name = activityName,
            date = date,
            activity_description = activityDescription,
            met_value = metValue,
            duration = duration
        )
        return redirect(request.META.get('HTTP_REFERER', 'user'))   
    else:
        form = FoodForm()
    return render(request, 'your_template.html', {'form': form})


def view_user_data(request,id):
    user = User.objects.get(id=id)


    
    food_data = FoodData.objects.filter(user=user)
    activity_data = ActivityData.objects.filter(user=user)

        
    food_data_by_date = food_data.values('date').annotate(total_calorie_in=Sum('calorie_in'))
    activity_data_by_date = activity_data.values('date').annotate(total_calorie_out=Sum('calorie_out'))

       
    data_by_date = {}
    for entry in food_data_by_date:
        date = entry['date']
        data_by_date[date] = {'date': date, 'calorie_in': entry['total_calorie_in']}

    for entry in activity_data_by_date:
        date = entry['date']
        if date in data_by_date:
            data_by_date[date]['calorie_out'] = entry['total_calorie_out']
        else:
             data_by_date[date] = {'date': date, 'calorie_out': entry['total_calorie_out']}

       
    user_bmr = User.objects.get(id=id).bmr
    user_name = User.objects.get(id=id).name


       
    for date, data in data_by_date.items():
         data['calorie_in'] = data.get('calorie_in', 0)  
         data['calorie_out'] = data.get('calorie_out', 0)
         data['net_calorie'] = data['calorie_in'] - user_bmr - data['calorie_out']
         data['bmr'] = user_bmr
         print(date)

        
    return render(request, 'view-user-data.html',{'data_by_date': data_by_date,'user':user})
  
def view_date_data(request):
    selected_date = None
    user = None

    if request.method == 'POST':
        selected_date_str = request.POST.get('selected_date')
        user_id = request.POST.get('user_id')

        print(user_id)
        user = User.objects.get(id=user_id)

        selected_date = datetime.strptime(selected_date_str, '%B %d, %Y').date()
        food_data = FoodData.objects.filter(user=user, date=selected_date)
        activity_data = ActivityData.objects.filter(user=user, date=selected_date)
        calorie_in_sum = food_data.aggregate(total_calorie_in=Sum('calorie_in'))['total_calorie_in']
        calorie_out_sum = activity_data.aggregate(total_calorie_out=Sum('calorie_out'))['total_calorie_out']
        if calorie_in_sum is None:
            calorie_in_sum = 0  
        if calorie_out_sum is None:
            calorie_out_sum = 0 

        net_calorie = calorie_in_sum - user.bmr - calorie_out_sum

     
        selected_date_str = selected_date.strftime('%Y-%m-%d')

       
        request.session['selected_date'] = selected_date_str
        request.session['user_id'] = user_id 

    elif request.method == 'GET':  
        selected_date_str = request.GET.get('selected_date')
        if selected_date_str:
            selected_date = timezone.datetime.strptime(selected_date_str, '%Y-%m-%d').date()
            user_id = request.GET.get('user_id')  
            user = User.objects.get(id=user_id)
            food_data = FoodData.objects.filter(user=user, date=selected_date)
            activity_data = ActivityData.objects.filter(user=user, date=selected_date)
            calorie_in_sum = food_data.aggregate(total_calorie_in=Sum('calorie_in'))['total_calorie_in']
            calorie_out_sum = activity_data.aggregate(total_calorie_out=Sum('calorie_out'))['total_calorie_out']
            if calorie_in_sum is None:
                calorie_in_sum = 0  
            if calorie_out_sum is None:
                calorie_out_sum = 0 
            
            net_calorie = calorie_in_sum - user.bmr - calorie_out_sum

            
            request.session['selected_date'] = selected_date_str
            request.session['user_id'] = user_id  

    elif 'selected_date' in request.session:
        selected_date_str = request.session['selected_date']
        selected_date = timezone.datetime.strptime(selected_date_str, '%Y-%m-%d').date()
        user_id = request.session['user_id']  
        user = User.objects.get(id=user_id)
        food_data = FoodData.objects.filter(user=user, date=selected_date)
        activity_data = ActivityData.objects.filter(user=user, date=selected_date)
        calorie_in_sum = food_data.aggregate(total_calorie_in=Sum('calorie_in'))['total_calorie_in']
        calorie_out_sum = activity_data.aggregate(total_calorie_out=Sum('calorie_out'))['total_calorie_out']
        if calorie_in_sum is None:
            calorie_in_sum = 0  
        if calorie_out_sum is None:
            calorie_out_sum = 0 
        
        net_calorie = calorie_in_sum - user.bmr - calorie_out_sum


    print(activity_data)

    return render(request, 'view-date-data.html', {'food_data': food_data, 'selectedDate': selected_date , 'activity_data': activity_data, 'user': user, 'calorieIn': calorie_in_sum, 'calorieOut': calorie_out_sum, 'netCalorie': net_calorie })


def delete_user(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user = get_object_or_404(User, id=user_id)
        user.delete()
        return redirect('user_list')
    else:
        return redirect('user_list')





