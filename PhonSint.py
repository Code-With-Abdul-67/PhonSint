import phonenumbers
from phonenumbers import geocoder, carrier, timezone
import logging
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
                 Made by 0x-Cyber-Lunerr
                       Version 1.0
<<<<<==================================================>>>>>

    """
    print(banner)

def save_to_file_as_text(data, filename):
    try:
        with open(filename, 'w') as f:
            for key, value in data.items():
                f.write(f"{key}: {value}\n")
        logging.info(f"Data saved to {filename}")
        print(f"Data saved to {filename}")
    except IOError as e:
        logging.error(f"IOError: {e}")
        print(f"Error: {e}")

def main():
    print_banner()
    
    parser = argparse.ArgumentParser(description="Get phone number information.")
    parser.add_argument("phone_number", help="The phone number to look up.")
    args = parser.parse_args()

    try:
        # Parse the phone number
        parsed_number = phonenumbers.parse(args.phone_number)
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
        print("\n")
        print("Final Report about your Target Phone Number")
        print("<<--------------------------------------->>")
        info = {
            "01- Phone-number": args.phone_number,
            "02- Country": country,
            "03- Sim-Carrier": sim_carrier,
            "04- Time-Zones": list(time_zones),
            "05- Validity": is_valid,
            "06- International-Format": international_format,
            "07- National-Format": national_format,
        }
        
        for key, value in info.items():
            print(f"{key}: {value}")
       
        save_prompt = input("Would you like to save the information in a form of text file? (yes/no): ").strip().lower()
        if save_prompt in ['yes', 'y']:
            filename = f"{args.phone_number}_info.txt"
            save_to_file_as_text(info, filename)
    except phonenumbers.NumberParseException as e:
        logging.error(f"NumberParseException: {e}")
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
