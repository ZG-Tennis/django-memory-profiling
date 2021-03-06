# django-memory-profiling

Measure memory taken by requested view and response using _pympler.muppy_ and/or psutil

Memory measurements can be:
* **_Displayed on Terminal_**, when running django development server
* **_Displayed on Loggin panel of django debug toolbar_**, if `SHOW_ON_DJANGO_DEBUG_TOOLBAR_LOGGIN_PANEL = True`
* **_Sent to an email list_**, when the memory threshold is surpassed

Works with `Debug = True or False`


### INSTALLATION

1. Run
`pip install git+git://github.com/giussepi/django-memory-profiling`

2. On settings.py
  1. Add your preffered middleware(s) to MIDDLEWARE_CLASSES
  ```
      'memory_profiling.psutil_middleware.MemoryUsageMiddleware',
      'memory_profiling.pympler_middleware.MemoryMiddleware2',
      'memory_profiling.pympler_middleware.MemoryMiddleware1',
  ```
  2. Add `memory_profiling` to INSTALLED_APPS
  3. Configurate as desired. Example:
  ```
  # MemoryMiddleware1 settings
  SHOW_REQUEST_SUMMARY = True
  SHOW_RESPONSE_SUMMARY = True
  SHOW_COMPARED_REQUEST_RESPONSE_SUMMARIES = True

  # MemoryMiddleware2 settings
  SHOW_TOP_X_MEMORY_DELTAS = 15

  # MemoryUsageMiddleware settings
  MEMORY_VIEW_THRESHOLD = 10  # Mb
  SHOW_MEMORY_USAGE_PER_REQUEST = True
  MEMORY_WARNINGS_RECEIVERS = ['receiver@mail.com']

  # General settings (applies to all memory_profiling middlewares)
  IGNORE_URLS_CONTAINING = [
      'site_media', 'static', '__debug__', 'undefined', 'pulse'
  ]
  SHOW_ON_DJANGO_DEBUG_TOOLBAR_LOGGIN_PANEL = True
  ```
