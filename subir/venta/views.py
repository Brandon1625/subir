from django.shortcuts import render
from easy_pdf.views import PDFTemplateView
from .models import Vale, Detalle_Vale


class FichaPDFView(PDFTemplateView):
    template_name = "ficha.html"

    def get_context_data(self, **kwargs):
        ids = self.request.GET.get("id")
        miventa = Vale.objects.get(id=ids)
        deta = Detalle_Vale.objects.all()
        return super(FichaPDFView, self).get_context_data(
            pagesize="Letter",
            title="Ficha",
            miventa=miventa,
            deta=deta,
            **kwargs
        )
