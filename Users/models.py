from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    weight = models.FloatField()
    height = models.FloatField()
    sex = models.CharField(max_length=10)
    age = models.PositiveIntegerField()  # Field to store age
    bmr = models.FloatField(null=True, blank=True) 

    def save(self, *args, **kwargs):
        print(f"Weight: {self.weight}, Height: {self.height}, Age: {self.age}")  # Add this line
        if self.sex.lower() == 'male':
            self.bmr = round(66.4730 + (13.7516 * float(self.weight)) + (5.0033 * float(self.height)) - (6.7550 * float(self.age)), 2)
        elif self.sex.lower() == 'female':
            self.bmr =round( 655.0955 + (9.5634 * float(self.weight)) + (1.8496 * float(self.height)) - (4.6756 * float(self.age)), 2)
        super().save(*args, **kwargs)



class FoodData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food = models.CharField(max_length=100)
    date = models.DateField()
    food_group = models.CharField(max_length=50)
    meal_type = models.CharField(max_length=50)
    serving = models.FloatField()
    calorie = models.FloatField()  # New field for calorie per serving
    calorie_in = models.FloatField(blank=True, null=True)  # Allow null initially

    def save(self, *args, **kwargs):
        self.calorie_in = float(self.serving) * float(self.calorie)
        print(self.calorie_in, self.calorie , self.food)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.name}'s {self.food} on {self.date}"
    


class ActivityData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_name = models.CharField(max_length=255)
    date = models.DateField()
    activity_description = models.CharField(max_length=2000)
    met_value = models.FloatField()
    duration = models.FloatField()
    calorie_out = models.FloatField(blank=True, null=True)  
    def save(self, *args, **kwargs):
        duration_hours = float(self.duration) / 60.0
        user_weight_kg = float(self.user.weight) 
        self.calorie_out = round(float(self.met_value) * float(user_weight_kg) * float(duration_hours), 2)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.name}'s {self.activity_description} on {self.date}"