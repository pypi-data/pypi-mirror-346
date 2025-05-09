# Copyright (C) 2024 University of Glasgow
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import pprint

from datetime import datetime
from email.utils import parseaddr

from ietfdata.datatracker  import *
from ietfdata.mailarchive2 import *

dt = DataTracker()
ma = MailArchive()

ml = ma.mailing_list("mod-discuss")
ml.update()

count = {}
total = 0

for msg in ml.messages():
    uid = msg.uid()
    h_from = msg.header("from")[0]
    h_subj = msg.header("subject")[0]
    #print(f"{uid:4} {h_from:50} {h_subj}")

    if h_from not in count:
        count[h_from] = 0
    count[h_from] += 1
    total += 1

index = 1
for n, c in count.items():
    #print(f"{c:4} {n}")
    #print(f"P{index:02} ", end="")
    #for x in range(0, c):
    #    print("*", end="")
    #print("")
    print(f"{index:4} {c:4} {c/total*100:.1f}")
    index += 1


