from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.utils import timezone
from .models import Kunde, Vermerk
from .forms import KundeForm, VermerkForm

def index(request):
    return render(request, 'kunden/index.html')

@login_required
@never_cache
def kunden_uebersicht(request):
    kunden = Kunde.objects.all() # Hole alle Kunden
    firma_filter = request.GET.get('firma', '')
    if firma_filter:
        kunden = kunden.filter(firma__icontains=firma_filter)

    return render(request, 'kunden/kunden_uebersicht.html', {
        'kunden': kunden,
        'firma_filter': firma_filter  # Für die Vorbelegung des Suchfelds
    })

@login_required
@never_cache
def vermerk_uebersicht(request):
    vermerk = Vermerk.objects.all() # Hole alle Vermerke

    wunsch_filter = request.GET.get('wunsch', '')
    if wunsch_filter:
        vermerk = vermerk.filter(wunsch__icontains=wunsch_filter)

    firma_filter = request.GET.get('firma', '')
    if firma_filter:
        vermerk = vermerk.filter(firmen_id_id__firma__icontains=firma_filter)

    wunsch_choices = Vermerk._meta.get_field('wunsch').choices

    return render(request, 'kunden/vermerk_uebersicht.html', {
        'vermerke': vermerk,
        'wunsch_filter': wunsch_filter,
        'wunsch_choices': wunsch_choices,
        'firma_filter': firma_filter
    })

@login_required
@never_cache
def kunden_detail(request, kunden_nr):
    kunde = get_object_or_404(Kunde, kunden_nr=kunden_nr)
    return render(request, 'kunden/kunden_detail.html', {'kunde': kunde})

@login_required
@never_cache
def vermerk_detail(request, gespraechs_id):
    vermerk = get_object_or_404(Vermerk, gespraechs_id=gespraechs_id)
    return render(request, 'kunden/vermerk_detail.html', {'vermerk': vermerk})

@login_required
@never_cache
def kunde_neu(request):
    if request.method == "POST":
        form = KundeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('kunden-uebersicht')
    else:
        form = KundeForm()
    return render(request, 'kunden/kunde_neu.html', {'form': form})

@login_required
@never_cache
def kunde_loeschen(request, kunden_nr):
    kunde = get_object_or_404(Kunde, kunden_nr=kunden_nr)
    if request.method == 'POST':
        kunde.delete()
        return redirect('kunden-uebersicht')
    return redirect('kunden-uebersicht')  # Optional: GET-Anfragen ignorieren

@login_required
@never_cache
def vermerk_loeschen(request, gespraechs_id):
    vermerk = get_object_or_404(Vermerk, gespraechs_id=gespraechs_id)
    if request.method == 'POST':
        vermerk.delete()
        return redirect('vermerk-uebersicht')
    return redirect('vermerk-uebersicht')  # Optional: GET-Anfragen ignorieren

@login_required
@never_cache
def vermerk_erfassen(request):
    if request.method == "POST":
        form = VermerkForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['firmen_id'] == "new":
                return redirect('kunde-neu')
            else:
                # # Erstelle das Vermerk-Objekt, aber speichere es noch nicht
                #vermerk = form.save(commit=False)
                # # Setze die Uhrzeit auf Stunden und Minuten
                # now = timezone.localtime(timezone.now())
                # adjusted_time = now.time().replace(second=0, microsecond=0)
                # vermerk.uhrzeit = adjusted_time
                # # Speichere das Objekt
                form.save()
                return redirect('vermerk-uebersicht')
    else:
        initial_data = {}
        kunden_nr = request.GET.get('kunden_nr')
        if kunden_nr:
            kunde = get_object_or_404(Kunde, kunden_nr=kunden_nr)
            initial_data = {
                'firmen_id': kunde.kunden_nr,
            }
        initial_data['datum'] = timezone.now()
        form = VermerkForm(initial=initial_data)
    return render(request, 'kunden/vermerk_erfassen.html', {'form': form})

@login_required
@never_cache
def get_kunde_data(request, kunden_nr):
    kunde = get_object_or_404(Kunde, kunden_nr=kunden_nr)
    data = {
        'firma': kunde.firma,
        'anschrift': kunde.anschrift,
        'telefon_nr': kunde.telefon_nr,
        'fax_nr': kunde.fax_nr,
    }
    return JsonResponse(data)

# Create your views here.
