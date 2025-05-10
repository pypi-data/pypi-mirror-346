#The Encoded By Sajad


# SajodeSx-project: --follow-imports

from __future__ import print_function

try:
    from SyntaxErroring import x
except Exception as e:
    print("Importing with syntax error gave:", type(e), e)

try:
    from IndentationErroring import x
except Exception as e:
    print("Importing with indentation error gave:", type(e), e)

print("Finished.")
.
