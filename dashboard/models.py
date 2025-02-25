from django.db import models
from django.core.validators import RegexValidator
# Create your models here.

phone_regex = RegexValidator(
    regex=r'^(?:\+98|0)?9\d{9}$', 
    message="شماره تلفن صحیح نیست"
)

class Idea(models.Model):
    title = models.CharField(max_length=255, verbose_name="عنوان ایده نوآورانه")
    goal = models.CharField(max_length=255, verbose_name="هدف ایده")
    importance = models.TextField(verbose_name="ضرورت و اهمیت ایده")
    details = models.TextField(verbose_name="توضیحات تکمیلی")
    date = models.DateField(verbose_name="تاریخ")
    identifier = models.PositiveIntegerField(verbose_name="شماره")
    is_in_meeting = models.BooleanField(default=False, verbose_name="در حال ارزیابی")
    judge1_score = models.PositiveIntegerField(null=True, blank=True, verbose_name="امتیاز داور اول")
    judge2_score = models.PositiveIntegerField(null=True, blank=True, verbose_name="امتیاز داور دوم")
    judge3_score = models.PositiveIntegerField(null=True, blank=True, verbose_name="امتیاز داور سوم")
    judge4_score = models.PositiveIntegerField(null=True, blank=True, verbose_name="امتیاز داور چهارم")
    final_average = models.FloatField(null=True, blank=True, verbose_name="میانگین نهایی")
    is_finally_approved = models.BooleanField(default=False, verbose_name="تایید نهایی")

    verification = models.CharField(
        max_length=10, choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('rejected', 'Rejected')],
        default='pending', verbose_name="وضعیت تایید"
    )

    def calculate_average(self):
        scores = [self.judge1_score, self.judge2_score, self.judge3_score, self.judge4_score]
        valid_scores = [score for score in scores if score is not None]
        if valid_scores:
            return sum(valid_scores) / len(valid_scores)
        return None
    
    def save(self, *args, **kwargs):
        self.final_average = self.calculate_average()
        if self.final_average is not None and self.final_average >= 14:
            self.is_finally_approved = True
        else:
            self.is_finally_approved = False
        super().save(*args, **kwargs)
    

    def __str__(self):
        return self.title


class Proposal(models.Model):
    titleFa = models.CharField(max_length=255, verbose_name="عنوان فارسی")
    titleEn = models.CharField(max_length=255, verbose_name="عنوان انگلیسی")
    keyWords = models.TextField(verbose_name="کلمات کلیدی")
    projectType = models.CharField(max_length=100, choices=[
        ('research', 'پروژه پژوهشی'),
        ('phd', 'پایان نامه دکتری'),
        ('master', 'پایان نامه کارشناسی ارشد')
    ], verbose_name="نوع پروژه")
    research_pole = models.CharField(max_length=255, verbose_name="قطب پژوهشی")
    research_pole_username = models.CharField(max_length=255, verbose_name="نام موسسه")
    developer = models.CharField(max_length=255, verbose_name="توسعه دهنده")
    costumer = models.CharField(max_length=255, verbose_name="متقاضی")
    nameAndNumberofPlan = models.CharField(max_length=255, verbose_name="نام و شماره طرح")
    #irst_nameAndLast_name = models.CharField(max_length=255, verbose_name="First and Last Name")
    #work_place = models.CharField(max_length=255, verbose_name="Workplace")
    #major = models.CharField(max_length=255, verbose_name="Major")
    #work_address = models.TextField(verbose_name="Work Address")
    #job = models.CharField(max_length=255, verbose_name="Job")
    #work_phone = models.CharField(max_length=15, verbose_name="Work Phone")
    #email = models.EmailField(verbose_name="Email Address")
    #phone = models.CharField(max_length=15, verbose_name="Phone Number")

'''
class User(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="نام")  
    last_name = models.CharField(max_length=100, verbose_name="نام خانوادگی")
    work_place = models.CharField(max_length=100, verbose_name="محل اشتغال")
    major = models.CharField(max_length=100, verbose_name="رشته تحصیلی")
    email = models.EmailField(verbose_name="ایمیل")
    phone = models.CharField(max_length=15, verbose_name="شماره تماس")
    nationalID = models.CharField(max_length=10, null=True, blank=True, verbose_name="کد ملی")'''