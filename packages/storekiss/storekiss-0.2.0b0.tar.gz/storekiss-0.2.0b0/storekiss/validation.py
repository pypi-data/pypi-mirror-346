"""
Data validation utilities inspired by FireStore.
"""
from typing import Any, Dict, List, Optional, Type, Union, Callable
import datetime
from storekiss.exceptions import ValidationError


class FieldValidator:
    """Base class for field validators."""
    
    def __init__(self, required: bool = True, indexed: bool = False):
        self.required = required
        self.indexed = indexed
        
    def validate(self, value: Any) -> Any:
        """Validate a value against this field's rules."""
        if value is None:
            if self.required:
                raise ValidationError(f"Field is required")
            return None
        return self._validate(value)
    
    def _validate(self, value: Any) -> Any:
        """Implement specific validation logic in subclasses."""
        return value
        
    def get_sqlite_type(self) -> str:
        """Get the SQLite type for this field."""
        return "TEXT"


class StringField(FieldValidator):
    """Validator for string fields."""
    
    def __init__(
        self, 
        required: bool = True,
        min_length: Optional[int] = None,
        max_length: Optional[int] = None,
        indexed: bool = False
    ):
        super().__init__(required, indexed)
        self.min_length = min_length
        self.max_length = max_length
        
    def _validate(self, value: Any) -> str:
        if not isinstance(value, str):
            raise ValidationError(f"Expected string, got {type(value).__name__}")
        
        if self.min_length is not None and len(value) < self.min_length:
            raise ValidationError(f"String must be at least {self.min_length} characters")
            
        if self.max_length is not None and len(value) > self.max_length:
            raise ValidationError(f"String must be at most {self.max_length} characters")
            
        return value


class NumberField(FieldValidator):
    """Validator for numeric fields."""
    
    def __init__(
        self, 
        required: bool = True,
        min_value: Optional[Union[int, float]] = None,
        max_value: Optional[Union[int, float]] = None,
        integer_only: bool = False,
        indexed: bool = False
    ):
        super().__init__(required, indexed)
        self.min_value = min_value
        self.max_value = max_value
        self.integer_only = integer_only
        
    def get_sqlite_type(self) -> str:
        """Get the SQLite type for this field."""
        return "INTEGER" if self.integer_only else "REAL"
        
    def _validate(self, value: Any) -> Union[int, float]:
        if self.integer_only and not isinstance(value, int):
            raise ValidationError(f"Expected integer, got {type(value).__name__}")
        elif not isinstance(value, (int, float)):
            raise ValidationError(f"Expected number, got {type(value).__name__}")
        
        if self.min_value is not None and value < self.min_value:
            raise ValidationError(f"Number must be at least {self.min_value}")
            
        if self.max_value is not None and value > self.max_value:
            raise ValidationError(f"Number must be at most {self.max_value}")
            
        return value


class BooleanField(FieldValidator):
    """Validator for boolean fields."""
    
    def __init__(self, required: bool = True, indexed: bool = False):
        super().__init__(required, indexed)
        
    def get_sqlite_type(self) -> str:
        """Get the SQLite type for this field."""
        return "INTEGER"
    
    def _validate(self, value: Any) -> bool:
        if not isinstance(value, bool):
            raise ValidationError(f"Expected boolean, got {type(value).__name__}")
        return value


class DateTimeField(FieldValidator):
    """Validator for datetime fields."""
    
    def __init__(self, required: bool = True, indexed: bool = False):
        super().__init__(required, indexed)
        
    def get_sqlite_type(self) -> str:
        """Get the SQLite type for this field."""
        return "TEXT"
    
    def _validate(self, value: Any) -> datetime.datetime:
        if isinstance(value, str):
            try:
                return datetime.datetime.fromisoformat(value)
            except ValueError:
                raise ValidationError(f"Invalid datetime format: {value}")
        elif isinstance(value, datetime.datetime):
            return value
        else:
            raise ValidationError(f"Expected datetime or ISO format string, got {type(value).__name__}")


