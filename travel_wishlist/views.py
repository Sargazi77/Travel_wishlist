from django.contrib.auth.models import User
from django.shortcuts import render,redirect,get_object_or_404
from .models import Place
from .forms import NewPlaceForm, TripReviewForm 
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages
@login_required
def place_list(request):
    if request.method == 'POST':
        form = NewPlaceForm(request.POST)
        place = form.save(commit=False) #creating a form from data
        place.user=request.user
        if form.is_valid():
            place.save()
            return redirect('place_list')
    places = Place.objects.filter(user = request.user).filter(visited=False).order_by('name')
    new_place_form = NewPlaceForm()
    return render(request, 'travel_wishlist/wishlist.html', { 'places': places, 'new_place_form': new_place_form })
@login_required
def about(request):
    author = 'Moe'
    about = 'A website to create a list of places to visit'
    return render (request,'travel_wishlist/about.html',{'author': author, 'about':about})

@login_required
def places_visited(request):
    visited = Place.objects.filter(visited=True)
    return render(request, 'travel_wishlist/visited.html', { 'visited': visited })
@login_required
def place_was_visited(request, place_pk):
    if request.method == 'POST':
        place = get_object_or_404(Place, pk=place_pk)
        if place.user == request.user:
            place.visited = True 
            place.save()
        else:
            return HttpResponseForbidden()    
    
    return redirect('place_list')    
@login_required
def place_details(request, place_pk):



    place = get_object_or_404(Place, pk=place_pk)
    #Does this place blong to the current user?
    if place.user != request.user:
        return HttpResponseForbidden()

        # Is this a get request (Show data + form) , or a POST request (update place object)


        #if POST request validates from update and data
    if request.method == 'POST':
        form = TripReviewForm(request.POST, request.FILES, instance=place)
        if form.is_valid():
            form.save()
            messages.info(request, 'Trip information updated! ')
        else:
            messages.error(request, form.errors)    #temprory, refine later

        return redirect('place_details', place_pk=place_pk)

    else:
        #if GET request , show Place info and optional form
        #if place is visited show the form and if not no form    
        if place.visited:
            review_form= TripReviewForm(instance=place)
            return render(request, 'travel_wishlist/place_details.html', {'place': place, 'review_form': review_form})
        else:    
            return render(request, 'travel_wishlist/place_details.html', {'place': place})
@login_required
def delete_place(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)
    if place.user == request.user:
        place.delete()
        return redirect('place_list')
    else:
        return HttpResponseForbidden() 

