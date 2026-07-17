# START_VERSION_BLOCK
VERSION_MAJOR = 0
VERSION_MINOR = 18
VERSION_BUILD = 1
VERSION_ALPHA = 1
# END_VERSION_BLOCK

# Release automation rewrites only the block above; the packaging metadata reads
# __version__ from here, so the two can never drift apart.
__version__ = f"{VERSION_MAJOR}.{VERSION_MINOR}.{VERSION_BUILD}"
if VERSION_ALPHA:
    __version__ += f"a{VERSION_ALPHA}"
