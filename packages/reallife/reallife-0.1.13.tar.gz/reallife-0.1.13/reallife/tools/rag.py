
import sys

from pypidoctor.query import Queryr

from pypidoctor.query import Queryr
from pypidoctor.build import build,Reader


import re
import sys
import sys


def main(prompt:str):
    qr = Queryr(persist_dir="/Users/zhaoxuefeng/GitHub/test1/obk")
    qr.load_query()
    result = qr.ask(prompt)
    return result


def main(prompt:str):
    qr = Queryr(persist_dir="/Users/zhaoxuefeng/GitHub/test1/obk")
    qr.load_query()
    result = qr.ask(prompt)
    return result



def main(file_path:str):
    build(file_path = file_path,
    persist_dir="/Users/zhaoxuefeng/GitHub/test1/obk",
    readertype=Reader.CustObsidianReader,
    debug=True,
    )



# curl http://127.0.0.1:9000/rebuild


