import flet as ft


class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model
        self._idMap = {}
        self.fillIDMap()

    # =========================================================================
    # PREPARAZIONE DELLA TENDINA
    # =========================================================================
    def fillIDMap(self):
        values = self._model.listNerc
        for v in values:
            # Salvo l'oggetto nella mappa usando il suo ID (o il suo valore stringa univoco) come chiave
            self._idMap[str(v.id)] = v

    def fillDD(self):
        self._view._ddNerc.options.clear()
        nercList = self._model.listNerc

        for n in nercList:
            # TRUCCO FLET: Nascondo l'ID (trasformato in stringa) nella 'key'
            # e mostro all'utente il nome del Nerc ('value')
            self._view._ddNerc.options.append(
                ft.dropdown.Option(
                    key=str(n.id),
                    text=n.value
                )
            )
        self._view.update_page()

    # =========================================================================
    # IL BOTTONE (Worst-Case Analysis)
    # =========================================================================
    def handleWorstCase(self, e):
        # 1. LEGGO E CONTROLLO LA TENDINA
        id_nerc_scelto = self._view._ddNerc.value
        if id_nerc_scelto is None:
            self._view.create_alert("Attenzione: seleziona un NERC dalla tendina!")
            return

        # Recupero l'OGGETTO NERC vero e proprio dalla mia mappa usando l'ID
        nerc_oggetto = self._idMap[id_nerc_scelto]

        # 2. LEGGO E CONTROLLO LE CASELLE DI TESTO (Try-Except fondamentale)
        try:
            anni = int(self._view._txtYears.value)
            ore = int(self._view._txtHours.value)
        except ValueError:
            self._view.create_alert("Attenzione: inserisci numeri interi validi per anni e ore!")
            return

        # 3. CHIAMO IL MODEL
        # Il model mi restituisce il record (la lista di eventi) e il max_clienti
        soluzione_ottima, max_clienti = self._model.worstCase(nerc_oggetto, anni, ore)

        # 4. PULISCO LA SCHERMATA
        # (Attenzione a usare _txtOut con il trattino basso come hai fatto nella View!)
        self._view._txtOut.controls.clear()

        # Se non ho trovato nulla
        if len(soluzione_ottima) == 0:
            self._view._txtOut.controls.append(ft.Text("Nessuna combinazione trovata che rispetti i vincoli."))
            self._view.update_page()
            return

        # 5. STAMPO I RISULTATI SECONDO LA TRACCIA (Figura 2)
        # Calcolo le ore totali della soluzione trovata
        ore_totali = sum(evento.durata_ore for evento in soluzione_ottima)

        self._view._txtOut.controls.append(ft.Text(f"Tot people affected: {max_clienti}", color="blue", weight="bold"))
        self._view._txtOut.controls.append(ft.Text(f"Tot hours of outage: {ore_totali}", color="blue"))

        # Stampo l'elenco degli eventi (uno per riga)
        for evento in soluzione_ottima:
            # Formatto la riga come richiesto dal professore
            riga = f"id={evento.id} customers_affected={evento.customers_affected} start_time={evento.date_event_began} end_time={evento.date_event_finished}"
            self._view._txtOut.controls.append(ft.Text(riga))

        self._view.update_page()