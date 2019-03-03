import argparse
import datetime
import json
import os
import time
import smtplib, ssl


# Define arguments.
parser = argparse.ArgumentParser(description=
  'Periodically send email updates on witnessed improvement in BLEU score.',
  formatter_class=argparse.ArgumentDefaultsHelpFormatter
)
parser.add_argument(
  '--out_dir',
  type=str,
  required=True,
  help='Training output directory.'
)
parser.add_argument(
  '--email_specs',
  type=str,
  default='email_specs.json',
  help='JSON file containing email specs. This should define three fields: '
  '"sender_email", "password", "receiver_emails".'
)
parser.add_argument(
  '--period',
  type=int,
  default=60,
  help='Check on currrent best-bleu every <period> seconds.'
)
args = parser.parse_args()


# Preprocess arguments.
def preprocess_arguments():
  setattr(args, 'name', os.path.basename(os.path.normpath(args.out_dir)))
  setattr(args, 'hparams', os.path.join(args.out_dir, 'hparams'))
  with open(args.email_specs) as email_specs:
    args.email_specs = json.loads(email_specs.read())
    for attr_name in ['sender_email', 'password', 'receiver_emails']:
      setattr(args, attr_name, args.email_specs[attr_name])
    del args.email_specs

# Helper methods.
def get_cur_metrics():
  with open(args.hparams) as hparams:
    params = json.loads(hparams.read())

  def get_checkpoint_steps(best_bleu_dir):
    with open(os.path.join(best_bleu_dir, 'checkpoint')) as checkpoint_file:
      line = checkpoint_file.readline().strip()
    try:
      assert line.startswith('model_checkpoint_path: ')
      line = line[23:None]
      assert line.startswith('"') and line.endswith('"')
      line = line[1:-1]
      stamp = str(datetime.datetime.fromtimestamp(os.path.getmtime(line + '.meta')))
      line = os.path.basename(line)
      assert line.startswith('translate.ckpt-')
      return int(line[15:]), stamp
    except:
      raise ValueError('Unable to locate/ parse checkpoint file.')

  def get_best_bleu_info(name='best_bleu'):
    info = '{name}: {val}'.format(
        name=name,
        val='%.2f' % params[name],
    )
    try:
      steps, stamp = get_checkpoint_steps(params[name + '_dir'])
      info += ', steps: {steps}, stamp: {stamp}'.format(
        steps=str(steps/1000) + 'K',
        stamp=stamp
      )
    except:
      pass
    return info

  metrics = get_best_bleu_info('best_bleu')
  if 'avg_best_bleu' in params:
    metrics = metrics + '\n' + get_best_bleu_info('avg_best_bleu')
  return metrics

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
  prev_metrics = None
  server = server_login()
  while True:
    time.sleep(args.period)
    message = None
    try:
      cur_metrics = get_cur_metrics()
      if cur_metrics != prev_metrics:
        prev_metrics = cur_metrics
        message = cur_metrics
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
