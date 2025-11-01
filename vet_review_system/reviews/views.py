from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from transformers import pipeline
from .models import Review, Veterinarian
from .forms import ReviewForm
from django.db.models import Avg, Count, Q

# Load Hugging Face model once
sentiment_analyzer = pipeline("sentiment-analysis")


def home(request):
    return render(request, 'home.html')


@login_required
def veterinarian_list(request):
    vets = Veterinarian.objects.all().order_by('name')
    return render(request, 'reviews/veterinarians.html', {'vets': vets})


@login_required
def add_review(request):
    vet_id = request.GET.get('vet_id')
    vet = get_object_or_404(Veterinarian, id=vet_id) if vet_id else None

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            if vet:
                review.vet = vet
            result = sentiment_analyzer(review.review_text)[0]
            review.sentiment = 1 if result['label'] == 'POSITIVE' else 0
            review.save()
            return render(request, 'reviews/review_result.html', {'review': review, 'result': result})
    else:
        form = ReviewForm(initial={'vet': vet})

    return render(request, 'reviews/add_review.html', {'form': form, 'vet': vet})


def vet_ratings(request):
    vets = (
        Veterinarian.objects.annotate(
            avg_sentiment=Avg('reviews__sentiment'),
            positive_count=Count('reviews', filter=Q(reviews__sentiment__gte=0.5)),
            negative_count=Count('reviews', filter=Q(reviews__sentiment__lt=0.5)),
        )
        .order_by('-avg_sentiment', 'name')
    )
    return render(request, 'reviews/vet_ratings.html', {'vets': vets})


