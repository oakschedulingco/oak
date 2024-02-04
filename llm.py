import sys
import time
import driver
import json
from yaspin import yaspin
from openai import OpenAI
from colorama import Fore, Style

KEY = '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'

client = OpenAI(api_key=KEY)
thread = client.beta.threads.create()

displayedMessages = []

med_list = {
    "5e2f5b13-d70e-4a87-8bfd-74bcae33343d": {
        "name": "Flu Vaccine",
        "age": "minimum 6 months of age"
    },
    "ec8e36dd-3949-48be-b035-26fa53f1bb07": {
        "name": "Flu Vaccine - Nasal Spray",
        "age": "minimum 2 years of age, and a maximum 49 years of age"
    },
    "8b8738d4-181c-48b3-91c7-e81bc8e44eca": {
        "name": "Flu Vaccine - Seniors",
        "age": "minimum 65 years of age"
    }
}

ctx = ''
with open('instructions.txt') as f:
    ctx = f.read()

fn_def = {
    "type": "function",
    "function": {
        "name": "get_avail_appts",
        "description": "Gets the available appointments for the given day and user information",
        "parameters": {
            "type": "object",
            "properties": {
                "zip": {"type": "string", "description": "The 5-digit US postal code provided by the user"},
                "dob": {"type": "string", "description": "The date of birth provided by the user, in the format MM/DD/YYYY. Reformat into this format if needed, but confirm with the user that the reformat is correct first."},
                "email": {"type": "string", "description": "The RFC-compliant email address provided by the user"},
                "phone": {"type": "string", "description": "The 10-digit US phone number provided by the user, without any spaces or dashes. Reformat if needed."},
                "smsyes": {"type": "boolean", "description": "Whether or not the user wants email and phone notifications about their appointment"},
                "flu": {"type": "boolean", "description": "Whether or not the user wants the Flu vaccine in this appointment. If no, default to false."},
                "covid": {"type": "boolean", "description": "Whether or not the user wants the updated COVID-19 vaccine in this appointment. If no, default to false."},
                "target_date": {"type": "string", "description": "The target date for the appointment, within a month from today 's date, in the format YYYY-MM-DD."}
            }
        }
    }
}

def get_avail_appts(zip, dob, email, phone, smsyes, flu, covid, target_date):
    return driver.check_date_availability(zip, dob, email, phone, smsyes, flu, covid, False, False, False, '10', target_date)

def run():
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id='asst_e88bh130ldWF8fNrJ9TErqYq',
        instructions=ctx
    )

    with yaspin(text='Willow is thinking...', color='green') as spinner:
        while run.status == 'queued' or run.status == 'in_progress' or run.status == 'requires_action':
            run = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
            time.sleep(0.5)
            if run.status == 'queued':
                spinner.text = 'Willow is thinking...'
            elif run.status == 'in_progress':
                spinner.text = 'Willow is responding...'
            elif run.status == 'requires_action':
                spinner.text = 'Contacting healthcare providers..'
                args = json.loads(run.required_action.submit_tool_outputs.tool_calls[0].function.arguments)
                # zip, dob, email, phone, smsyes, flu, covid, target_date
                resp = get_avail_appts(args['zip'], args['dob'], args['email'], args['phone'], args['smsyes'], 'flu' in args and args['flu'], 'covid' in args and args['covid'], args['target_date'])
                run = client.beta.threads.runs.submit_tool_outputs(
                    thread_id=thread.id,
                    run_id=run.id,
                    tool_outputs=[
                        {
                            "tool_call_id": run.required_action.submit_tool_outputs.tool_calls[0].id,
                            "output": '\n'.join(resp)
                        }
                    ]
                )

        if run.status == 'completed':
            spinner.text = 'Responded'
            spinner.hide()
        elif run.status == 'cancelling':
            spinner.fail('💥 Job is being cancelled by OpenAI')
            sys.exit(1)
        elif run.status == 'cancelled':
            spinner.fail('💥 Job cancelled by OpenAI')
            sys.exit(1)
        elif run.status == 'failed':
            spinner.fail('💥 Response generation failed')
            print(run.last_error)
            sys.exit(1)
        elif run.status == 'expired':
            spinner.fail('💥 Response took too long to generate')
            sys.exit(1)



    messages = client.beta.threads.messages.list(
        thread_id=thread.id
    )
    for message in messages:
        if message.id not in displayedMessages and not message.assistant_id == None:
            for content in message.content:
                print(Style.BRIGHT + Fore.BLUE + 'Willow: ' + Style.RESET_ALL + content.text.value.replace('[DONE///CONVERSATIONCOMPLETE]', ''))
                if '[DONE///CONVERSATIONCOMPLETE]' in content.text.value:
                    print(Style.BRIGHT + Fore.BLUE + "Willow" + Style.NORMAL + " ended the conversation." + Style.RESET_ALL)
                    sys.exit()
            displayedMessages.append(message.id)


def add_message(msg):
    try:
        message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=msg
        )
    except:
        time.sleep(0.5)
        add_message(msg)

with open('logo.txt') as f:
    print(Style.BRIGHT + Fore.GREEN + f.read() + Style.RESET_ALL)

try:
    run()

    while True:
        add_message(input(Style.BRIGHT + Fore.GREEN + 'User: ' + Style.RESET_ALL))
        run()
except KeyboardInterrupt:
    print()
    print(Style.BRIGHT + Fore.GREEN + "User" + Style.NORMAL + " ended the conversation." + Style.RESET_ALL)