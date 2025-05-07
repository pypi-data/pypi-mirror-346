# MinIO Python Library for Amazon S3 Compatible Cloud Storage,
# (C) 2018 MinIO, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
This module implements a progress printer while communicating with MinIO server

:copyright: (c) 2018 by MinIO, Inc.
:license: Apache 2.0, see LICENSE for more details.

"""

from enum import Enum
import logging
import multiprocessing
import threading
import time
from queue import Empty, Queue
from threading import Thread
from typing import Optional
from venv import logger

from tqdm import tqdm

logger = logging.getLogger(__name__)

class ProgressRole(Enum):
    CONSUMER = 1
    PRODUCER = 2
    
class Progress(Thread):

    def __init__(self, process_queue: Queue[int], mode: ProgressRole=ProgressRole.PRODUCER, interval=1, progress_title: str="Processing..."):
        Thread.__init__(self)
        self.daemon = True
        self.interval = interval
        
        self.object_name = None
        
        self.total_length = 0
        self.current_size = 0
        
        self.process_queue = process_queue
        
        self.mode = mode
        self.initial_time = time.time()
        
        self.progress_title = progress_title
        self.bar = None
        
        self.running = True
        self.start()

    def set_meta(self, total_length: int, object_name: Optional[str] = ""):
        """
        Metadata settings for the object. This method called before uploading
        object
        :param total_length: Total length of object.
        :param object_name: Object name to be showed.
        """
        self.total_length = total_length
        self.object_name = object_name
        
        if self.mode == ProgressRole.CONSUMER:
            self.bar = tqdm(total=self.total_length, unit='B', unit_scale=True, unit_divisor=1024, desc=self.progress_title)

    def run(self):
        while self.current_size <= self.total_length:
            if self.mode == ProgressRole.PRODUCER:
                time.sleep(1)
                continue
            try:
                delta = self.process_queue.get(timeout=self.interval)
            except Empty:
                continue
            except EOFError:
                break

            if self.bar:
                self.bar.update(delta)
                
            self.process_queue.task_done()
            self.current_size += delta
            if self.current_size >= self.total_length:
                self.done_progress()
                return

    def update(self, size):
        """
        Update object size to be showed. This method called while uploading
        :param size: Object size to be showed. The object size should be in
                     bytes.
        """
        if not isinstance(size, int):
            raise ValueError('{} type can not be displayed. '
                             'Please change it to Int.'.format(type(size)))
        
        self.process_queue.put(size)

    def done_progress(self):
        self.total_length = 0
        self.object_name = None
        self.last_printed_len = 0
        self.current_size = 0
        
        if self.mode == ProgressRole.PRODUCER:
            logger.info("Process %s complete.", self.object_name)

        if self.bar:
            self.bar.close()
            

class ProgressTracker:
    def __init__(self, bucket_name: str, object_key: str):
        self.bar = None
        self.last_bytes = 0
        self.bucket_name = bucket_name
        self.object_key = object_key
        self.lock = threading.Lock()

    def create_bar(self, object_length: int):
        process_name = multiprocessing.current_process().name
        process_number = int(process_name.split("-")[-1])

        self.bar = tqdm(
            total=int(object_length),
            desc=
            f"Downloading {self.object_key} from {self.bucket_name} ({process_name})",
            unit="B",
            unit_scale=True,
            unit_divisor=1024,
            position=process_number)

        self.bar.update(0)

    def update(self, consumed_bytes: int, total_bytes: int):
        with self.lock:
            if self.bar is None:
                self.create_bar(total_bytes)

            increment = int(consumed_bytes - self.last_bytes)
            if increment > 0:
                try:
                    if self.bar:
                        self.bar.update(increment)
                    self.last_bytes = consumed_bytes
                except AttributeError:
                    return  # Handle case where bar disappeared

            if consumed_bytes >= total_bytes:
                if self.bar is not None:
                    self.bar.close()
