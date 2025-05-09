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

from datetime import datetime
from email.utils import parseaddr

from ietfdata.datatracker  import *
from ietfdata.mailarchive2 import *

dt = DataTracker()
ma = MailArchive()

#ma.update()

def date_in_range(date):
    if date is None:
        return False
    return date > datetime(2019, 6, 12) and date < datetime(2024, 6, 12)

# How many people posted to all the IETF lists?

print("Checking lists:")
mcount_all = 0
all_addrs = {}
for ml_name in ma.mailing_list_names():
    if ml_name in ["dmarc-report"]:
        print(f"  {ml_name} skipped")
        continue
    print(f"  {ml_name}")
    ml = ma.mailing_list(ml_name)
    for msg in ml.messages():
        if date_in_range(msg.date()):
            mcount_all += 1
            addr_hdr = msg.header("from")
            if len(addr_hdr) == 1:
                name, addr = parseaddr(addr_hdr[0])
                if addr in all_addrs:
                    all_addrs[addr] += 1
                else:
                    all_addrs[addr] = 1

count_all = len(all_addrs)

print(f"Addresses posting to all lists: {count_all}")

# How many people posted to the ietf@ietf.org list?

mcount_ietf = 0
ietf_addrs = {}
ietf_list = ma.mailing_list("ietf")
for msg in ietf_list.messages():
    if date_in_range(msg.date()):
        mcount_ietf += 1
        addr_hdr = msg.header("from")
        if len(addr_hdr) == 1:
            name, addr = parseaddr(addr_hdr[0])
            if addr in ietf_addrs:
                ietf_addrs[addr] += 1
            else:
                ietf_addrs[addr] = 1

count_ietf = len(ietf_addrs)
percentage = count_ietf / count_all * 100.0

print(f"Addresses posting to ietf@ietf.org: {count_ietf}")
print(f"{percentage}%")
print(f"")

pm = mcount_ietf / mcount_all * 100.0

print(f"Number of messages (all): {mcount_all}")
print(f"Number of messages (IETF): {mcount_ietf} ({pm}%)")

print("")
c_msg = 0
c_per = 0
for addr in sorted(ietf_addrs, key = ietf_addrs.get, reverse=True):
    c_per += 1
    c_msg += ietf_addrs[addr]
    print(c_per, c_msg, c_msg/mcount_ietf * 100, addr, ietf_addrs[addr])
    if c_msg > (mcount_ietf * 0.5):
        break

