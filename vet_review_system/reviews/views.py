from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Review, Veterinarian
from .forms import ReviewForm
from transformers import pipeline
from django.db.models import Avg

# Load Hugging Face model once
sentiment_analyzer = pipeline("sentiment-analysis")

@login_required
def submit_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            result = sentiment_analyzer(review.review_text)[0]
            review.sentiment = 1 if result['label'] == 'POSITIVE' else 0
            review.save()
            return redirect('vet_ratings')
    else:
        form = ReviewForm()
    return render(request, 'reviews/submit_review.html', {'form': form})

def vet_ratings(request):
    vets = Veterinarian.objects.annotate(avg_sentiment=Avg('reviews__sentiment')).order_by('-avg_sentiment')
    return render(request, 'reviews/vet_ratings.html', {'vets': vets})
    
@login_required
def add_review(request):
    from .forms import ReviewForm

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user

            # Run sentiment prediction
            result = sentiment_model(review.review_text)[0]
            review.sentiment = 1 if result['label'] == 'POSITIVE' else 0
            review.save()

            return render(request, 'reviews/review_result.html', {'review': review, 'result': result})
    else:
        form = ReviewForm()

    return render(request, 'reviews/add_review.html', {'form': form})