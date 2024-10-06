from django.contrib import admin
from .models import Country, VisaType, VisaRequirement, VisaDocument, VisaAssessment, VisaOrder, FAQ

admin.site.register(Country)
admin.site.register(VisaType)
admin.site.register(VisaRequirement)
admin.site.register(VisaDocument)
admin.site.register(VisaAssessment)
admin.site.register(VisaOrder)
admin.site.register(FAQ)
