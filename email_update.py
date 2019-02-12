import argparse
import json
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
args = parser.parse_args()


# Preprocess arguments.
def preprocess_arguments():
  for attr_name in ['out_dir', 'email_specs']:
    attr_val = getattr(args, attr_name)
    if isinstance(attr_val, list):
      assert len(attr_val) == 1
      setattr(args, attr_name, attr_val[0])
    else:
      assert isinstance(attr_val, str)
  setattr(args, 'name', os.path.basename(os.path.normpath(args.out_dir)))
  setattr(args, 'hparams', os.path.join(args.out_dir, 'hparams'))
  with open(args.email_specs) as email_specs:
    args.email_specs = json.loads(email_specs.read())
    for attr_name in ['sender_email', 'password', 'receiver_emails']:
      setattr(args, attr_name, args.email_specs[attr_name])
    del args.email_specs

# Helper methods.
def get_cur_bleu():
  with open(args.hparams) as hparams:
    params = json.loads(hparams.read())
    best_bleu = '%.2f' % params['best_bleu']
    if 'avg_best_bleu' in params:
      best_bleu = best_bleu + '\nAVG:%.2f' % params['avg_best_bleu']
  return best_bleu

def server_login():
  server = smtplib.SMTP_SSL(
      "smtp.gmail.com",
      port=465,
      context=ssl.create_default_context())
  server.login(args.sender_email, args.password)
  return server

def server_send(server, message):
  server.sendmail(
      args.sender_email,
      args.receiver_emails,
      "Subject: {name}\n\n{message}".format(
          name=args.name, message=message))

def main():
  preprocess_arguments()
  last_bleu = None
  server = server_login()
  while True:
    time.sleep(args.period)
    message = None
    try:
      cur_bleu = get_cur_bleu()
      if cur_bleu != last_bleu:
        last_bleu = cur_bleu
        message = cur_bleu
    except Exception as e:
      message = str(e)
    if message:
      try:
        server_send(server, message)
      except Exception as e:
        server = server_login()
        server_send(server, message)

if __name__ == '__main__':
  main()
