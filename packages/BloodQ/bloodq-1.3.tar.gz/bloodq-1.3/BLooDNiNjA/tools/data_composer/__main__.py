#     Copyright 2025, BLOOD, tnmn4219@gmail.com find license text at end of file


""" Internal tool, assemble a constants blob for BloodQ from module constants.

"""

import os
import sys

if __name__ == "__main__":
    sys.path.insert(0, os.environ["BloodSx_PACKAGE_HOME"])

    import BLooDNiNjA  # just to have it loaded from there, pylint: disable=unused-import

    del sys.path[0]

    sys.path = [
        path_element
        for path_element in sys.path
        if os.path.dirname(os.path.abspath(__file__)) != path_element
    ]

    from BLooDNiNjA.tools.data_composer.DataComposer import main

    main()


