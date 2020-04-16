"""
© Copyright 2020 HP Development Company, L.P.
SPDX-License-Identifier: GPL-2.0-only
"""

import click
import mlgit.admin as admin

from mlgit.commands.repository import repository
from click_didyoumean import DYMGroup


@repository.group("store", help="Store management for this ml-git repository", cls=DYMGroup)
def store():
    pass


@store.command("add", help="Add a store BUCKET_NAME to ml-git")
@click.argument("bucket-name")
@click.option("--credentials", default="default", help="Profile name for store credentials [default: default]")
@click.option("--region", default="us-east-1", help="Aws region name for S3 bucket [default: us-east-1]")
@click.option("--type", default="s3h", help="Store type (s3h, s3, ...) [default: s3h]")
def store_add(**kwargs):
    admin.store_add(kwargs['type'], kwargs['bucket_name'], kwargs['credentials'])


@store.command("del", help="Delete a store BUCKET_NAME from ml-git")
@click.argument("bucket-name")
@click.option("--type", default="s3h", help="Store type (s3h, s3, ...) [default: s3h]")
def store_del(**kwargs):
    admin.store_del(kwargs['type'], kwargs['bucket_name'])