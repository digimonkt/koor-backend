from django.urls import path

from .views import (
    CountryView, CityView, JobCategoryView,
    EducationLevelView, LanguageView, SkillView,
    TagView, ChangePasswordView, UserRightsView,
    PrivacyPolicyView, CandidatesListView, EmployerListView,
    JobsListView, UsersCountView, UserView,
    JobsRevertView, DashboardView, CoreUpdateView,
    TenderCategoryView, UploadCountryView,
    JobSubCategoryView, WorldCountryView, UploadCityView,
    WorldCityView, ChoiceView, OpportunityTypeView,
    TenderListView, TenderRevertView, ResourcesView,
    LinksView, AboutUsView, FaqCategoryView,
    FaqView, ResourcesDetailView, UploadLogo,
    TestimonialView, NewsletterUserView, SetPointsView,
    TestimonialDetailView, JobsCreateView, TenderCreateView,
    PackageView, GenerateInvoiceView, InvoiceDetailView,
    InvoiceSendView, DownloadInvoiceView, ResourcesMoreView,
    GoogleAddSenseCodeView, FinancialCountView
)

app_name = "superadmin"

urlpatterns = [

    path('/country', CountryView.as_view(), name="country"),
    path('/country/<str:countryId>', CountryView.as_view(), name="country"),

    path('/city', CityView.as_view(), name="city"),
    path('/city/<str:cityId>', CityView.as_view(), name="city"),

    path('/job-category', JobCategoryView.as_view(), name="job_category"),
    path('/job-category/<str:jobCategoryId>', JobCategoryView.as_view(), name="job_category"),

    path('/education-level', EducationLevelView.as_view(), name="education_level"),
    path('/education-level/<str:educationLevelId>', EducationLevelView.as_view(), name="education_level"),

    path('/language', LanguageView.as_view(), name="language"),
    path('/language/<str:languageId>', LanguageView.as_view(), name="language"),

    path('/skills', SkillView.as_view(), name="skills"),
    path('/skills/<str:skillId>', SkillView.as_view(), name="skills"),

    path('/tag', TagView.as_view(), name="tag"),
    path('/tag/<str:tagId>', TagView.as_view(), name="tag"),

    path('/change-password', ChangePasswordView.as_view(), name="change_password"),

    path('/user-rights', UserRightsView.as_view(), name="user_rights"),

    path('/privacy-policy', PrivacyPolicyView.as_view(), name="privacy_policy"),

    path('/candidates', CandidatesListView.as_view(), name="candidates_list"),
        
    path('/faq', FaqView.as_view(), name="faq"),
    path('/faq/<str:faqId>', FaqView.as_view(), name="faq"),
    path('/<str:role>/faq/<str:faqCategoryId>', FaqView.as_view(), name="faq"),
    
    path('/employer', EmployerListView.as_view(), name="employer_list"),
    path('/employer/<str:employerId>/<str:action>', EmployerListView.as_view(), name="employer_list"),

    path('/user/<str:userId>', UserView.as_view(), name="user"),

    path('/jobs', JobsListView.as_view(), name="jobs_list"),
    path('/jobs/create', JobsCreateView.as_view(), name="jobs_create"),
    path('/jobs/create/<str:jobId>', JobsCreateView.as_view(), name="jobs_create"),
    path('/jobs/<str:jobId>', JobsListView.as_view(), name="jobs_list"),
    path('/jobs/<str:jobId>/revert', JobsRevertView.as_view(), name="jobs_revert"),

    path('/users-count', UsersCountView.as_view(), name="users_count"),
    path('/financial-count', FinancialCountView.as_view(), name="financial_count"),
    path('/dashboard', DashboardView.as_view(), name="dashboard"),
    path('/core-update', CoreUpdateView.as_view(), name="core_update"),

    path('/tender-category', TenderCategoryView.as_view(), name="tender_category"),
    path('/tender-category/<str:tenderCategoryId>', TenderCategoryView.as_view(), name="tender_category"),

    path('/upload-country', UploadCountryView.as_view(), name="upload_country"),
    path('/upload-city', UploadCityView.as_view(), name="upload_city"),
    path("/upload-logo", UploadLogo.as_view(), name="upload_logo"),
    path("/upload-logo/<str:logoId>", UploadLogo.as_view(), name="upload_logo"),
    
    path('/job-sub-category', JobSubCategoryView.as_view(), name="job_sub_category"),
    path('/job-sub-category/<str:jobSubCategoryId>', JobSubCategoryView.as_view(), name="job_sub_category"),
    
    path('/world-country', WorldCountryView.as_view(), name="world_country"),
    path('/world-city', WorldCityView.as_view(), name="world_city"),
        
    path('/sector', ChoiceView.as_view(), name="sector"),
    path('/sector/<str:sectorId>', ChoiceView.as_view(), name="sector"),
            
    path('/opportunity-type', OpportunityTypeView.as_view(), name="opportunity_type"),
    path('/opportunity-type/<str:opportunityId>', OpportunityTypeView.as_view(), name="opportunity_type"),
    
    path('/tender', TenderListView.as_view(), name="tender_list"),
    path('/tender/create', TenderCreateView.as_view(), name="tender_create"),
    path('/tender/create/<str:tenderId>', TenderCreateView.as_view(), name="tender_create"),
    path('/tender/<str:tenderId>', TenderListView.as_view(), name="tender_list"),
    path('/tender/<str:tenderId>/revert', TenderRevertView.as_view(), name="tender_revert"),
    
    path('/resources', ResourcesView.as_view(), name="resources"),
    path('/resources/<str:resourcesId>', ResourcesView.as_view(), name="resources"),
    path('/resources/<str:resourcesId>/more', ResourcesMoreView.as_view(), name="resources_more"),
    path('/resources/<str:resourcesId>/detail', ResourcesDetailView.as_view(), name="resources_detail"),
        
    path('/links', LinksView.as_view(), name="links"),
    path('/links/<str:linkId>', LinksView.as_view(), name="links"),
    
    path('/about-us', AboutUsView.as_view(), name="about_us"),
    
    path('/faq-category', FaqCategoryView.as_view(), name="faq_category"),
    path('/faq-category/<str:faqCategoryId>', FaqCategoryView.as_view(), name="faq_category"),
    
    path("/testimonial", TestimonialView.as_view(), name="testimonial"),
    path("/testimonial/<str:testimonialId>", TestimonialView.as_view(), name="testimonial"),
    path('/testimonial/<str:testimonialId>/detail', TestimonialDetailView.as_view(), name="testimonial_detail"), 
    
    path("/newsletter-user", NewsletterUserView.as_view(), name="newsletter_user"),
    path("/newsletter-user/<str:newsletterId>", NewsletterUserView.as_view(), name="newsletter_user"),
    
    path('/set-points', SetPointsView.as_view(), name="set_points"),
    
    path('/invoice', GenerateInvoiceView.as_view(), name="generate_invoice"),
    path('/invoice/download', DownloadInvoiceView.as_view(), name='download_invoice'),
    path('/invoice/<str:invoiceId>/detail', InvoiceDetailView.as_view(), name="invoice_detail"),
    path('/invoice/<str:invoiceId>/send', InvoiceSendView.as_view(), name="invoice_send"),
    
    path('/package', PackageView.as_view(), name="package"),
    
    path('/google-add-sense-code', GoogleAddSenseCodeView.as_view(), name="google_add_sense_code"),
    path('/google-add-sense-code/<str:codeId>', GoogleAddSenseCodeView.as_view(), name="google_add_sense_code"),

    path('/user-rights', UserRightsView.as_view(), name="user_rights"),
]
