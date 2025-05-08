from dataclasses import dataclass, field
from exsited.exsited.common.dto.common_dto import CurrencyDTO, TimeZoneDTO, PaginationDTO, CustomAttributesDTO, TaxDTO, \
    AddressDTO, CustomFormsDTO, CustomObjectDTO
from exsited.sdlize.ab_base_dto import ABBaseDTO
from exsited.exsited.account.dto.account_nested_dto import AccountingCodeDTO, CommunicationPreferenceDTO, \
    PaymentMethodsDataDTO, BillingPreferencesDTO, PaymentMethodsDTO, PaymentCardMethodsDTO, PaymentCardMethodsDataDTO, \
    PaymentMethodListDTO, AccountContacts, AccountContactsType, AccountContactsUpdate, AccountContactUpdate, ContactDTO, \
    PricingLevelDTO


@dataclass(kw_only=True)
class AccountDataDTO(ABBaseDTO):
    name: str = None
    emailAddress: str = None
    status: str = None
    id: str = None
    displayName: str = None
    description: str = None
    invoiceParentAccount: str = None
    type: str = None
    imageUri: str = None
    grantPortalAccess: str = None
    website: str = None
    linkedin: str = None
    twitter: str = None
    facebook: str = None
    createdBy: str = None
    createdOn: str = None
    lastUpdatedBy: str = None
    lastUpdatedOn: str = None
    uuid: str = None
    version: str = None
    parentAccount: str = None
    group: str = None
    manager: str = None
    referralTracking: str = None
    salesRep: str = None
    pricingLevel: PricingLevelDTO = None

    currency: CurrencyDTO = None
    timeZone: TimeZoneDTO = None
    tax: TaxDTO = None
    accountingCode: AccountingCodeDTO = None
    communicationPreference: list[CommunicationPreferenceDTO] = None
    paymentMethods: list[PaymentMethodsDataDTO] = None
    billingPreferences: BillingPreferencesDTO = None
    customAttributes: list[CustomAttributesDTO] = None
    addresses: list[AddressDTO] = None
    customForms: CustomFormsDTO = None
    eventUuid: str = None
    customObjects: list[CustomObjectDTO] = None
    kpis: dict = None
    contacts: list[ContactDTO] = None


@dataclass(kw_only=True)
class AccountCreateDTO(ABBaseDTO):
    account: AccountDataDTO


@dataclass(kw_only=True)
class AccountUpdateInformationDTO(ABBaseDTO):
    account: AccountDataDTO


@dataclass(kw_only=True)
class AccountDetailsDTO(ABBaseDTO):
    account: AccountDataDTO = None


@dataclass(kw_only=True)
class AccountReactiveResponseDTO(ABBaseDTO):
    eventUuid: str = None

@dataclass(kw_only=True)
class AccountCancelResponseDTO(ABBaseDTO):
    eventUuid: str = None


@dataclass(kw_only=True)
class AccountListDTO(ABBaseDTO):
    accounts: list[AccountDataDTO] = None
    pagination: PaginationDTO = None


@dataclass(kw_only=True)
class PaymentMethodsAddDTO(ABBaseDTO):
    account: PaymentMethodsDTO = None

    def method(self, payment_method: PaymentMethodsDataDTO):
        self.account = PaymentMethodsDTO(paymentMethod=payment_method)
        return self


@dataclass(kw_only=True)
class PaymentMethodsDetailsDTO(ABBaseDTO):
    account: PaymentMethodsDTO = None


@dataclass(kw_only=True)
class PaymentCardMethodsAddDTO(ABBaseDTO):
    account: PaymentCardMethodsDTO = None

    def method(self, payment_method: PaymentCardMethodsDataDTO):
        self.account = PaymentCardMethodsDTO(paymentMethod=payment_method)
        return self


@dataclass(kw_only=True)
class PaymentMethodsListDTO(ABBaseDTO):
    account: PaymentMethodListDTO = None


@dataclass(kw_only=True)
class AccountCancelDataDTO(ABBaseDTO):
    effectiveDate: str


@dataclass(kw_only=True)
class AccountCancelDTO(ABBaseDTO):
    account: AccountCancelDataDTO


@dataclass(kw_only=True)
class AccountReactivateDataDTO(ABBaseDTO):
    effectiveDate: str = None


@dataclass(kw_only=True)
class AccountReactivateDTO(ABBaseDTO):
    account: AccountReactivateDataDTO


@dataclass(kw_only=True)
class AccountContactsDTO(ABBaseDTO):
    account: AccountContacts = None


@dataclass(kw_only=True)
class AccountContactsTypeDTO(ABBaseDTO):
    account: AccountContactsType = None


@dataclass(kw_only=True)
class AccountContactUpdateDTO(ABBaseDTO):
    account: AccountContactUpdate = None


@dataclass(kw_only=True)
class AccountContactsUpdateDTO(ABBaseDTO):
    account: AccountContactsUpdate = None


@dataclass(kw_only=True)
class AccountAddressesAdd(ABBaseDTO):
    addresses: list[AddressDTO] = None


@dataclass(kw_only=True)
class AccountAddressesAddDTO(ABBaseDTO):
    account: AccountAddressesAdd = None