"""Hydra YAML semantic token definitions and utilities."""

from dataclasses import dataclass, field
from enum import IntEnum, IntFlag, auto
from typing import Self

from hydra_yaml_lsp.core.detections import (
    ArgKeyPosition as TargetArgKeyPos,
    HydraPackagePosition,
    InterpolationHighlight,
    SpecialKeyPosition,
    TargetValueHighlight,
)


def to_camel_case(name: str) -> str:
    """Convert `UPPER_SNAKE_CASE` to `lowerCamelCase`.

    Args:
        name: Enum member name in upper-snake (e.g. ``"SPECIAL_KEY"``).

    Returns:
        Converted lower-camel string (e.g. ``"specialKey"``).
    """
    parts: list[str] = name.lower().split("_")
    if not parts:
        return ""
    return parts[0] + "".join(word.capitalize() for word in parts[1:])


class TokenType(IntEnum):
    """Definition of semantic token types."""

    SPECIAL_KEY = 0  # Hydra special keys (_target_, _args_, etc.)
    TARGET_VALUE = auto()  # Values of _target_ fields
    TARGET_ARG = auto()  # Args keys of _target_ fields
    INTERPOLATION_REF = (
        auto()  # Interpolation references (reference parts in ${path.to.value})
    )
    INTERPOLATION_FUNC = (
        auto()
    )  # Interpolation functions (function name in ${func:args})
    INTERPOLATION_BRACKET = auto()  # Interpolation brackets
    PACKAGE_DIRECTIVE = auto()  # @package directive
    PACKAGE_NAME = auto()  # Package name

    @classmethod
    def get_legend(cls) -> list[str]:
        """Return the legend for token types."""
        return [to_camel_case(e.name) for e in cls]


class TokenModifier(IntFlag):
    """Definition of semantic token modifiers."""

    NONE = 0
    DECLARATION = auto()
    REFERENCE = auto()
    FUNCTION = auto()
    MODULE = auto()
    CLASS = auto()
    VARIABLE = auto()
    CONSTANT = auto()
    BRACKET = auto()

    @classmethod
    def get_legend(cls) -> list[str]:
        """Return the legend for token modifiers."""
        return [to_camel_case(e.name) for e in cls if e.name is not None]


@dataclass(frozen=True)
class SemanticToken:
    """Basic information for a semantic token.

    Attributes:
        line: Line number of the token (0-indexed)
        start: Starting column of the token
        length: Length of the token
        token_type: Index of the token type
        token_modifiers: Bit flags for token modifiers
    """

    line: int
    start: int
    length: int
    token_type: int
    token_modifiers: int

    def __lt__(self, other: Self) -> bool:
        """Compare tokens by line and column."""
        return (self.line, self.start) < (other.line, other.start)

    @classmethod
    def from_special_key(cls, key: SpecialKeyPosition) -> Self:
        """Create a semantic token from a special key."""
        return cls(
            line=key.lineno,
            start=key.start,
            length=key.end - key.start,
            token_type=TokenType.SPECIAL_KEY,
            token_modifiers=TokenModifier.DECLARATION,
        )

    @classmethod
    def from_target_highlight(cls, highlight: TargetValueHighlight) -> Self:
        """Create a semantic token from a target highlight."""
        # Determine modifiers based on object type
        match highlight.object_type:
            case "module":
                modifiers = TokenModifier.MODULE
            case "class":
                modifiers = TokenModifier.CLASS
            case "function":
                modifiers = TokenModifier.FUNCTION
            case "method":
                modifiers = TokenModifier.FUNCTION
            case "variable":
                modifiers = TokenModifier.VARIABLE
            case "constant":
                modifiers = TokenModifier.CONSTANT
            case "other":
                modifiers = TokenModifier.NONE

        return cls(
            line=highlight.lineno,
            start=highlight.start,
            length=len(highlight.content),
            token_type=TokenType.TARGET_VALUE,
            token_modifiers=modifiers,
        )

    @classmethod
    def from_target_arg_key(cls, position: TargetArgKeyPos) -> Self:
        return cls(
            line=position.lineno,
            start=position.start,
            length=len(position.content),
            token_type=TokenType.TARGET_ARG,
            token_modifiers=TokenModifier.VARIABLE,
        )

    @classmethod
    def from_interpolation_highlight(cls, highlight: InterpolationHighlight) -> Self:
        """Create a semantic token from an interpolation highlight."""
        match highlight.token_type:
            case "reference":
                token_type = TokenType.INTERPOLATION_REF
                modifiers = TokenModifier.REFERENCE
            case "function":
                token_type = TokenType.INTERPOLATION_FUNC
                modifiers = TokenModifier.FUNCTION
            case "bracket_close" | "bracket_open":
                token_type = TokenType.INTERPOLATION_BRACKET
                modifiers = TokenModifier.BRACKET

        return cls(
            line=highlight.start_line,
            start=highlight.start_column,
            length=len(highlight.content),
            token_type=token_type,
            token_modifiers=modifiers,
        )

    @classmethod
    def from_package_directive(cls, package: HydraPackagePosition) -> tuple[Self, Self]:
        """Create semantic tokens from a package declaration."""
        directive_token = cls(
            line=0,  # Always in the first line
            start=package.directive.start,
            length=len(package.directive.content),
            token_type=TokenType.PACKAGE_DIRECTIVE,
            token_modifiers=TokenModifier.DECLARATION,
        )

        name_token = cls(
            line=0,  # Always in the first line
            start=package.name.start,
            length=len(package.name.content),
            token_type=TokenType.PACKAGE_NAME,
            token_modifiers=TokenModifier.MODULE,
        )

        return (directive_token, name_token)


@dataclass
class SemanticTokensBuilder:
    """Builder for a collection of semantic tokens.

    This class manages a collection of semantic tokens and
    converts them to the data format required by the Language Server Protocol
    (a continuous array of integers).

    Attributes:
        tokens: List of semantic tokens
    """

    tokens: list[SemanticToken] = field(default_factory=list)

    def add_tokens(self, *tokens: SemanticToken) -> None:
        """Add multiple tokens to the collection."""
        self.tokens.extend(tokens)

    def build(self) -> list[int]:
        """Convert tokens to LSP data format.

        Returns:
            Data array in LSP format (each token is represented as 5 consecutive numbers)
        """
        if not self.tokens:
            return []

        # Sort tokens by line and column
        sorted_tokens = sorted(self.tokens)

        # Convert to the data format required by LSP
        data: list[int] = []
        prev_line = 0
        prev_start = 0

        for token in sorted_tokens:
            # Calculate line offset (difference from previous token)
            delta_line = token.line - prev_line

            # Calculate column offset if on same line, or absolute position if on a new line
            delta_start = token.start - prev_start if delta_line == 0 else token.start

            # Add 5 values to the data array
            data.extend(
                [
                    delta_line,
                    delta_start,
                    token.length,
                    token.token_type,
                    token.token_modifiers,
                ]
            )

            # Update current position
            prev_line = token.line
            prev_start = token.start

        return data
