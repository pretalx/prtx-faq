import sys

PRTX = (
    "pretalx"
    if "pretalx" in sys.modules
    else "pretix"
    if "pretix" in sys.modules
    else None
)
if not PRTX:
    raise Exception(
        "Neiter pretix nor pretalx are installed, prtx_faq cannot run on its own!"
    )
