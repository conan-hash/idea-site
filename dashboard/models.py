from django.db import models
from django.core.validators import RegexValidator
from django.conf import settings
from django.core.validators import MaxValueValidator


phone_regex = RegexValidator(
    regex=r'^(?:\+98|0)?9\d{9}$', 
    message="شماره تلفن صحیح نیست"
)



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



class Idea(models.Model):
    title = models.CharField(max_length=255, verbose_name="عنوان ایده نوآورانه")
    keywords = models.CharField(max_length=255, verbose_name='کلمات کلیدی')
    goal = models.CharField(max_length=255, verbose_name="هدف ایده")
    importance = models.TextField(verbose_name="ضرورت و اهمیت ایده")
    details = models.TextField(verbose_name="توضیحات تکمیلی")
    date = models.DateField(verbose_name="تاریخ")
    identifier = models.CharField(max_length=20, verbose_name="شماره")
    proposal = models.OneToOneField(Proposal, null=True, blank=True, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, verbose_name="وضعیت")
    proposal_modifacation = models.BooleanField(default=False, verbose_name="اصلاح پروپوزال")
    judge1 = models.CharField(max_length=255, null=True, blank=True, verbose_name=" داور اول")
    judge2 = models.CharField(max_length=255, null=True, blank=True, verbose_name=" داور دوم")
    judge3 = models.CharField(max_length=255, null=True, blank=True, verbose_name=" داور سوم")
    judge4 = models.CharField(max_length=255, null=True, blank=True, verbose_name=" داور چهارم")
    judge1_score = models.PositiveIntegerField(null=True, blank=True, verbose_name="امتیاز داور اول")
    judge2_score = models.PositiveIntegerField(null=True, blank=True, verbose_name="امتیاز داور دوم")
    judge3_score = models.PositiveIntegerField(null=True, blank=True, verbose_name="امتیاز داور سوم")
    judge4_score = models.PositiveIntegerField(null=True, blank=True, verbose_name="امتیاز داور چهارم")
    

    
    def save(self, *args, **kwargs):
        if not self.pk:  
            date_str = self.date.strftime("%Y%m%d")
            
            same_day_count = Idea.objects.filter(
                date=self.date
            ).count() + 1 
            
            self.identifier = f"{date_str}-{same_day_count:02d}"

        final_average = self.calculate_average()
        if final_average is not None and final_average >= 14:
            self.is_finally_approved = True
        else:
            self.is_finally_approved = False
        super().save(*args, **kwargs)


    def calculate_average(self):
        scores = [self.judge1_score, self.judge2_score, self.judge3_score, self.judge4_score]
        valid_scores = [score for score in scores if score is not None]
        if valid_scores:
            return sum(valid_scores) / len(valid_scores)
        return None

    def __str__(self):
        return self.title



class Contributor(models.Model):
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE, related_name='contributors')
    name = models.CharField(max_length=255)
    contribution_percent_idea = models.PositiveIntegerField(
        help_text="Percentage of contribution",
        validators=[MaxValueValidator(100)]  
    )
    contribution_percent_project = models.PositiveIntegerField(
        help_text="Percentage of contribution",
        validators=[MaxValueValidator(100)]  
    )