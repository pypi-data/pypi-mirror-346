"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2025
SEE COPYRIGHT NOTICE BELOW
"""

import typing as h

import numpy as nmpy
from color_spec_changer.constant.name import (
    HEX_SOURCE_SPEC_PREFIX,
    HEX_TARGET_SPEC_PREFIX,
)
from color_spec_changer.task.analysis import CSCSpecification
from color_spec_changer.task.reference import ReferenceFromSource, TargetFromReference
from color_spec_changer.type.color import color_h, colors_h, opacities_h, opacity_h
from color_spec_changer.type.specification import specification_t

array_t = nmpy.ndarray

target_outer_type_h = h.Literal["same"] | type[tuple] | type[list] | type[array_t]
target_inner_type_h = target_outer_type_h
index_or_reduction_h = (
    int | h.Literal["min", "mean", "median", "max"] | h.Callable | None
)

_TRUE_SEQUENCE_TYPES = (tuple, list, array_t)  # True=not str.


def TargetMatchesSource(target: str, source: str, /) -> bool:
    """"""
    if target == source:
        return True

    if (
        (target == HEX_TARGET_SPEC_PREFIX) and (source == f"{HEX_SOURCE_SPEC_PREFIX}6")
    ) or (
        (target == f"{HEX_TARGET_SPEC_PREFIX}a")
        and (source == f"{HEX_SOURCE_SPEC_PREFIX}6a")
    ):
        return True

    return False


def NewTranslatedColor(
    color: color_h | colors_h,
    target_spec: str,
    /,
    *,
    target_outer_type: target_outer_type_h = "same",
    target_inner_type: target_inner_type_h = "same",
    index_or_reduction: index_or_reduction_h = None,
) -> color_h | colors_h | tuple[color_h, opacity_h] | tuple[colors_h, opacities_h]:
    """
    Translate a color, or a set of colors, from their original (source) specification
    into a target specification.

    This function translates the passed color(s) **color** from their original (source)
    specification into the target one **target_spec**, potentially extracting, or
    adding, an opacity information (see *Opacity value(s)*). The accepted color
    specifications are described at:
    https://src.koda.cnrs.fr/eric.debreuve/colorspecchanger/-/wikis/home

    *Opacity value(s)*: Whether the passed color(s) contain(s) or not (an) opacity
    component(s) (a.k.a. alpha channel) and the target specification mentions or not
    opacity, the function returns or not, on top of the translated color(s), an
    additional opacity variable based on the following rules:

    - target spec mentions opacity: no opacity variable is returned. If the passed
      color(s) do(es) not have opacity, the opacity component of the translated color(s)
      gets the default, fully opaque opacity value (see *Default opacity*);

    - target spec does not mention opacity: an opacity variable is returned in the form
      of an opacity value (single color passed), or a tuple of opacity values (several
      colors passed). If the passed color(s) do(es) not have opacity, this variable
      is/contains the default opacity value. Otherwise, the opacity value(s) are
      extracted from the passed color(s).

    *Default opacity*: if the target spec is RGB-based or RGBA-based, and the
    color/opacity components are floating-point numbers (in [0,1]), then the default
    opacity value is 1.0. Otherwise, it is 255.

    If several colors are passed, then the following (optional) keywork-only arguments
    are taken into account: target_outer_type, target_inner_type and index_or_reduction.

    *To be continued.*

    *Note and caution:* If target_outer_type is a Numpy array, then target_inner_type is
    forced to Numpy array. Other than this, no conformity check is performed on the
    target types. Consequently, passing incorrect types might lead to an incorrect
    translation or an exception, in this function or later on. An example is if
    requesting an str-based target specification like "hex" with `target_inner_type`
    being `tuple`.

    :param color: a color, or several colors.
    :type color: str
    :param target_spec:
    :param target_outer_type: Type of the container if several colors. "same"=same as
                              input colors.
    :param target_inner_type: Type of the (individual) color(s). "same"=same as input
                              color(s).
    :param index_or_reduction:
    :return:
    """
    source_spec = CSCSpecification(color)
    n_colors = source_spec.n_colors
    target_spec = specification_t.NewFromTargetName(target_spec)

    if target_outer_type == "same":
        target_outer_type = source_spec.outer_type
    if target_inner_type == "same":
        target_inner_type = source_spec.inner_type

    if target_outer_type is array_t:
        target_inner_type = array_t

    if TargetMatchesSource(target_spec.name, source_spec.name):
        out_color = color
        if target_spec.has_opacity:  # So does source_spec/color.
            out_opacity = None
        else:  # Neither specs have opacity.
            default_opacity = source_spec.component_type(
                source_spec.max_component_value
            )
            if n_colors > 1:
                out_opacity = n_colors * (default_opacity,)
            else:
                out_opacity = default_opacity
    elif n_colors > 1:
        colors = color
        if isinstance(index_or_reduction, int):
            reference = ReferenceFromSource(colors[index_or_reduction])
            output = TargetFromReference(reference, target_spec.name)
            if output[-1]:
                out_color, out_opacity = output[0], output[1]
            else:
                out_color, out_opacity = output[0], None
            n_colors = 1
        else:
            out_color, out_opacity = [], []

            for color in colors:
                reference = ReferenceFromSource(color)
                local = TargetFromReference(reference, target_spec.name)
                out_color.append(local[0])
                if local[-1]:
                    out_opacity.append(local[1])

            if index_or_reduction is None:
                if out_opacity.__len__() == 0:
                    out_opacity = None
            else:
                if isinstance(index_or_reduction, str):
                    index_or_reduction = getattr(nmpy, index_or_reduction)
                    out_color = index_or_reduction(out_color, axis=0)
                else:
                    out_color = index_or_reduction(out_color)
                if out_opacity.__len__() > 0:
                    out_opacity = index_or_reduction(out_opacity)
                else:
                    out_opacity = None
                n_colors = 1
    else:
        reference = ReferenceFromSource(color)
        output = TargetFromReference(reference, target_spec.name)
        if output[-1]:
            out_color, out_opacity = output[0], output[1]
        else:
            out_color, out_opacity = output[0], None

    if n_colors > 1:
        color_type = type(out_color[0])
        if (
            (not issubclass(color_type, target_inner_type))
            and (color_type in _TRUE_SEQUENCE_TYPES)
            and (target_inner_type in _TRUE_SEQUENCE_TYPES)
        ):
            if target_inner_type is array_t:
                target_inner_type = nmpy.array
            if target_outer_type is array_t:
                target_outer_type = nmpy.array
            out_color = target_outer_type(
                tuple(target_inner_type(_) for _ in out_color)
            )
        elif not issubclass(type(out_color), target_outer_type):
            if target_outer_type is array_t:
                target_outer_type = nmpy.array
            out_color = target_outer_type(out_color)
    else:
        color_type = type(out_color)
        if (
            (not issubclass(color_type, target_inner_type))
            and (color_type in _TRUE_SEQUENCE_TYPES)
            and (target_inner_type in _TRUE_SEQUENCE_TYPES)
        ):
            if target_inner_type is array_t:
                target_inner_type = nmpy.array
            out_color = target_inner_type(out_color)

    if out_opacity is None:
        return out_color

    if n_colors > 1:
        return out_color, tuple(out_opacity)

    return out_color, out_opacity


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
