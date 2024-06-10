import phonenumbers
from phonenumbers import geocoder, carrier, timezone
# import requests
import logging
import json
import argparse

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def print_banner():
    banner = """ 
\033[38;2;75;0;130m
    

 ██▓███   ██░ ██  ▒█████   ███▄    █   ██████  ██▓ ███▄    █ ▄▄▄█████▓
▓██░  ██▒▓██░ ██▒▒██▒  ██▒ ██ ▀█   █ ▒██    ▒ ▓██▒ ██ ▀█   █ ▓  ██▒ ▓▒
▓██░ ██▓▒▒██▀▀██░▒██░  ██▒▓██  ▀█ ██▒░ ▓██▄   ▒██▒▓██  ▀█ ██▒▒ ▓██░ ▒░
▒██▄█▓▒ ▒░▓█ ░██ ▒██   ██░▓██▒  ▐▌██▒  ▒   ██▒░██░▓██▒  ▐▌██▒░ ▓██▓ ░ 
▒██▒ ░  ░░▓█▒░██▓░ ████▓▒░▒██░   ▓██░▒██████▒▒░██░▒██░   ▓██░  ▒██▒ ░ 
▒▓▒░ ░  ░ ▒ ░░▒░▒░ ▒░▒░▒░ ░ ▒░   ▒ ▒ ▒ ▒▓▒ ▒ ░░▓  ░ ▒░   ▒ ▒   ▒ ░░   
░▒ ░      ▒ ░▒░ ░  ░ ▒ ▒░ ░ ░░   ░ ▒░░ ░▒  ░ ░ ▒ ░░ ░░   ░ ▒░    ░    
░░        ░  ░░ ░░ ░ ░ ▒     ░   ░ ░ ░  ░  ░   ▒ ░   ░   ░ ░   ░      
          ░  ░  ░    ░ ░           ░       ░   ░           ░          
                                                                      

\033[0m

<<<<<==================================================>>>>>
                        PhonSint
A Comprehensive Information Tool to Hunt down Phone Numbers
<<<<<==================================================>>>>>


    """
    print(banner)

def get_phone_number_info(phone_number: str):
    try:
        # Parse the phone number
        parsed_number = phonenumbers.parse(phone_number)
        logging.debug(f"Parsed number: {parsed_number}")
        
        # Get country information
        country = geocoder.description_for_number(parsed_number, "en")
        logging.debug(f"Country: {country}")
        
        # Get carrier information
        sim_carrier = carrier.name_for_number(parsed_number, "en")
        logging.debug(f"Carrier: {sim_carrier}")
        
        # Get time zones
        time_zones = timezone.time_zones_for_number(parsed_number)
        logging.debug(f"Time zones: {time_zones}")
        
        # Check if the phone number is valid
        is_valid = phonenumbers.is_valid_number(parsed_number)
        logging.debug(f"Is valid: {is_valid}")
        
        # Format the number in international format
        international_format = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        logging.debug(f"International format: {international_format}")
        
        # Format the number in national format
        national_format = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.NATIONAL)
        logging.debug(f"National format: {national_format}")
        
        # Get location details from external API (using country code)
        # country_code = parsed_number.country_code
        # try:
        #     location_details_response = requests.get(f'https://restcountries.com/v3.1/alpha/{country_code}', timeout=5)
        #     location_details_response.raise_for_status()  # Raise HTTPError for bad responses
        #     location_details = location_details_response.json()
        #     logging.debug(f"Location details: {location_details}")
        # except requests.RequestException as e:
        #     logging.error(f"RequestException: {e}")
        #     location_details = [{"error": "Could not retrieve location details"}]

        return {
            "phone_number": phone_number,
            "country": country,
            "carrier": sim_carrier,
            "time_zones": list(time_zones),
            "is_valid": is_valid,
            "international_format": international_format,
            "national_format": national_format,
            # "location_details": location_details[0] if location_details else {}
        }
    except phonenumbers.NumberParseException as e:
        logging.error(f"NumberParseException: {e}")
        return {"error": str(e)}

def save_to_file(data, filename):
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        logging.info(f"Data saved to {filename}")
    except IOError as e:
        logging.error(f"IOError: {e}")

def main():
    print_banner()
    
    parser = argparse.ArgumentParser(description="Get phone number information.")
    parser.add_argument("phone_number", help="The phone number to look up.")
    parser.add_argument("--output", "-o", help="The file to save the results to.")
    args = parser.parse_args()

    info = get_phone_number_info(args.phone_number)
    if "error" in info:
        print(f"Error: {info['error']}")
    else:
        print(json.dumps(info, indent=4))
        if args.output:
            save_to_file(info, args.output)

if __name__ == "__main__":
    main()
