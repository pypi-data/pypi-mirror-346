from pydantic import BaseModel, Field
from abc import ABC, abstractmethod
from itertools import count
from datetime import date
from typing import List, Optional
from enum import Enum

class Address(BaseModel):
    street: str
    city: str
    zip: int

class StoreType(Enum):
    SUPERMARKET = "supermarket"
    BEAUTY = "beauty"
    CLOTHING = "clothing"
    FURNITURE = "furniture"
    GARDEN = "garden"
    TOYS = "toys"
    SPORTS = "sports"
    PHARMACY = "pharmacy"
    ELECTRONICS = "electronics"

class PaymentMethodType(Enum):
    CASH = "cash"
    CARD = "card"

class PaymentMethod(BaseModel):
    method: PaymentMethodType
    card: Optional[str] = None


class TaxClass(Enum):
    REGULAR = 0.19
    REDUCED = 0.07
    EXEMPT = 0.0


class QuantityUnit(Enum):
    KG = "kg"
    G = "g"
    L = "l"
    ML = "ml"
    PCS = "pcs"

class Quantity(BaseModel):
    unit: QuantityUnit
    weight: Optional[float] = None

class Item(BaseModel):
    name: str
    price: float
    unit: Optional[str] = None
    weight: Optional[float] = None
    description: Optional[str] = None
    tax_class: Optional[float] = None
    receipt_uid: Optional[str] = None

class Store(BaseModel,ABC):
    name: str
    type: StoreType
    UID : str = None
    id: int = Field(default_factory=count().__next__)
    address: Optional[Address] = None
    phone: Optional[str] = None

    @abstractmethod
    def _address_extract(self,raw_text: str) -> "Address":
        """
        Extracts the address from the raw text of the receipt.
        """
        pass
            
    @abstractmethod
    def _phone_extract(self, raw_text: str) -> str:
        """
        Extracts the phone number from the raw text of the receipt.
        """
        pass

    
    @abstractmethod
    def _uid_extract(self, raw_text: str) -> str:
        """
        Extracts the UID from the raw text of the receipt.
        """
        pass

    @abstractmethod
    def _items_extract(self, ebon_list: List) -> str:
        """
        Extracts the Items from the raw text of the receipt.
        """
        pass

    @abstractmethod
    def _sum_extract(self, raw_text: str) -> float:
        """
        Extracts the total sum from the raw text of the receipt.
        """
        pass

    @abstractmethod
    def _payment_extract(self, raw_text: str) -> float:
        """
        Extracts the Payment method from the raw text of the receipt.
        """
        pass

    @abstractmethod
    def _date_extract(self, raw_text: str) -> float:
        """
        Extracts the date from the raw text of the receipt.
        """
        pass  
    @abstractmethod
    def _bonNr_extract(self, raw_text: str) -> float:
        """
        Extracts Bon Number from the raw text of the receipt.
        """
        pass  
    @abstractmethod
    def parse_ebon(self, ebon_pdf) -> "Receipt":
        """
        Parses a PDF receipt file into a Receipt model.
        """
        raise NotImplementedError("PDF parsing not yet implemented.")

class Receipt(BaseModel):
    ebonNr: int
    store: Store
    date: date
    total: float
    payment_method: PaymentMethod
    items: List[Item]
    