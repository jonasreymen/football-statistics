# Football Statistics

## Research Question

Hoe evolueren de technische en tactische prestaties van voetballers gedurende een seizoen, en hoe verschillen deze evoluties tussen basisspelers en spelers met beperkte speelfrequentie?

## Pages

### Synchronization
- PageBuilder: [app/gui/widgets/sync_page.py](app/gui/widgets/sync_page.py)

### Player Comparison List
- Pagebuilder: [app/gui/widgets/comparison_statistic_page.py](app/gui/widgets/comparison_statistic_page.py)

### Player Comparison
- Pagebuilder: [app/gui/widgets/comparison_statistic_detail_page.py](app/gui/widgets/comparison_statistic_detail_page.py)

### Player Comparison Generation
- Pagebuilder: [app/gui/widgets/comparison_entry_page.py](app/gui/widgets/comparison_entry_page.py)

### General Statistics
- Pagebuilder: [app/gui/widgets/general_statistic_page.py](app/gui/widgets/general_statistic_page.py)

## Synchronisation

Insert new entities in the database or update located entities.

**Key class:** [`Synchroniser`](app/sync/synchronizer.py)

### Components:

- **Source:** Retrieves data from any source (e.g. API-Football)  
  [`app/sync/source`](app/sync/source)

- **Mapper:** Maps data into an entity or object  
  [`app/sync/mapper`](app/sync/mapper)

- **Locator:** Locates mapped entity in your dataset or database  
  [`app/sync/locator`](app/sync/locator)

- **Merger:** Merges data from located entity with mapped entity  
  [`app/sync/merger`](app/sync/merger)

- **Storage:** Any provided storage can be used  
  [`app/sync/storage`](app/sync/storage)