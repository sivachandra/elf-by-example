## What is a PIE?

A PIE binary and all of its dependencies are loaded into random locations
within virtual memory each time the application is executed. PIE binaries
satisfy the [ASLR](https://en.wikipedia.org/wiki/Address_space_layout_randomization)
requirements. PIE binaries can either be [statically linked](static_pie.md), or
dynamically linked.
