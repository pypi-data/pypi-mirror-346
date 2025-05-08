"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2025
SEE COPYRIGHT NOTICE BELOW
"""

from color_spec_changer.constant.name import (
    FUNCTION_SPEC_PREFIX,
    HEX_SOURCE_SPEC_PREFIX,
    HEX_TARGET_SPEC_PREFIX,
    NAME_SPEC,
)
from color_spec_changer.constant.specification import (
    OPACITY_MARKER,
    SPEC_G,
    SPEC_MAX_1,
    SPEC_MAX_255,
    SPECS_WITH_OPACITY,
    SPECS_WITHOUT_OPACITY,
)


def _AllSourceFormats() -> tuple[str, ...]:
    """"""
    output = [NAME_SPEC]

    for length in (3, 6):
        for opacity in ("", OPACITY_MARKER):
            output.append(f"{HEX_SOURCE_SPEC_PREFIX}{length}{opacity}")

    for prefix in ("", FUNCTION_SPEC_PREFIX):
        should_exclude_gray = prefix == FUNCTION_SPEC_PREFIX
        for spec in SPECS_WITHOUT_OPACITY + SPECS_WITH_OPACITY:
            if should_exclude_gray and (spec == SPEC_G):
                continue

            for max_ in (SPEC_MAX_1, SPEC_MAX_255):
                output.append(f"{prefix}{spec}{max_}")

    return tuple(output)


def _AllTargetFormatsWithOpacity() -> tuple[str, ...]:
    """"""
    output = [f"{HEX_TARGET_SPEC_PREFIX}{OPACITY_MARKER}"]

    for prefix in ("", FUNCTION_SPEC_PREFIX):
        for spec in SPECS_WITH_OPACITY:
            for max_ in (SPEC_MAX_1, SPEC_MAX_255):
                output.append(f"{prefix}{spec}{max_}")

    return tuple(output)


def _AllTargetFormats(with_opacity: tuple[str, ...], /) -> tuple[str, ...]:
    """"""
    output = [NAME_SPEC, HEX_TARGET_SPEC_PREFIX]

    for prefix in ("", FUNCTION_SPEC_PREFIX):
        should_exclude_gray = prefix == FUNCTION_SPEC_PREFIX
        for spec in SPECS_WITHOUT_OPACITY:
            if should_exclude_gray and (spec == SPEC_G):
                continue

            for max_ in (SPEC_MAX_1, SPEC_MAX_255):
                output.append(f"{prefix}{spec}{max_}")

    return tuple(output) + with_opacity


SOURCE_SPEC_NAMES = _AllSourceFormats()
TARGET_SPECS_W_OPACITY = _AllTargetFormatsWithOpacity()
TARGET_SPEC_NAMES = _AllTargetFormats(TARGET_SPECS_W_OPACITY)

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
