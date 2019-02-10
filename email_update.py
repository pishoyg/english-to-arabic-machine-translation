import argparse
import json
import os
import time
import smtplib, ssl

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
args = parser.parse_args()
for attr_name in ['out_dir', 'email_specs']:
  attr_val = getattr(args, attr_name)
  if isinstance(attr_val, list):
    assert len(attr_val) == 1
    setattr(args, attr_name, attr_val[0])
  else:
    assert isinstance(attr_val, str)


def get_cur_bleu():
  try:
    hparams = open(os.path.join(args.out_dir, 'hparams'))
  except FileNotFoundError as e:
    return -1.0
  return json.loads(hparams.read())['best_bleu']


with open(args.email_specs) as email_specs:
  args.email_specs = json.loads(email_specs.read())
  for attr_name in ['sender_email', 'password', 'receiver_emails']:
    setattr(args, attr_name, args.email_specs[attr_name])
  del args.email_specs


with smtplib.SMTP_SSL("smtp.gmail.com",
                      port=465,
                      context=ssl.create_default_context()) as server:
  server.login(args.sender_email, args.password)
  last_bleu = -1.0
  while True:
    cur_bleu = get_cur_bleu()
    if cur_bleu != last_bleu:
      server.sendmail(
          args.sender_email,
          args.receiver_emails,
          "Subject: {name}\n\n{cur_bleu}".format(
              name=os.path.basename(args.out_dir),
              cur_bleu=cur_bleu))
      last_bleu = cur_bleu
    time.sleep(args.period)

