import os
from twilio.rest import Client
from enum import Enum
from dotenv import load_dotenv

load_dotenv()

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
prod_account_sid = os.environ["TWILIO_ACCOUNT_SID"]
prod_auth_token = os.environ["TWILIO_AUTH_TOKEN"]

main_account_sid = os.environ["MAIN_TWILIO_SID"]
main_auth_token = os.environ["MAIN_TWILIO_AUTH_TOKEN"]

prod_client = Client(prod_account_sid, prod_auth_token)
main_client = Client(main_account_sid, main_auth_token)

# other IDs
TWILIO_BUSINESS_PROFILE_SID = os.environ["TWILIO_BUSINESS_PROFILE_SID"]


class WaymarkerAreaCodes(int, Enum):
    RICHMOND = 804
    HAMPTON_ROADS = 757
    SEATTLE = 206
    DEFAULT = 628  # San Franciscos


def generate_new_twilio_number(area_code: str) -> str:
    new_numbers = prod_client.available_phone_numbers("US").local.list(
        area_code=area_code, limit=1
    )

    return new_numbers[0].phone_number


async def provision_new_twilio_number(phone_number: str, friendly_name: str):
    incoming_phone_number = prod_client.incoming_phone_numbers.create(
        phone_number=phone_number,
        friendly_name=friendly_name,
        emergency_address_sid=os.environ["TWILIO_ADDRESS_SID"],
        voice_application_sid=os.environ["TWILIO_VOICE_APP_SID"],
    )

    number_sid = incoming_phone_number.sid

    # Add the number to all the test products
    # TODO: do any of these 'trust products' actually work?
    await _add_number_to_business_profile(number_sid=number_sid)
    await _add_number_to_shaken(number_sid=number_sid)
    await _add_number_to_cnam(number_sid=number_sid)
    await _add_number_to_voice_integrity(number_sid=number_sid)

    # Add the number to the messaging service
    await _add_number_to_messaging_service(number_sid=number_sid)


async def _add_number_to_business_profile(number_sid: str):
    customer_profiles_channel_endpoint_assignment = (
        main_client.trusthub.v1.customer_profiles(
            os.environ["TWILIO_BUSINESS_PROFILE_SID"]
        ).customer_profiles_channel_endpoint_assignment.create(
            channel_endpoint_type="phone-number",
            channel_endpoint_sid=number_sid,
        )
    )
    print(customer_profiles_channel_endpoint_assignment.sid)


async def _add_number_to_shaken(number_sid: str):
    main_client.trusthub.v1.trust_products(
        os.environ["TWILIO_SHAKEN_SID"]
    ).trust_products_channel_endpoint_assignment.create(
        channel_endpoint_type="phone-number",
        channel_endpoint_sid=number_sid,
    )


async def _add_number_to_cnam(number_sid: str):
    """Add Caller ID to this number

    Caller ID Name (CNAM) is a feature that displays the name of the caller
    the receiving end of a call.
    Args:
        number_sid (str): the SID of the Twilio phone number
    """
    main_client.trusthub.v1.trust_products(
        os.environ["TWILIO_CNAM_SID"]
    ).trust_products_channel_endpoint_assignment.create(
        channel_endpoint_type="phone-number",
        channel_endpoint_sid=number_sid,
    )


async def _add_number_to_voice_integrity(number_sid: str):
    main_client.trusthub.v1.trust_products(
        os.environ["TWILIO_VOICE_INTEGRITY_SID"]
    ).trust_products_channel_endpoint_assignment.create(
        channel_endpoint_type="phone-number",
        channel_endpoint_sid=number_sid,
    )


async def _add_number_to_messaging_service(number_sid: str):
    phone_number = prod_client.messaging.v1.services(
        os.environ["TWILIO_SMS_APP_SID"]
    ).phone_numbers.create(phone_number_sid=number_sid)
    print(phone_number.sid)
