import copy

from database.DAO import DAO


class Model:
    def __init__(self):
        self._solBest = []
        self._listNerc = None
        self._listEvents = None
        self.loadNerc()
        self._maxCustomers = 0



    def worstCase(self, nerc, maxY, maxH):
        self.loadEvents(nerc)

        self._solBest = []
        self._maxCustomers = 0

        self.ricorsione([], maxY, maxH, 0)

        return self._solBest, self._maxCustomers


    def ricorsione(self, parziale, maxY, maxH, pos):
        clienti_attuali = sum(e.customers_affected for e in parziale)

        # Se questa combinazione fa più danni del mio record storico, la salvo!
        if clienti_attuali > self._maxCustomers:
            self._maxCustomers = clienti_attuali
            # OBBLIGATORIO: deepcopy! Altrimenti salva un collegamento alla lista 'parziale'
            # che poi verrà svuotata dal backtracking, cancellando anche la soluzione ottima.
            self._solBest = copy.deepcopy(parziale)

        for i in range(pos, len(self._listEvents)):
            evento = self._listEvents[i]

            parziale.append(evento)

            if self._vincoli_rispettati(parziale, maxY, maxH):
                # Se i vincoli reggono, vado in profondità!
                # Passo (i + 1) così al prossimo giro guarderà dall'evento successivo
                self.ricorsione(parziale, maxY, maxH, i + 1)

            parziale.pop()

    def _vincoli_rispettati(self, parziale, maxY, maxH):
        """
        Controlla se la combinazione temporanea rispetta le regole imposte.
        Presuppone che il DTO abbia le @property 'durata_ore' e 'anno'.
        """
        # 1. VINCOLO DELLE ORE MASSIME
        ore_totali = sum(e.durata_ore for e in parziale)
        if ore_totali > maxH:
            return False

        # 2. VINCOLO DEGLI ANNI MASSIMI (Delta tra il più vecchio e il più nuovo)
        # Se c'è un solo evento, la differenza di anni è 0, quindi sicuramente valida.
        if len(parziale) >= 2:
            anni = [e.anno for e in parziale]
            differenza_anni = max(anni) - min(anni)
            if differenza_anni > maxY:
                return False

        # Se supera entrambi i controlli, la combinazione è valida
        return True


    def loadEvents(self, nerc):
        self._listEvents = DAO.getAllEvents(nerc)

    def loadNerc(self):
        self._listNerc = DAO.getAllNerc()

    @property
    def listNerc(self):
        # Questo lo chiamerà il Controller per riempire la tendina
        if self._listNerc is None:
            self.loadNerc()
        return self._listNerc