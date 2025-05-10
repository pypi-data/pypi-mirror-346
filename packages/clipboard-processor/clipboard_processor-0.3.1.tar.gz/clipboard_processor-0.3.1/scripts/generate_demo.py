#!/usr/bin/env python
import json
import os
import textwrap

from openai import OpenAI

from clipboard_processor.cli import PLUGINS
from clipboard_processor import __version__


def main():
    name = 'Merlin the Admin'
    prompt = f'''
        Please generate a demo text for a tool that parses machine-readable strings and displays the results in a human-readable format.
        The demo text should be a nerdy fairy tale in a medieval setting and include all of the following example inputs.
        To better embed the examples, a short explanation of the input is also given.
        Do not include the explanation in the final text.
        Do not include the human-readable version of the output in the text, as this should be done with the tool.
        The story should be a journey of a grumpy wizard "{name}" where those example strings pop up naturally as part of the story.
        Please use humorous language and a lot of cursing.
        Please also format the output in markdown, highlighting each of the example inputs as inline code, but without quotes.
        No headings or subheadings.
    '''
    prompt = textwrap.dedent(prompt)

    prompt2 = '''
        Please use these points as a skeleton:
        * the wizard wakes up at "cron time" (far too early for his taste)
        * he get's a "base64" encoded message from his friend and curses about the content
        * he goes out to the nearby castle
        * along the way and finds a part of an old carriage containing a VIN (he hates cars)
        * to gain access, needs the hex encoded "password", which makes him complain about weak security and suggesting to use a jwt instead
        * the guard at the gate files his complaint under the unix time of "now" as a primary id
        * even more angry, starts a discussion with the guard about data loss and why they don't use ULIDs as identifiers
        * in the castle, he needs to use a magic mirror - on a label on the back there is the MAC address
    '''
    prompt2 = textwrap.dedent(prompt2)

    example_inputs = []
    for plugin in PLUGINS:
        example_inputs.append({'input': plugin.example_input(), 'explanation': plugin.__doc__})

    client = OpenAI(
        api_key=os.environ.get('OPENAI_API_KEY'),
        base_url=os.environ.get('OPENAI_API_BASE', 'https://api.openai.com/v1'),
    )
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[{
            "role": "user",
            "content": prompt,
        }, {
            "role": "user",
            "content": json.dumps(example_inputs, indent=2),
        }, {
            "role": "user",
            "content": prompt2,
        }],
    )
    print(completion.choices[0].message.content)
    with open('DEMO.new.md', 'w') as f:
        f.write(f'# The Quest of {name}\n')
        f.write(f'### Demo text for clipboard-processor v{__version__}\n')
        f.write(completion.choices[0].message.content)


if __name__ == '__main__':
    main()
