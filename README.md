# django-memory-profiling

Measure memory taken by requested view and response using pympler.muppy

Memory measurements can be shown on:
* **_Terminal_**, when running django development server
* **_Loggin panel of django debug toolbar_** (if `SHOW_ON_DJANGO_DEBUG_TOOLBAR_LOGGIN_PANEL = True`)

Works with `Debug = True or False`


### INSTALLATION

1. Run
`pip install git+git://github.com/giussepi/django-memory-profiling`

2. On settings.py
  1. Add your preffered middleware(s) to MIDDLEWARE_CLASSES
  ```
      'memory_profiling.pympler_middleware.MemoryMiddleware2',
      'memory_profiling.pympler_middleware.MemoryMiddleware1',
  ```
  2. Add `memory_profiling` to INSTALLED_APPS
  3. Configurate as desired. Example:
  ```
  SHOW_REQUEST_SUMMARY = True
  SHOW_RESPONSE_SUMMARY = True
  SHOW_COMPARED_REQUEST_RESPONSE_SUMMARIES = True
  IGNORE_URLS_CONTAINING = [
      'site_media', 'static', '__debug__', 'undefined', 'pulse'
  ]
  SHOW_ON_DJANGO_DEBUG_TOOLBAR_LOGGIN_PANEL = True
  SHOW_TOP_X_MEMORY_DELTAS = 15
  ```
