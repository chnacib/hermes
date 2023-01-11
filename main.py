from src.services import s3, ami, ebs, ec2, iam, loadbalancer, rds, snapshot, sg_ec2, sg_rds
from src.common import excel

import argparse
parser = argparse.ArgumentParser()

parser.add_argument("--sg-rds", action='store_true',
                    help="Include RDS security group")
parser.add_argument("--sg-ec2", action='store_true',
                    help="Include EC2 security groups")
parser.add_argument("--s3", action='store_true', help="Include S3")
parser.add_argument("--ec2", action='store_true', help="Include EC2")
parser.add_argument("--ami", action='store_true', help="Include AMI")
parser.add_argument("--ebs", action='store_true', help="Include EBS")
parser.add_argument("--iam", action='store_true', help="Include IAM")
parser.add_argument("--loadbalancer", action='store_true',
                    help="Include LoadBalancer")
parser.add_argument("--rds", action='store_true', help="Include RDS")
parser.add_argument("--snapshot", action='store_true', help="Include Snapshot")
parser.add_argument("-a", "--all", action='store_true', help="Include All")
parser.add_argument("-j", "--join", action='store_true',
                    help="Join all files in one excel file")

args = vars(parser.parse_args())

if args['s3'] or args['all']:
    s3.run()

if args['ec2'] or args['all']:
    ec2.run()

if args['sg_ec2'] or args['all']:
    sg_ec2.run()

if args['ami'] or args['all']:
    ami.run()

if args['ebs'] or args['all']:
    ebs.run()

if args['iam'] or args['all']:
    iam.run()

if args['loadbalancer'] or args['all']:
    loadbalancer.run()

if args['rds'] or args['all']:
    rds.run()

if args['sg_rds'] or args['all']:
    sg_rds.run()

if args['snapshot'] or args['all']:
    snapshot.run()

if args['join']:
    excel.join_files()
