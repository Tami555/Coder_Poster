class DataFormMixin:
    extra_context = {}
    title_page = None
    btn_title = None

    def __init__(self):
        if self.title_page:
            self.extra_context['title'] = self.title_page
        if self.btn_title:
            self.extra_context['btn_title'] = self.btn_title

    def get_context_mixin(self, context, **kwargs):
        context.update(kwargs)
        return context