from django.contrib import admin
from .models import VisaAssessment, VisaOrder, Country, VisaType, VisaRequirement, VisaDocument, FAQ, DocumentUpload

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    search_fields = ('name',)

@admin.register(VisaType)
class VisaTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')
    search_fields = ('name', 'country__name')

@admin.register(VisaRequirement)
class VisaRequirementAdmin(admin.ModelAdmin):
    list_display = ('visa_type', 'requirement')
    search_fields = ('visa_type__name',)

@admin.register(VisaDocument)
class VisaDocumentAdmin(admin.ModelAdmin):
    list_display = ('document_name', 'visa_type')
    search_fields = ('document_name', 'visa_type__name')

@admin.register(VisaAssessment)
class VisaAssessmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at', 'status')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'email', 'citizenship')
    readonly_fields = ('created_at',)

@admin.register(VisaOrder)
class VisaOrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'visa_type', 'order_date', 'status', 'assigned_manager')
    list_filter = ('status', 'order_date', 'assigned_manager')
    search_fields = ('user__username', 'visa_type__name')
    filter_horizontal = ('required_documents',)

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'visa_type')
    search_fields = ('question', 'answer', 'visa_type__name')

@admin.register(DocumentUpload)
class DocumentUploadAdmin(admin.ModelAdmin):
    list_display = ('order', 'document_type', 'uploaded_at')
    list_filter = ('uploaded_at',)
    search_fields = ('order__user__username', 'document_type')
