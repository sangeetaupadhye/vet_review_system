from django.db import models

# Create your models here.
from django.contrib.auth.models import User


class Veterinarian(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    experience = models.PositiveIntegerField()
    # 👇 remove rating input — we’ll calculate it dynamically
    rating = models.FloatField(default=0, editable=False)

    def __str__(self):
        return self.name

    def update_rating(self):
        """Automatically update average rating based on related reviews."""
        reviews = self.reviews.all()
        if reviews.exists():
            self.rating = sum([r.sentiment for r in reviews]) / len(reviews)
        else:
            self.rating = 0
        self.save()



class Review(models.Model):
    vet = models.ForeignKey(Veterinarian, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review_text = models.TextField()
    sentiment = models.IntegerField(
    choices=[(1, 'Positive'), (0, 'Negative')],
    default=1  # 👈 default value added
)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.vet.name}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.vet.update_rating()  # 👈 update average rating automatically

