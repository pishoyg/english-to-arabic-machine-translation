import argparse
import json
import logging
import os
import time
import smtplib, ssl

# Define arguments.
parser = argparse.ArgumentParser(description=
  'Periodically send email updates on witnessed improvement in BLEU score.'
)
parser.add_argument(
  '--out_dir',
  type=str,
  required=True,
  nargs=1,
  help='Training output directory.'
)
parser.add_argument(
  '--email_specs',
  type=str,
  nargs=1,
  default='email_specs.json',
  help='JSON file containing email specs.'
)
parser.add_argument(
  '--period',
  type=int,
  nargs=1,
  default=60,
  help='Check on currrent best-bleu every <period> seconds.'
)
parser.add_argument(
  '--must_send_every_n_periods',
  type=int,
  nargs=1,
  default=30,
  help='Must send an update email every <n> periods.'
)
args = parser.parse_args()

# Preprocess arguments.
for attr_name in ['out_dir', 'email_specs']:
  attr_val = getattr(args, attr_name)
  if isinstance(attr_val, list):
    assert len(attr_val) == 1
    setattr(args, attr_name, attr_val[0])
  else:
    assert isinstance(attr_val, str)
with open(args.email_specs) as email_specs:
  args.email_specs = json.loads(email_specs.read())
  for attr_name in ['sender_email', 'password', 'receiver_emails']:
    setattr(args, attr_name, args.email_specs[attr_name])
  del args.email_specs

# Get-current-BLEU-score method.
def get_cur_bleu():
  with open(os.path.join(args.out_dir, 'hparams')) as hparams:
    return json.loads(hparams.read())['best_bleu']

# Experiment name.
name = os.path.basename(os.path.normpath(args.out_dir))

# Loop for email updates.
with smtplib.SMTP_SSL("smtp.gmail.com",
                      port=465,
                      context=ssl.create_default_context()) as server:
  server.login(args.sender_email, args.password)
  last_bleu = -1.0
  counter = 0
  while True:
    time.sleep(args.period)
    send = False
    send |= (counter == 0)
    counter = (counter + 1) % args.must_send_every_n_periods
    try:
      cur_bleu = get_cur_bleu()
      message = str(cur_bleu)
      send |= (cur_bleu != last_bleu)
    except Exception as e:
      message = str(e)
      send |= True
    if send:
      server.sendmail(
          args.sender_email,
          args.receiver_emails,
          "Subject: {name}\n\n{message}".format(
              name=name, message=message))
      last_bleu = cur_bleu
