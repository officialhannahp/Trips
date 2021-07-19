from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt

def main(request):
    return render(request, 'login.html')



def register(request):
    #reg errors
    errors = User.objects.user_validator(request.POST)

    if len(errors) > 0:
        for k, v in errors.items():
            messages.error(request, v)
        return redirect('/')

    #password hashing
    pw = request.POST['pw']
    pw_hash = bcrypt.hashpw(pw.encode(), bcrypt.gensalt()).decode()
    print(pw_hash)

    #creating a new user
    print(request.POST)
    new_user =  User.objects.create(
        f_name = request.POST['f_name'],
        l_name = request.POST['l_name'],
        email = request.POST['email'],
        pw = pw_hash
    )
    request.session['user_id'] = new_user.id
    return redirect('/dashboard')



def login(request):
    matching_email = User.objects.filter(email=request.POST['email']).first()
    print(matching_email)

    errors = User.objects.login_validator(request.POST)

    if len(errors) > 0:
            for k, v in errors.items():
                messages.error(request, v)
            return redirect('/')

    request.session['sEmail'] = request.POST['email']

    if matching_email is not None:
        #from vid
        # if matching_email.pw == request.POST['pw']:
        if bcrypt.checkpw (request.POST['pw'].encode(), matching_email.pw.encode()):
            request.session['user_id'] = matching_email.id

            return redirect('/dashboard')

        else:
            print('pw incorrect')
            messages.add_messages(request, messages.ERROR, "invalid Credentials.")
            return redirect('/')
    else:
        print ('no user found')
        return redirect('/')



def dashboard(request):

    if 'user_id' not in request.session:
        return redirect('/')

    context = {
        'user' : User.objects.get(id=request.session['user_id']), 
        'new_trip' : Trip.objects.all()
    }

    
    return render(request, 'dashboard.html', context)



def new(request):
    user = User.objects.get(id=request.session['user_id'])

    context = {
        'user' : user,
    }

    return render(request, 'new.html', context)


def create(request):
    errors = Trip.objects.trip_validator(request.POST)

    if len(errors) > 0:
        for k, v in errors.items():
            messages.error(request, v)
        return redirect('/new')

    else:
        current_user = User.objects.get(id=request.session['user_id'])
        new_trip =  Trip.objects.create(
            destination = request.POST['destination'],
            start_date = request.POST['start_date'],
            end_date = request.POST['end_date'],
            plan = request.POST['plan'],
            user = current_user
        )
        request.session['new_trip_id'] = new_trip.id

        return redirect('/dashboard')



def delete(request, trip_id):
    trip = Trip.objects.get(id=trip_id)
    trip.delete()
    return redirect('/dashboard')



def trip_info(request, trip_id):
    trip = Trip.objects.get(id=trip_id)
    user = User.objects.get(id=request.session['user_id'])

    context = {
        'user' : user,
        'trip' : trip,
    }
    return render(request, 'show.html', context)



def edit(request, trip_id):
    trip = Trip.objects.get(id=trip_id)
    user = User.objects.get(id=request.session['user_id'])

    context = {
        'user' : user,
        'trip' : trip,
    }
    return render(request, 'edit.html', context)



def update(request, trip_id):
    errors = Trip.objects.trip_validator(request.POST)
    trip =  Trip.objects.get(id=trip_id)

    if len(errors) > 0:
        for k, v in errors.items():
            messages.error(request, v)
        return redirect(f'/trips/edit/{trip.id}')

    else:
        trip =  Trip.objects.get(id=trip_id)
        trip.destination = request.POST['destination']
        trip.start_date = request.POST['start_date']
        trip.end_date = request.POST['end_date']
        trip.plan = request.POST['plan']
        trip.save()
        return redirect('/dashboard')



def logout(request):
    request.session.clear()
    return redirect('/')



def wipeDB(request):
    User.objects.all().delete()
    return redirect('/')