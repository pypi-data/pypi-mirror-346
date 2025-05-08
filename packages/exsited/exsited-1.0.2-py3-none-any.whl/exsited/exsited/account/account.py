from exsited.exsited.account.account_api_url import AccountApiUrl
from exsited.exsited.account.dto.account_dto import AccountCreateDTO, AccountDetailsDTO, AccountListDTO, \
    AccountUpdateInformationDTO, AccountContactsDTO, PaymentMethodsAddDTO, PaymentMethodsDetailsDTO, \
    PaymentCardMethodsAddDTO, \
    PaymentMethodsListDTO, AccountCancelDTO, AccountCancelDataDTO, AccountReactivateDataDTO, AccountReactivateDTO, \
    AccountContactsTypeDTO, AccountContactUpdateDTO, AccountContactsUpdateDTO, AccountReactiveResponseDTO, \
    AccountAddressesAddDTO, AccountCancelResponseDTO
from exsited.exsited.account.dto.account_nested_dto import AccountContactsUpdate, ContactDTO
from exsited.exsited.common.common_enum import SortDirection
from exsited.common.sdk_util import SDKUtil
from exsited.http.ab_rest_processor import ABRestProcessor


class Account(ABRestProcessor):

    def create(self, request_data: AccountCreateDTO) -> AccountDetailsDTO:
        response = self.post(url=AccountApiUrl.ACCOUNTS, request_obj=request_data, response_obj=AccountDetailsDTO())
        return response

    def create_v3(self, request_data: AccountCreateDTO) -> AccountDetailsDTO:
        response = self.post(url=AccountApiUrl.ACCOUNTS_V3, request_obj=request_data, response_obj=AccountDetailsDTO())
        return response

    def list(self, limit: int = None, offset: int = None, direction: SortDirection = None,
             order_by: str = None) -> AccountListDTO:
        params = SDKUtil.init_pagination_params(limit=limit, offset=offset, direction=direction, order_by=order_by)
        response = self.get(url=AccountApiUrl.ACCOUNTS, params=params, response_obj=AccountListDTO())
        return response

    def details(self, id: str) -> AccountDetailsDTO:
        response = self.get(url=AccountApiUrl.ACCOUNTS_V3 + f"/{id}", response_obj=AccountDetailsDTO())
        return response

    def details_information(self, id: str) -> AccountDetailsDTO:
        response = self.get(url=AccountApiUrl.ACCOUNT_INFORMATION.format(id=id), response_obj=AccountDetailsDTO())
        return response

    def cancel(self, id: str, request_data: AccountCancelDataDTO):
        cancel_request = AccountCancelDTO(account=request_data)
        response = self.post(url=AccountApiUrl.ACCOUNT_CANCEL.format(id=id), request_obj=cancel_request,
                             response_obj=AccountCancelResponseDTO())
        return response

    def reactivate(self, id: str, request_data: AccountReactivateDataDTO) -> AccountDetailsDTO:
        reactivate_request = AccountReactivateDTO(account=request_data)
        response = self.post(url=AccountApiUrl.ACCOUNT_REACTIVATE.format(id=id), request_obj=reactivate_request,
                             response_obj=AccountReactiveResponseDTO())
        return response

    def reactivate_v3(self, id: str, request_data: AccountReactivateDataDTO) -> AccountDetailsDTO:
        reactivate_request = AccountReactivateDTO(account=request_data)
        response = self.post(url=AccountApiUrl.ACCOUNT_REACTIVATE_V3.format(id=id), request_obj=reactivate_request,
                             response_obj=AccountReactiveResponseDTO())
        return response

    def delete(self, id: str):
        response = self.delete_request(url=AccountApiUrl.ACCOUNT_DELETE.format(id=id))
        return response

    def contact_delete(self, id: str, contact_type: str):
        response = self.delete_request(
            url=AccountApiUrl.ACCOUNT_CONTACT_DELETE.format(id=id, contact_type=contact_type))
        return response

    def update_information(self, id: str, request_data: AccountUpdateInformationDTO) -> AccountDetailsDTO:
        response = self.patch(url=AccountApiUrl.ACCOUNT_UPDATE_INFORMATION.format(id=id), request_obj=request_data,
                              response_obj=AccountDetailsDTO())
        return response

    def get_contacts(self, id: str) -> AccountContactsDTO:
        response = self.get(url=AccountApiUrl.ACCOUNT_CONTACTS.format(id=id), response_obj=AccountContactsDTO())
        return response

    def get_contact_type(self, id: str, contact_type: str) -> AccountContactsDTO:
        response = self.get(url=AccountApiUrl.ACCOUNT_CONTACT_TYPE.format(id=id, contact_type=contact_type),
                            response_obj=AccountContactsDTO())
        return response

    def update_contact(self, id: str, contact_type: str,
                       request_data: AccountContactUpdateDTO) -> AccountContactsUpdateDTO:
        response = self.put(url=AccountApiUrl.ACCOUNT_CONTACT_UPDATE.format(id=id, contact_type=contact_type),
                            request_obj=request_data, response_obj=AccountContactsUpdateDTO)
        return response

    def update_contact_v3(self, id: str, contact_type: str,
                       request_data: AccountContactUpdateDTO) -> AccountContactsUpdateDTO:
        response = self.put(url=AccountApiUrl.ACCOUNT_CONTACT_UPDATE_V3.format(id=id, contact_type=contact_type),
                            request_obj=request_data, response_obj=AccountContactsUpdateDTO)
        return response

    def add_payment_method(self, account_id: str, request_data: PaymentMethodsAddDTO) -> PaymentMethodsDetailsDTO:
        response = self.post(url=AccountApiUrl.ACCOUNT_PAYMENT_METHODS.format(id=account_id), request_obj=request_data,
                             response_obj=PaymentMethodsDetailsDTO())
        return response

    def add_payment_card_method(self, account_id: str,
                                request_data: PaymentCardMethodsAddDTO) -> PaymentMethodsDetailsDTO:
        response = self.post(url=AccountApiUrl.ACCOUNT_PAYMENT_METHODS.format(id=account_id), request_obj=request_data,
                             response_obj=PaymentMethodsDetailsDTO())
        return response

    def add_payment_card_method_v3(self, account_id: str,
                                request_data: PaymentCardMethodsAddDTO) -> PaymentMethodsDetailsDTO:
        response = self.post(url=AccountApiUrl.ACCOUNT_PAYMENT_METHODS_V3.format(id=account_id), request_obj=request_data,
                             response_obj=PaymentMethodsDetailsDTO())
        return response

    def list_payment_method(self, account_id: str) -> PaymentMethodsListDTO:
        response = self.get(url=AccountApiUrl.ACCOUNT_PAYMENT_METHODS.format(id=account_id),
                            response_obj=PaymentMethodsListDTO())
        return response

    def delete_payment_method(self, account_id: str, reference: str):
        response = self.delete_request(
            url=AccountApiUrl.EACH_PAYMENT_METHODS.format(id=account_id, reference=reference))
        return response

    def delete_payment_method_v3(self, account_id: str, reference: str):
        response = self.delete_request(
            url=AccountApiUrl.EACH_PAYMENT_METHODS_V3.format(id=account_id, reference=reference))
        return response


    def payment_method_details(self, account_id: str, reference: str) -> PaymentMethodsDetailsDTO:
        response = self.get(url=AccountApiUrl.EACH_PAYMENT_METHODS.format(id=account_id, reference=reference),
                            response_obj=PaymentMethodsDetailsDTO())
        return response

    def billing_preference_details(self, account_id: str) -> AccountDetailsDTO:
        response = self.get(url=AccountApiUrl.ACCOUNT_BILLING_PREFERENCE.format(id=account_id),
                            response_obj=AccountDetailsDTO())
        return response