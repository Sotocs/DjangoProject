from django import forms
from .models import Product

FORBIDDEN_WORDS = [
    "казино", "криптовалюта", "крипта", "биржа",
    "дешево", "бесплатно", "обман", "полиция", "радар"
]

def _contains_forbidden_words(text: str) -> bool:
    text_lower = text.lower()
    return any(word in text_lower for word in FORBIDDEN_WORDS)

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Стилизация полей (под общую стилистику платформы)
        self.fields["name"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Название продукта"
        })
        self.fields["description"].widget.attrs.update({
            "class": "form-control",
            "rows": 4,
            "placeholder": "Описание продукта"
        })
        self.fields["price"].widget.attrs.update({
            "class": "form-control",
            "step": "0.01",
            "placeholder": "Цена"
        })

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if not name:
            return name
        if _contains_forbidden_words(name):
            raise forms.ValidationError("В названии продукта запрещено использовать запрещённые слова.")
        return name

    def clean_description(self):
        description = self.cleaned_data.get("description")
        if not description:
            return description
        if _contains_forbidden_words(description):
            raise forms.ValidationError("В описании продукта запрещено использовать запрещённые слова.")
        return description

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price is not None and price < 0:
            raise forms.ValidationError("Цена не может быть отрицательной.")
        return price
