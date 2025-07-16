# cloud_enum.py
# by @rootnorth (github)

import boto3
from botocore.exceptions import NoCredentialsError, ClientError

class AWSCloudEnum:
    def __init__(self):
        try:
            self.s3 = boto3.client('s3')
            self.ec2 = boto3.client('ec2')
        except Exception as e:
            print(f"Başlangıç hatası: {e}")

    def list_s3_buckets(self):
        try:
            buckets = self.s3.list_buckets()
            print(f"[+] Toplam {len(buckets['Buckets'])} S3 bucket bulundu:")
            for bucket in buckets['Buckets']:
                print(f" - {bucket['Name']}")
        except NoCredentialsError:
            print("AWS kimlik bilgisi bulunamadı.")
        except ClientError as e:
            print(f"AWS hatası: {e}")

    def list_ec2_instances(self):
        try:
            response = self.ec2.describe_instances()
            instances = []
            for reservation in response['Reservations']:
                for instance in reservation['Instances']:
                    instances.append({
                        "InstanceId": instance['InstanceId'],
                        "State": instance['State']['Name'],
                        "Type": instance['InstanceType'],
                        "PublicIp": instance.get('PublicIpAddress', 'Yok')
                    })
            print(f"[+] Toplam {len(instances)} EC2 instance bulundu:")
            for inst in instances:
                print(f" - {inst['InstanceId']} | {inst['State']} | {inst['Type']} | IP: {inst['PublicIp']}")
        except NoCredentialsError:
            print("AWS kimlik bilgisi bulunamadı.")
        except ClientError as e:
            print(f"AWS hatası: {e}")

    def run(self):
        print("=== AWS Cloud Infrastructure Enumerator ===")
        self.list_s3_buckets()
        print()
        self.list_ec2_instances()
        print("\n[*] Diğer bulut servisleri (Azure, GCP) desteği ileride eklenebilir.")

if __name__ == "__main__":
    enum = AWSCloudEnum()
    enum.run()
