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
    DEFAULT = 628  # San Francisco


async def provision_new_waymarker_number(market: str, friendly_name: str):
    """Wrapper function to provision a new waymarker number through Twilio

    Args:
        market (str): The market of the Waymarker
        friendly_name (str): The friendly name of the number, to show up
            on the Twilio Console

    Raises:
        Exception: error when provisioning the new number

    Returns:
        twilio_number (str): the new Twilio number
    """
    try:
        area_code = get_area_code(market)
        twilio_number = generate_new_twilio_number(area_code)
        await provision_new_twilio_number(
            phone_number=twilio_number, friendly_name=friendly_name
        )
    except Exception as e:
        raise Exception(f"Error provisioning new waymarker number: {e}")
    return twilio_number


def get_area_code(market: str) -> int:
    """Gets the area code for a given market

    Args:
        market (str): the market that Waymark servers

    Raises:
        ValueError: if the market is not one of the accepted markets
    Returns:
        int: the area code for the market
    """
    if market == "Seattle":
        return WaymarkerAreaCodes.SEATTLE.value
    if market == "Richmond":
        return WaymarkerAreaCodes.RICHMOND.value
    if market == "Hampton Roads":
        return WaymarkerAreaCodes.HAMPTON_ROADS.value
    raise ValueError(f"Market {market} not found")


def generate_new_twilio_number(area_code: str) -> str:
    # Find a new available number with the selected area code
    new_numbers = prod_client.available_phone_numbers("US").local.list(
        area_code=area_code, limit=1
    )

    return new_numbers[0].phone_number


async def provision_new_twilio_number(phone_number: str, friendly_name: str):
    incoming_phone_number = prod_client.incoming_phone_numbers.create(
        phone_number=phone_number,
        friendly_name=friendly_name,
        emergency_address_sid=os.environ["TWILIO_ADDRESS_SID"],
        voice_application_sid=os.environ["TWILIO_TWIML_SID"],
    )

    number_sid = incoming_phone_number.sid

    # Add the number to all the test products
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
