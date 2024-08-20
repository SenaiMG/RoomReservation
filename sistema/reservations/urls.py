from django.urls import path
from .views import *

urlpatterns = [
    path('calendario/', CalendarReservation.as_view(), name='calendar'),#ok
    path('docentes/', ListReservation.as_view(), name='requests'),#ok
    path('cancelar/docentes/', ListReservation.as_view(), name='request_user_cancel'),#ok
    path('pendentes/', ListReservationPending.as_view(), name='requests_pending'),#ok
    path('solicitacao/<int:id>/', ManageSolicitationView.as_view(), name='manage_solicitation'),#ok
    path('calendario/gestor/', CalendarManagerReservation.as_view(), name='calendar_manager'),#ok
    path('dashboard/', DashboardRequestPageView.as_view(), name="request_dashboard"),#ok
    path('todas/', ListReservationManager.as_view(), name='total_request'),#ok
    path('cancelar/', ListReservationManager.as_view(), name='request_cancel'),#ok
    path("listar/horarios/", HourListView.as_view(), name="all_hours"),#ok
    path("criar/horario/", HourCreateView.as_view(), name="create_hours"),#ok
    path("editar/horario/<int:hours_id>/", HourUpdateView.as_view(), name="edit_hours"),#ok
    path("deletar/horario/<int:hours_id>/", HourDeleteView.as_view(), name="delete_hours"),#ok

]