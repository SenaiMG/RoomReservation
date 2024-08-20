from django.test import TestCase
from reservations.forms import HourForm
from reservations.models import Hour

class HourFormTest(TestCase):

    def test_hour_form_valid_data(self):
        # Testa se o formulário é válido quando os dados corretos são fornecidos
        form = HourForm(data={
            'range_hour': '07:01 - 08:00'
        })
        self.assertTrue(form.is_valid())
        hour = form.save()
        self.assertEqual(hour.range_hour, '07:01 - 08:00')

    def test_hour_form_invalid_data(self):
        # Testa se o formulário é inválido quando os dados estão incorretos ou faltando
        form = HourForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)  # Espera-se um erro para o campo 'range_hour'

    def test_hour_form_placeholder(self):
        # Testa se o placeholder é renderizado corretamente no widget
        form = HourForm()
        self.assertIn('placeholder="Ex: 07:01 - 08:00"', str(form))

    def test_hour_form_class(self):
        # Testa se a classe CSS correta é aplicada ao widget
        form = HourForm()
        self.assertIn('class="form-control"', str(form))

    def test_hour_form_label(self):
        # Testa se o label é renderizado corretamente
        form = HourForm()
        self.assertIn('Siga o exemplo de horário:', form.as_p())