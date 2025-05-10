"""Chemical element."""

from __future__ import annotations

import enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import sys
    if sys.version_info < (3, 11):
        from typing_extensions import Self
    else:
        from typing import Self


__all__ = ["Element"]


@enum.unique
class Element(enum.Enum):
    """Enumeration of chemical elements.

    Examples
    --------
    Access a member by a value or an atomic number.

    >>> Element(1)
    <Element.HYDROGEN: 1>

    Access a member by a name.

    >>> Element["HYDROGEN"]
    <Element.HYDROGEN: 1>

    Members are compared in terms of atomic numbers.

    >>> Element.HYDROGEN == Element.HYDROGEN
    True
    >>> Element.HYDROGEN < Element.HELIUM
    True
    """

    if TYPE_CHECKING:
        value: int
        _symbol: str

    HYDROGEN = (1, "H")
    HELIUM = (2, "He")
    LITHIUM = (3, "Li")
    BERYLLIUM = (4, "Be")
    BORON = (5, "B")
    CARBON = (6, "C")
    NITROGEN = (7, "N")
    OXYGEN = (8, "O")
    FLUORIN = (9, "F")
    NEON = (10, "Ne")
    SODIUM = (11, "Na")
    MAGNESIUM = (12, "Mg")
    ALUMINIUM = (13, "Al")
    SILICON = (14, "Si")
    PHOSPHORUS = (15, "P")
    SULFUR = (16, "S")
    CHLORINE = (17, "Cl")
    ARGON = (18, "Ar")
    POTASSIUM = (19, "K")
    CALCIUM = (20, "Ca")
    SCANDIUM = (21, "Sc")
    TITANIUM = (22, "Ti")
    VANADIUM = (23, "V")
    CHROMIUM = (24, "Cr")
    MANGANESE = (25, "Mn")
    IRON = (26, "Fe")
    COBALT = (27, "Co")
    NICKEL = (28, "Ni")
    COPPER = (29, "Cu")
    ZINC = (30, "Zn")
    GALLIUM = (31, "Ga")
    GERMANIUM = (32, "Ge")
    ARSENIC = (33, "As")
    SELENIUM = (34, "Se")
    BROMINE = (35, "Br")
    KRYPTON = (36, "Kr")
    RUBIDIUM = (37, "Rb")
    STRONTIUM = (38, "Sr")
    YTTRIUM = (39, "Y")
    ZIRCONIUM = (40, "Zr")
    NIOBIUM = (41, "Nb")
    MOLYBDENUM = (42, "Mo")
    TECHNETIUM = (43, "Tc")
    RUTHENIUM = (44, "Ru")
    RHODIUM = (45, "Rh")
    PALLADIUM = (46, "Pd")
    SILVER = (47, "Ag")
    CADMIUM = (48, "Cd")
    INDIUM = (49, "In")
    TIN = (50, "Sn")
    ANTIMONY = (51, "Sb")
    TELLURIUM = (52, "Te")
    IODINE = (53, "I")
    XENON = (54, "Xe")
    CAESIUM = (55, "Cs")
    BARIUM = (56, "Ba")
    LANTHANUM = (57, "La")
    CERIUM = (58, "Ce")
    PRASEODYMIUM = (59, "Pr")
    NEODYMIUM = (60, "Nd")
    PROMETHIUM = (61, "Pm")
    SAMARIUM = (62, "Sm")
    EUROPIUM = (63, "Eu")
    GADOLINIUM = (64, "Gd")
    TERBIUM = (65, "Tb")
    DYSPROSIUM = (66, "Dy")
    HOLMIUM = (67, "Ho")
    ERBIUM = (68, "Er")
    THULIUM = (69, "Tm")
    YTTERBIUM = (70, "Yb")
    LUTETIUM = (71, "Lu")
    HAFNIUM = (72, "Hf")
    TANTALUM = (73, "Ta")
    TUNGSTEN = (74, "W")
    RHENIUM = (75, "Re")
    OSMIUM = (76, "Os")
    IRIDIUM = (77, "Ir")
    PLATINUM = (78, "Pt")
    GOLD = (79, "Au")
    MERCURY = (80, "Hg")
    THALLIUM = (81, "Tl")
    LEAD = (82, "Pb")
    BISMUTH = (83, "Bi")
    POLONIUM = (84, "Po")
    ASTATINE = (85, "At")
    RADON = (86, "Rn")
    FRANCIUM = (87, "Fr")
    RADIUM = (88, "Ra")
    ACTINIUM = (89, "Ac")
    THORIUM = (90, "Th")
    PROTACTINIUM = (91, "Pa")
    URANIUM = (92, "U")
    NEPTUNIUM = (93, "Np")
    PLUTONIUM = (94, "Pu")
    AMERICIUM = (95, "Am")
    CURIUM = (96, "Cm")
    BERKELIUM = (97, "Bk")
    CALIFORNIUM = (98, "Cf")
    EINSTEINIUM = (99, "Es")
    FERMIUM = (100, "Fm")
    MENDELEVIUM = (101, "Md")
    NOBELIUM = (102, "No")
    LAWRENCIUM = (103, "Lr")
    RUTHERFORDIUM = (104, "Rf")
    DUBNIUM = (105, "Db")
    SEABORGIUM = (106, "Sg")
    BOHRIUM = (107, "Bh")
    HASSIUM = (108, "Hs")
    MEITNERIUM = (109, "Mt")
    DARMSTADTIUM = (110, "Ds")
    ROENTGENIUM = (111, "Rg")
    COPERNICIUM = (112, "Cn")
    NIHONIUM = (113, "Nh")
    FLEROVIUM = (114, "Fl")
    MOSCOVIUM = (115, "Mc")
    LIVERMORIUM = (116, "Lv")
    TENNESSINE = (117, "Ts")
    OGANESSON = (118, "Og")

    def __new__(cls, atomic_number: int, symbol: str) -> Self:  # noqa: D102
        obj = object.__new__(cls)
        obj._value_ = atomic_number
        obj._symbol = symbol

        return obj

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented

        return self.value < other.value

    def __le__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented

        return self.value <= other.value

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented

        return self.value > other.value

    def __ge__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented

        return self.value >= other.value

    @property
    def symbol(self) -> str:
        """str: Symbol of a chemical element."""
        return self._symbol

    @classmethod
    def from_symbol(cls, symbol: str) -> Self:
        """Access a member by a symbol.

        Parameters
        ----------
        symbol : str
            Symbol of a chemical element.

        Returns
        -------
        ptvis.Element
            Member.

        Examples
        --------
        >>> Element.from_symbol("H")
        <Element.HYDROGEN: 1>
        """
        try:
            return next(member for member in cls if member._symbol == symbol)
        except StopIteration:
            raise ValueError("invalid `symbol`")
