# Problémy v kódu TaskManager

Tento dokument obsahuje přehled všech problémů záměrně vložených do kódu TaskManager. Slouží pro vyhodnocení, kolik z těchto problémů dokáže jazykový model identifikovat.

## 1. Zjevné problémy (měly by být snadno odhalitelné)

1. **Chybějící validace dat:** V metodě `__init__` třídy `Task` chybí validace vstupů (např. kontrola, zda je priorita v rozmezí 1-5).
   
2. **Nebezpečné defaultní hodnoty:** Ukládání do pevné cesty "tasks.json" v `__init__` třídy `TaskManager` může způsobit problémy v různých prostředích.

3. **Nekonsistentní návratové hodnoty:** Metoda `search_tasks` vrací vždy seznam, zatímco `get_task` vrací buď objekt, nebo None.

4. **Potenciální ztráta dat:** V `save_tasks()` se přepisuje celý soubor bez zálohy nebo ošetření případu, kdy by zápis selhal.

## 2. Středně závažné problémy (vyžadují hlubší analýzu)

1. **Absence nezbytné chybové logiky:** Metoda `from_dict` předpokládá, že vstupní slovník obsahuje všechny povinné klíče a nezpracovává chybějící klíče.

2. **Neoptimální vyhledávací algoritmus:** Metoda `get_task` prochází celý seznam úkolů, což je neefektivní pro velké množství dat.

3. **Nekonzistentní práce s časem:** Vytvářejí se objekty `datetime.datetime.now()`, ale není specifikována časová zóna.

4. **Nevhodná struktura kódu:** Metoda `to_dict` a `from_dict` nejsou navzájem symetrické - `from_dict` neobnoví všechny atributy správně.

## 3. Subtilní problémy (vyžadují hlubší zamyšlení nebo znalost kontextu)

1. **Riziko souběhu:** Při vícenásobném přístupu k souboru může dojít ke konfliktu (race condition), protože chybí zamykání souborů.

2. **Chybějící ošetření vyčerpání paměti:** Při načtení velkého množství úkolů by mohlo dojít k vyčerpání paměti, chybí stránkování nebo limity.

3. **Porušení principu jedné odpovědnosti:** Třída `TaskManager` zajišťuje jak business logiku, tak i persistenci dat.

4. **Potenciální bezpečnostní problém:** Uživatelský vstup (názvy úkolů, popisy) není nikde ošetřen proti injekci nebo XSS při případném zobrazení.

5. **Absence testů a dokumentace:** Kód postrádá jednotkové testy a podrobnější dokumentaci, což je důležité pro udržitelnost.

6. **Design antipattern:** Použití seznamu místo slovníku pro ukládání úkolů komplikuje vyhledávání podle ID.
