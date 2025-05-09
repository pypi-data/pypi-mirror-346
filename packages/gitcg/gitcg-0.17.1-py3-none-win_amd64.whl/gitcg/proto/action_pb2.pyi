import enums_pb2 as _enums_pb2
import preview_pb2 as _preview_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ActionValidity(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ACTION_VALIDITY_VALID: _ClassVar[ActionValidity]
    ACTION_VALIDITY_CONDITION_NOT_MET: _ClassVar[ActionValidity]
    ACTION_VALIDITY_NO_TARGET: _ClassVar[ActionValidity]
    ACTION_VALIDITY_NO_DICE: _ClassVar[ActionValidity]
    ACTION_VALIDITY_NO_ENERGY: _ClassVar[ActionValidity]
    ACTION_VALIDITY_DISABLED: _ClassVar[ActionValidity]
ACTION_VALIDITY_VALID: ActionValidity
ACTION_VALIDITY_CONDITION_NOT_MET: ActionValidity
ACTION_VALIDITY_NO_TARGET: ActionValidity
ACTION_VALIDITY_NO_DICE: ActionValidity
ACTION_VALIDITY_NO_ENERGY: ActionValidity
ACTION_VALIDITY_DISABLED: ActionValidity

class Action(_message.Message):
    __slots__ = ("switch_active", "play_card", "use_skill", "elemental_tuning", "declare_end", "preview", "required_cost", "auto_selected_dice", "validity")
    SWITCH_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    PLAY_CARD_FIELD_NUMBER: _ClassVar[int]
    USE_SKILL_FIELD_NUMBER: _ClassVar[int]
    ELEMENTAL_TUNING_FIELD_NUMBER: _ClassVar[int]
    DECLARE_END_FIELD_NUMBER: _ClassVar[int]
    PREVIEW_FIELD_NUMBER: _ClassVar[int]
    REQUIRED_COST_FIELD_NUMBER: _ClassVar[int]
    AUTO_SELECTED_DICE_FIELD_NUMBER: _ClassVar[int]
    VALIDITY_FIELD_NUMBER: _ClassVar[int]
    switch_active: SwitchActiveAction
    play_card: PlayCardAction
    use_skill: UseSkillAction
    elemental_tuning: ElementalTuningAction
    declare_end: DeclareEndAction
    preview: _containers.RepeatedCompositeFieldContainer[_preview_pb2.PreviewData]
    required_cost: _containers.RepeatedCompositeFieldContainer[_enums_pb2.DiceRequirement]
    auto_selected_dice: _containers.RepeatedScalarFieldContainer[_enums_pb2.DiceType]
    validity: ActionValidity
    def __init__(self, switch_active: _Optional[_Union[SwitchActiveAction, _Mapping]] = ..., play_card: _Optional[_Union[PlayCardAction, _Mapping]] = ..., use_skill: _Optional[_Union[UseSkillAction, _Mapping]] = ..., elemental_tuning: _Optional[_Union[ElementalTuningAction, _Mapping]] = ..., declare_end: _Optional[_Union[DeclareEndAction, _Mapping]] = ..., preview: _Optional[_Iterable[_Union[_preview_pb2.PreviewData, _Mapping]]] = ..., required_cost: _Optional[_Iterable[_Union[_enums_pb2.DiceRequirement, _Mapping]]] = ..., auto_selected_dice: _Optional[_Iterable[_Union[_enums_pb2.DiceType, str]]] = ..., validity: _Optional[_Union[ActionValidity, str]] = ...) -> None: ...

class SwitchActiveAction(_message.Message):
    __slots__ = ("character_id", "character_definition_id")
    CHARACTER_ID_FIELD_NUMBER: _ClassVar[int]
    CHARACTER_DEFINITION_ID_FIELD_NUMBER: _ClassVar[int]
    character_id: int
    character_definition_id: int
    def __init__(self, character_id: _Optional[int] = ..., character_definition_id: _Optional[int] = ...) -> None: ...

class PlayCardAction(_message.Message):
    __slots__ = ("card_id", "card_definition_id", "target_ids", "will_be_effectless")
    CARD_ID_FIELD_NUMBER: _ClassVar[int]
    CARD_DEFINITION_ID_FIELD_NUMBER: _ClassVar[int]
    TARGET_IDS_FIELD_NUMBER: _ClassVar[int]
    WILL_BE_EFFECTLESS_FIELD_NUMBER: _ClassVar[int]
    card_id: int
    card_definition_id: int
    target_ids: _containers.RepeatedScalarFieldContainer[int]
    will_be_effectless: bool
    def __init__(self, card_id: _Optional[int] = ..., card_definition_id: _Optional[int] = ..., target_ids: _Optional[_Iterable[int]] = ..., will_be_effectless: bool = ...) -> None: ...

class UseSkillAction(_message.Message):
    __slots__ = ("skill_definition_id", "target_ids", "main_damage_target_id")
    SKILL_DEFINITION_ID_FIELD_NUMBER: _ClassVar[int]
    TARGET_IDS_FIELD_NUMBER: _ClassVar[int]
    MAIN_DAMAGE_TARGET_ID_FIELD_NUMBER: _ClassVar[int]
    skill_definition_id: int
    target_ids: _containers.RepeatedScalarFieldContainer[int]
    main_damage_target_id: int
    def __init__(self, skill_definition_id: _Optional[int] = ..., target_ids: _Optional[_Iterable[int]] = ..., main_damage_target_id: _Optional[int] = ...) -> None: ...

class ElementalTuningAction(_message.Message):
    __slots__ = ("removed_card_id", "target_dice")
    REMOVED_CARD_ID_FIELD_NUMBER: _ClassVar[int]
    TARGET_DICE_FIELD_NUMBER: _ClassVar[int]
    removed_card_id: int
    target_dice: _enums_pb2.DiceType
    def __init__(self, removed_card_id: _Optional[int] = ..., target_dice: _Optional[_Union[_enums_pb2.DiceType, str]] = ...) -> None: ...

class DeclareEndAction(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