class ListField(FieldValidator):
    """Validator for list fields."""
    
    def __init__(
        self, 
        item_validator: FieldValidator,
        required: bool = True,
        min_length: Optional[int] = None,
        max_length: Optional[int] = None,
        indexed: bool = False
    ):
        super().__init__(required, indexed)
        self.item_validator = item_validator
        self.min_length = min_length
        self.max_length = max_length
        
    def _validate(self, value: Any) -> List[Any]:
        if not isinstance(value, list):
            raise ValidationError(f"Expected list, got {type(value).__name__}")
        
        if self.min_length is not None and len(value) < self.min_length:
            raise ValidationError(f"List must have at least {self.min_length} items")
            
        if self.max_length is not None and len(value) > self.max_length:
            raise ValidationError(f"List must have at most {self.max_length} items")
        
        return [self.item_validator.validate(item) for item in value]


class MapField(FieldValidator):
    """Validator for map/dict fields."""
    
    def __init__(
        self, 
        field_validators: Dict[str, FieldValidator],
        required: bool = True,
        allow_extra_fields: bool = False,
        indexed: bool = False
    ):
        super().__init__(required, indexed)
        self.field_validators = field_validators
        self.allow_extra_fields = allow_extra_fields
        
    def _validate(self, value: Any) -> Dict[str, Any]:
        if not isinstance(value, dict):
            raise ValidationError(f"Expected dict, got {type(value).__name__}")
        
        result = {}
        
        for field_name, validator in self.field_validators.items():
            if field_name in value:
                result[field_name] = validator.validate(value[field_name])
            elif validator.required:
                raise ValidationError(f"Required field '{field_name}' is missing")
            else:
                result[field_name] = None
        
        if not self.allow_extra_fields:
            extra_fields = set(value.keys()) - set(self.field_validators.keys())
            if extra_fields:
                raise ValidationError(f"Unexpected fields: {', '.join(extra_fields)}")
        else:
            for field_name in value:
                if field_name not in self.field_validators:
                    result[field_name] = value[field_name]
        
        return result


class Schema:
    """Schema definition for document validation.
    
    Firestoreと同様に、デフォルトですべてのフィールドを許可します。
    スキーマで定義されたフィールドは型チェックされますが、
    定義されていないフィールドも自由に書き込むことができます。
    """
    
    def __init__(self, fields: Dict[str, FieldValidator], allow_extra_fields: bool = True, index_all_fields: bool = False):
        self.fields = fields
        self.allow_extra_fields = allow_extra_fields  # デフォルトでTrue（すべてのフィールドを許可）
        self.index_all_fields = index_all_fields
        
        if index_all_fields:
            for field in self.fields.values():
                field.indexed = True
        
    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate data against this schema.
        
        スキーマで定義されたフィールドのみ検証し、
        定義されていないフィールドはそのまま通過させます。
        """
        if not isinstance(data, dict):
            raise ValidationError(f"Expected dict, got {type(data).__name__}")
        
        result = {}
        
        # スキーマで定義されたフィールドを検証
        for field_name, validator in self.fields.items():
            if field_name in data:
                result[field_name] = validator.validate(data[field_name])
            elif validator.required:
                raise ValidationError(f"Required field '{field_name}' is missing")
            else:
                result[field_name] = None
        
        # 追加フィールドの処理
        # allow_extra_fieldsがFalseの場合でも、警告のみ出して通過させる
        if not self.allow_extra_fields:
            extra_fields = set(data.keys()) - set(self.fields.keys())
            if extra_fields:
                import logging
                logging.warning(f"Unexpected fields in document: {', '.join(extra_fields)}")
        
        # すべてのフィールドをresultに追加
        for field_name in data:
            if field_name not in self.fields:
                result[field_name] = data[field_name]
        
        return result
