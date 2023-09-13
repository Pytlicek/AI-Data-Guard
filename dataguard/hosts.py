from django_hosts import patterns, host

host_patterns = patterns(
    "",
    # host(r"", "dataguard.urls", name="dataguard"),
    host(r"dataguard", "api.urls", name="api"),
)
