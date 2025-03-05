"""
Copyright (C) 2022  GlaxoSmithKline plc - Mathieu Chevalley;

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import os
from causalscbench.data_access.utils import download


# Due to CORUM has changed its API, the following function will not work.
# Instead, we directly download the file from database and store it in the data folder.
# version 5.1
def download_corum(output_directory):
    # URL = "https://mips.helmholtz-muenchen.de/corum/download/releases/current/humanComplexes.txt.zip"
    filename = "corum_complexes.txt.zip"
    # path = download.download_if_not_exist(URL, output_directory, filename)
    path = os.path.join(output_directory, filename)
    return path


def download_ligand_receptor_pairs(output_directory):
    URL = "https://raw.githubusercontent.com/LewisLabUCSD/Ligand-Receptor-Pairs/ba44c3c4b4a3e501667309dd9ce7208501aeb961/Human/Human-2020-Shao-LR-pairs.txt"
    filename = "human_lr_pair.txt"
    path = download.download_if_not_exist(URL, output_directory, filename)
    return path


def download_string_network(output_directory):
    URL = "https://stringdb-static.org/download/protein.links.detailed.v11.5/9606.protein.links.detailed.v11.5.txt.gz"
    filename = "protein.links.txt.gz"
    path = download.download_if_not_exist(URL, output_directory, filename)
    return path


def download_string_physical(output_directory):
    URL = "https://stringdb-static.org/download/protein.physical.links.detailed.v11.5/9606.protein.physical.links.detailed.v11.5.txt.gz"
    filename = "protein.physical.links.txt.gz"
    path = download.download_if_not_exist(URL, output_directory, filename)
    return path


def download_string_protein_info(output_directory):
    URL = "https://stringdb-static.org/download/protein.info.v11.5/9606.protein.info.v11.5.txt.gz"
    filename = "protein.info.txt.gz"
    path = download.download_if_not_exist(URL, output_directory, filename)
    return path
