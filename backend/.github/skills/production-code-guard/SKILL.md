---
name: production-code-guard
description: "Use when: richiesta di codice di produzione, hardening backend, refactor production-ready, clean code, gestione errori robusta, logging applicativo completo."
---

# Production Code Guard

Skill per generare e validare codice di produzione con una quality gate obbligatoria su:

1. Clean code
2. Error handling robusto
3. Logging esaustivo

## Activation

Attiva questa skill quando la richiesta contiene temi come:

- codice di produzione
- production-ready
- hardening
- clean code
- gestione errori
- logging

## Mandatory Workflow

1. Comprendi i requisiti funzionali e non funzionali.
2. Implementa la modifica minima necessaria, evitando refactor non richiesti.
3. Esegui la quality gate seguendo tutte le checklist sotto.
4. Se una checklist fallisce, correggi il codice e riesegui i controlli.
5. Concludi solo con gate PASS oppure con FAIL motivato + piano di fix.

## Checklist 1: Clean Code (obbligatoria)

Verifica tutti i punti:

- Nomi chiari e intenzionali per funzioni, classi, variabili, costanti.
- Funzioni piccole, con responsabilita singola (single responsibility).
- Nessuna duplicazione evitabile (DRY), soprattutto in validazioni e logica dominio.
- Complessita ciclomatica contenuta; preferire early return e guard clauses.
- Dipendenze esplicite; evitare side effect nascosti.
- Commenti solo dove necessario; il codice deve spiegare il cosa, i commenti il perche.
- Nessun dead code, import inutili, parametri non usati.
- Compatibilita con lo stile esistente del repository.

Criterio PASS:

- Tutti i punti sopra soddisfatti oppure trade-off dichiarati esplicitamente nel report finale.

## Checklist 2: Error Handling Robusto (obbligatoria)

Verifica tutti i punti:

- Validazione input completa su boundary e casi invalidi.
- Uso di eccezioni specifiche; evitare catch generici senza gestione.
- Ogni errore previsto produce risposta controllata e non crasha il processo.
- Messaggi di errore utili per debug interno ma sicuri per l'utente.
- Nessuna perdita silenziosa di errori (no except pass).
- Nei layer API: mappatura consistente degli errori verso codici HTTP corretti.
- Risorse esterne gestite in sicurezza (file, rete, parse dati) con fallback o fail-fast controllato.
- Stato applicativo coerente dopo errore (no stato parziale inconsistente).

Criterio PASS:

- Nessun percorso di errore identificato che possa causare crash non gestito.

## Checklist 3: Logging Esaustivo (obbligatoria)

Verifica tutti i punti:

- Log presenti su eventi chiave: start/stop, richieste importanti, errori, operazioni dominio critiche.
- Livelli corretti: DEBUG, INFO, WARNING, ERROR, CRITICAL.
- Ogni log di errore include contesto minimo utile (operazione, input rilevante non sensibile, causa).
- Nessun dato sensibile nei log (segreti, token, credenziali, dati personali non necessari).
- Messaggi log consistenti e ricercabili (formato stabile).
- Errori con stack trace quando utile al troubleshooting.
- Nei flussi API: loggare endpoint, esito, e metadati essenziali senza rumorosita eccessiva.

Criterio PASS:

- Copertura logging adeguata dei path happy-path e failure-path principali.

## Project-Specific Validation (regression-project)

Quando il cambiamento coinvolge il backend in `backend/`:

1. Verificare almeno `GET /`.
2. Verificare almeno `POST /regression/points`.

Quando il cambiamento coinvolge il frontend in `frontend/`:

1. Eseguire almeno build produzione (`npm run build`).

## Output Contract

Prima della risposta finale, includi sempre una mini-sezione di audit con:

1. Clean code: PASS o FAIL + note.
2. Error handling: PASS o FAIL + note.
3. Logging: PASS o FAIL + note.
4. Test/validazioni eseguite.
5. Rischi residui.

Se uno dei tre blocchi e FAIL:

- Non dichiarare la soluzione production-ready.
- Proporre fix specifici e ordinati per priorita.
