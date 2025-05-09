# Copyright (C) 2025 University of Glasgow
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

import os
import pprint
import re
import requests
import sys
import textwrap

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pathlib              import Path
from ietfdata.datatracker import *
from ietfdata.rfcindex    import *


def normalise(affiliation):
    affiliation = affiliation.strip()
    affiliation = affiliation.replace("\n", "")
    for suffix in [" AB", 
                   " AG",
                   " B.V.",
                   " Corp.",
                   " Corp",
                   " GmbH",
                   ", Inc.",
                   ", Inc",
                   " Inc.",
                   " Incorporated",
                   " Inc",
                   ",  L.P.",
                   " L.P.",
                   " LP",
                   " LLC",
                   " Ltd.",
                   " Ltd",
                   " Limited",
                   " Oy"]:
        affiliation = affiliation.removesuffix(suffix)
    return " ".join(affiliation.split())


save_file = Path("cache/rfc-affiliations.json")

dt = DataTracker(cache_dir = "cache", cache_timeout = timedelta(minutes = 60 * 24 * 7))
ri = RFCIndex(cache_dir = "cache")

if save_file.exists():
    with open(save_file, "r") as inf:
        rfc_list = json.load(inf)
    print(f"Loaded {len(rfc_list)} items from {save_file}")
else:
    rfc_list = {}

# -------------------------------------------------------------------------------------------------
# Fetch data about the RFCs:

print("Fetching IETF stream RFCs:")
for rfc in ri.rfcs(stream="IETF", since="1995-01"):
    print(f"   {rfc.doc_id}: {textwrap.shorten(rfc.title, width=80, placeholder='...')}")
    if rfc.doc_id not in rfc_list:
        dt_document = dt.document_from_rfc(rfc.doc_id)
        dt_authors  = []

        for dt_author in dt.document_authors(dt_document):
            if dt_author.email is not None:
                email = dt.email(dt_author.email).address
            else:
                email = ""

            affiliation = dt_author.affiliation

            dt_person = dt.person(dt_author.person)
            names     = []
            for name in [dt_person.name, dt_person.name_from_draft, dt_person.ascii, dt_person.ascii_short, dt_person.plain]:
                if name is not None and name != "" and name not in names:
                    names.append(name)

            dt_authors.append({"names": names, "email": email, "affiliation": affiliation})

        item = {"doc_id": rfc.doc_id,
                "title":  rfc.title,
                "year":   rfc.year,
                "month":  rfc.month,
                "ri_authors"  : rfc.authors,
                "dt_authors"  : dt_authors
        }
        rfc_list[rfc.doc_id] = item


# -------------------------------------------------------------------------------------------------
# Save RFC data:

print(f"Saving to {save_file}:")
with open(save_file, "w") as outf:
    json.dump(rfc_list, outf, indent=3)


# -------------------------------------------------------------------------------------------------
# Normalise affiliations:

def find_canonical_affiliations(rfc_list):
    affiliations_per_domain = {}
    canonical_affiliations  = {}
    canonical_domains = []

    for num, rfc in rfc_list.items():
        for dt_author in rfc["dt_authors"]:
            if "@" in dt_author["email"]:
                affiliation = dt_author["affiliation"]
                parts  = dt_author["email"].split("@")[1].split(".")
                for tld in ["com", "org", "net"]:
                    if len(parts) >= 2 and parts[-1] == tld:
                        domain = f"{parts[-2]}.{parts[-1]}".lower()
                        if affiliation.lower() == parts[-2].lower():
                            if not domain in canonical_domains:
                                canonical_domains.append(domain)
                                affiliations_per_domain[domain] = {}

                            if not affiliation in affiliations_per_domain[domain]:
                                affiliations_per_domain[domain][affiliation] = 1
                            else:
                                affiliations_per_domain[domain][affiliation] += 1

    for domain in canonical_domains:
        max_count = 0
        for affiliation, count in affiliations_per_domain[domain].items():
            if count > max_count:
                max_count = count
                canonical_affiliations[domain] = affiliation

    return canonical_affiliations


def normalise_affiliation(affiliation, email, canonical_affiliations):
    for domain, canonical in canonical_affiliations.items():
        if affiliation.lower().startswith(canonical.lower()):
            affiliation = canonical
    return affiliation



canonical_affiliations  = find_canonical_affiliations(rfc_list)

for num, rfc in rfc_list.items():
    for dt_author in rfc["dt_authors"]:
        normalised = normalise_affiliation(dt_author["affiliation"], dt_author["email"], canonical_affiliations)
        print(f"{dt_author['email']:30} {dt_author['affiliation']} -> {normalised}")




