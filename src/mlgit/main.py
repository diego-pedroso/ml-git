"""
© Copyright 2020 HP Development Company, L.P.
SPDX-License-Identifier: GPL-2.0-only
"""

from mlgit.config import config_load, list_repos
from mlgit.log import init_logger, set_level
from mlgit.repository import Repository
from mlgit.admin import init_mlgit, store_add
from mlgit.utils import is_sample
from docopt import docopt
from pprint import pprint
from schema import Schema, And, Use, SchemaError, Or



def repository_entity_cmd(config, args):

	repotype = "project"
	if args["dataset"] == True:
		repotype = "dataset"
	if args["labels"] == True:
		repotype = "labels"
	if args["model"] == True:
		repotype = "model"

	r = Repository(config, repotype)
	if args["--verbose"] == True:
		print("ml-git config:")
		pprint(config)
		print("docopt argumens:")
		pprint(args)
		set_level("debug")

	if repotype == "project":
		if args["init"]:
			init_mlgit()

		if args["config"] == True and args["list"] == True:
			print("config:")
			pprint(config)

		bucket = args["<bucket-name>"]
		type = "s3h"
		region = "us-east-1"
		credentials = "default"
		if "--type" in args and args["--type"] is not None: type = args["--type"]
		if "--region" in args and args["--region"] is not None: region = args["--region"]
		if "--credentials" in args and args["--credentials"] is not None: credentials = args["--credentials"]
		if args["store"] == True and args["add"] == True:
			print("add store %s %s %s %s" % (type, bucket, credentials, region))
			store_add(type, bucket, credentials, region)
		return

	remote_url = args["<ml-git-remote-url>"]
	if args["remote"] == True and args["add"] == True:
		r.repo_remote_add(repotype, remote_url)
		return

	spec = args["<ml-entity-name>"]
	retry = 2
	if "--retry" in args and args["--retry"] is not None: retry = int(args["--retry"])
	if args["add"] == True:
		bumpversion = args["--bumpversion"]
		run_fsck = args["--fsck"]
		del_files = args["--del"]
		r.add(spec, bumpversion, run_fsck, del_files)
	if args["commit"] == True:
		dataset_tag = args["--dataset"]
		labels_tag = args["--labels"]
		tags = {}
		if dataset_tag is not None: tags["dataset"] = dataset_tag
		if labels_tag is not None: tags["labels"] = labels_tag
		run_fsck = args["--fsck"]
		r.commit(spec, tags, run_fsck)
	if args["push"] == True:
		r.push(spec, retry)
	if args["branch"] == True:
		r.branch(spec)
	if args["status"] == True:
		r.status(spec)
	if args["show"] == True:
		r.show(spec)
	if args["tag"] == True:
		tag = args["<tag>"]
		if args["add"] == True:
			r.tag(spec, tag)
		if args["list"] == True:
			r.list_tag(spec)
		return

	tag = args["<ml-entity-tag>"]
	if args["checkout"] == True:
		r.checkout(tag)
	if args["get"] == True:
		if is_sample(args):
			group_sample = args['--group-sample']
			seed = args['--seed']
			group_samples = {}
			if group_sample is not None:group_samples['group_sample'] = group_sample
			if seed is not None:group_samples["seed"] = seed
			r.get(tag, group_samples, retry)
		elif args['--group-sample'] is None and args['--seed'] is None:
			r.get(tag, None, retry)
		else:
			print("To use sampling you must pass <group-sample> and <seed> parameters")		
	if args["fetch"] == True:
		if is_sample(args):
			group_sample = args['--group-sample']
			seed = args['--seed']
			group_samples = {}
			if group_sample is not None:
				group_samples['group_sample'] = group_sample
			if seed is not None:
				group_samples["seed"] = seed
			r.fetch(tag, group_samples)
		elif args['--group-sample'] is None and args['--seed'] is None:
			r.fetch(tag, None)
		else:
			print("To use sampling you must pass <group-sample> and <seed> parameters")
	if args["init"] == True:
		r.init()
	if args["update"] == True:
		r.update()
	if args["fsck"] == True:
		r.fsck()
	if args["gc"] == True:
		r.gc()
	if args["list"] == True:
		# TODO: use MetadataManager list in repository!
		r.list()


def run_main():
	"""ml-git: a distributed version control system for ML
	Usage:
	ml-git init [--verbose]
	ml-git store (add|del) <bucket-name> [--credentials=<profile>] [--region=<region-name>] [--type=<store-type>] [--verbose]
	ml-git (dataset|labels|model) remote (add|del) <ml-git-remote-url> [--verbose]
	ml-git (dataset|labels|model) (init|list|update|fsck|gc) [--verbose]
	ml-git (dataset|labels|model) (branch|show|status) <ml-entity-name> [--verbose]
	ml-git (dataset|labels|model) (checkout|get|fetch) <ml-entity-tag> [--group-sample=<amount:group-size>]  [--seed=<value>] [--verbose]
	ml-git (dataset|labels|model) push <ml-entity-name> [--retry=<retries>] [--verbose]
	ml-git (dataset|labels|model) (checkout|get|fetch) <ml-entity-tag> [--verbose]
	ml-git (dataset|labels|model) get <ml-entity-tag> [--group-sample=<amount:group-size>] [--seed=<value>] [--retry=<retries>] [--verbose]
	ml-git (dataset|labels|model) add <ml-entity-name> [--fsck] [--bumpversion] [--verbose] [--del]
	ml-git dataset commit <ml-entity-name> [--tag=<tag>] [--verbose] [--fsck]
	ml-git labels commit <ml-entity-name> [--dataset=<dataset-name>] [--tag=<tag>] [--verbose]
	ml-git model commit <ml-entity-name> [--dataset=<dataset-name] [--labels=<labels-name>] [--tag=<tag>] [--verbose]
	ml-git (dataset|labels|model) tag <ml-entity-name> list  [--verbose]
	ml-git (dataset|labels|model) tag <ml-entity-name> (add|del) <tag> [--verbose]
	ml-git config list

	Options:
	--credentials=<profile>            Profile of AWS credentials [default: default].
	--fsck                             Run fsck after command execution
	--del                              Persist the files' removal
	--region=<region>                  AWS region name [default: us-east-1].
	--type=<store-type>                Data store type [default: s3h].
	--tag                              A ml-git tag to identify a specific version of a ML entity.
	--verbose                          Verbose mode
	--bumpversion                      (dataset add only) increment the dataset version number when adding more files.
	--retry=<retries>                  Number of retries to upload or download the files from the storage [default: 2]
	--group-sample=<amount:group-size> The sample option consists of amount and group used to download a sample. 				
	--seed=<value>				       The seed is used to initialize the pseudorandom numbers.
	-h --help                          Show this screen.
	--version                          Show version.
	"""
	config = config_load()
	init_logger()

	arguments = docopt(run_main.__doc__, version="1.0")

	schema = Schema({
		'--retry': Or(None, And(Use(int), lambda n: 0 < n), error='--retry=<retries> should be integer (0 < retries)')},
		ignore_extra_keys=True)
	try:
		schema.validate(arguments)
	except SchemaError as e:
		exit(e)

	repository_entity_cmd(config, arguments)


if __name__ == "__main__":
	run_main()

