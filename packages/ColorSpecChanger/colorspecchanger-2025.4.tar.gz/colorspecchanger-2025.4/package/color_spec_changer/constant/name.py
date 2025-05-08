"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2025
SEE COPYRIGHT NOTICE BELOW
"""

from color_spec_changer.constant.specification import (
    SPEC_G,
    SPEC_GA,
    SPEC_MAX_1,
    SPEC_MAX_255,
    SPEC_RGB,
    SPEC_RGBA,
)

# Specification source names.
HEX_SOURCE_SPEC_PREFIX = "hex_"
HEX_LENGTHS_WITH_OPACITY = (5, 9)

SPEC_FROM_N_COMPONENTS = {1: SPEC_G, 2: SPEC_GA, 3: SPEC_RGB, 4: SPEC_RGBA}
HAS_OPACITY_FROM_N_COMPONENTS = {1: False, 2: True, 3: False, 4: True}
SPEC_PATTERN_G_RGB_COMPONENT = (
    rf"^({SPEC_G}|{SPEC_GA}|{SPEC_RGB}|{SPEC_RGBA})({SPEC_MAX_1}|{SPEC_MAX_255})"
)

SPEC_PATTERN_G_RGB_FUNCTION = (
    rf"^({SPEC_GA}|{SPEC_RGB}|{SPEC_RGBA})({SPEC_MAX_1}|{SPEC_MAX_255})"
)

# Specification source and target names.
NAME_SPEC = "name"
FUNCTION_SPEC_PREFIX = "function_"

# Specification target names.
HEX_TARGET_SPEC_PREFIX = "hex"

"""
COPYRIGHT NOTICE

This software is governed by the CeCILL  license under French law and
abiding by the rules of distribution of free software.  You can  use,
modify and/ or redistribute the software under the terms of the CeCILL
license as circulated by CEA, CNRS and INRIA at the following URL
"http://www.cecill.info".

As a counterpart to the access to the source code and  rights to copy,
modify and redistribute granted by the license, users are provided only
with a limited warranty  and the software's author,  the holder of the
economic rights,  and the successive licensors  have only  limited
liability.

In this respect, the user's attention is drawn to the risks associated
with loading,  using,  modifying and/or developing or reproducing the
software by the user in light of its specific status of free software,
that may mean  that it is complicated to manipulate,  and  that  also
therefore means  that it is reserved for developers  and  experienced
professionals having in-depth computer knowledge. Users are therefore
encouraged to load and test the software's suitability as regards their
requirements in conditions enabling the security of their systems and/or
data to be ensured and,  more generally, to use and operate it in the
same conditions as regards security.

The fact that you are presently reading this means that you have had
knowledge of the CeCILL license and that you accept its terms.

SEE LICENCE NOTICE: file README-LICENCE-utf8.txt at project source root.

This software is being developed by Eric Debreuve, a CNRS employee and
member of team Morpheme.
Team Morpheme is a joint team between Inria, CNRS, and UniCA.
It is hosted by the Centre Inria d'Université Côte d'Azur, Laboratory
I3S, and Laboratory iBV.

CNRS: https://www.cnrs.fr/index.php/en
Inria: https://www.inria.fr/en/
UniCA: https://univ-cotedazur.eu/
Centre Inria d'Université Côte d'Azur: https://www.inria.fr/en/centre/sophia/
I3S: https://www.i3s.unice.fr/en/
iBV: http://ibv.unice.fr/
Team Morpheme: https://team.inria.fr/morpheme/
"""
