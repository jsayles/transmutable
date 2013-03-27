import os
import sys
import time
import urllib
import datetime

from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from apple.backup import S3Util

class Command(BaseCommand):
	requires_model_validation = False
	args = ['<aws access key>', '<aws secret key>', '<s3 Bucket> <file> ...']
	option_list = BaseCommand.option_list # + (make_option('--verbose', action='store_true', dest='verbose', default=False, help='print debugging info'),)

	def handle(self, *args, **options):
		if len(args) < 4: raise CommandError(' '.join(Command.args))
		s3_utils = S3Util(args[0], args[1])
		s3_utils.write_files_to_bucket(args[2], args[3:])

# Copyright 2013 Trevor F. Smith (http://trevor.smith.name/) Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
