from django.db import models
from django.core.validators import RegexValidator
from django.conf import settings
from django.core.validators import MaxValueValidator
from authentication.models import CustomUser
from django.db.models.signals import post_save
from django.dispatch import receiver


phone_regex = RegexValidator(
    regex=r'^(?:\+98|0)?9\d{9}$', 
    message="شماره تلفن صحیح نیست"
)



class Proposal(models.Model):
    projectTitleFa = models.CharField(max_length=255, verbose_name="عنوان فارسی")
    projectTitleEn = models.CharField(max_length=255, verbose_name="عنوان انگلیسی")
    keywords = models.TextField(verbose_name="کلمات کلیدی")
    projectType = models.CharField(max_length=100, choices=[
        ('research', 'پروژه پژوهشی'),
        ('phd', 'پایان نامه دکتری'),
        ('masters', 'پایان نامه کارشناسی ارشد')
    ], verbose_name="نوع پروژه")
    researchPole = models.CharField(max_length=100, choices=[
        ('research', 'پروژه پژوهشی'),
        ('phd', 'پایان نامه دکتری'),
        ('masters', 'پایان نامه کارشناسی ارشد')
    ], verbose_name="قطب پژوهشی")
    researchPoleUsername = models.CharField(max_length=255, verbose_name="نام موسسه")
    developer = models.CharField(max_length=255, verbose_name="توسعه دهنده")
    finalCustomer = models.CharField(max_length=255, verbose_name="متقاضی/مشتری نهایی")
    nameAndNumberofPlan = models.CharField(max_length=255, verbose_name="نام و شماره طرح")
    projectImportance = models.CharField(max_length=100, choices=[
        ('fundamental', 'بنیادی'),
        ('applied', 'کاربردی'),
        ('developmental', 'توسعه ای'),
        ('studies', 'مطالعاتی')
    ], verbose_name="اهمیت پروژه")
    researchGroup = models.CharField(max_length=100, choices=[
        ('research', 'پروژه پژوهشی'),
        ('phd', 'پایان نامه دکتری'),
        ('masters', 'پایان نامه کارشناسی ارشد')
    ], verbose_name="گروه پژوهشی")
    chiefName = models.CharField(max_length=255, verbose_name="نام رئیس گروه پژوهشی")
    teamName = models.CharField(max_length=255, verbose_name="نام تیم پژوهشی")
    secretaryName = models.CharField(max_length=255, verbose_name="نام دبیر تیم پژوهشی")
    projectScale = models.CharField(max_length=100, choices=[
        ('feasibility', 'امکان سنجی'),
        ('lab', 'آزمایشگاهی'),
        ('small', 'پیشتاز کوچک'),
        ('large', 'پیشتاز بزرگ'),
        ('industrial', 'صنعتی')
    ], verbose_name="مقیاس پروژه")
    goal = models.TextField(verbose_name="هدف")
    achievement = models.TextField(verbose_name="دستاورد")
    application = models.TextField(verbose_name="کاربرد")
    economicBenefits = models.TextField(verbose_name="صرفه اقتصادی")
    relatedReaserch = models.TextField(verbose_name="پژوهش مرتبط")
    researchMethod = models.TextField(verbose_name="روش تحقیق")
    service = models.TextField(verbose_name="خدمات")



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

    def save(self, *args, **kwargs):
        if not self.pk:  
            date_str = self.date.strftime("%Y%m%d")
            
            same_day_count = Idea.objects.filter(
                date=self.date
            ).count() + 1 
            
            self.identifier = f"{date_str}-{same_day_count:02d}"
        super().save(*args, **kwargs)


class JudgeEvaluation(models.Model):
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE, related_name="evaluations")
    judge = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="evaluations")
    assigned_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_judges")
    assigned_at = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = ("idea", "judge")

class Presentation(models.Model):
    idea = models.OneToOneField(Idea, on_delete=models.CASCADE, related_name="presentation")
    presentation_time = models.DateTimeField(null=True)
    presentation_file = models.FileField(upload_to='presentations/', null=True)
    approved = models.BooleanField(default=False)
    average_grade = models.FloatField(null=True)

    def calculate_average_grade(self):
        evaluations = self.idea.evaluations.all()
        total_score = sum([eval.score for eval in evaluations if eval.score is not None])
        count = len([eval for eval in evaluations if eval.score is not None])
        if count > 0:
            return total_score / count
        return None
    

@receiver(post_save, sender=Presentation)
def update_average_grade_after_approval(sender, instance, **kwargs):
    if instance.approved:
        average = instance.calculate_average_grade()
        if average is not None:
            instance.average_grade = average
            instance.save()

    






